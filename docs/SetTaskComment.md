# SetTaskComment API

Sets the user comment on a workflow task. The comment is stored with the task and visible to supervisors and other users with access to the workflow.

Pass an empty string to clear an existing comment.

## Endpoint

```
/srv.asmx/SetTaskComment
```

## Methods

- **GET** `/srv.asmx/SetTaskComment?authenticationTicket=...&taskId=...&comments=...`
- **POST** `/srv.asmx/SetTaskComment` (form data)
- **SOAP** Action: `http://tempuri.org/SetTaskComment`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `taskId` | integer | Yes | Unique numeric ID of the task. |
| `comments` | string | Yes | Comment text for the task. Pass an empty string to clear the comment. |

## Response

### Success Response

```xml
<root success="true" />
```

### Error Response

```xml
<root success="false" error="Access Denied" />
```

## Required Permissions

The calling user must be the **current task assignee**.

Anonymous access is not permitted.

## Eligible Task States

The task must be in one of the following states:

| Status | Allowed |
|--------|---------|
| `InProgress` | Yes |
| `DueDateChanged` | Yes |
| `NotStarted` | No |
| `Completed` | No |
| `Dropped` | No |
| `Reassigned` | No |

## Example

### GET Request

```
GET /srv.asmx/SetTaskComment
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &taskId=4812
    &comments=Reviewed+the+document.+All+sections+look+correct.
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/SetTaskComment HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&taskId=4812&comments=Reviewed+the+document.+All+sections+look+correct.
```

## Notes

- Comments are stored in two places: a database field (truncated to 255 characters) and a warehouse XML file (full length). Retrieving the task via [GetTask](GetTask.md) returns the full-length comment from the warehouse.
- Setting a comment does **not** complete the task. Call [CompleteTask](CompleteTask.md) to advance the workflow.
- The associated document must not be in an **offline** state.
- Line endings in the `comments` parameter are normalized before storage.

## Related APIs

- [GetTask](GetTask.md) -" Get full details of a task including its current comment.
- [CompleteTask](CompleteTask.md) -" Mark a task as completed and advance the workflow.
- [SetTaskApprovalStatus](SetTaskApprovalStatus.md) -" Set the approval decision on a task.
- [SetTaskPriority](SetTaskPriority.md) -" Set the priority of a task.

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed -" invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Task not found | No task with the specified `taskId` exists. |
| Access Denied | Calling user is not the task assignee. |
| Document offline | The associated document is currently offline. |
| Task dropped | The task has been dropped. |
| Task reassigned | The task has been reassigned. |
| Task completed | The task has already been completed. |
| Task not started | The task is in `NotStarted` state. |
