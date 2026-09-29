# GetDueTaskDocuments API

Returns the list of documents that have active (due) workflow tasks currently assigned to the authenticated user. Results are sorted by task due date in ascending order.

## Endpoint

```
/srv.asmx/GetDueTaskDocuments
```

## Methods

- **GET** `/srv.asmx/GetDueTaskDocuments?authenticationTicket=...`
- **POST** `/srv.asmx/GetDueTaskDocuments` (form data)
- **SOAP** Action: `http://tempuri.org/GetDueTaskDocuments`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |

## Response

### Success Response

One `<document>` per document that has at least one open (due) task assigned to the caller, listed
once. Tasks whose document has been deleted, or that the caller can no longer read, are left out.

```xml
<response success="true" error="">
  <document DocumentID="1051" Name="Proposal.docx" Path="\Projects\My Project" Description="" UpdateInstructions=""
            CreationDate="2024-03-01T09:00:00.000Z" ModificationDate="2024-06-15T14:30:00.000Z"
            CheckoutDate="" CheckoutBy="" CheckoutByUserName="" Size="204800" Type="Office Document"
            PercentComplete="0" CompletionDate="" Importance="Normal" RetentionDate="" DispositionDate=""
            CutoffDate="" RDDefId="0" ExpirationDate="" RegisterDate="2024-03-01T09:00:00.000Z"
            RegisteredBy="John Smith" DocTypeID="0" DocTypeName="" AIEnhanced="0" AIExtractConfidence="0"
            VersionNumber="3000000" PublishedVersionNumber="3000000" PublishingRule="LATEST"
            OwnerName="John Smith" WorkflowId="12" WorkflowName="Contract Approval"
            WorkflowStepNumber="1" WorkflowStepName="Review"
            Author="" Language="" Source="" ApprovalStatus="NoResult" ClassificationLevel="NoMarkings"
            ClassificationLevelId="0" DeclassifyOn="" DomainId="1001" DomainName="Projects" DowngradeOn=""
            FolderId="1170" Foldername="My Project" IsShortcut="FALSE" TargetDocumentId="0"
            LastISOReviewDate="" NextISOReviewDate="" OwnerId="7" RegisterById="7" TemplateID="0"
            VersionCount="3" UserViewStatus="2" />
  <document DocumentID="1052" ...same attributes... />
</response>
```

A caller with nothing due gets an empty list:

```xml
<response success="true" error="" />
```

### `<document>` element

The element [GetDocument](GetDocument.md) returns with all four of its flags `false` - see its
[attribute table](GetDocument.md#document-element-attributes). The only child it can have is a
`<DescriptionLog>`, written when the description has a recorded author; there is no owner, property
set, access list or version history. The element carries `AIEnhanced` and `AIExtractConfidence` - see
[AIEnhanced](GetDocument.md#aienhanced) and [AIExtractConfidence](GetDocument.md#aiextractconfidence).

The `<document>` tells you which document is due, not which task: use [getTasks](getTasks.md) for the
tasks themselves.

### Error Response

```xml
<response success="false" error="Session expired or invalid ticket" errorCode="4010" />
```

## Required Permissions

Any authenticated user may call this API. Only tasks assigned to the calling user are returned.

## JavaScript

Every call answers XML with HTTP 200, success or not, so `success` is the thing to branch on and
`errorCode` is the number to report.

```javascript
async function call(action, params) {
  const response = await fetch(`/srv.asmx/${action}?${new URLSearchParams(params)}`);
  const root = new DOMParser()
    .parseFromString(await response.text(), 'text/xml')
    .documentElement;

  if (root.getAttribute('success') !== 'true') {
    throw new Error(`${root.getAttribute('errorCode')}: ${root.getAttribute('error')}`);
  }
  return root;
}
```

Lists the documents the caller has a task due on. It takes nothing but the ticket.

```javascript
const root = await call('GetDueTaskDocuments', { authenticationTicket: ticket });

for (const document of root.querySelectorAll(':scope > document')) {
  console.log(document.getAttribute('DocumentID'), document.getAttribute('Name'), document.getAttribute('Path'));
}
```

When the caller has nothing due the answer is a success with no `<document>` elements.

## Notes

- Only documents with tasks in **Due** status are returned -" tasks that are currently active and within their scheduled time window.
- Overdue tasks (past their due date), completed tasks, and tasks not yet started are excluded.
- The list is sorted by **task due date ascending** (earliest due date first).
- Each `<document>` element contains standard document properties. Rules, custom property sets, security details, and version history are not included in the response.
- Each `<document>` element includes a `UserViewStatus` integer attribute: `0` = never viewed, `1` = viewed but the published version has since changed, `2` = viewed the current published version. See `GetDocument` for the full attribute reference.
- To retrieve full task details for a document, use [GetTask](GetTask.md) or [getTasks](getTasks.md).

## Related APIs

- [GetTask](GetTask.md) -" Get full details of a specific workflow task.
- [getTasks](getTasks.md) -" Get a filtered and sorted list of workflow tasks.
- [CompleteTask](CompleteTask.md) -" Mark a task as completed.
- [ChangeTaskDueDate](ChangeTaskDueDate.md) -" Change the due date of an active task.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
