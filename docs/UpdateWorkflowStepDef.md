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
<response success="true" error="" errorCode="0" />
```

### Error Response

```xml
<response success="false" error="Error message" />
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

Renames a step and sets the folder the document moves to when the step starts.
`onStartMoveToFolderPath` is declared optional, so an empty value clears the move.

```javascript
await call('UpdateWorkflowStepDef', {
  authenticationTicket: ticket,
  domainName: 'Public',
  workflowName: 'Invoice approval',
  stepNumber: 1,
  newStepName: 'Checked',
  onStartMoveToFolderPath: ''
});
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

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4041` | `stepNumber` names no step of that definition |
| `4000` | no definition by that name, or `onStartMoveToFolderPath` names no folder |
| `4030` | the caller may not manage workflows in that library |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
