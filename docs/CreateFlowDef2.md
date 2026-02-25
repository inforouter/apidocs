# CreateFlowDef2 API

Creates a new workflow definition on the specified domain/library with an optional on-end destination folder and an optional supervisor. The workflow is created in **inactive** state.

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
<root success="true">
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
</root>
```

See [CreateFlowDef](CreateFlowDef.md) for a full description of all response attributes.

### Error Response

```xml
<root success="false" error="[901] Session expired or Invalid ticket" />
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

## Notes

- `Supervisor` is a **login name** (username), not a display name or user ID.
- The supervisor user must exist in the infoRouter system. An invalid username returns an error.
- Pass an empty string for `Supervisor` to create the workflow without a supervisor.
- `OnEndMoveToPath` must refer to an existing folder if non-empty. An invalid path returns an error.
- The `OnEndEventUrl` and `Hide` fields are fixed at `""` and `false` respectively. Use `CreateFlowDef3` to configure those.
- The workflow is created in **inactive** state. Activate with `ActivateFlowDef` after adding steps and tasks.

## Related APIs

- [CreateFlowDef](CreateFlowDef.md) – Minimal variant.
- [CreateFlowDef1](CreateFlowDef1.md) – Adds `OnEndMoveToPath` only.
- [CreateFlowDef3](CreateFlowDef3.md) – Full variant with all options including event URL and hidden flag.
- [AddFlowStepDef](AddFlowStepDef.md) – Add steps after creation.
- [ActivateFlowDef](ActivateFlowDef.md) – Activate the workflow definition.

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed — invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Domain not found | The specified `DomainName` does not exist. |
| Folder not found | `ActiveFolderPath` or `OnEndMoveToPath` does not exist. |
| Empty active folder | `ActiveFolderPath` cannot be empty. |
| Supervisor not found | The specified `Supervisor` username does not exist. |
| Name validation error | `FlowName` exceeds 32 characters or contains invalid characters. |
| Duplicate name | A workflow with the same name already exists in this domain. |
| Permission error | Calling user is not a domain manager or administrator. |
