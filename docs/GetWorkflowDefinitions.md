# GetWorkflowDefinitions API

Returns all workflow definitions defined in the system, optionally filtered by domain/library and/or active status.

Step definitions are **not** included in the response. Use [GetFlowDef](GetFlowDef.md) to retrieve the full definition with steps and tasks for a specific workflow.

## Endpoint

```
/srv.asmx/GetWorkflowDefinitions
```

## Methods

- **GET** `/srv.asmx/GetWorkflowDefinitions?authenticationTicket=...&domainName=...&activeWorkflowOnly=...`
- **POST** `/srv.asmx/GetWorkflowDefinitions` (form data)
- **SOAP** Action: `http://tempuri.org/GetWorkflowDefinitions`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `domainName` | string | No | Name of the domain/library to filter by. Omit or leave empty to return workflow definitions across all domains. |
| `activeWorkflowOnly` | boolean | Yes | `true` to return only active workflow definitions; `false` to return all definitions including inactive ones. |

## Response

### Success Response

```xml
<root success="true">
  <FlowDefs>
    <FlowDef
      FlowDefID="12"
      FlowName="ContractApproval"
      DomainId="3"
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
    <FlowDef
      FlowDefID="18"
      FlowName="InvoiceReview"
      DomainId="5"
      DomainName="Finance"
      ActiveFolderPath="/Finance/Invoices"
      RequiresStartUpPlayers="false"
      Active="false"
      OnEndMoveToPath=""
      OnEndEventUrl=""
      Hide="False">
      <Supervisors />
    </FlowDef>
  </FlowDefs>
</root>
```

An empty result (no workflow definitions exist) returns:

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

Requires system administrator role.

## Example

### GET Request

```
GET /srv.asmx/GetWorkflowDefinitions
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &domainName=Corporate
    &activeWorkflowOnly=false
HTTP/1.1
Host: yourserver
```

All domains (omit `domainName`):

```
GET /srv.asmx/GetWorkflowDefinitions
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &activeWorkflowOnly=true
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/GetWorkflowDefinitions HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&domainName=Corporate&activeWorkflowOnly=false
```

### SOAP 1.1 Request

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetWorkflowDefinitions"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetWorkflowDefinitions xmlns="http://tempuri.org/">
      <authenticationTicket>3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c</authenticationTicket>
      <domainName>Corporate</domainName>
      <activeWorkflowOnly>false</activeWorkflowOnly>
    </GetWorkflowDefinitions>
  </soap:Body>
</soap:Envelope>
```

## Notes

- Step and task definitions are **not** included. To get the full workflow definition with all steps and tasks, call [GetFlowDef](GetFlowDef.md) with the `FlowName` and `DomainName` from the response.
- Use `activeWorkflowOnly=true` to limit results to workflows that can currently accept document submissions.
- Use `activeWorkflowOnly=false` to see all workflows including those that are still being configured (inactive).
- Pass `domainName` to scope results to a single domain/library; omit it to return workflows across all domains.
- To list workflows active on a specific folder, use [GetFolderFlows](GetFolderFlows.md).

## Related APIs

- [GetDomainFlows](GetDomainFlows.md) - List all workflow definitions for a domain/library.
- [GetFolderFlows](GetFolderFlows.md) - List workflow definitions active on a specific folder.
- [GetFlowDef](GetFlowDef.md) - Get the full definition of a single workflow including steps and tasks.
- [ActivateFlowDef](ActivateFlowDef.md) - Activate a workflow definition.
- [DeactivateFlowDef](DeactivateFlowDef.md) - Deactivate a workflow definition.
- [SubmitDocumentToFlow](SubmitDocumentToFlow.md) - Submit a document to a workflow.

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed - invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| `[2730]` | Insufficient rights - system administrator role required. |
