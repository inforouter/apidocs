# SetTaskApprovalStatus API

Sets the approval decision on a workflow task. This is used for tasks that have an **Approval** requirement, where the assignee must record their approval decision (Approve or Reject) before completing the task.

## Endpoint

```
/srv.asmx/SetTaskApprovalStatus
```

## Methods

- **GET** `/srv.asmx/SetTaskApprovalStatus?authenticationTicket=...&taskId=...&approvalDecision=...`
- **POST** `/srv.asmx/SetTaskApprovalStatus` (form data)
- **SOAP** Action: `http://tempuri.org/SetTaskApprovalStatus`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `taskId` | integer | Yes | Unique numeric ID of the task. |
| `approvalDecision` | integer | Yes | Approval decision code. See table below. |

### Approval Decision Values

| Value | Name | Description |
|-------|------|-------------|
| `0` | `NoStatus` | Clears any previously set approval decision. |
| `5` | `Reject` | Marks the task as Rejected. |
| `6` | `Approve` | Marks the task as Approved. |

Any other value returns an error.

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
GET /srv.asmx/SetTaskApprovalStatus
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &taskId=4812
    &approvalDecision=6
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/SetTaskApprovalStatus HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&taskId=4812&approvalDecision=6
```

## Notes

- Setting the approval status does **not** complete the task. Call [CompleteTask](CompleteTask.md) after setting the approval status to advance the workflow.
- To clear a previously set decision, pass `approvalDecision=0`.
- To retrieve a task's current approval status, use [GetTask](GetTask.md) and inspect the `ApprovalStatus` field.
- Approval decisions are only meaningful for tasks that have an **Approval** requirement type. The field is stored but has no effect on tasks without this requirement.

## Related APIs

- [GetTask](GetTask.md) -" Get full details of a task including its current approval status.
- [CompleteTask](CompleteTask.md) -" Mark a task as completed and advance the workflow.
- [SetTaskComment](SetTaskComment.md) -" Set the comment on a task.
- [TestTaskCompletion](TestTaskCompletion.md) -" Check whether a task can be completed based on its requirements.

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed -" invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Task not found | No task with the specified `taskId` exists. |
| Access Denied | Calling user is not the task assignee. |
| Invalid decision | `approvalDecision` is not 0, 5, or 6. |
| Task dropped | The task has been dropped and cannot be updated. |
| Task reassigned | The task has been reassigned and cannot be updated. |
| Task completed | The task has already been completed. |
| Task not started | The task is in `NotStarted` state and cannot be updated. |
