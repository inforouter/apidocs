# CreateFlowDef API

Creates a new workflow definition on the specified domain/library. The workflow is created in **inactive** state -" steps and tasks must be added with `AddFlowStepDef` and `AddFlowTaskDef` before activating it with `ActivateFlowDef`.

> **This overload cannot succeed on the current release.** The service tests whether the
> supervisor name is *empty* and then looks that empty name up, so a call that carries no
> supervisor always fails with `errorCode="4041"` "User not found". Use `CreateFlowDef3` with a
> real `Supervisor` until the condition is corrected.

This is the minimal variant. Use the numbered variants for additional configuration:

| Variant | Extra parameters |
|---------|-----------------|
| `CreateFlowDef` | *(base -" no extras)* |
| `CreateFlowDef1` | `OnEndMoveToPath` |
| `CreateFlowDef2` | `OnEndMoveToPath`, `Supervisor` |
| `CreateFlowDef3` | `OnEndMoveToPath`, `Supervisor`, `OnEndEventUrl`, `Hide` |

## Endpoint

```
/srv.asmx/CreateFlowDef
```

## Methods

- **GET** `/srv.asmx/CreateFlowDef?authenticationTicket=...&DomainName=...&FlowName=...&ActiveFolderPath=...`
- **POST** `/srv.asmx/CreateFlowDef` (form data)
- **SOAP** Action: `http://tempuri.org/CreateFlowDef`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DomainName` | string | Yes | Name of the domain/library in which to create the workflow definition. |
| `FlowName` | string | Yes | Name of the new workflow definition. Maximum 32 alphanumeric characters. Must be unique within the domain. |
| `ActiveFolderPath` | string | Yes | Full infoRouter path of the folder where the workflow is active (e.g. `/Corporate/Contracts`). Documents in this folder and its sub-folders can be submitted to this workflow. |

## Response

### Success Response

```xml
<response success="true">
  <FlowDef
    FlowDefID="123"
    FlowName="ContractApproval"
    DomainId="45"
    DomainName="Corporate"
    ActiveFolderPath="/Corporate/Contracts"
    RequiresStartUpPlayers="false"
    Active="false"
    OnEndMoveToPath=""
    OnEndEventUrl=""
    Hide="False">
    <Supervisors />
  </FlowDef>
</response>
```

| Attribute | Description |
|-----------|-------------|
| `FlowDefID` | The unique integer ID of the newly created workflow definition. |
| `FlowName` | Name of the workflow definition. |
| `DomainId` | Internal ID of the owning domain/library. |
| `DomainName` | Name of the owning domain/library. |
| `ActiveFolderPath` | Path of the folder where the workflow is active. |
| `RequiresStartUpPlayers` | Whether the workflow requires startup players to be defined. |
| `Active` | Always `"false"` for a newly created workflow. |
| `OnEndMoveToPath` | Path of the folder documents are moved to when the workflow ends (empty if not set). |
| `OnEndEventUrl` | Webhook URL called when the workflow ends (empty if not set). |
| `Hide` | Whether the workflow is hidden from the folder UI. |
| `Supervisors` | List of supervisor users and groups. Empty for this variant. |

### Error Response

```xml
<response success="false" error="Session expired or invalid ticket" errorCode="4010" />
```

## Required Permissions

The calling user must be a **domain/library manager** or a **system administrator**.

## Example

### GET Request

```
GET /srv.asmx/CreateFlowDef
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &DomainName=Corporate
    &FlowName=ContractApproval
    &ActiveFolderPath=/Corporate/Contracts
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/CreateFlowDef HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&DomainName=Corporate&FlowName=ContractApproval&ActiveFolderPath=/Corporate/Contracts
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

Creates a workflow definition over a folder. **This overload cannot succeed today**: the service
looks the supervisor up when the name is *empty*, so a call that carries none always fails 4041
"User not found". Use `CreateFlowDef3` with a `Supervisor` until that is fixed.

```javascript
// Fails with 4041 on every release that still has the inverted check.
await call('CreateFlowDef', {
  authenticationTicket: ticket,
  DomainName: 'Public',
  FlowName: 'Invoice approval',
  ActiveFolderPath: '/Public/Invoices'
});
```

## Notes

- The workflow is created in **inactive** state. No documents can be submitted to it until it is activated with `ActivateFlowDef`.
- `FlowName` must be alphanumeric, maximum 32 characters, and must be unique within the domain/library.
- `ActiveFolderPath` must refer to an existing infoRouter folder. It cannot be empty.
- The `OnEndMoveToPath`, supervisor, `OnEndEventUrl`, and `Hide` fields are all left at their defaults (empty / `false`) by this variant. Use `CreateFlowDef1`, `CreateFlowDef2`, or `CreateFlowDef3` to configure those.
- The typical workflow-building sequence is: **CreateFlowDef -' AddFlowStepDef -' AddFlowTaskDef -' ActivateFlowDef**.

## Related APIs

- [CreateFlowDef1](CreateFlowDef1.md) -" Creates a workflow definition with an on-end destination folder.
- [CreateFlowDef2](CreateFlowDef2.md) -" Creates a workflow definition with an on-end folder and a supervisor.
- [CreateFlowDef3](CreateFlowDef3.md) -" Creates a workflow definition with all options including event URL and hidden flag.
- [AddFlowStepDef](AddFlowStepDef.md) -" Add steps to the workflow definition after creation.
- [AddFlowTaskDef](AddFlowTaskDef.md) -" Add task definitions to workflow steps.
- [ActivateFlowDef](ActivateFlowDef.md) -" Activate the workflow so documents can be submitted to it.
- [GetFlowDef](GetFlowDef.md) -" Retrieve the full definition of a workflow.
- [DeactivateFlowDef](DeactivateFlowDef.md) -" Deactivate a workflow to modify its steps.
- [DeleteWorkflow](DeleteWorkflow.md) -" Permanently delete a workflow definition.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4041` | always - the supervisor lookup is run against an empty name (see Notes) |
| `4030` | the caller may not manage workflows in that library |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
