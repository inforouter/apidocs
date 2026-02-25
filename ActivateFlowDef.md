# ActivateFlowDef API

Activates a workflow definition, allowing documents to be submitted to the workflow. The workflow must pass all validation rules before it can be activated.

## Endpoint

```
/srv.asmx/ActivateFlowDef
```

## Methods

- **GET** `/srv.asmx/ActivateFlowDef?authenticationTicket=...&domainName=...&flowName=...`
- **POST** `/srv.asmx/ActivateFlowDef` (form data)
- **SOAP** Action: `http://tempuri.org/ActivateFlowDef`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `domainName` | string | Yes | Name of the domain/library containing the workflow |
| `flowName` | string | Yes | Name of the workflow definition to activate |

## Response

### Success Response

```xml
<root success="true" />
```

### Error Response

```xml
<root success="false" error="[ErrorCode] Error message" />
```

## Required Permissions

- User must be authenticated (anonymous users cannot perform this action)
- User must have administrative rights to the domain containing the workflow
- User must have permission to manage workflow definitions

## Workflow Activation Requirements

Before a workflow can be activated, it must meet the following criteria:

1. **At least one step defined** - The workflow must contain one or more workflow steps
2. **Valid step configuration** - Each step must be properly configured
3. **Task assignments** - Each step must have at least one task with valid player assignments (users or groups)
4. **Active folder** - The workflow must have a valid active folder path assigned
5. **No circular dependencies** - Step transitions must not create infinite loops

## Example

### Request (GET)

```
GET /srv.asmx/ActivateFlowDef?authenticationTicket=abc123-def456&domainName=Engineering&flowName=DocumentReview HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/ActivateFlowDef HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&domainName=Engineering&flowName=DocumentReview
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/ActivateFlowDef"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <ActivateFlowDef xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
      <domainName>Engineering</domainName>
      <flowName>DocumentReview</flowName>
    </ActivateFlowDef>
  </soap:Body>
</soap:Envelope>
```

### Success Response

```xml
<?xml version="1.0" encoding="utf-8"?>
<root success="true" />
```

### Error Response Example

```xml
<?xml version="1.0" encoding="utf-8"?>
<root success="false" error="Workflow must have at least one step defined" />
```

## Related APIs

- `CreateFlowDef` - Create a new workflow definition
- `CreateFlowDef1` - Create workflow with end folder
- `CreateFlowDef2` - Create workflow with supervisor
- `CreateFlowDef3` - Create workflow with full options
- `DeactivateFlowDef` - Deactivate an active workflow
- `GetFlowDef` - Get workflow definition details
- `GetDomainFlows` - List all workflows in a domain
- `AddFlowStepDef` - Add a step to workflow
- `AddFlowTaskDef` - Add a task to workflow step
- `SubmitDocumentToFlow` - Submit a document to active workflow
- `SubmitDocumentToFlow1` - Submit with player assignments

## Notes

- Once activated, documents can be submitted to the workflow using `SubmitDocumentToFlow` API
- An active workflow cannot be modified - it must be deactivated first using `DeactivateFlowDef`
- The workflow validation checks are performed server-side during activation
- If activation fails due to validation errors, the error message will indicate the specific issue
- Workflows can be re-activated after being deactivated
- Active workflows appear in the workflow submission UI for users with appropriate permissions

## Error Codes

Common error responses:

| Error | Description |
|-------|-------------|
| `[901]Session expired or Invalid ticket` | Invalid authentication ticket |
| `[2730]Insufficient rights. Anonymous users cannot perform this action` | User is not authenticated |
| `Domain not found` | The specified domain does not exist |
| `Workflow definition not found` | The specified workflow does not exist in the domain |
| `Workflow must have at least one step defined` | Cannot activate workflow without steps |
| `Step [N] must have at least one task` | A workflow step is missing task definitions |
| `Task [N] in step [M] must have at least one player` | A task has no assigned users or groups |
| `Active folder path is not valid` | The workflow's active folder path is invalid or inaccessible |
| `User does not have permission to activate workflows` | User lacks workflow management permissions |

## Workflow Lifecycle

```
Created (Inactive) 
    ?
[ActivateFlowDef] ? Active (Ready for submissions)
    ?
[DeactivateFlowDef] ? Inactive (No new submissions)
    ?
[ActivateFlowDef] ? Active (Can be re-activated)
```

## Best Practices

1. **Test Before Activation**: Verify workflow configuration using `GetFlowDef` before activating
2. **Document Requirements**: Ensure all steps and tasks are properly documented for workflow participants
3. **Permission Review**: Verify that all assigned players (users/groups) have appropriate access to the active folder
4. **Notification Setup**: Configure task notification settings before activation
5. **Version Control**: Consider naming conventions for workflow versions (e.g., "DocumentReview_v2")
