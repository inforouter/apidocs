# CreateFlowDef3 API

Creates a new workflow definition on the specified domain/library with the full set of configuration options: on-end destination folder, supervisor, webhook event URL, and visibility. The workflow is created in **inactive** state.

> **`Supervisor` is required in practice and then discarded.** An empty name fails with
> `errorCode="4041"`, and a real one is accepted but not attached: the new definition comes back
> with `<Supervisors />` empty. `UpdateWorkflowDefinition` is the only operation that actually
> sets supervisors.

This is the most complete variant of the CreateFlowDef family. Use it when you need to configure `OnEndEventUrl` or `Hide`.

| Variant | Parameters |
|---------|-----------|
| `CreateFlowDef` | `DomainName`, `FlowName`, `ActiveFolderPath` |
| `CreateFlowDef1` | + `OnEndMoveToPath` |
| `CreateFlowDef2` | + `OnEndMoveToPath`, `Supervisor` |
| `CreateFlowDef3` | + `OnEndMoveToPath`, `Supervisor`, `OnEndEventUrl`, `Hide` |

## Endpoint

```
/srv.asmx/CreateFlowDef3
```

## Methods

- **GET** `/srv.asmx/CreateFlowDef3?authenticationTicket=...&DomainName=...&FlowName=...&ActiveFolderPath=...&OnEndMoveToPath=...&Supervisor=...&OnEndEventUrl=...&Hide=...`
- **POST** `/srv.asmx/CreateFlowDef3` (form data)
- **SOAP** Action: `http://tempuri.org/CreateFlowDef3`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DomainName` | string | Yes | Name of the domain/library in which to create the workflow definition. |
| `FlowName` | string | Yes | Name of the new workflow definition. Maximum 32 alphanumeric characters. Must be unique within the domain. |
| `ActiveFolderPath` | string | Yes | Full infoRouter path of the folder where the workflow is active (e.g. `/Corporate/Contracts`). Documents in this folder can be submitted to this workflow. |
| `OnEndMoveToPath` | string | No | Full infoRouter path of the folder where documents are automatically moved when the workflow completes. Pass an empty string to leave documents in place. |
| `Supervisor` | string | No | Login name of the user to assign as the workflow supervisor. Pass an empty string if no supervisor is needed. |
| `OnEndEventUrl` | string | No | Webhook URL that the server calls when the workflow completes. Pass an empty string to disable the event callback. |
| `Hide` | boolean | No | When `true`, the workflow definition is hidden from the document library folder UI. Default: `false`. |

## Response

### Success Response

```xml
<response success="true">
  <FlowDef
    FlowDefID="126"
    FlowName="ContractApproval"
    DomainId="45"
    DomainName="Corporate"
    ActiveFolderPath="/Corporate/Contracts"
    RequiresStartUpPlayers="false"
    Active="false"
    OnEndMoveToPath="/Corporate/Archive"
    OnEndEventUrl="https://erp.example.com/workflow-complete"
    Hide="True">
    <Supervisors>
      <User id="7" />
    </Supervisors>
  </FlowDef>
</response>
```

See [CreateFlowDef](CreateFlowDef.md) for a full description of all response attributes.

### Error Response

```xml
<response success="false" error="Session expired or invalid ticket" errorCode="4010" />
```

## Required Permissions

The calling user must be a **domain/library manager** or a **system administrator**.

## Example

### GET Request

```
GET /srv.asmx/CreateFlowDef3
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &DomainName=Corporate
    &FlowName=ContractApproval
    &ActiveFolderPath=/Corporate/Contracts
    &OnEndMoveToPath=/Corporate/Archive
    &Supervisor=john.smith
    &OnEndEventUrl=https://erp.example.com/workflow-complete
    &Hide=false
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/CreateFlowDef3 HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&DomainName=Corporate&FlowName=ContractApproval&ActiveFolderPath=/Corporate/Contracts&OnEndMoveToPath=/Corporate/Archive&Supervisor=john.smith&OnEndEventUrl=https%3A%2F%2Ferp.example.com%2Fworkflow-complete&Hide=false
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

The overload to use: it takes the supervisor, the end-of-workflow URL and the hidden flag. The
supervisor must be a real user name even though the definition does not keep it.

```javascript
const root = await call('CreateFlowDef3', {
  authenticationTicket: ticket,
  DomainName: 'Public',
  FlowName: 'Invoice approval',
  ActiveFolderPath: '/Public/Invoices',
  OnEndMoveToPath: '/Public/Invoices/Approved',
  Supervisor: 'jsmith',
  OnEndEventUrl: '',
  Hide: false
});

const flowDef = root.querySelector('FlowDef');
console.log(flowDef.getAttribute('FlowDefID'),
            flowDef.getAttribute('Active'),   // "false" - a new definition starts off
            flowDef.getAttribute('Hide'));    // "False" - this one is capitalised
```

## Notes

- `Supervisor` is a **login name** (username), not a display name or user ID. The user must exist in the infoRouter system.
- Pass an empty string for `Supervisor` to create the workflow without a supervisor.
- `OnEndMoveToPath` must refer to an existing folder if non-empty. An invalid path returns an error.
- `OnEndEventUrl` is a plain URL string stored against the workflow. The server calls this URL via HTTP when the workflow ends. Pass an empty string to disable the webhook.
- `Hide=true` hides the workflow from the folder-level workflow list in the document library UI, but administrators and managers can still see it.
- `FlowName` must be alphanumeric, maximum 32 characters, and unique within the domain/library.
- `ActiveFolderPath` must refer to an existing infoRouter folder and cannot be empty.
- The workflow is created in **inactive** state. The typical build sequence is: **CreateFlowDef3 -' AddFlowStepDef -' AddFlowTaskDef -' ActivateFlowDef**.

## Related APIs

- [CreateFlowDef](CreateFlowDef.md) -" Minimal variant with only the three required parameters.
- [CreateFlowDef1](CreateFlowDef1.md) -" Adds `OnEndMoveToPath`.
- [CreateFlowDef2](CreateFlowDef2.md) -" Adds `OnEndMoveToPath` and `Supervisor`.
- [AddFlowStepDef](AddFlowStepDef.md) -" Add steps to the workflow after creation.
- [AddFlowTaskDef](AddFlowTaskDef.md) -" Add task definitions to workflow steps.
- [ActivateFlowDef](ActivateFlowDef.md) -" Activate the workflow so documents can be submitted to it.
- [GetFlowDef](GetFlowDef.md) -" Retrieve the full definition of a workflow.
- [DeactivateFlowDef](DeactivateFlowDef.md) -" Deactivate a workflow to modify it.
- [DeleteWorkflow](DeleteWorkflow.md) -" Permanently delete a workflow definition.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4041` | no folder at `ActiveFolderPath`, or no user by the name in `Supervisor` - including an empty one |
| `4090` | a definition of that name already exists in the library |
| `4030` | the caller may not manage workflows in that library |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
