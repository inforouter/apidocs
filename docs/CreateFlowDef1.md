# CreateFlowDef1 API

Creates a new workflow definition on the specified domain/library, with an optional destination folder for documents when the workflow ends. The workflow is created in **inactive** state.

This extends `CreateFlowDef` by adding the `OnEndMoveToPath` parameter. For the full parameter set see `CreateFlowDef3`.

| Variant | Extra parameters |
|---------|-----------------|
| `CreateFlowDef` | *(base)* |
| `CreateFlowDef1` | `OnEndMoveToPath` |
| `CreateFlowDef2` | `OnEndMoveToPath`, `Supervisor` |
| `CreateFlowDef3` | `OnEndMoveToPath`, `Supervisor`, `OnEndEventUrl`, `Hide` |

## Endpoint

```
/srv.asmx/CreateFlowDef1
```

## Methods

- **GET** `/srv.asmx/CreateFlowDef1?authenticationTicket=...&DomainName=...&FlowName=...&ActiveFolderPath=...&OnEndMoveToPath=...`
- **POST** `/srv.asmx/CreateFlowDef1` (form data)
- **SOAP** Action: `http://tempuri.org/CreateFlowDef1`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DomainName` | string | Yes | Name of the domain/library in which to create the workflow definition. |
| `FlowName` | string | Yes | Name of the new workflow definition. Maximum 32 alphanumeric characters. Must be unique within the domain. |
| `ActiveFolderPath` | string | Yes | Full infoRouter path of the folder where the workflow is active (e.g. `/Corporate/Contracts`). |
| `OnEndMoveToPath` | string | No | Full infoRouter path of the folder where documents are automatically moved when the workflow completes. Pass an empty string or omit to leave documents in place. |

## Response

### Success Response

```xml
<response success="true">
  <FlowDef
    FlowDefID="124"
    FlowName="ContractApproval"
    DomainId="45"
    DomainName="Corporate"
    ActiveFolderPath="/Corporate/Contracts"
    RequiresStartUpPlayers="false"
    Active="false"
    OnEndMoveToPath="/Corporate/Archive"
    OnEndEventUrl=""
    Hide="False">
    <Supervisors />
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
GET /srv.asmx/CreateFlowDef1
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &DomainName=Corporate
    &FlowName=ContractApproval
    &ActiveFolderPath=/Corporate/Contracts
    &OnEndMoveToPath=/Corporate/Archive
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/CreateFlowDef1 HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&DomainName=Corporate&FlowName=ContractApproval&ActiveFolderPath=/Corporate/Contracts&OnEndMoveToPath=/Corporate/Archive
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

Same as `CreateFlowDef` with a folder to move the document to when the workflow ends. It carries no
supervisor either, so it hits the same inverted check and always fails 4041.

```javascript
// Fails with 4041 on every release that still has the inverted check.
await call('CreateFlowDef1', {
  authenticationTicket: ticket,
  DomainName: 'Public',
  FlowName: 'Invoice approval',
  ActiveFolderPath: '/Public/Invoices',
  OnEndMoveToPath: '/Public/Invoices/Approved'
});
```

## Notes

- `OnEndMoveToPath` must refer to an existing infoRouter folder if provided. An invalid path returns an error.
- Pass an empty string for `OnEndMoveToPath` to create the workflow without an end-move folder (equivalent to `CreateFlowDef`).
- The workflow is created in **inactive** state. Activate with `ActivateFlowDef` after adding steps and tasks.
- The typical workflow-building sequence is: **CreateFlowDef1 -' AddFlowStepDef -' AddFlowTaskDef -' ActivateFlowDef**.

## Related APIs

- [CreateFlowDef](CreateFlowDef.md) -" Minimal variant without `OnEndMoveToPath`.
- [CreateFlowDef2](CreateFlowDef2.md) -" Adds a `Supervisor` parameter.
- [CreateFlowDef3](CreateFlowDef3.md) -" Full variant with all options.
- [AddFlowStepDef](AddFlowStepDef.md) -" Add steps after creation.
- [ActivateFlowDef](ActivateFlowDef.md) -" Activate the workflow definition.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4041` | always - the supervisor lookup is run against an empty name (see Notes) |
| `4030` | the caller may not manage workflows in that library |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
