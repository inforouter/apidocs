# DeleteFlowTaskDef API

Deletes a task definition from the specified workflow step. The workflow definition must be inactive to delete a task definition.

## Endpoint

```
/srv.asmx/DeleteFlowTaskDef
```

## Methods

- **GET** `/srv.asmx/DeleteFlowTaskDef?AuthenticationTicket=...&DomainName=...&FlowName=...&StepNumber=...&TaskDefId=...`
- **POST** `/srv.asmx/DeleteFlowTaskDef` (form data)
- **SOAP** Action: `http://tempuri.org/DeleteFlowTaskDef`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `DomainName` | string | Yes | The domain/library name containing the workflow |
| `FlowName` | string | Yes | The workflow definition name |
| `StepNumber` | int | Yes | The step number containing the task definition |
| `TaskDefId` | int | Yes | The ID of the task definition to delete |

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

1. **Workflow Task Management**
   - Remove unnecessary or incorrect task definitions from a workflow step
   - Clean up task definitions before reactivating a workflow

2. **Workflow Redesign**
   - Delete tasks as part of restructuring a workflow step
   - Remove outdated task assignments from workflow definitions

## Example Requests

### Request (GET)

```
GET /srv.asmx/DeleteFlowTaskDef?AuthenticationTicket=abc123-def456&DomainName=MyLibrary&FlowName=ApprovalFlow&StepNumber=1&TaskDefId=42 HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/DeleteFlowTaskDef HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=abc123-def456&DomainName=MyLibrary&FlowName=ApprovalFlow&StepNumber=1&TaskDefId=42
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/DeleteFlowTaskDef"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <DeleteFlowTaskDef xmlns="http://tempuri.org/">
      <AuthenticationTicket>abc123-def456</AuthenticationTicket>
      <DomainName>MyLibrary</DomainName>
      <FlowName>ApprovalFlow</FlowName>
      <StepNumber>1</StepNumber>
      <TaskDefId>42</TaskDefId>
    </DeleteFlowTaskDef>
  </soap:Body>
</soap:Envelope>
```

## Notes

- The workflow definition must be inactive before a task definition can be deleted. If the workflow is active, deactivate it first using `DeactivateFlowDef`.
- The step must exist within the workflow definition; otherwise an error is returned.
- If the specified `TaskDefId` does not exist within the step, an error is returned.

## Error Codes

Common error responses:

| Error | Description |
|-------|-------------|
| `[901]Session expired or Invalid ticket` | Invalid or expired authentication ticket |
| `Step not found` | The specified step number does not exist in the workflow definition |
| Workflow not found | The specified domain/flow combination does not exist |
| Workflow is active | The workflow definition is currently active and must be deactivated first |

## Related APIs

- `AddFlowTaskDef` - Add a task definition to a workflow step
- `AddFlowStepDef` - Add a step to a workflow definition
- `DeleteFlowStepDef` - Delete a step from a workflow definition
- `ActivateFlowDef` - Activate a workflow definition
- `DeactivateFlowDef` - Deactivate a workflow definition

## Version History

- **New**: Added to provide programmatic access to workflow task definition deletion previously only available through the Control Panel UI
