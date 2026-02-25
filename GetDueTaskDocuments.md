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
<root success="true">
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
</root>
```

An empty result set (no due tasks) returns:

```xml
<root success="true" />
```

### Error Response

```xml
<root success="false" error="[901] Session expired or Invalid ticket" />
```

## Required Permissions

Any authenticated user may call this API. Only tasks assigned to the calling user are returned.

## Notes

- Only documents with tasks in **Due** status are returned — tasks that are currently active and within their scheduled time window.
- Overdue tasks (past their due date), completed tasks, and tasks not yet started are excluded.
- The list is sorted by **task due date ascending** (earliest due date first).
- Each `<document>` element contains standard document properties. Rules, custom property sets, security details, and version history are not included in the response.
- To retrieve full task details for a document, use [GetTask](GetTask) or [getTasks](getTasks).

## Related APIs

- [GetTask](GetTask) – Get full details of a specific workflow task.
- [getTasks](getTasks) – Get a filtered and sorted list of workflow tasks.
- [CompleteTask](CompleteTask) – Mark a task as completed.
- [ChangeTaskDueDate](ChangeTaskDueDate) – Change the due date of an active task.

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed — invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
