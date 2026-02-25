# DeleteFlowStepDef API

Deletes a step from the specified workflow definition. The workflow definition must be inactive to delete a step.

## Endpoint

```
/srv.asmx/DeleteFlowStepDef
```

## Methods

- **GET** `/srv.asmx/DeleteFlowStepDef?AuthenticationTicket=...&DomainName=...&FlowName=...&StepName=...`
- **POST** `/srv.asmx/DeleteFlowStepDef` (form data)
- **SOAP** Action: `http://tempuri.org/DeleteFlowStepDef`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `DomainName` | string | Yes | The domain/library name containing the workflow |
| `FlowName` | string | Yes | The workflow definition name |
| `StepName` | string | Yes | The name of the step to delete |

## Response Structure

### Success Response

```xml
<response success="true" />
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

## Required Permissions

- User must be authenticated (valid authentication ticket required)
- User must have workflow management permissions for the domain
- The workflow definition must be inactive (not active)

## Use Cases

1. **Workflow Definition Management**
   - Remove unnecessary or incorrect steps from a workflow definition
   - Simplify workflow definitions by removing unused steps

2. **Workflow Redesign**
   - Delete steps as part of restructuring a workflow definition
   - Clean up steps before reactivating a modified workflow

## Example Requests

### Request (GET)

```
GET /srv.asmx/DeleteFlowStepDef?AuthenticationTicket=abc123-def456&DomainName=MyLibrary&FlowName=ApprovalFlow&StepName=ReviewStep HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/DeleteFlowStepDef HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=abc123-def456&DomainName=MyLibrary&FlowName=ApprovalFlow&StepName=ReviewStep
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/DeleteFlowStepDef"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <DeleteFlowStepDef xmlns="http://tempuri.org/">
      <AuthenticationTicket>abc123-def456</AuthenticationTicket>
      <DomainName>MyLibrary</DomainName>
      <FlowName>ApprovalFlow</FlowName>
      <StepName>ReviewStep</StepName>
    </DeleteFlowStepDef>
  </soap:Body>
</soap:Envelope>
```

## Notes

- The workflow definition must be inactive before a step can be deleted. If the workflow is active, deactivate it first using `DeactivateFlowDef`.
- Deleting a step also removes all task definitions associated with that step.
- The step is identified by name (case-insensitive match).
- If the step has an associated "on start move to" folder, that association is also removed.

## Error Codes

Common error responses:

| Error | Description |
|-------|-------------|
| `[901]Session expired or Invalid ticket` | Invalid or expired authentication ticket |
| `Step not found` | The specified step name does not exist in the workflow definition |
| Workflow not found | The specified domain/flow combination does not exist |
| Workflow is active | The workflow definition is currently active and must be deactivated first |

## Related APIs

- `AddFlowStepDef` - Add a step to a workflow definition
- `AddFlowStepDef1` - Add a step with an "on start move to" folder
- `ActivateFlowDef` - Activate a workflow definition
- `DeactivateFlowDef` - Deactivate a workflow definition
- `AddFlowTaskDef` - Add a task definition to a workflow step

## Version History

- **New**: Added to provide programmatic access to workflow step deletion previously only available through the Control Panel UI
