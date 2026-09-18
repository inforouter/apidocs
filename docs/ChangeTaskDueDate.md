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
<response success="true" error="" errorCode="0" />
```

### Error Response

```xml
<response success="false" error="Session expired or invalid ticket" errorCode="4010" />
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
<response success="true" error="" errorCode="0" />
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

Moves a task's due date. `allowedStartTimeSpan` is the number of hours after assignment in which
the assignee has to start; `0` means no restriction.

```javascript
await call('ChangeTaskDueDate', {
  authenticationTicket: ticket,
  taskId: 7328,
  newDueDate: '2098-01-01',
  allowedStartTimeSpan: 0
});
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

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4000` | no task by that id, or the caller may not move its due date |
| `4030` | there is no ticket at all |
