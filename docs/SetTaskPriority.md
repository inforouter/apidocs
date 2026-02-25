# SetTaskPriority API

Sets the priority of a workflow task. Priority helps assignees and supervisors gauge the urgency of pending work.

## Endpoint

```
/srv.asmx/SetTaskPriority
```

## Methods

- **GET** `/srv.asmx/SetTaskPriority?authenticationTicket=...&taskId=...&taskPriority=...`
- **POST** `/srv.asmx/SetTaskPriority` (form data)
- **SOAP** Action: `http://tempuri.org/SetTaskPriority`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `taskId` | integer | Yes | Unique numeric ID of the task. |
| `taskPriority` | integer | Yes | Priority level code. See table below. |

### Priority Values

| Value | Name | Description |
|-------|------|-------------|
| `0` | `NoPriority` | No priority assigned. |
| `1` | `Low` | Low priority. |
| `5` | `Normal` | Normal priority. |
| `10` | `High` | High priority. |
| `11` | `Urgent` | Urgent priority. |

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

The calling user must be either:
- The **task assignee** who has the **Change Priority** permission on the task, or
- A **workflow supervisor** for the task.

Anonymous access is not permitted.

## Eligible Task States

Priority cannot be changed for tasks in `Completed` state. All other states (InProgress, DueDateChanged, NotStarted, Dropped, Reassigned) are allowed if permissions are satisfied.

## Example

### GET Request

```
GET /srv.asmx/SetTaskPriority
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &taskId=4812
    &taskPriority=10
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/SetTaskPriority HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&taskId=4812&taskPriority=10
```

## Notes

- The **Change Priority** permission is configured on the workflow task definition. If the assignee does not have this permission, only the supervisor can change the priority.
- To retrieve a task's current priority, use [GetTask](GetTask.md) and inspect the `Priority` field.

## Related APIs

- [GetTask](GetTask.md) -" Get full details of a task including its current priority.
- [CompleteTask](CompleteTask.md) -" Mark a task as completed and advance the workflow.
- [SetTaskComment](SetTaskComment.md) -" Set the comment on a task.
- [SetTaskApprovalStatus](SetTaskApprovalStatus.md) -" Set the approval decision on a task.
- [ChangeTaskDueDate](ChangeTaskDueDate.md) -" Change the due date of a task.

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed -" invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Task not found | No task with the specified `taskId` exists. |
| Access Denied | Calling user is not the task assignee with Change Priority permission, or a supervisor. |
| Task completed | Priority cannot be changed for a completed task. |
