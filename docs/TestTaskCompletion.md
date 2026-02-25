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
<root success="true" />
```

### Failure -" requirement not met

```xml
<root success="false" error="This task cannot be completed. You did not read the document." />
```

### Failure -" access denied

```xml
<root success="false" error="Access Denied" />
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

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed -" invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Task not found | No task with the specified `taskId` exists. |
| Access Denied | Calling user is not the task assignee. |
| Task not completable | Task is in `NotStarted`, `Completed`, `Dropped`, or `Reassigned` state. |
| Comments required | The task requires a comment but none has been set (unless `exceptTaskComments=true`). |
| Document not read | The latest or published version of the document has not been read by the assignee. |
| AllowedStartDate not reached | The task cannot be completed before its configured allowed start time. |
| Document checked out | The assignee has the document checked out -" must check in before completing. |
| ISO/SOX log required | An ISO or SOX review log entry must be added before completing. |
