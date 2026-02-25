# ReassignTask API

Reassigns an active workflow task to a different user with a new due date and instructions. The original task is marked as **Reassigned** and a new task is created for the target user. Task attachments and requirements are inherited by the new task.

## Endpoint

```
/srv.asmx/ReassignTask
```

## Methods

- **GET** `/srv.asmx/ReassignTask?authenticationTicket=...&taskId=...&reassignTo=...&newDueDate=...&newInstructions=...&sendTaskNotice=...`
- **POST** `/srv.asmx/ReassignTask` (form data)
- **SOAP** Action: `http://tempuri.org/ReassignTask`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `taskId` | integer | Yes | Unique numeric ID of the task to reassign. |
| `reassignTo` | string | Yes | Login name of the user to reassign the task to. |
| `newDueDate` | DateTime | Yes | New due date for the reassigned task. Must be a future date/time. Recommended format: `yyyy-MM-ddTHH:mm:ss`. |
| `newInstructions` | string | Yes | Instructions for the new assignee. Pass an empty string to reuse the original instructions. |
| `sendTaskNotice` | boolean | Yes | `true` to send a task notification email to the new assignee; `false` to suppress it. |

## Response

### Success Response

```xml
<response success="true">
  <Value>
    <TaskId>4813</TaskId>
    <AssigneeId>15</AssigneeId>
    <AssigneeFullName>Alice Jones</AssigneeFullName>
    <RedirectedfromUserId>0</RedirectedfromUserId>
    <RedirectedfromUserFullName></RedirectedfromUserFullName>
  </Value>
</response>
```

### Error Response

```xml
<response success="false" error="Access Denied" />
```

## Response Field Reference

| Element | Description |
|---------|-------------|
| `TaskId` | ID of the **new** task created for the reassigned user. |
| `AssigneeId` | User ID of the new task assignee (may differ from `reassignTo` if that user has an active task redirection). |
| `AssigneeFullName` | Full display name of the new assignee. |
| `RedirectedfromUserId` | If the new assignee has a task redirection active and the task was auto-forwarded, this is the user ID of the originally specified `reassignTo` user. `0` if no further redirection occurred. |
| `RedirectedfromUserFullName` | Full name of the `reassignTo` user when redirection occurred. Empty if no further redirection. |

## Required Permissions

The calling user must be either:
- The **current task assignee**, or
- A **workflow supervisor** for the task.

Anonymous access is not permitted.

## Eligible Task States

Only tasks in the following states can be reassigned:

| Status | Reassignable |
|--------|-------------|
| `InProgress` | Yes |
| `DueDateChanged` | Yes |
| `NotStarted` | No |
| `Completed` | No |
| `Dropped` | No |
| `Reassigned` | No -" already reassigned |

## What Happens on Success

1. The original task status is set to **Reassigned**.
2. A new task is created for the `reassignTo` user with status **InProgress** and the specified `newDueDate` and `newInstructions`.
3. All task **attachments** from the original task are copied to the new task.
4. Task **requirements** (Approval, Sign, ISOReview, etc.) are inherited from the original task.
5. If the `reassignTo` user has an active **task redirection**, the task is automatically forwarded to their redirect target and `RedirectedfromUserId` is populated in the response.
6. Email notifications are sent to the **original assignee** and the **original task assigner**. If `sendTaskNotice=true`, the new assignee also receives a notification.

## Example

### GET Request

```
GET /srv.asmx/ReassignTask
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &taskId=4812
    &reassignTo=alice.jones
    &newDueDate=2024-04-15T17:00:00
    &newInstructions=Please review and approve by end of month.
    &sendTaskNotice=true
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/ReassignTask HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&taskId=4812&reassignTo=alice.jones&newDueDate=2024-04-15T17:00:00&newInstructions=Please+review+and+approve+by+end+of+month.&sendTaskNotice=true
```

## Notes

- The `reassignTo` parameter is a **login name**, not a display name or user ID.
- `newDueDate` must be a future date. Passing a past date returns an error.
- If `newInstructions` is empty, the instructions field of the new task will be empty. Pass the original instructions explicitly if they should be preserved.
- The `TaskId` in the response is the **new** task ID, not the original. Use this ID for subsequent calls such as [CompleteTask](CompleteTask.md) or [GetTask](GetTask.md).
- To obtain the original task ID, use [getTasks](getTasks.md) or [GetTask](GetTask.md) before calling ReassignTask.

## Related APIs

- [GetTask](GetTask.md) -" Get full details of a task including its current status.
- [getTasks](getTasks.md) -" Get a filtered list of tasks.
- [CompleteTask](CompleteTask.md) -" Mark a task as completed.
- [DeleteTask](DeleteTask.md) -" Delete a task.
- [ChangeTaskDueDate](ChangeTaskDueDate.md) -" Change the due date without reassigning.

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed -" invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Task not found | No task with the specified `taskId` exists. |
| User not found | The specified `reassignTo` login name does not exist. |
| Access Denied | Calling user is not the task assignee or a workflow supervisor. |
| Invalid status | Task is in `NotStarted`, `Completed`, `Dropped`, or `Reassigned` state. |
| Past due date | `newDueDate` is in the past. |
| Document offline | The associated document is currently offline. |
