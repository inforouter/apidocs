# ChangeTaskDueDate API

Changes the due date and the allowed start time span of an active workflow task. The new due date must be in the future. The task's reminder date, supervisor notification date, and allowed start date are all recalculated automatically based on the new due date.

The task must be in **InProgress** or **DueDateChanged** status -" the due date cannot be changed on tasks that have not yet started, or that are already completed, dropped, or reassigned.

## Endpoint

```
/srv.asmx/ChangeTaskDueDate
```

## Methods

- **GET** `/srv.asmx/ChangeTaskDueDate?authenticationTicket=...&taskId=...&newDueDate=...&allowedStartTimeSpan=...`
- **POST** `/srv.asmx/ChangeTaskDueDate` (form data)
- **SOAP** Action: `http://tempuri.org/ChangeTaskDueDate`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `taskId` | integer | Yes | The ID of the task to update. Task IDs are returned by `getTasks` and `GetTask`. |
| `newDueDate` | datetime | Yes | The new due date and time for the task. Must be a future date/time. Recommended format: `yyyy-MM-ddTHH:mm:ss` (e.g. `2026-03-15T17:00:00`). |
| `allowedStartTimeSpan` | integer | Yes | Number of hours before the new due date during which the assignee is allowed to start the task. Pass `0` to remove the allowed-start restriction. |

## Response

### Success Response

```xml
<root success="true" />
```

### Error Response

```xml
<root success="false" error="[901] Session expired or Invalid ticket" />
```

## Required Permissions

The calling user must satisfy **one** of the following conditions:

- The calling user is the **task assignee** and the task definition has the **"Postpone" (change due date) permission** enabled for assignees.
- The calling user is a **workflow supervisor** for this task.

## Example

### GET Request

```
GET /srv.asmx/ChangeTaskDueDate
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &taskId=8821
    &newDueDate=2026-03-15T17:00:00
    &allowedStartTimeSpan=24
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/ChangeTaskDueDate HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&taskId=8821&newDueDate=2026-03-15T17:00:00&allowedStartTimeSpan=24
```

### Success Response

```xml
<root success="true" />
```

## Notes

- The task must be in **InProgress** (status 10) or **DueDateChanged** (status 20) state. Calling this API on a task with any other status (e.g. NotStarted, Completed, Dropped, Reassigned) returns an error.
- `newDueDate` must be a **future** date/time relative to the server clock. Passing a past date/time returns an error.
- The new due date does **not** need to be later than the current due date -" it can also be moved to an earlier future time.
- On success, the following fields are recalculated automatically:
  - **Task status** is set to `DueDateChanged` (20).
  - **Reminder date** is shifted to `newDueDate -' reminderTimeSpan hours` (if a reminder was configured).
  - **Supervisor notification date** is recalculated from `newDueDate`.
  - **Allowed start date** is set to `newDueDate -' allowedStartTimeSpan hours` (or cleared if `allowedStartTimeSpan` is `0`).
  - Any pending reminder, supervisor, and overdue notification flags are cleared.
- `allowedStartTimeSpan` is in **hours**. Setting it to `0` removes the allowed-start restriction -" the assignee can start the task at any time.
- Use `GetTask` to retrieve a task's current `taskId`, status, and assignee before calling this API.

## Related APIs

- [GetTask](GetTask.md) -" Retrieve the details of a specific task including its current status and due date.
- [getTasks](getTasks.md) -" Get a filtered list of tasks to find task IDs.
- [ReassignTask](ReassignTask.md) -" Reassign a task to a different user, optionally with a new due date.
- [UpdateTaskFinishDate](UpdateTaskFinishDate.md) -" Update the recorded finish date of a completed task.
- [SetTaskPriority](SetTaskPriority.md) -" Change the priority of a task.
- [CompleteTask](CompleteTask.md) -" Mark a task as completed.

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed -" invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Task not active | The task is not in InProgress or DueDateChanged status. Due date can only be changed on active tasks. |
| Due date in the past | `newDueDate` is earlier than the current server date/time. |
| Access denied | The calling user is not the assignee with postpone permission, and is not a workflow supervisor for this task. |
| Task not found | No task with the given `taskId` exists or the calling user does not have access to it. |
