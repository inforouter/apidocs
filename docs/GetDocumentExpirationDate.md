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

Reads the expiration date of a document.

```javascript
const root = await call('GetDocumentExpirationDate', {
  authenticationTicket: ticket,
  path: '/Finance/Reports/Q1.pdf'
});

const expires = new Date(root.querySelector('Value').textContent);
const neverExpires = expires.getFullYear() === 1900;
```

**There is no "not set".** A document that never expires reports `1900-01-01`, the base date the whole
system uses for an unset date - so check the year rather than checking for an empty value. The date is
written with the server's UTC offset (`1900-01-01T00:00:00+02:00`) rather than the trailing `Z` most
of the API uses.

## Notes

- If the path does not resolve to a valid document, API returns `success="false"` with error details.
- Path input is normalized/validated by the WebAPI layer before business logic execution.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | no document at that path - including a folder path, and one the caller may not see |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

A call with no ticket signs in as the anonymous user, so a document in a library flagged as anonymous
can be read without authenticating.
