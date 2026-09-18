# AddWorkflowAttachment API

Attaches a document to an active workflow task. The attached document becomes visible in the task's Attachments list and is accessible to the task assignee and supervisors.

## Endpoint

```
/srv.asmx/AddWorkflowAttachment
```

## Methods

- **GET** `/srv.asmx/AddWorkflowAttachment?authenticationTicket=...&taskId=...&documentPath=...&versionNumber=...`
- **POST** `/srv.asmx/AddWorkflowAttachment` (form data)
- **SOAP** Action: `http://tempuri.org/AddWorkflowAttachment`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `taskId` | integer | Yes | Unique numeric ID of the task to attach the document to. |
| `documentPath` | string | Yes | Full infoRouter path of the document to attach (e.g. `/Finance/Reports/Q1.pdf`). |
| `versionNumber` | integer | Yes | Version number of the document to attach. Pass `0` to attach the current (latest) version. |

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
POST /srv.asmx/AddWorkflowAttachment HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&taskId=4812&documentPath=/Finance/Reports/Q1.pdf&versionNumber=0
```

### Request (GET)

```
GET /srv.asmx/AddWorkflowAttachment?authenticationTicket=abc123&taskId=4812&documentPath=/Finance/Reports/Q1.pdf&versionNumber=0
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

Attaches a document version to a task. `versionNumber` is the packed version number
(`major * 1000000 + minor * 1000 + revision`), so version 1 is `1000000`.

```javascript
await call('AddWorkflowAttachment', {
  authenticationTicket: ticket,
  taskId: 7328,
  documentPath: '/Public/Invoices/po-1001.pdf',
  versionNumber: 1000000
});
```

## Notes

- Pass `versionNumber=0` to always attach the current version of the document.
- If a non-zero `versionNumber` is specified, that exact version must exist on the document or the call returns an error.
- The same document can be attached multiple times with different version numbers.

## Related APIs

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
