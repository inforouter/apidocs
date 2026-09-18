# AddFlowStepDef1 API

Adds a new step to an existing workflow definition and optionally specifies a folder where documents are automatically moved when that step becomes active. Steps are numbered sequentially; the new step receives the next available number automatically. The workflow definition must be in **inactive** (deactivated) state -" you cannot add steps to an active workflow.

This is the extended variant of `AddFlowStepDef`. Use it when you need to configure the "on-start move-to" folder behaviour. Pass `0` for `OnStartMoveTo` to skip the folder move (equivalent to calling `AddFlowStepDef`).

## Endpoint

```
/srv.asmx/AddFlowStepDef1
```

## Methods

- **GET** `/srv.asmx/AddFlowStepDef1?authenticationTicket=...&DomainName=...&FlowName=...&StepName=...&OnStartMoveTo=...`
- **POST** `/srv.asmx/AddFlowStepDef1` (form data)
- **SOAP** Action: `http://tempuri.org/AddFlowStepDef1`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DomainName` | string | Yes | Name of the domain/library that owns the workflow definition. |
| `FlowName` | string | Yes | Name of the workflow definition to which the step will be added. |
| `StepName` | string | Yes | Display name for the new step. Maximum 32 characters; must be alphanumeric (no special characters or spaces). |
| `OnStartMoveTo` | integer | Yes | Folder ID of the folder where documents are moved when this workflow step starts. Pass `0` to disable the automatic folder move for this step. |

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
GET /srv.asmx/AddFlowStepDef1?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &DomainName=Corporate&FlowName=Document+Approval&StepName=LegalReview&OnStartMoveTo=1042
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/AddFlowStepDef1 HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&DomainName=Corporate&FlowName=Document+Approval&StepName=LegalReview&OnStartMoveTo=1042
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

`AddFlowStepDef` with a folder the document is moved to when the step starts. `OnStartMoveTo` is a
folder **id**, and `0` means the document stays where it is.

```javascript
const root = await call('AddFlowStepDef1', {
  authenticationTicket: ticket,
  DomainName: 'Public',
  FlowName: 'Invoice approval',
  StepName: 'Approve',
  OnStartMoveTo: 0
});

console.log(root.getAttribute('StepNumber'));   // "2" when Review was added first
```

## Notes

- The workflow definition must be **inactive** before steps can be added. If the workflow is currently active, first call `DeactivateFlowDef` to deactivate it.
- `OnStartMoveTo` is a **folder ID** (integer), not a folder path. Use `GetFolder` or `GetFolders` to look up the folder ID if you only know the path. Pass `0` to leave the on-start folder unset.
- When a non-zero `OnStartMoveTo` folder ID is provided, the target folder is automatically marked as a workflow folder in the system (`WFFOLDER=1`). This flag indicates the folder participates in workflow routing.
- Step numbers are assigned automatically as `MAX(existing step number) + 1`. There is no way to insert a step at a specific position.
- `StepName` must consist of alphanumeric characters only (letters and digits); spaces and special characters are not allowed. Maximum length is 32 characters.
- After adding all steps and tasks, activate the workflow with `ActivateFlowDef` before documents can be submitted to it.

## Related APIs

- [AddFlowStepDef](AddFlowStepDef.md) -" Same operation without the `OnStartMoveTo` folder parameter.
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
