# UpdateTaskStatus API

Updates the status, finish date, and comment of a workflow task in a single call. This is the composite operation that mirrors the UPDATESTATUS form submission in the task UI — it saves the comment first, then applies the new status and finish date.

## Endpoint

```
/srv.asmx/UpdateTaskStatus
```

## Methods

- **GET** `/srv.asmx/UpdateTaskStatus?authenticationTicket=...&taskId=...&taskStatus=...&finishDate=...&comments=...`
- **POST** `/srv.asmx/UpdateTaskStatus` (form data)
- **SOAP** Action: `http://tempuri.org/UpdateTaskStatus`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from AuthenticateUser |
| `taskId` | integer | Yes | Unique numeric ID of the task to update |
| `taskStatus` | integer | Yes | New task status: -2=Reassigned, -1=Dropped, 0=NotStarted, 10=InProgress, 20=DueDateChanged, 30=Completed |
| `finishDate` | DateTime | Yes | Actual finish date. Honoured only when status is Completed or Dropped and the assignee has ChangeFinishDate permission; otherwise the current time is used. Pass `0001-01-01T00:00:00` to omit |
| `comments` | string | No | User comment to record on the task. Pass an empty string to clear an existing comment |

## Response

### Success Response
```xml
<response success="true" error="" errorCode="0" />
```

### Error Response
```xml
<response success="false" error="Error message" errorCode="4000"/>
```

## Required Permissions

The calling user must be the task assignee. When `taskStatus` is `30` (Completed), all task requirements (Approval, Sign, ISOReview, etc.) must be satisfied first — use `TestTaskCompletion` to verify readiness before calling this API.

## Behavior Notes

- The comment is persisted **before** the status change. If the status update fails, the comment is still saved.
- For `Completed` (30) and `Dropped` (-1) statuses: if the assignee has the ChangeFinishDate permission and a valid `finishDate` is supplied, that date is used; otherwise the finish date is set to the current time.
- For all other statuses the finish date is ignored and stored as the system base date.
- Passing `null` or whitespace for `comments` skips the comment update entirely; passing an empty string clears any existing comment.

## Example

### Request (POST)
```
POST /srv.asmx/UpdateTaskStatus HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&taskId=42&taskStatus=30&finishDate=2026-04-15T10:00:00&comments=Review+complete
```

### Request (GET)
```
GET /srv.asmx/UpdateTaskStatus?authenticationTicket=abc123&taskId=42&taskStatus=30&finishDate=2026-04-15T10:00:00&comments=Review+complete
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

Sets a task's status and, when it is given, its comment. `taskStatus` is the numeric `TaskStatusX`
value: `-2` reassigned, `-1` dropped, `0` not started, `10` in progress, `20` due date changed,
`30` completed. A task that is already completed or reassigned is refused.

```javascript
await call('UpdateTaskStatus', {
  authenticationTicket: ticket,
  taskId: 7328,
  taskStatus: 10,
  finishDate: '2098-01-01',
  comments: 'Started the review.'
});
```

## Related APIs

- `CompleteTask` — shorthand for setting status to Completed with no explicit finish date
- `SetTaskComment` — sets only the comment without changing task status
- `UpdateTaskFinishDate` — updates the finish date of an already-completed task
- `TestTaskCompletion` — validates all task requirements before completing

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4000` | no task by that id, or it is already completed or reassigned |
| `4030` | there is no ticket at all |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
