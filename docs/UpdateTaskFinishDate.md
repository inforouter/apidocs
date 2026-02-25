# UpdateTaskFinishDate API

Updates the finish date of a **completed** workflow task. Use this to retroactively correct a task's recorded completion date when the original timestamp was inaccurate.

This operation only applies to already-completed tasks. To change the due date of an active task, use [ChangeTaskDueDate](ChangeTaskDueDate.md).

## Endpoint

```
/srv.asmx/UpdateTaskFinishDate
```

## Methods

- **GET** `/srv.asmx/UpdateTaskFinishDate?authenticationTicket=...&taskId=...&finishDate=...`
- **POST** `/srv.asmx/UpdateTaskFinishDate` (form data)
- **SOAP** Action: `http://tempuri.org/UpdateTaskFinishDate`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `taskId` | integer | Yes | Unique numeric ID of the completed task to update. |
| `finishDate` | DateTime | Yes | New finish date to record for the task. Recommended format: `yyyy-MM-ddTHH:mm:ss`. |

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
- The **original task assignee** who also has the **Change Finish Date** permission on the task, or
- A **workflow supervisor** for the task.

Anonymous access is not permitted.

## Eligible Task States

Only **completed** tasks can have their finish date updated:

| Status | Allowed |
|--------|---------|
| `Completed` | Yes |
| `InProgress` | No |
| `DueDateChanged` | No |
| `NotStarted` | No |
| `Dropped` | No |
| `Reassigned` | No |

## Example

### GET Request

```
GET /srv.asmx/UpdateTaskFinishDate
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &taskId=4812
    &finishDate=2024-04-10T14:30:00
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/UpdateTaskFinishDate HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&taskId=4812&finishDate=2024-04-10T14%3A30%3A00
```

## Notes

- The **Change Finish Date** permission is configured on the workflow task definition. If the assignee does not have this permission, only the supervisor can update the finish date.
- This API does not validate whether `finishDate` is in the past or future.
- To retrieve a task's current finish date, use [GetTask](GetTask.md).

## Related APIs

- [GetTask](GetTask.md) -" Get full details of a task including its current finish date.
- [ChangeTaskDueDate](ChangeTaskDueDate.md) -" Change the due date of an active (not yet completed) task.
- [CompleteTask](CompleteTask.md) -" Complete a task (sets the finish date automatically).

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed -" invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Task not found | No task with the specified `taskId` exists. |
| Access Denied | Calling user is not the task assignee with Change Finish Date permission, or a supervisor. |
| Task not completed | The task is not in `Completed` state. |
