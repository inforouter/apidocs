# UpdateWorkflowStepDef API

Updates the display name and on-start folder move of an existing workflow step definition.

## Endpoint

```
/srv.asmx/UpdateWorkflowStepDef
```

## Methods

- **GET** `/srv.asmx/UpdateWorkflowStepDef?authenticationTicket=...&domainName=...&workflowName=...&stepNumber=...&newStepName=...&onStartMoveToFolderPath=...`
- **POST** `/srv.asmx/UpdateWorkflowStepDef` (form data)
- **SOAP** Action: `http://tempuri.org/UpdateWorkflowStepDef`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `domainName` | string | Yes | Name of the domain/library that owns the workflow definition. |
| `workflowName` | string | Yes | Name of the workflow definition containing the step to update. |
| `stepNumber` | integer | Yes | 1-based number of the step to update. |
| `newStepName` | string | Yes | New display name for the step. |
| `onStartMoveToFolderPath` | string | No | Full infoRouter folder path where documents are automatically moved when this step starts. Pass an empty string to remove the on-start folder move. |

## Response

### Success Response

```xml
<root success="true" />
```

### Error Response

```xml
<root success="false" error="Error message" />
```

## Required Permissions

Requires workflow supervisor, domain/library manager, or system administrator role.

The workflow definition must be **inactive** before it can be modified. Use [DeactivateFlowDef](DeactivateFlowDef.md) first if the workflow is currently active.

## Example

### Request (POST)

```
POST /srv.asmx/UpdateWorkflowStepDef HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&domainName=Corporate&workflowName=ContractApproval&stepNumber=2&newStepName=LegalReview&onStartMoveToFolderPath=/Corporate/InReview
```

### Request (GET)

```
GET /srv.asmx/UpdateWorkflowStepDef
    ?authenticationTicket=abc123
    &domainName=Corporate
    &workflowName=ContractApproval
    &stepNumber=2
    &newStepName=LegalReview
    &onStartMoveToFolderPath=/Corporate/InReview
HTTP/1.1
Host: yourserver
```

## Notes

- To clear the on-start folder move without setting a new one, pass an empty string for `onStartMoveToFolderPath`.
- Only the step name and on-start folder move are updatable via this API. To change step order or task definitions, use [DeleteFlowStepDef](DeleteFlowStepDef.md) and [AddFlowStepDef1](AddFlowStepDef1.md).
- Use [GetFlowDef](GetFlowDef.md) to retrieve existing step numbers and names before calling this API.

## Related APIs

- [GetFlowDef](GetFlowDef.md) - Retrieve the full workflow definition including all step and task definitions.
- [DeactivateFlowDef](DeactivateFlowDef.md) - Deactivate a workflow definition so its steps can be modified.
- [ActivateFlowDef](ActivateFlowDef.md) - Activate a workflow definition after modifications are complete.
- [AddFlowStepDef1](AddFlowStepDef1.md) - Add a new step to a workflow definition with an on-start folder move.
- [DeleteFlowStepDef](DeleteFlowStepDef.md) - Delete a step from a workflow definition.
- [UpdateWorkflowDefinition](UpdateWorkflowDefinition.md) - Update the top-level properties of a workflow definition.

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed — invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Workflow not found | No workflow definition matching `domainName` and `workflowName` exists. |
| Step not found | No step with the specified `stepNumber` exists in the workflow. |
| Folder not found | The path supplied for `onStartMoveToFolderPath` does not exist. |
