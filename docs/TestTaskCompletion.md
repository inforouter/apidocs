# TestTaskCompletion API

Tests whether a workflow task can currently be completed by checking all of its configured requirements. This is a **dry-run** -" no state is changed, no task is completed. Use it to validate preconditions before calling [CompleteTask](CompleteTask.md).

Returns `success="true"` if all requirements are met, or `success="false"` with an error message describing the first unmet requirement.

## Endpoint

```
/srv.asmx/TestTaskCompletion
```

## Methods

- **GET** `/srv.asmx/TestTaskCompletion?authenticationTicket=...&taskId=...&exceptTaskComments=...`
- **POST** `/srv.asmx/TestTaskCompletion` (form data)
- **SOAP** Action: `http://tempuri.org/TestTaskCompletion`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `taskId` | integer | Yes | Unique numeric ID of the task to test. |
| `exceptTaskComments` | boolean | Yes | `true` to skip the Comments requirement check (useful when the caller intends to provide comments right before completing); `false` to include all requirements. |

## Response

### Success -" all requirements met

```xml
<response success="true" error="" errorCode="0" />
```

### Failure -" requirement not met

```xml
<response success="false" error="This task cannot be completed. You did not read the document." />
```

### Failure -" access denied

```xml
<response success="false" error="Access denied." errorCode="4030" />
```

## Required Permissions

The calling user must be the **current task assignee**.

Anonymous access is not permitted.

## Eligible Task States

The task must be completable (same criteria as [CompleteTask](CompleteTask.md)):

| Status | Testable |
|--------|---------|
| `InProgress` | Yes |
| `DueDateChanged` | Yes |
| `NotStarted` | No |
| `Completed` | No |
| `Dropped` | No |
| `Reassigned` | No |

## Requirements Checked

The following task requirement types are evaluated:

| Requirement Type | Check |
|-----------------|-------|
| `Comments` | Task must have a non-empty comment. Skipped if `exceptTaskComments=true`. |
| `LastestVersionRead` | The assignee must have read the latest version of the associated document. |
| `PublishedVersionRead` | The assignee must have read the published version (or latest if no published version). |
| `Edit` | The document must have been edited in accordance with the task's edit requirement. |
| `Sign` | Always passes -" no pre-check needed for electronic signatures. |
| `ISOReview` | An ISO Review log entry must have been added since the task's start date. |
| `SOXReview` | A SOX Review log entry must have been added since the task's start date. |
| `AllowedStartDate` | The current time must be on or after the task's allowed start time. |
| Document checked out | The document must not be checked out by the assignee themselves. |

## Example

### GET Request

```
GET /srv.asmx/TestTaskCompletion
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &taskId=4812
    &exceptTaskComments=false
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/TestTaskCompletion HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&taskId=4812&exceptTaskComments=false
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

A dry run of `CompleteTask`: it reports whether the task's requirements have been met and leaves the
task open. With `exceptTaskComments=true` the comment requirement is not counted.

```javascript
try {
  await call('TestTaskCompletion', {
    authenticationTicket: ticket, taskId: 7328, exceptTaskComments: false
  });
  await call('CompleteTask', { authenticationTicket: ticket, taskId: 7328, comments: 'Done.' });
} catch (error) {
  console.log('not ready:', error.message);
}
```

## Notes

- The error message in a failure response is human-readable and describes exactly which requirement is not yet satisfied, making it suitable for display in a user interface.
- Call this before [CompleteTask](CompleteTask.md) to surface unmet requirements to the user without triggering the side effects of task completion.
- To retrieve all requirements associated with a task, use [GetTask](GetTask.md) and inspect the `<RequirementDetails>` element.

## Related APIs

- [CompleteTask](CompleteTask.md) -" Mark a task as completed (includes the same requirement checks).
- [GetTask](GetTask.md) -" Get full task details including requirements and current status.
- [SetTaskComment](SetTaskComment.md) -" Set the task comment to satisfy a Comments requirement.
- [SetTaskApprovalStatus](SetTaskApprovalStatus.md) -" Set the approval decision on a task.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4000` | no task by that id, or a requirement has not been met |
| `4030` | there is no ticket at all |
