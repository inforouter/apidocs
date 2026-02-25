# SubmitDocumentToFlow API

Submits a document to a workflow definition. Once submitted, the workflow engine creates running tasks based on the workflow definition, assigns them to the configured task assignees, and sends task notification emails.

To override the task assignees for the first step at submission time, use [SubmitDocumentToFlow1](SubmitDocumentToFlow1.md).

## Endpoint

```
/srv.asmx/SubmitDocumentToFlow
```

## Methods

- **GET** `/srv.asmx/SubmitDocumentToFlow?authenticationTicket=...&Path=...&FlowDefID=...`
- **POST** `/srv.asmx/SubmitDocumentToFlow` (form data)
- **SOAP** Action: `http://tempuri.org/SubmitDocumentToFlow`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full path of the document to submit (e.g. `/Cabinet/Project/document.pdf`). |
| `FlowDefID` | integer | Yes | Numeric ID of the workflow definition to submit the document to. Must be a positive integer. |

## Response

### Success Response

```xml
<root success="true" />
```

### Error Response

```xml
<root success="false" error="Workflow submission failed. Document is currently checked out." />
```

## Required Permissions

The calling user must have the **Submit to Workflow** permission on the document.

Anonymous access is not permitted. The infoRouter server must have a Workflow license.

## Preconditions

| Condition | Required |
|-----------|----------|
| Document must exist at the specified path | Yes |
| Document must not be offline | Yes |
| Document must not be checked out | Yes |
| Document must not already be in a workflow | Yes |
| Document must not be a shortcut | Yes |
| Workflow definition must exist and be **active** | Yes |
| Workflow definition must belong to the same library as the document | Yes |

## Example

### GET Request

```
GET /srv.asmx/SubmitDocumentToFlow
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &Path=/Cabinet/ProjectDocs/proposal.pdf
    &FlowDefID=42
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/SubmitDocumentToFlow HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&Path=/Cabinet/ProjectDocs/proposal.pdf&FlowDefID=42
```

## Notes

- The `FlowDefID` is the ID of the workflow **definition** (created with [CreateFlowDef](CreateFlowDef.md)), not the ID of a running workflow instance.
- Task assignees are taken from the workflow definition. To specify custom assignees for the first step at submission time, use [SubmitDocumentToFlow1](SubmitDocumentToFlow1.md).
- To find the workflow definition ID, use [GetFolderFlows](GetFolderFlows.md) or [GetDomainFlows](GetDomainFlows.md).
- After a successful submission, the document's `CurrentFlowId` is set to the running workflow ID. Use [GetTask](GetTask.md) or [getTasks](getTasks.md) to retrieve the created tasks.
- A document can only be in one active workflow at a time. Stop or remove the current workflow before re-submitting.

## Related APIs

- [SubmitDocumentToFlow1](SubmitDocumentToFlow1.md) -" Submit with custom first-step task assignees.
- [GetFolderFlows](GetFolderFlows.md) -" List workflow definitions available for a folder.
- [GetDomainFlows](GetDomainFlows.md) -" List workflow definitions for a library/domain.
- [StopCurrentWorkflow](StopCurrentWorkflow.md) -" Stop a running workflow gracefully.
- [RemoveCurrentWorkflow](RemoveCurrentWorkflow.md) -" Remove a running workflow (hard delete).
- [getTasks](getTasks.md) -" Get the workflow tasks created after submission.

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed -" invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Document not found | No document exists at the specified path. |
| Access Denied | Calling user does not have Submit to Workflow permission. |
| Document offline | The document is currently offline. |
| Document checked out | The document is currently checked out. |
| Already in workflow | The document is already in an active workflow. |
| Document is shortcut | Shortcuts cannot be submitted to workflows. |
| Workflow not found | No active workflow definition with the specified `FlowDefID` exists. |
| Workflow inactive | The workflow definition is not active. Activate it with [ActivateFlowDef](ActivateFlowDef.md). |
| Library mismatch | The workflow definition does not belong to the same library as the document. |
| License required | The server does not have a Workflow license. |
