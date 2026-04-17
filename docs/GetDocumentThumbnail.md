# GetDocumentThumbnail API

Retrieves the thumbnail image bytes for a document. Returns the raw GIF image data that was previously uploaded via `UpdateDocumentThumbnail`.

## Endpoint

```
/srv.asmx/GetDocumentThumbnail
```

## Methods

- **GET** `/srv.asmx/GetDocumentThumbnail?authenticationTicket=...&documentPath=...`
- **POST** `/srv.asmx/GetDocumentThumbnail` (form data)
- **SOAP** Action: `http://tempuri.org/GetDocumentThumbnail`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `documentPath` | string | Yes | Full infoRouter path of the document (e.g. `/Finance/Reports/Q1Summary.pdf`). |

## Response

### Success Response

Raw GIF image bytes (`image/gif`). The response body contains the binary thumbnail data with no XML wrapper.

### Failure Response

An empty byte array is returned (zero-length response body) when:
- Authentication fails or the ticket is invalid.
- The document does not exist at the specified path.
- The document exists but has no thumbnail uploaded.
- An internal error occurs reading the thumbnail.

There is no XML error envelope — callers should treat a zero-length response as "no thumbnail available".

## Required Permissions

The calling user must have read access to the document.

## Example

### Request (GET)

```
GET /srv.asmx/GetDocumentThumbnail?authenticationTicket=abc123&documentPath=/Finance/Reports/Q1Summary.pdf
```

### Request (POST)

```
POST /srv.asmx/GetDocumentThumbnail HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&documentPath=/Finance/Reports/Q1Summary.pdf
```

## Notes

- Thumbnails are stored as GIF images regardless of the source document type.
- To check whether a document has a thumbnail before calling this API, inspect the `ThumbnailExists` attribute returned by `GetDocument`.
- To upload or replace a thumbnail, use `UpdateDocumentThumbnail`.
- To delete a thumbnail, use `DeleteDocumentThumbnail`.

## Related APIs

- [UpdateDocumentThumbnail](UpdateDocumentThumbnail.md) — Upload a thumbnail image for a document.
- [DeleteDocumentThumbnail](DeleteDocumentThumbnail.md) — Remove the thumbnail image from a document.
- [GetDocument](GetDocument.md) — Get full document properties including the `ThumbnailExists` flag.
