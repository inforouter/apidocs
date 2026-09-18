# DistributeDocument API

Sends an immediate OnChange distribution notification email to all subscribers of a document. This triggers the same notification that is automatically sent when a document changes, but fires it on demand regardless of whether the document has changed.

## Endpoint

```
/srv.asmx/DistributeDocument
```

## Methods

- **GET** `/srv.asmx/DistributeDocument?authenticationTicket=...&documentPath=...`
- **POST** `/srv.asmx/DistributeDocument` (form data)
- **SOAP** Action: `http://tempuri.org/DistributeDocument`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `documentPath` | string | Yes | Full path of the document to distribute |

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

The caller must have read access to the document. Subscription notifications must be enabled in system settings.

## Example

### Distribute a document (GET)

```
GET /srv.asmx/DistributeDocument?authenticationTicket=abc123-def456&documentPath=/Library/Policies/policy.pdf HTTP/1.1
```

### Distribute a document (POST)

```
POST /srv.asmx/DistributeDocument HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&documentPath=/Library/Policies/policy.pdf
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/DistributeDocument"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <DistributeDocument xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
      <documentPath>/Library/Policies/policy.pdf</documentPath>
    </DistributeDocument>
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

Hands a document to the mail agent for distribution to the people on its distribution list.

```javascript
await call('DistributeDocument', {
  authenticationTicket: ticket,
  documentPath: '/Quality/Procedures/qp-001.pdf'
});
```

There is no "already distributed" state - each call distributes again. The operation is document
only; a folder path is answered "document not found".

> **It accepts a caller with no ticket.** `DocumentServices.DistributeDocumentAsync` looks the
> document up and distributes it, with no permission check of its own. Any document an anonymous
> caller can read - one in a library flagged for anonymous access - can be sent out to its
> distribution list by an unauthenticated request.

## Notes

- Only subscribers with the **OnChange** subscription type receive the notification email
- If the document has no OnChange subscribers the call succeeds silently
- The operation fails if subscription notifications are disabled in system settings

## Related APIs

- [`Subscribe`](Subscribe.md) — Subscribe a user or group to a document or folder

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | no document at that path - including a folder path |
| *(none)* | a caller with no ticket is accepted for any document they can read |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
