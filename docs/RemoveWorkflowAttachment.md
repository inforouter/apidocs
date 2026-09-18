# RemoveWorkflowAttachment API

Removes a previously attached document from an active workflow task. The document is detached from the task's Attachments list.

## Endpoint

```
/srv.asmx/RemoveWorkflowAttachment
```

## Methods

- **GET** `/srv.asmx/RemoveWorkflowAttachment?authenticationTicket=...&taskId=...&documentPath=...&versionNumber=...`
- **POST** `/srv.asmx/RemoveWorkflowAttachment` (form data)
- **SOAP** Action: `http://tempuri.org/RemoveWorkflowAttachment`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `taskId` | integer | Yes | Unique numeric ID of the task to remove the attachment from. |
| `documentPath` | string | Yes | Full infoRouter path of the document to remove (e.g. `/Finance/Reports/Q1.pdf`). |
| `versionNumber` | integer | Yes | Version number of the attached document to remove. Pass `0` to remove the current (latest) version. |

## Response

### Success Response

```xml
<response success="true" error="" errorCode="0" />
```

### Error Response

```xml
<response success="false" error="Error message" />
```

## Required Permissions

The calling user must be the task assignee or a workflow supervisor.

## Example

### Request (POST)

```
POST /srv.asmx/RemoveWorkflowAttachment HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&taskId=4812&documentPath=/Finance/Reports/Q1.pdf&versionNumber=0
```

### Request (GET)

```
GET /srv.asmx/RemoveWorkflowAttachment?authenticationTicket=abc123&taskId=4812&documentPath=/Finance/Reports/Q1.pdf&versionNumber=0
```

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

Takes an attachment back off a task. It names the same document and version `AddWorkflowAttachment`
was given.

```javascript
await call('RemoveWorkflowAttachment', {
  authenticationTicket: ticket,
  taskId: 7328,
  documentPath: '/Public/Invoices/po-1001.pdf',
  versionNumber: 1000000
});
```

## Notes

- Pass `versionNumber=0` to remove the current version attachment.
- If a non-zero `versionNumber` is specified, that exact version must be currently attached to the task or the call returns an error.
- The document must still exist in infoRouter at the specified path.

## Related APIs

- [AddWorkflowAttachment](AddWorkflowAttachment.md) — Attach a document to an active workflow task.
- [GetTask](GetTask.md) — Get task details including the current Attachments list.
- [GetTasks](getTasks.md) — Get a filtered list of tasks.
- [CompleteTask](CompleteTask.md) — Mark a task as completed.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4041` | no document at that path, or no version by that number |
| `4000` | no task by that id |
| `4030` | there is no ticket at all |
