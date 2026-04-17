# UpdateDocumentThumbnail API

Uploads or replaces the thumbnail image for a document. Any existing thumbnail is overwritten.

## Endpoint

```
/srv.asmx/UpdateDocumentThumbnail
```

## Methods

- **GET** `/srv.asmx/UpdateDocumentThumbnail?authenticationTicket=...&documentPath=...&thumbnailContent=...`
- **POST** `/srv.asmx/UpdateDocumentThumbnail` (form data)
- **SOAP** Action: `http://tempuri.org/UpdateDocumentThumbnail`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `documentPath` | string | Yes | Full infoRouter path of the document (e.g. `/Finance/Reports/Q1Summary.pdf`). |
| `thumbnailContent` | byte[] | Yes | Raw image bytes of the thumbnail. GIF format is recommended. |

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

### Request (POST)

```
POST /srv.asmx/UpdateDocumentThumbnail HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&documentPath=/Finance/Reports/Q1Summary.pdf&thumbnailContent=<base64-encoded-gif-bytes>
```

## Notes

- If a thumbnail already exists for the document it is replaced by the new content.
- To retrieve the current thumbnail, use `GetDocumentThumbnail`.
- To remove a thumbnail without replacing it, use `DeleteDocumentThumbnail`.
- GIF format is the native thumbnail format used by infoRouter.

## Related APIs

- [GetDocumentThumbnail](GetDocumentThumbnail.md) — Retrieve the thumbnail image bytes for a document.
- [DeleteDocumentThumbnail](DeleteDocumentThumbnail.md) — Remove the thumbnail image from a document.
- [GetDocument](GetDocument.md) — Get full document properties including the `ThumbnailExists` flag.
