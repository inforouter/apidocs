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
POST /srv.asmx/RemoveWorkflowAttachment HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&taskId=4812&documentPath=/Finance/Reports/Q1.pdf&versionNumber=0
```

### Request (GET)

```
GET /srv.asmx/RemoveWorkflowAttachment?authenticationTicket=abc123&taskId=4812&documentPath=/Finance/Reports/Q1.pdf&versionNumber=0
```

## Notes

- Pass `versionNumber=0` to remove the current version attachment.
- If a non-zero `versionNumber` is specified, that exact version must be currently attached to the task or the call returns an error.
- The document must still exist in infoRouter at the specified path.

## Related APIs

- [AddWorkflowAttachment](AddWorkflowAttachment.md) — Attach a document to an active workflow task.
- [GetTask](GetTask.md) — Get task details including the current Attachments list.
- [GetTasks](GetTasks.md) — Get a filtered list of tasks.
- [CompleteTask](CompleteTask.md) — Mark a task as completed.
