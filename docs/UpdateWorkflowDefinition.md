# UpdateWorkflowDefinition API

Updates the properties of an existing workflow definition, including its name, active folder, active status, on-end behavior, visibility, and supervisors.

## Endpoint

```
/srv.asmx/UpdateWorkflowDefinition
```

## Methods

- **GET** `/srv.asmx/UpdateWorkflowDefinition?authenticationTicket=...&domainName=...&workflowName=...&xmlParameters=...`
- **POST** `/srv.asmx/UpdateWorkflowDefinition` (form data)
- **SOAP** Action: `http://tempuri.org/UpdateWorkflowDefinition`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `domainName` | string | Yes | The domain (library) name that owns the workflow definition. |
| `workflowName` | string | Yes | The current name of the workflow definition to update. Used to locate the definition. |
| `xmlParameters` | string | Yes | XML-serialized `WorkflowDefinitionRequestModel` containing all updated property values (see structure below). |

### xmlParameters Structure

```xml
<WorkflowDefinitionRequestModel>
  <NewFlowName>Document Approval</NewFlowName>
  <ActiveFolderPath>/MyDomain/Active Documents</ActiveFolderPath>
  <Active>false</Active>
  <OnEndMoveToPath>/MyDomain/Archive</OnEndMoveToPath>
  <OnEndEventUrl></OnEndEventUrl>
  <Hide>false</Hide>
  <SupervisorUserNames>
    <string>jdoe</string>
  </SupervisorUserNames>
  <SupervisorUsergroupNames>
    <string>MyDomain/Approvers</string>
  </SupervisorUsergroupNames>
</WorkflowDefinitionRequestModel>
```

To specify no supervisors, use empty elements:

```xml
<SupervisorUserNames />
<SupervisorUsergroupNames />
```

#### WorkflowDefinitionRequestModel Fields

| Field | Type | Description |
|-------|------|-------------|
| `NewFlowName` | string | The new name for the workflow definition. Pass the same value as `workflowName` to keep the name unchanged. Must be unique within the domain. |
| `ActiveFolderPath` | string | Full infoRouter path of the folder this workflow applies to (must be within the same domain). |
| `Active` | bool | `true` to activate the workflow, `false` to deactivate it. |
| `OnEndMoveToPath` | string | Full infoRouter path of the folder documents are moved to when the workflow ends. Pass an empty string for no movement on end. |
| `OnEndEventUrl` | string | URL called when the workflow ends (webhook). Pass an empty string for none. |
| `Hide` | bool | `true` to hide the workflow from non-administrators; `false` to show it. |
| `SupervisorUserNames` | string[] | Login names of users to assign as workflow supervisors. Use an empty element for no user supervisors. |
| `SupervisorUsergroupNames` | string[] | Names of user groups to assign as workflow supervisors. Use the format `DomainName/GroupName` to disambiguate groups with the same name across domains, or just `GroupName` if unique. Use an empty element for no group supervisors. |

---

## Response

### Success Response

```xml
<response success="true" error="" />
```

### Error Response

```xml
<response success="false" error="Error message" errorCode="4000" />
```

---

## Required Permissions

The authenticated user must be a **system administrator** or a **current supervisor** of the workflow definition. Domain-level workflow management rights are enforced by the system.

---

## Example

### Request (POST)

```
POST /srv.asmx/UpdateWorkflowDefinition HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&domainName=MyDomain
&workflowName=Document+Approval
&xmlParameters=<WorkflowDefinitionRequestModel><NewFlowName>Document+Approval</NewFlowName><ActiveFolderPath>/MyDomain/Active+Documents</ActiveFolderPath><Active>false</Active><OnEndMoveToPath>/MyDomain/Archive</OnEndMoveToPath><OnEndEventUrl></OnEndEventUrl><Hide>false</Hide><SupervisorUserNames><string>jdoe</string></SupervisorUserNames><SupervisorUsergroupNames /></WorkflowDefinitionRequestModel>
```

### Request (GET)

