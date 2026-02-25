# GetDomainFlows API

Returns a list of workflow definitions associated with the specified domain/library. Each workflow definition includes its ID, name, status, and associated folder path.

## Endpoint

```
/srv.asmx/GetDomainFlows
```

## Methods

- **GET** `/srv.asmx/GetDomainFlows?authenticationTicket=...&DomainName=...`
- **POST** `/srv.asmx/GetDomainFlows` (form data)
- **SOAP** Action: `http://tempuri.org/GetDomainFlows`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DomainName` | string | Yes | Name of the domain/library whose workflow definitions to retrieve. |

---

## Response

### Success Response

Returns a `<FlowDefs>` collection with one `<FlowDef>` element per workflow definition. Step definitions are not included (use `GetFlowDef` for full step detail).

```xml
<response success="true" error="">
  <FlowDefs>
    <FlowDef FlowDefID="10"
             FlowName="Document Approval"
             DomainId="123"
             DomainName="Finance"
             ActiveFolderPath="/Finance/Incoming"
             RequiresStartUpPlayers="false"
             Active="true"
             OnEndMoveToPath="/Finance/Approved"
             OnEndEventUrl=""
             Hide="False">
      <Supervisors>
        <User id="101" />
      </Supervisors>
    </FlowDef>
    <FlowDef FlowDefID="11"
             FlowName="Archive Review"
             DomainId="123"
             DomainName="Finance"
             ActiveFolderPath="/Finance/Archive"
             RequiresStartUpPlayers="false"
             Active="false"
             OnEndMoveToPath=""
             OnEndEventUrl=""
             Hide="False">
      <Supervisors />
    </FlowDef>
  </FlowDefs>
</response>
```

If the domain has no workflow definitions, the `<FlowDefs>` element is empty:

```xml
<response success="true" error="">
  <FlowDefs />
</response>
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

---

## FlowDef Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `FlowDefID` | int | Unique numeric ID of the workflow definition. |
| `FlowName` | string | Name of the workflow definition. |
| `DomainId` | int | ID of the domain this workflow belongs to. |
| `DomainName` | string | Name of the domain this workflow belongs to. |
| `ActiveFolderPath` | string | The infoRouter folder path where this workflow is active (documents submitted here start the workflow). |
| `RequiresStartUpPlayers` | bool | If `true`, task assignees must be specified when a document is submitted to the workflow. |
| `Active` | bool | `true` if the workflow definition is active and can accept new submissions; `false` if deactivated. |
| `OnEndMoveToPath` | string | Folder path where documents are moved when the workflow completes. Empty if no move-on-completion is configured. |
| `OnEndEventUrl` | string | URL of the external event handler called when the workflow completes. Empty if not configured. |
| `Hide` | bool | If `true`, the workflow is hidden from the user submission list. |

---

## Required Permissions

Any **authenticated user** can call this API.

---

## Example

### GET Request

```
GET /srv.asmx/GetDomainFlows
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DomainName=Finance
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetDomainFlows HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&DomainName=Finance
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetDomainFlows>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:DomainName>Finance</tns:DomainName>
    </tns:GetDomainFlows>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Step definitions (tasks within each workflow step) are **not** included in this response. Use `GetFlowDef` to retrieve a specific workflow definition with its full step details.
- Both active (`Active="true"`) and inactive (`Active="false"`) workflow definitions are returned.
- Hidden workflows (`Hide="True"`) are included in the list but are not shown to users in the submission UI.
- To retrieve workflow definitions for a specific folder (including inherited ones), use `GetFolderFlows`.

---

## Related APIs

- [GetFolderFlows](GetFolderFlows) - Get workflow definitions for a specific folder
- [GetFlowDef](GetFlowDef) - Get a specific workflow definition with full step details
- [SubmitDocumentToFlow](SubmitDocumentToFlow) - Submit a document to a workflow

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `[115] Domain not found` | The specified DomainName does not exist. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/GetDomainFlows*
