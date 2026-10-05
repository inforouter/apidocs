# GetDueTaskDocuments API

Returns the documents whose due tasks need the caller's attention: tasks **assigned to** them, tasks they **assigned**, and tasks they **supervise**. Overdue tasks are included. Each document is listed once, in the order of its earliest due task, and says in `DueTaskRoles` why it is listed.

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

One `<document>` per document that has at least one due task needing the caller's attention, listed
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
            VersionCount="3" UserViewStatus="2" DueTaskRoles="assignee" />
  <document DocumentID="1052" ...same attributes... DueTaskRoles="assigner,supervisor" />
</response>
```

A caller with nothing due gets an empty list:

```xml
<response success="true" error="" />
```

### Which tasks count

A task counts when it is **started and not finished** - due, overdue, or with its due date changed - in a
live library, and the caller has at least one of these roles on it:

| Role in `DueTaskRoles` | The caller... |
|---|---|
| `assignee` | is the user the task is assigned to (a task assigned to a group is not counted as any member's) |
| `assigner` | assigned the task - for a workflow task, is the user the workflow records as assigning it (usually whoever submitted the document) |
| `supervisor` | is the task's supervisor |

`DueTaskRoles` lists every role the caller has on any of the document's due tasks, comma separated, always in
the order `assignee,assigner,supervisor`. Use it to tell the caller's own work (`assignee`) from what they are
following (`assigner`, `supervisor`).

Not counted: tasks not yet started, completed tasks, and tasks the caller has none of the three roles on - even
in a library the caller administers.

> **Changed in 9.0.** In 8.7 this call also listed every due task in each library the caller administers - for
> sysadmin, every open task on the server - and the elements carried no `DueTaskRoles`. To list other people's
> tasks, use [getTasks](getTasks.md).

### `<document>` element

The element [GetDocument](GetDocument.md) returns with all four of its flags `false` - see its
[attribute table](GetDocument.md#document-element-attributes) - plus `DueTaskRoles`. The only child it can have is a
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

Any authenticated user may call this API. Only tasks the caller is assigned, assigned or supervises are counted,
and only documents the caller may read are listed.

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

const mine = [], following = [];
for (const document of root.querySelectorAll(':scope > document')) {
  const roles = document.getAttribute('DueTaskRoles').split(',');
  (roles.includes('assignee') ? mine : following).push(document.getAttribute('Name'));
}
console.log('My tasks:', mine, 'Following:', following);
```

When the caller has nothing due the answer is a success with no `<document>` elements.

## Notes

- Started, unfinished tasks count, **overdue included**; completed tasks and tasks not yet started do not.
- The list is sorted by each document's **earliest due task**, so documents with an overdue task come first.
- A document with several due tasks is listed once.
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
