# StopCurrentWorkflow API

Gracefully stops the running workflow on a document. All pending tasks are dropped, email notifications are sent to dropped task assignees, and the workflow submitter and supervisors receive a workflow-finished notification. The on-end event URL is also fired if the workflow definition has one configured.

Unlike [RemoveCurrentWorkflow](RemoveCurrentWorkflow.md), this operation:
- Works **even if some tasks have already been completed**
- Sends **email notifications** to affected users
- Fires the workflow **on-end event** with `FinishStatus: "Stop"`

## Endpoint

```
/srv.asmx/StopCurrentWorkflow
```

## Methods

- **GET** `/srv.asmx/StopCurrentWorkflow?authenticationTicket=...&path=...`
- **POST** `/srv.asmx/StopCurrentWorkflow` (form data)
- **SOAP** Action: `http://tempuri.org/StopCurrentWorkflow`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full path of the document whose running workflow should be stopped (e.g. `/Cabinet/Project/document.pdf`). |

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
| No restriction on completed tasks | -" |

Unlike [RemoveCurrentWorkflow](RemoveCurrentWorkflow.md), this API does **not** fail if some tasks have already been completed.

## What Happens on Success

1. All **pending workflow tasks** are dropped (status set to Dropped).
2. The **running workflow record** and related data are marked as stopped.
3. Email notifications are sent to all **dropped task assignees** (ON_WORKFLOWSTOPPED event).
4. An **ON_WORKFLOWFINISHED** notification is sent to the workflow **submitter** and all **supervisors**, indicating who stopped the workflow.
5. If the workflow definition has an **on-end event URL** configured, it is called with a JSON payload containing `FinishStatus: "Stop"` and the workflow details.

## Example

### GET Request

```
GET /srv.asmx/StopCurrentWorkflow
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &path=/Cabinet/ProjectDocs/proposal.pdf
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/StopCurrentWorkflow HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&path=/Cabinet/ProjectDocs/proposal.pdf
```

## Notes

- After a successful call, the document is no longer associated with an active workflow and can be submitted to a new workflow via [SubmitDocumentToFlow](SubmitDocumentToFlow.md).
- Use `StopCurrentWorkflow` (with notifications) when you want to formally halt a workflow and inform participants. Use [RemoveCurrentWorkflow](RemoveCurrentWorkflow.md) (no notifications, hard delete) to silently purge an incomplete workflow that has no finished tasks.
- To check whether a document is in a workflow, use [GetDocument](GetDocument.md) and inspect the `CurrentFlowId` field.

## Related APIs

- [RemoveCurrentWorkflow](RemoveCurrentWorkflow.md) -" Permanently remove a running workflow (hard delete, no notifications, fails if completed tasks exist).
- [SubmitDocumentToFlow](SubmitDocumentToFlow.md) -" Submit a document to a workflow.
- [GetTask](GetTask.md) -" Get details of a specific workflow task.
- [getTasks](getTasks.md) -" Get a filtered list of workflow tasks.

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed -" invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Document not found | No document exists at the specified path. |
| Document not in workflow | The document does not have an active running workflow. |
| Access Denied | Calling user is not the workflow submitter or a workflow supervisor. |
