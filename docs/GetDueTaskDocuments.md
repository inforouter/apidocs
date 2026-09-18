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

```xml
<response success="true">
  <document
    id="1024"
    name="ContractDraft.pdf"
    path="/Corporate/Contracts/ContractDraft.pdf"
    checkedout="false"
    checkoutby=""
    checkoutbyid="0"
    owner="john.smith"
    ownerid="7"
    ownerFullName="John Smith"
    createdate="2024-03-01 09:15:00"
    modifydate="2024-03-10 14:22:00"
    versioncount="3"
    currentversion="3"
    size="245760"
    mimetype="application/pdf"
    importance="0"
    expired="false"
    expirationdate=""
    domainname="Corporate"
    domainid="45" />
  <document ... />
</response>
```

An empty result set (no due tasks) returns:

```xml
<response success="true" />
```

Documents come back as the full `<document>` element. Since 9.0 it also carries `AIEnhanced` and
`AIExtractConfidence`. The first says which of the document's attributes infoRouter Connect
produced, as a set of bits - `0` when none did; the second how sure it was about the weakest value
it put in a property set, as a percentage. See [AIEnhanced](GetDocument.md#aienhanced) and
[AIExtractConfidence](GetDocument.md#aiextractconfidence).

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

for (const document of root.querySelectorAll('Document')) {
  console.log(document.getAttribute('Path'));
}
```

When the caller has nothing due it answers 4041 "document not found" rather than an empty list, so
treat that code as "nothing due" instead of a fault.

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
| `4041` | the caller has no task due - a normal answer, not a fault |
