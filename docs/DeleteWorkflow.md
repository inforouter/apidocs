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
<response success="true" error="" errorCode="0" />
```

### Error Response

```xml
<response success="false" error="Error message" errorCode="4000" />
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

Deletes a workflow definition. Unlike every other edit, this one does **not** need the definition to
be inactive: an active definition is deleted where it stands, and documents running under it lose
the definition behind their workflow.

```javascript
await call('DeleteWorkflow', {
  authenticationTicket: ticket, domainName: 'Public', flowName: 'Invoice approval'
});
```

## Notes

- This operation is **irreversible**. All workflow steps and task definitions associated with the workflow are permanently deleted.
- The workflow definition must belong to a domain for which the caller has domain manager rights.
- Both `domainName` and `flowName` are case-insensitive.


## Related APIs

- `ActivateFlowDef` - Activate a workflow definition
- `DeleteFlowStepDef` - Delete a single step from a workflow
- `DeleteFlowTaskDef` - Delete a task definition from a workflow step
- `GetWorkflowStatistics` - Get performance statistics for a workflow

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4000` | no definition by that name in the library |
| `4030` | the caller may not manage workflows in that library |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
