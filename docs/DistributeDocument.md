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
<root success="true" />
```

### Error Response

```xml
<root success="false" error="[ErrorCode] Error message" />
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

## Notes

- Only subscribers with the **OnChange** subscription type receive the notification email
- If the document has no OnChange subscribers the call succeeds silently
- The operation fails if subscription notifications are disabled in system settings

## Related APIs

- [`Subscribe`](Subscribe.md) — Subscribe a user or group to a document or folder
