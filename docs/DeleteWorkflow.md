# DeleteWorkflow API

Permanently deletes a workflow definition and all of its associated steps and task definitions from the system.

## Endpoint

```
/srv.asmx/DeleteWorkflow
```

## Methods

- **GET** `/srv.asmx/DeleteWorkflow?authenticationTicket=...&domainName=...&flowName=...`
- **POST** `/srv.asmx/DeleteWorkflow` (form data)
- **SOAP** Action: `http://tempuri.org/DeleteWorkflow`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `domainName` | string | Yes | The name of the domain/library containing the workflow |
| `flowName` | string | Yes | The name of the workflow definition to delete |

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

- The caller must be authenticated.
- The caller must be a **domain manager** of the library that contains the workflow definition.

## Example

### Request (GET)

```
GET /srv.asmx/DeleteWorkflow?authenticationTicket=abc123-def456&domainName=Engineering&flowName=DocumentReview HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/DeleteWorkflow HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&domainName=Engineering&flowName=DocumentReview
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/DeleteWorkflow"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <DeleteWorkflow xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
      <domainName>Engineering</domainName>
      <flowName>DocumentReview</flowName>
    </DeleteWorkflow>
  </soap:Body>
</soap:Envelope>
```

## Notes

- This operation is **irreversible**. All workflow steps and task definitions associated with the workflow are permanently deleted.
- The workflow definition must belong to a domain for which the caller has domain manager rights.
- Both `domainName` and `flowName` are case-insensitive.

## Error Codes

| Error | Description |
|-------|-------------|
| `[901] Session expired or Invalid ticket` | Invalid or expired authentication ticket |
| `Flow definition cannot be found in this domain` | No workflow with the given name exists in the specified domain |
| `Insufficient rights` | Caller is not a domain manager of the workflow's library |

## Related APIs

- `ActivateFlowDef` - Activate a workflow definition
- `DeleteFlowStepDef` - Delete a single step from a workflow
- `DeleteFlowTaskDef` - Delete a task definition from a workflow step
- `GetWorkflowStatistics` - Get performance statistics for a workflow
