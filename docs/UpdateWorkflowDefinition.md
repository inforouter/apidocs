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
| `xmlParameters` | string | Yes | XML-serialized `WorkflowDefintionRequestModel` containing all updated property values (see structure below). |

### xmlParameters Structure

```xml
<WorkflowDefintionRequestModel>
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
</WorkflowDefintionRequestModel>
```

To specify no supervisors, use empty elements:

```xml
<SupervisorUserNames />
<SupervisorUsergroupNames />
```

#### WorkflowDefintionRequestModel Fields

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
<response success="false" error="[ErrorCode] Error message" />
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
&xmlParameters=<WorkflowDefintionRequestModel><NewFlowName>Document+Approval</NewFlowName><ActiveFolderPath>/MyDomain/Active+Documents</ActiveFolderPath><Active>false</Active><OnEndMoveToPath>/MyDomain/Archive</OnEndMoveToPath><OnEndEventUrl></OnEndEventUrl><Hide>false</Hide><SupervisorUserNames><string>jdoe</string></SupervisorUserNames><SupervisorUsergroupNames /></WorkflowDefintionRequestModel>
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
        &lt;WorkflowDefintionRequestModel&gt;
          &lt;NewFlowName&gt;Document Approval&lt;/NewFlowName&gt;
          &lt;ActiveFolderPath&gt;/MyDomain/Active Documents&lt;/ActiveFolderPath&gt;
          &lt;Active&gt;false&lt;/Active&gt;
          &lt;OnEndMoveToPath&gt;/MyDomain/Archive&lt;/OnEndMoveToPath&gt;
          &lt;OnEndEventUrl&gt;&lt;/OnEndEventUrl&gt;
          &lt;Hide&gt;false&lt;/Hide&gt;
          &lt;SupervisorUserNames&gt;&lt;string&gt;jdoe&lt;/string&gt;&lt;/SupervisorUserNames&gt;
          &lt;SupervisorUsergroupNames /&gt;
        &lt;/WorkflowDefintionRequestModel&gt;
      </tns:xmlParameters>
    </tns:UpdateWorkflowDefinition>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Identify the workflow to update by `domainName` + `workflowName` (the current name). Use `GetFlowDef` to retrieve current values before calling this API.
- To rename the workflow, supply a different value in `NewFlowName`. The new name must be unique within the domain; if a workflow with that name already exists, the call returns an error.
- Activating a workflow (`Active=true`) requires that at least one step with at least one task is defined. If no steps or tasks exist, the activation is rejected.
- `ActiveFolderPath` must point to a folder within the same domain as the workflow. Specifying a folder from a different domain returns an error.
- Setting `OnEndMoveToPath` to an empty string clears any existing on-end move-to folder.
- Multiple supervisors can be specified — both individual users (`SupervisorUserNames`) and groups (`SupervisorUsergroupNames`) are supported simultaneously.
- For `SupervisorUsergroupNames`, use the format `DomainName/GroupName` when the group name is not unique across domains. If the group name is unique, just the group name is sufficient.
- Use `ActivateFlowDef` or `DeactivateFlowDef` if you only need to toggle the active state without changing other properties.
- Note: The class name in the XML root element is `WorkflowDefintionRequestModel` (single `i` in `Defintion` — this is the spelling used in the codebase).

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Invalid XML format | `xmlParameters` could not be deserialized into `WorkflowDefintionRequestModel`. |
| Workflow not found | The `domainName` + `workflowName` combination does not exist. |
| Access denied | The calling user is not an administrator or supervisor of this workflow. |
| Flow with this name already exists | `NewFlowName` is already used by another workflow in the same domain. |
| Workflow cannot be activated | `Active=true` was requested but the workflow has no steps or tasks defined. |
| Folder not found | `ActiveFolderPath` or `OnEndMoveToPath` does not resolve to an existing folder. |
| Folder must be in the same domain | `ActiveFolderPath` belongs to a different domain than the workflow. |
| User not found | A username in `SupervisorUserNames` does not exist. |
| Group not found | A group name in `SupervisorUsergroupNames` does not exist. |

---

## Related APIs

- [GetFlowDef](GetFlowDef.md) - Retrieve current workflow definition properties
- [CreateFlowDef3](CreateFlowDef3.md) - Create a new workflow definition with all options
- [ActivateFlowDef](ActivateFlowDef.md) - Activate a workflow definition
- [DeactivateFlowDef](DeactivateFlowDef.md) - Deactivate a workflow definition
- [DeleteWorkflow](DeleteWorkflow.md) - Delete a workflow definition
