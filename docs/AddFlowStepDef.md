# AddFlowStepDef API

Adds a new step to an existing workflow definition. Steps are numbered sequentially starting at 1; the new step receives the next available number automatically. The workflow definition must be in **inactive** (deactivated) state — you cannot add steps to an active workflow.

Use `AddFlowStepDef1` if you also need to specify a folder where documents are moved when this step starts.

## Endpoint

```
/srv.asmx/AddFlowStepDef
```

## Methods

- **GET** `/srv.asmx/AddFlowStepDef?authenticationTicket=...&DomainName=...&FlowName=...&StepName=...`
- **POST** `/srv.asmx/AddFlowStepDef` (form data)
- **SOAP** Action: `http://tempuri.org/AddFlowStepDef`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DomainName` | string | Yes | Name of the domain/library that owns the workflow definition. |
| `FlowName` | string | Yes | Name of the workflow definition to which the step will be added. |
| `StepName` | string | Yes | Display name for the new step. Maximum 32 characters; must be alphanumeric (no special characters). |

## Response

### Success Response

```xml
<root success="true" StepNumber="2" />
```

| Attribute | Description |
|-----------|-------------|
| `success` | `"true"` when the step was created successfully. |
| `StepNumber` | The step number assigned to the new step (integer, sequential). |

### Error Response

```xml
<root success="false" error="[901] Session expired or Invalid ticket" />
```

## Required Permissions

The calling user must be a **workflow supervisor**, a **domain/library manager**, or a **system administrator**. Regular members of the domain cannot modify workflow definitions.

## Example

### GET Request

```
GET /srv.asmx/AddFlowStepDef?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &DomainName=Corporate&FlowName=Document+Approval&StepName=Legal+Review
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/AddFlowStepDef HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&DomainName=Corporate&FlowName=Document+Approval&StepName=Legal+Review
```

### Success Response

```xml
<root success="true" StepNumber="3" />
```

## Notes

- The workflow definition must be **inactive** before steps can be added. If the workflow is currently active, first call `DeactivateFlowDef` to deactivate it.
- Step numbers are assigned automatically as `MAX(existing step number) + 1`. There is no way to insert a step at a specific position.
- `StepName` must consist of alphanumeric characters only (letters and digits); spaces and special characters are not allowed.
- This variant always creates the step **without** an "on-start move-to" folder (the folder where documents are relocated when this step begins). To specify such a folder, use `AddFlowStepDef1` and provide the folder ID in `OnStartMoveTo`.
- After adding all steps and tasks, activate the workflow with `ActivateFlowDef` before documents can be submitted to it.

## Related APIs

- [AddFlowStepDef1](AddFlowStepDef1.md) – Same operation with an additional `OnStartMoveTo` folder ID parameter.
- [AddFlowTaskDef](AddFlowTaskDef.md) – Add a task definition to a workflow step.
- [CreateFlowDef](CreateFlowDef.md) – Create the workflow definition before adding steps.
- [DeactivateFlowDef](DeactivateFlowDef.md) – Deactivate an active workflow so its steps can be modified.
- [DeleteFlowStepDef](DeleteFlowStepDef.md) – Delete a step from a workflow definition.
- [GetFlowDef](GetFlowDef.md) – Retrieve the full definition of a workflow including its steps.

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed — invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Workflow active error | Cannot add steps to an active workflow definition. Deactivate first using `DeactivateFlowDef`. |
| Name validation error | Step name exceeds 32 characters or contains invalid characters. |
| Workflow not found | The specified `DomainName`/`FlowName` combination does not exist. |
| Permission error | Calling user does not have workflow management permissions for this domain. |
