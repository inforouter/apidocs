# AddFlowStepDef API

Adds a new step to an existing workflow definition. Steps are numbered sequentially starting at 1; the new step receives the next available number automatically. The workflow definition must be in **inactive** (deactivated) state -" you cannot add steps to an active workflow.

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
<response success="true" StepNumber="2" />
```

| Attribute | Description |
|-----------|-------------|
| `success` | `"true"` when the step was created successfully. |
| `StepNumber` | The step number assigned to the new step (integer, sequential). |

### Error Response

```xml
<response success="false" error="Session expired or invalid ticket" errorCode="4010" />
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
<response success="true" StepNumber="3" />
```

## JavaScript

Every call answers XML with HTTP 200, success or not, so `success` is the thing to branch on and
`errorCode` is the number to report.

```javascript
async function call(action, params) {
  const response = await fetch(`/srv.asmx/${action}?${new URLSearchParams(params)}`);
  const root = new DOMParser()
    .parseFromString(await response.text(), 'text/xml')
    .documentElement;

  if (root.getAttribute('success') !== 'true') {
    throw new Error(`${root.getAttribute('errorCode')}: ${root.getAttribute('error')}`);
  }
  return root;
}
```

Adds a step and answers with the number it was given. Step numbers start at 1 and go up in the order
the steps are added; names are not checked for uniqueness, so two steps can share one.

```javascript
const root = await call('AddFlowStepDef', {
  authenticationTicket: ticket,
  DomainName: 'Public',
  FlowName: 'Invoice approval',
  StepName: 'Review'
});

const stepNumber = root.getAttribute('StepNumber');   // "1"
```

## Notes

- The workflow definition must be **inactive** before steps can be added. If the workflow is currently active, first call `DeactivateFlowDef` to deactivate it.
- Step numbers are assigned automatically as `MAX(existing step number) + 1`. There is no way to insert a step at a specific position.
- `StepName` must consist of alphanumeric characters only (letters and digits); spaces and special characters are not allowed.
- This variant always creates the step **without** an "on-start move-to" folder (the folder where documents are relocated when this step begins). To specify such a folder, use `AddFlowStepDef1` and provide the folder ID in `OnStartMoveTo`.
- After adding all steps and tasks, activate the workflow with `ActivateFlowDef` before documents can be submitted to it.

## Related APIs

- [AddFlowStepDef1](AddFlowStepDef1.md) -" Same operation with an additional `OnStartMoveTo` folder ID parameter.
- [AddFlowTaskDef](AddFlowTaskDef.md) -" Add a task definition to a workflow step.
- [CreateFlowDef](CreateFlowDef.md) -" Create the workflow definition before adding steps.
- [DeactivateFlowDef](DeactivateFlowDef.md) -" Deactivate an active workflow so its steps can be modified.
- [DeleteFlowStepDef](DeleteFlowStepDef.md) -" Delete a step from a workflow definition.
- [GetFlowDef](GetFlowDef.md) -" Retrieve the full definition of a workflow including its steps.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4000` | no definition by that name in the library, or the definition is active |
| `4030` | the caller may not manage workflows in that library |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
