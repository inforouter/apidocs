# DeleteTask API

Deletes an active workflow task by its task ID. All task attachments are also removed as part of the operation.

## Endpoint

```
/srv.asmx/DeleteTask
```

## Methods

- **GET** `/srv.asmx/DeleteTask?authenticationTicket=...&taskId=...`
- **POST** `/srv.asmx/DeleteTask` (form data)
- **SOAP** Action: `http://tempuri.org/DeleteTask`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `taskId` | integer | Yes | Unique numeric ID of the task to delete. |

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

The calling user must have the **Remove Task** permission on the document the task is associated with. The user who originally assigned the task is also always permitted to delete it.

## Behavior

The exact behavior depends on the relationship between the task and its workflow definition:

| Scenario | Result |
|----------|--------|
| Task belongs to the current workflow definition | Task record and all its attachments are permanently deleted. |
| Ad-hoc task whose workflow definition has since changed | Task status is set to **Dropped** (soft delete); workflow advancement is triggered if it was the last task in its step. |
| Regular workflow task whose workflow definition has since changed | Returns an error — such tasks cannot be deleted directly. |

## Example

### GET Request

```
GET /srv.asmx/DeleteTask
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &taskId=4812
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/DeleteTask HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&taskId=4812
```

## Notes

- The `taskId` is the unique numeric identifier for the task, available from APIs such as [GetTask](GetTask) or [getTasks](getTasks).
- Deleting a task also removes all workflow attachments associated with it.
- For ad-hoc tasks in a changed workflow, deletion sets the task to `Dropped` status rather than physically removing the record. The workflow may automatically advance if that was the last pending task in the step.
- To obtain a list of tasks for a document or user, use [getTasks](getTasks).

## Related APIs

- [GetTask](GetTask) – Retrieve full details of a task including its task ID.
- [getTasks](getTasks) – Get a filtered list of workflow tasks.
- [CompleteTask](CompleteTask) – Mark a task as completed.
- [ReassignTask](ReassignTask) – Reassign a task to a different user.
- [StopCurrentWorkflow](StopCurrentWorkflow) – Stop the entire active workflow on a document.

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed — invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Task not found | No task with the specified `taskId` exists. |
| Permission error | Calling user does not have the Remove Task permission on the document. |
| Workflow mismatch | Regular (non-ad-hoc) task whose workflow definition has changed cannot be deleted. |
