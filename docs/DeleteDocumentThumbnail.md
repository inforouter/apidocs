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

## Notes

- If the document has no thumbnail the call succeeds without error.
- To upload a thumbnail, use `UpdateDocumentThumbnail`.
- To retrieve the current thumbnail bytes, use `GetDocumentThumbnail`.

## Related APIs

- [GetDocumentThumbnail](GetDocumentThumbnail.md) — Retrieve the thumbnail image bytes for a document.
- [UpdateDocumentThumbnail](UpdateDocumentThumbnail.md) — Upload or replace the thumbnail image for a document.
- [GetDocument](GetDocument.md) — Get full document properties including the `ThumbnailExists` flag.
