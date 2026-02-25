# GetFolderFlows API

Returns the workflow definitions that are active on a specified folder. Optionally includes workflows inherited from parent folders.

Step definitions are **not** included in the response. Use [GetFlowDef](GetFlowDef.md) to retrieve the full definition with steps and tasks for a specific workflow.

## Endpoint

```
/srv.asmx/GetFolderFlows
```

## Methods

- **GET** `/srv.asmx/GetFolderFlows?AuthenticationTicket=...&FolderPath=...&IncludeInheritedFlows=...`
- **POST** `/srv.asmx/GetFolderFlows` (form data)
- **SOAP** Action: `http://tempuri.org/GetFolderFlows`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `FolderPath` | string | Yes | Full infoRouter path of the folder (e.g. `/Corporate/Contracts`). |
| `IncludeInheritedFlows` | boolean | Yes | `true` to also include workflows inherited from parent folders; `false` to return only workflows directly assigned to this folder. |

## Response

### Success Response

```xml
<root success="true">
  <FlowDefs>
    <FlowDef
      FlowDefID="126"
      FlowName="ContractApproval"
      DomainId="45"
      DomainName="Corporate"
      ActiveFolderPath="/Corporate/Contracts"
      RequiresStartUpPlayers="false"
      Active="true"
      OnEndMoveToPath="/Corporate/Archive"
      OnEndEventUrl=""
      Hide="False">
      <Supervisors>
        <User id="7" />
      </Supervisors>
    </FlowDef>
    <FlowDef ... />
  </FlowDefs>
</root>
```

An empty result (no workflows on the folder) returns:

```xml
<root success="true">
  <FlowDefs />
</root>
```

### Error Response

```xml
<root success="false" error="[901] Session expired or Invalid ticket" />
```

## FlowDef Attributes

| Attribute | Description |
|-----------|-------------|
| `FlowDefID` | Unique numeric identifier of the workflow definition. |
| `FlowName` | Name of the workflow definition. |
| `DomainId` | Numeric ID of the owning domain/library. |
| `DomainName` | Name of the owning domain/library. |
| `ActiveFolderPath` | Full infoRouter path of the folder where the workflow is active. |
| `RequiresStartUpPlayers` | `true` if the workflow requires startup players to be assigned at submission time. |
| `Active` | `true` if the workflow is currently active and accepting new submissions. |
| `OnEndMoveToPath` | Path documents are moved to when the workflow completes. Empty string if disabled. |
| `OnEndEventUrl` | Webhook URL called when the workflow completes. Empty string if disabled. |
| `Hide` | `True` if the workflow is hidden from the folder UI. |

The `<Supervisors>` child element lists workflow-level supervisors as `<User id="..."/>` and `<Group id="..."/>` entries.

## Required Permissions

Any authenticated user may call this API.

## Example

### GET Request

```
GET /srv.asmx/GetFolderFlows
    ?AuthenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &FolderPath=/Corporate/Contracts
    &IncludeInheritedFlows=false
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/GetFolderFlows HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&FolderPath=/Corporate/Contracts&IncludeInheritedFlows=false
```

## Notes

- Step and task definitions are **not** included. To get the full workflow definition with all steps and tasks, call [GetFlowDef](GetFlowDef.md) with the `FlowName` and `DomainName` from the response.
- Use `IncludeInheritedFlows=true` to see all workflows a document in this folder could be submitted to, including those defined on ancestor folders.
- Use `IncludeInheritedFlows=false` to see only workflows whose `ActiveFolderPath` is exactly this folder.
- To list all workflows for a domain regardless of folder, use [GetDomainFlows](GetDomainFlows.md).

## Related APIs

- [GetDomainFlows](GetDomainFlows.md) -" List all workflow definitions for a domain.
- [GetFlowDef](GetFlowDef.md) -" Get the full definition of a single workflow including steps and tasks.
- [SubmitDocumentToFlow](SubmitDocumentToFlow.md) -" Submit a document to a workflow.
- [CreateFlowDef](CreateFlowDef.md) -" Create a new workflow definition.

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed -" invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Folder not found | The specified `FolderPath` does not exist. |
