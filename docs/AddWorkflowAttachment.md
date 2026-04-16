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
<root success="true" />
```

### Error Response

```xml
<root success="false" error="Error message" />
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

## Notes

- Pass `versionNumber=0` to always attach the current version of the document.
- If a non-zero `versionNumber` is specified, that exact version must exist on the document or the call returns an error.
- The same document can be attached multiple times with different version numbers.

## Related APIs

- [GetTask](GetTask.md) — Get task details including the current Attachments list.
- [GetTasks](GetTasks.md) — Get a filtered list of tasks.
- [CompleteTask](CompleteTask.md) — Mark a task as completed.
