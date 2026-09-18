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
<response success="true" error="" errorCode="0" />
```

### Error Response

```xml
<response success="false" error="Access denied." errorCode="4030" />
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

Corrects the finish date of a task that is **already complete**. A task still open is refused - use
`ChangeTaskDueDate` for the due date of an open one.

```javascript
await call('CompleteTask', { authenticationTicket: ticket, taskId: 7328, comments: 'Done.' });
await call('UpdateTaskFinishDate', { authenticationTicket: ticket, taskId: 7328, finishDate: '2026-01-02' });
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

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4000` | no task by that id, or the task is not finished yet |
