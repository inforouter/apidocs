# CompleteTask API

Marks a workflow task as completed. If a comment string is provided it is saved to the task before the status change. After the task is marked complete, the workflow engine automatically evaluates whether the step is finished and advances the workflow to the next step if all tasks in the current step are done.

All task requirements (e.g. Approval, Sign, ISOReview) configured on the task definition must be satisfied before the task can be completed. Use `TestTaskCompletion` to check readiness without changing status.

## Endpoint

```
/srv.asmx/CompleteTask
```

## Methods

- **GET** `/srv.asmx/CompleteTask?authenticationTicket=...&taskId=...&comments=...`
- **POST** `/srv.asmx/CompleteTask` (form data)
- **SOAP** Action: `http://tempuri.org/CompleteTask`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `taskId` | integer | Yes | The ID of the task to complete. Task IDs are returned by `getTasks` and `GetTask`. |
| `comments` | string | No | Optional completion comment from the assignee. Pass an empty string if no comment is needed. The first 255 characters are stored in the database; the full text is also stored in the document warehouse. |

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

The calling user must be the **task assignee**. Only the assigned user can complete a task. Supervisors and administrators cannot complete tasks on behalf of the assignee through this API (use `ReassignTask` to transfer ownership first).

## Example

### GET Request

```
GET /srv.asmx/CompleteTask
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &taskId=8821
    &comments=Document+reviewed+and+approved.
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/CompleteTask HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&taskId=8821&comments=Document+reviewed+and+approved.
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

Closes a task and records the assignee's closing comment. Completing a task twice is refused.

```javascript
await call('CompleteTask', {
  authenticationTicket: ticket,
  taskId: 7328,
  comments: 'Approved, matches the purchase order.'
});
```

`comments` is a required string: an empty one is refused by model binding with HTTP 400. Call
`TestTaskCompletion` first to find out whether the task's requirements have been met.

## Notes

- The calling user must be the **assignee** of the task. Attempting to complete a task assigned to a different user returns an access-denied error.
- The task must be in **InProgress** (10) or **DueDateChanged** (20) status. Tasks in any of the following states cannot be completed:
  - `NotStarted` (0) -" the assignee must open and start the task first.
  - `Completed` (30) -" already done.
  - `Dropped` (-1) -" has been dropped by a supervisor.
  - `Reassigned` (-2) -" has been transferred to another user.
- All **task requirements** (Approval, Sign, ISOReview, etc.) configured in the task definition must be fulfilled before this call will succeed. Use `TestTaskCompletion` to verify readiness without committing the status change.
- The **finish date** is automatically set to the current server date/time on completion.
- If `comments` is non-empty, it is saved to the task record before the status is changed. If saving the comment fails (e.g. the document is offline/archived), the entire operation fails.
- Comments are stored in two places: the first 255 characters in the database and the full text in the document warehouse XML.
- After successful completion, the workflow engine runs automatically: if all tasks in the current step are now complete the workflow advances to the next step, triggers notifications, and may move the document to the configured "on-end" folder.
- If the task is a **step-0** (non-step) task, workflow advancement is skipped after completion.
- The document associated with the task must not be in **Offline** (archived) state.

## Related APIs

- [GetTask](GetTask.md) -" Retrieve task details including current status and requirements.
- [getTasks](getTasks.md) -" Get a filtered list of tasks.
- [TestTaskCompletion](TestTaskCompletion.md) -" Test whether all requirements are met before calling CompleteTask.
- [ReassignTask](ReassignTask.md) -" Transfer a task to a different user before completing.
- [SetTaskComment](SetTaskComment.md) -" Set the task comment without completing the task.
- [SetTaskApprovalStatus](SetTaskApprovalStatus.md) -" Set the approval status of a task (Approve/Reject/No status).
- [ChangeTaskDueDate](ChangeTaskDueDate.md) -" Extend or move the task due date.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4000` | no task by that id, it is already complete, or a requirement has not been met |
| `4030` | there is no ticket at all |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