```
GET /srv.asmx/UpdateWorkflowDefinition
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &domainName=MyDomain
  &workflowName=Document+Approval
  &xmlParameters=...
HTTP/1.1
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:UpdateWorkflowDefinition>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:domainName>MyDomain</tns:domainName>
      <tns:workflowName>Document Approval</tns:workflowName>
      <tns:xmlParameters>
        &lt;WorkflowDefinitionRequestModel&gt;
          &lt;NewFlowName&gt;Document Approval&lt;/NewFlowName&gt;
          &lt;ActiveFolderPath&gt;/MyDomain/Active Documents&lt;/ActiveFolderPath&gt;
          &lt;Active&gt;false&lt;/Active&gt;
          &lt;OnEndMoveToPath&gt;/MyDomain/Archive&lt;/OnEndMoveToPath&gt;
          &lt;OnEndEventUrl&gt;&lt;/OnEndEventUrl&gt;
          &lt;Hide&gt;false&lt;/Hide&gt;
          &lt;SupervisorUserNames&gt;&lt;string&gt;jdoe&lt;/string&gt;&lt;/SupervisorUserNames&gt;
          &lt;SupervisorUsergroupNames /&gt;
        &lt;/WorkflowDefinitionRequestModel&gt;
      </tns:xmlParameters>
    </tns:UpdateWorkflowDefinition>
  </soap:Body>
</soap:Envelope>
```

---

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

Rewrites a definition from an XML document. The root element is **`<WorkflowDefinitionRequest>`**,
not the class name - sending `<WorkflowDefinitionRequestModel>` is a 5000 "error in XML document
(1, 2)". It is also the only operation that can attach supervisors, since `CreateFlowDef2` and
`CreateFlowDef3` discard the one they are given.

```javascript
const definition = `
<WorkflowDefinitionRequest>
  <NewFlowName>Invoice approval</NewFlowName>
  <ActiveFolderPath>/Public/Invoices</ActiveFolderPath>
  <Active>false</Active>
  <OnEndMoveToPath />
  <OnEndEventUrl />
  <Hide>false</Hide>
  <SupervisorUserNames><string>jsmith</string></SupervisorUserNames>
  <SupervisorUsergroupNames />
</WorkflowDefinitionRequest>`;

await call('UpdateWorkflowDefinition', {
  authenticationTicket: ticket,
  domainName: 'Public',
  workflowName: 'Invoice approval',
  xmlParameters: definition
});
```

Putting a different name in `<NewFlowName>` renames the definition.

## Notes

- Identify the workflow to update by `domainName` + `workflowName` (the current name). Use `GetFlowDef` to retrieve current values before calling this API.
- To rename the workflow, supply a different value in `NewFlowName`. The new name must be unique within the domain; if a workflow with that name already exists, the call returns an error.
- Activating a workflow (`Active=true`) requires that at least one step with at least one task is defined. If no steps or tasks exist, the activation is rejected.
- `ActiveFolderPath` must point to a folder within the same domain as the workflow. Specifying a folder from a different domain returns an error.
- Setting `OnEndMoveToPath` to an empty string clears any existing on-end move-to folder.
- Multiple supervisors can be specified — both individual users (`SupervisorUserNames`) and groups (`SupervisorUsergroupNames`) are supported simultaneously.
- For `SupervisorUsergroupNames`, use the format `DomainName/GroupName` when the group name is not unique across domains. If the group name is unique, just the group name is sufficient.
- Use `ActivateFlowDef` or `DeactivateFlowDef` if you only need to toggle the active state without changing other properties.
- Note: The class name in the XML root element is `WorkflowDefinitionRequestModel` (single `i` in `Defintion` — this is the spelling used in the codebase).

---


## Related APIs

- [GetFlowDef](GetFlowDef.md) - Retrieve current workflow definition properties
- [CreateFlowDef3](CreateFlowDef3.md) - Create a new workflow definition with all options
- [ActivateFlowDef](ActivateFlowDef.md) - Activate a workflow definition
- [DeactivateFlowDef](DeactivateFlowDef.md) - Deactivate a workflow definition
- [DeleteWorkflow](DeleteWorkflow.md) - Delete a workflow definition

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `5000` | `xmlParameters` is not a `<WorkflowDefinitionRequest>` document |
| `4000` | no definition by that name, no folder at `ActiveFolderPath`, or a supervisor name that is not a user |
| `4030` | the caller may not manage workflows in that library |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
