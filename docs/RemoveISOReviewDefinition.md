# RemoveISOReviewDefinition API

Removes the ISO review schedule from a document. After removal, no periodic review tasks or workflows will be generated for the document.

## Endpoint

```
/srv.asmx/RemoveISOReviewDefinition
```

## Methods

- **GET** `/srv.asmx/RemoveISOReviewDefinition?authenticationTicket=...&documentPath=...`
- **POST** `/srv.asmx/RemoveISOReviewDefinition` (form data)
- **SOAP** Action: `http://tempuri.org/RemoveISOReviewDefinition`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `documentPath` | string | Yes | Full path of the document |

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

The caller must have **Change Document Properties** permission on the document.

## Example

### Remove ISO review from a document (GET)

```
GET /srv.asmx/RemoveISOReviewDefinition?authenticationTicket=abc123-def456&documentPath=/Library/Policies/policy.pdf HTTP/1.1
```

### Remove ISO review from a document (POST)

```
POST /srv.asmx/RemoveISOReviewDefinition HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&documentPath=/Library/Policies/policy.pdf
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/RemoveISOReviewDefinition"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <RemoveISOReviewDefinition xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
      <documentPath>/Library/Policies/policy.pdf</documentPath>
    </RemoveISOReviewDefinition>
  </soap:Body>
</soap:Envelope>
```

## Notes

- Has no effect if no ISO review schedule is currently set on the document
- Does not cancel any review tasks or workflows already in progress

## Related APIs

- [`SetISOReviewDefinition`](SetISOReviewDefinition.md) — Set the ISO review schedule on a document
- [`GetISOReviewDefinition`](GetISOReviewDefinition.md) — Get the current ISO review schedule definition for a document
