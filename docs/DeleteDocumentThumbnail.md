# DeleteDocumentThumbnail API

Removes the thumbnail image from a document.

## Endpoint

```
/srv.asmx/DeleteDocumentThumbnail
```

## Methods

- **GET** `/srv.asmx/DeleteDocumentThumbnail?authenticationTicket=...&documentPath=...`
- **POST** `/srv.asmx/DeleteDocumentThumbnail` (form data)
- **SOAP** Action: `http://tempuri.org/DeleteDocumentThumbnail`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `documentPath` | string | Yes | Full infoRouter path of the document (e.g. `/Finance/Reports/Q1Summary.pdf`). |

## Response

### Success Response

```xml
<root success="true" />
```

### Error Response

```xml
<root success="false" error="Error message" />
```

## Required Permissions

The calling user must have **Change Document Properties** permission on the document.

## Example

### Request (GET)

```
GET /srv.asmx/DeleteDocumentThumbnail?authenticationTicket=abc123&documentPath=/Finance/Reports/Q1Summary.pdf
```

### Request (POST)

```
POST /srv.asmx/DeleteDocumentThumbnail HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&documentPath=/Finance/Reports/Q1Summary.pdf
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

Removes the stored thumbnail of a document. The thumbnail is regenerated on demand afterwards, so
this is how a stale one is cleared.

```javascript
await call('DeleteDocumentThumbnail', {
  authenticationTicket: ticket,
  documentPath: '/Finance/Reports/Q1.pdf'
});
```

A document with no thumbnail is a success, so this is safe to call blindly. A document that is not
there is `4041`.

## Notes

- If the document has no thumbnail the call succeeds without error.
- To upload a thumbnail, use `UpdateDocumentThumbnail`.
- To retrieve the current thumbnail bytes, use `GetDocumentThumbnail`.

## Related APIs

- [GetDocumentThumbnail](GetDocumentThumbnail.md) — Retrieve the thumbnail image bytes for a document.
- [UpdateDocumentThumbnail](UpdateDocumentThumbnail.md) — Upload or replace the thumbnail image for a document.
- [GetDocument](GetDocument.md) — Get full document properties including the `ThumbnailExists` flag.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all - the anonymous user is refused |
| `4041` | no document at that path - including one the caller may not see |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

