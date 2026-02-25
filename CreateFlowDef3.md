# CreateFlowDef3 API

Creates a new workflow definition on the specified domain/library with the full set of configuration options: on-end destination folder, supervisor, webhook event URL, and visibility. The workflow is created in **inactive** state.

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
<root success="true">
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
</root>
```

See [CreateFlowDef](CreateFlowDef) for a full description of all response attributes.

### Error Response

```xml
<root success="false" error="[901] Session expired or Invalid ticket" />
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

## Notes

- `Supervisor` is a **login name** (username), not a display name or user ID. The user must exist in the infoRouter system.
- Pass an empty string for `Supervisor` to create the workflow without a supervisor.
- `OnEndMoveToPath` must refer to an existing folder if non-empty. An invalid path returns an error.
- `OnEndEventUrl` is a plain URL string stored against the workflow. The server calls this URL via HTTP when the workflow ends. Pass an empty string to disable the webhook.
- `Hide=true` hides the workflow from the folder-level workflow list in the document library UI, but administrators and managers can still see it.
- `FlowName` must be alphanumeric, maximum 32 characters, and unique within the domain/library.
- `ActiveFolderPath` must refer to an existing infoRouter folder and cannot be empty.
- The workflow is created in **inactive** state. The typical build sequence is: **CreateFlowDef3 → AddFlowStepDef → AddFlowTaskDef → ActivateFlowDef**.

## Related APIs

- [CreateFlowDef](CreateFlowDef) – Minimal variant with only the three required parameters.
- [CreateFlowDef1](CreateFlowDef1) – Adds `OnEndMoveToPath`.
- [CreateFlowDef2](CreateFlowDef2) – Adds `OnEndMoveToPath` and `Supervisor`.
- [AddFlowStepDef](AddFlowStepDef) – Add steps to the workflow after creation.
- [AddFlowTaskDef](AddFlowTaskDef) – Add task definitions to workflow steps.
- [ActivateFlowDef](ActivateFlowDef) – Activate the workflow so documents can be submitted to it.
- [GetFlowDef](GetFlowDef) – Retrieve the full definition of a workflow.
- [DeactivateFlowDef](DeactivateFlowDef) – Deactivate a workflow to modify it.
- [DeleteWorkflow](DeleteWorkflow) – Permanently delete a workflow definition.

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
