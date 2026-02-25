# DeactivateFlowDef API

Sets a workflow definition back to **inactive** state so its steps and tasks can be modified. A workflow must be inactive before steps or tasks can be added, removed, or changed.

This is the counterpart to [ActivateFlowDef](ActivateFlowDef). The operation is **idempotent**: calling it on an already-inactive workflow returns success immediately without error.

## Endpoint

```
/srv.asmx/DeactivateFlowDef
```

## Methods

- **GET** `/srv.asmx/DeactivateFlowDef?authenticationTicket=...&domainName=...&flowName=...`
- **POST** `/srv.asmx/DeactivateFlowDef` (form data)
- **SOAP** Action: `http://tempuri.org/DeactivateFlowDef`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `domainName` | string | Yes | Name of the domain/library that owns the workflow definition. |
| `flowName` | string | Yes | Name of the workflow definition to deactivate. |

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

The calling user must be a **domain/library manager** or a **system administrator**.

## Example

### GET Request

```
GET /srv.asmx/DeactivateFlowDef
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &domainName=Corporate
    &flowName=ContractApproval
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/DeactivateFlowDef HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&domainName=Corporate&flowName=ContractApproval
```

## Notes

- The operation is **idempotent**: if the workflow is already inactive, the call succeeds without error.
- Unlike `ActivateFlowDef`, deactivation does not perform structural validation — it always succeeds as long as permissions are met.
- After deactivating, you can add or remove steps and task definitions. When finished, call `ActivateFlowDef` to put the workflow back into service.
- Active workflow **instances** (documents currently in the workflow) are not affected by deactivation. Only new submissions are blocked while the definition is inactive.
- The typical edit cycle is: **DeactivateFlowDef → AddFlowStepDef / AddFlowTaskDef / DeleteFlowStepDef / DeleteFlowTaskDef → ActivateFlowDef**.

## Related APIs

- [ActivateFlowDef](ActivateFlowDef) – Activate the workflow definition so documents can be submitted to it.
- [CreateFlowDef](CreateFlowDef) – Create a new workflow definition (created in inactive state).
- [AddFlowStepDef](AddFlowStepDef) – Add a step to an inactive workflow definition.
- [AddFlowTaskDef](AddFlowTaskDef) – Add a task definition to a workflow step.
- [DeleteFlowStepDef](DeleteFlowStepDef) – Remove a step from an inactive workflow definition.
- [DeleteFlowTaskDef](DeleteFlowTaskDef) – Remove a task definition from a workflow step.
- [GetFlowDef](GetFlowDef) – Retrieve the current state and definition of a workflow.
- [DeleteWorkflow](DeleteWorkflow) – Permanently delete a workflow definition.

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed — invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Domain not found | The specified `domainName` does not exist. |
| Workflow not found | No workflow named `flowName` exists in the specified domain. |
| Permission error | Calling user is not a domain manager or system administrator. |
