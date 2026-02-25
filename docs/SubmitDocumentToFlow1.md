# SubmitDocumentToFlow1 API

Submits a document to a workflow definition, with the ability to specify which users and/or groups should be assigned to the **first step** of the workflow at submission time. This overrides the default task assignees configured in the workflow definition for the first step only.

For all subsequent steps, the workflow definition's configured assignees are used.

To submit with the default assignees from the workflow definition, use [SubmitDocumentToFlow](SubmitDocumentToFlow.md).

## Endpoint

```
/srv.asmx/SubmitDocumentToFlow1
```

## Methods

- **GET** `/srv.asmx/SubmitDocumentToFlow1?authenticationTicket=...&Path=...&FlowDefID=...&StepPlayerIDs=...&StepGroupIDs=...`
- **POST** `/srv.asmx/SubmitDocumentToFlow1` (form data)
- **SOAP** Action: `http://tempuri.org/SubmitDocumentToFlow1`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full path of the document to submit (e.g. `/Cabinet/Project/document.pdf`). |
| `FlowDefID` | integer | Yes | Numeric ID of the workflow definition. Must be a positive integer. |
| `StepPlayerIDs` | string | No | Comma-separated list of user IDs to assign as task assignees for the first step (e.g. `15,23,47`). Pass empty or omit to use the workflow definition's default assignees. |
| `StepGroupIDs` | string | No | Comma-separated list of user group IDs to assign as task assignees for the first step (e.g. `3,7`). Pass empty or omit to use the workflow definition's default assignees. |

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

Same as [SubmitDocumentToFlow](SubmitDocumentToFlow.md):

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

### GET Request -" assigning users to the first step

```
GET /srv.asmx/SubmitDocumentToFlow1
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &Path=/Cabinet/ProjectDocs/proposal.pdf
    &FlowDefID=42
    &StepPlayerIDs=15,23
    &StepGroupIDs=
HTTP/1.1
Host: yourserver
```

### GET Request -" assigning a group to the first step

```
GET /srv.asmx/SubmitDocumentToFlow1
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &Path=/Cabinet/ProjectDocs/proposal.pdf
    &FlowDefID=42
    &StepPlayerIDs=
    &StepGroupIDs=7
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/SubmitDocumentToFlow1 HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&Path=/Cabinet/ProjectDocs/proposal.pdf&FlowDefID=42&StepPlayerIDs=15%2C23&StepGroupIDs=
```

## Notes

- `StepPlayerIDs` contains **user IDs** (numeric), not login names. To get a user's ID, use [GetUser](GetUser.md).
- `StepGroupIDs` contains **user group IDs** (numeric). To get a group's ID, use [GetUserGroup](GetUserGroup.md).
- Both `StepPlayerIDs` and `StepGroupIDs` can be specified simultaneously to mix individual users and groups for the first step.
- Only the **first step** assignees are overridden. All subsequent steps use the workflow definition's configured assignees.
- If both `StepPlayerIDs` and `StepGroupIDs` are empty, the workflow definition's default first-step assignees are used (equivalent to calling [SubmitDocumentToFlow](SubmitDocumentToFlow.md)).
- The `FlowDefID` is the workflow **definition** ID, not a running workflow ID. Use [GetFolderFlows](GetFolderFlows.md) to find definition IDs.

## Related APIs

- [SubmitDocumentToFlow](SubmitDocumentToFlow.md) -" Submit using the workflow definition's default assignees.
- [GetFolderFlows](GetFolderFlows.md) -" List workflow definitions available for a folder.
- [GetUser](GetUser.md) -" Get a user's numeric ID by login name.
- [GetUserGroup](GetUserGroup.md) -" Get a group's numeric ID by name.
- [StopCurrentWorkflow](StopCurrentWorkflow.md) -" Stop a running workflow gracefully.
- [getTasks](getTasks.md) -" Get workflow tasks created after submission.

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
