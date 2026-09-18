# CreateFlowDef2 API

Creates a new workflow definition on the specified domain/library with an optional on-end destination folder and an optional supervisor. The workflow is created in **inactive** state.

> **`Supervisor` is required in practice and then discarded.** An empty name fails with
> `errorCode="4041"`, and a real one is accepted but not attached: the new definition comes back
> with `<Supervisors />` empty. `UpdateWorkflowDefinition` is the only operation that actually
> sets supervisors.

This extends `CreateFlowDef1` by adding the `Supervisor` parameter. For the full parameter set see `CreateFlowDef3`.

| Variant | Extra parameters |
|---------|-----------------|
| `CreateFlowDef` | *(base)* |
| `CreateFlowDef1` | `OnEndMoveToPath` |
| `CreateFlowDef2` | `OnEndMoveToPath`, `Supervisor` |
| `CreateFlowDef3` | `OnEndMoveToPath`, `Supervisor`, `OnEndEventUrl`, `Hide` |

## Endpoint

```
/srv.asmx/CreateFlowDef2
```

## Methods

- **GET** `/srv.asmx/CreateFlowDef2?authenticationTicket=...&DomainName=...&FlowName=...&ActiveFolderPath=...&OnEndMoveToPath=...&Supervisor=...`
- **POST** `/srv.asmx/CreateFlowDef2` (form data)
- **SOAP** Action: `http://tempuri.org/CreateFlowDef2`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DomainName` | string | Yes | Name of the domain/library in which to create the workflow definition. |
| `FlowName` | string | Yes | Name of the new workflow definition. Maximum 32 alphanumeric characters. Must be unique within the domain. |
| `ActiveFolderPath` | string | Yes | Full infoRouter path of the folder where the workflow is active (e.g. `/Corporate/Contracts`). |
| `OnEndMoveToPath` | string | No | Full infoRouter path of the folder where documents are moved when the workflow completes. Pass an empty string to leave documents in place. |
| `Supervisor` | string | No | Login name of the user to assign as the workflow supervisor. Pass an empty string or omit if no supervisor is needed. |

## Response

### Success Response

```xml
<response success="true">
  <FlowDef
    FlowDefID="125"
    FlowName="ContractApproval"
    DomainId="45"
    DomainName="Corporate"
    ActiveFolderPath="/Corporate/Contracts"
    RequiresStartUpPlayers="false"
    Active="false"
    OnEndMoveToPath="/Corporate/Archive"
    OnEndEventUrl=""
    Hide="False">
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
GET /srv.asmx/CreateFlowDef2
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &DomainName=Corporate
    &FlowName=ContractApproval
    &ActiveFolderPath=/Corporate/Contracts
    &OnEndMoveToPath=/Corporate/Archive
    &Supervisor=john.smith
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/CreateFlowDef2 HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&DomainName=Corporate&FlowName=ContractApproval&ActiveFolderPath=/Corporate/Contracts&OnEndMoveToPath=/Corporate/Archive&Supervisor=john.smith
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

Creates a workflow definition and names a supervisor. The supervisor has to be given - an empty one
fails 4041 - but it is then discarded, so the definition comes back with `<Supervisors />` empty.
`UpdateWorkflowDefinition` is the only operation that actually attaches one.

```javascript
const root = await call('CreateFlowDef2', {
  authenticationTicket: ticket,
  DomainName: 'Public',
  FlowName: 'Invoice approval',
  ActiveFolderPath: '/Public/Invoices',
  OnEndMoveToPath: '',
  Supervisor: 'jsmith'
});

const flowDefId = root.querySelector('FlowDef').getAttribute('FlowDefID');
console.log(flowDefId);   // pass this to SubmitDocumentToFlow later
```

## Notes

- `Supervisor` is a **login name** (username), not a display name or user ID.
- The supervisor user must exist in the infoRouter system. An invalid username returns an error.
- Pass an empty string for `Supervisor` to create the workflow without a supervisor.
- `OnEndMoveToPath` must refer to an existing folder if non-empty. An invalid path returns an error.
- The `OnEndEventUrl` and `Hide` fields are fixed at `""` and `false` respectively. Use `CreateFlowDef3` to configure those.
- The workflow is created in **inactive** state. Activate with `ActivateFlowDef` after adding steps and tasks.

## Related APIs

- [CreateFlowDef](CreateFlowDef.md) -" Minimal variant.
- [CreateFlowDef1](CreateFlowDef1.md) -" Adds `OnEndMoveToPath` only.
- [CreateFlowDef3](CreateFlowDef3.md) -" Full variant with all options including event URL and hidden flag.
- [AddFlowStepDef](AddFlowStepDef.md) -" Add steps after creation.
- [ActivateFlowDef](ActivateFlowDef.md) -" Activate the workflow definition.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4041` | no folder at `ActiveFolderPath`, or no user by the name in `Supervisor` - including an empty one |
| `4090` | a definition of that name already exists in the library |
| `4030` | the caller may not manage workflows in that library |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
