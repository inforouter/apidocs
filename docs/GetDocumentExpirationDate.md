# GetDocumentExpirationDate API

Returns the expiration date assigned to a document.

## Endpoint

`/srv.asmx/GetDocumentExpirationDate`

## Methods

- **GET** `/srv.asmx/GetDocumentExpirationDate?authenticationTicket=...&path=...`
- **POST** `/srv.asmx/GetDocumentExpirationDate` (form data)
- **SOAP** Action: `http://tempuri.org/GetDocumentExpirationDate`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full infoRouter document path, or short document ID path (`~D{id}` or `~D{id}.ext`). |

## Response

### Success Response

```xml
<root success="true" expirationDate="2026-12-31T00:00:00" />
```

## Required Permissions

Caller must have access permissions to the target document.

## Example

### Request (POST)

```http
POST /srv.asmx/GetDocumentExpirationDate HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&path=/Finance/Reports/Q1.pdf
```

## Notes

- If the path does not resolve to a valid document, API returns `success="false"` with error details.
- Path input is normalized/validated by the WebAPI layer before business logic execution.