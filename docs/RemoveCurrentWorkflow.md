# RemoveCurrentWorkflow API

Permanently removes the running workflow from a document. All workflow tasks, task attachments, running workflow steps, and the workflow execution record are deleted. The document's workflow fields are cleared so it can be submitted to a new workflow.

This is a hard delete with **no email notifications**. To stop a workflow gracefully (with notifications to task assignees), use [StopCurrentWorkflow](StopCurrentWorkflow.md) instead.

## Endpoint

```
/srv.asmx/RemoveCurrentWorkflow
```

## Methods

- **GET** `/srv.asmx/RemoveCurrentWorkflow?authenticationTicket=...&path=...`
- **POST** `/srv.asmx/RemoveCurrentWorkflow` (form data)
- **SOAP** Action: `http://tempuri.org/RemoveCurrentWorkflow`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full path of the document whose running workflow should be removed (e.g. `/Cabinet/Project/document.pdf`). |

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
- The **workflow submitter** (the user who submitted the document to the workflow), or
- A **workflow supervisor** for the running workflow.

Anonymous access is not permitted.

## Preconditions

| Condition | Required |
|-----------|----------|
| Document must exist at the specified path | Yes |
| Document must currently be in a workflow (`CurrentFlowId > 0`) | Yes |
| No tasks in the workflow may have been both **started and finished** | Yes |

If any task has both a `StartDate` and a `FinishDate` set (i.e., it was completed), the operation is rejected. Use [StopCurrentWorkflow](StopCurrentWorkflow.md) if completed tasks are present.

## What Happens on Success

1. All **workflow task attachments** linked to the running workflow are deleted.
2. All **workflow tasks** (IRTASKS) belonging to the running workflow are deleted.
3. All **running workflow steps** (RUNNINGWFSTEPS) are deleted.
4. The **running workflow record** (RUNNINGWF) is deleted.
5. The document's workflow fields in the PUBLICATION table are cleared (e.g., `CurrentFlowId` reset to 0).
6. **No email notifications** are sent to task assignees or the submitter.

## Example

### GET Request

```
GET /srv.asmx/RemoveCurrentWorkflow
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &path=/Cabinet/ProjectDocs/proposal.pdf
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/RemoveCurrentWorkflow HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&path=/Cabinet/ProjectDocs/proposal.pdf
```

## Notes

- After a successful call, the document is no longer associated with any workflow and can be submitted to a new workflow via [SubmitDocumentToFlow](SubmitDocumentToFlow.md).
- This operation is irreversible. All task history for the removed workflow is permanently deleted.
- To check whether a document is currently in a workflow, use [GetDocument](GetDocument.md) and inspect the `CurrentFlowId` field.
- If you need to stop a workflow while preserving the ability for assignees to be notified, use [StopCurrentWorkflow](StopCurrentWorkflow.md).

## Related APIs

- [StopCurrentWorkflow](StopCurrentWorkflow.md) -" Stop a running workflow gracefully, with notifications to task assignees.
- [SubmitDocumentToFlow](SubmitDocumentToFlow.md) -" Submit a document to a workflow.
- [GetTask](GetTask.md) -" Get details of a specific workflow task.
- [getTasks](getTasks.md) -" Get a filtered list of workflow tasks.
- [DeleteTask](DeleteTask.md) -" Delete a specific task from a running workflow.

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed -" invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Document not found | No document exists at the specified path. |
| Document not in workflow | The document does not have an active running workflow. |
| Access Denied | Calling user is not the workflow submitter or a workflow supervisor. |
| Finished tasks exist | One or more tasks have already been completed; the workflow cannot be removed. |
