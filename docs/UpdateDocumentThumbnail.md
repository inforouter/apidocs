# UpdateDocumentThumbnail API

Uploads or replaces the thumbnail image for a document. Any existing thumbnail is overwritten.

## Endpoint

```
/srv.asmx/UpdateDocumentThumbnail
```

## Methods

- **POST** `/srv.asmx/UpdateDocumentThumbnail` (form data)
- **SOAP** Action: `http://tempuri.org/UpdateDocumentThumbnail`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `documentPath` | string | Yes | Full infoRouter path of the document (e.g. `/Finance/Reports/Q1Summary.pdf`). |
| `thumbnailContent` | byte[] | Yes | Raw image bytes of the thumbnail, in any common image format. The image is re-encoded before it is stored, so the format sent does not have to be the format kept. |

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

authenticationTicket=abc123&documentPath=/Finance/Reports/Q1Summary.pdf&thumbnailContent=<base64-encoded-image-bytes>
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

**POST only.** The content is a `byte[]`, which model binding cannot read from a query string: a GET is
answered **HTTP 415 Unsupported Media Type** before the operation runs. Post it as a form field
holding base64.

```javascript
const body = new URLSearchParams({
  authenticationTicket: ticket,
  documentPath: '/Finance/Reports/Q1.pdf',
  thumbnailContent: btoa(String.fromCharCode(...pngBytes))
});

await fetch('/srv.asmx/UpdateDocumentThumbnail', {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body
});
```

Read it back with [GetDocumentThumbnail](GetDocumentThumbnail.md), and clear it with
[DeleteDocumentThumbnail](DeleteDocumentThumbnail.md) so that the server regenerates one on next use.

## Notes

- If a thumbnail already exists for the document it is replaced by the new content.
- To retrieve the current thumbnail, use `GetDocumentThumbnail`.
- To remove a thumbnail without replacing it, use `DeleteDocumentThumbnail`.
- JPEG is the native thumbnail format used by infoRouter since 9.0; before that it was GIF. Whatever is uploaded is re-encoded as a JPEG of at most 240 pixels on the longest edge, with the aspect ratio preserved and no enlargement of a smaller image, so the stored thumbnail will not match the uploaded bytes.

## Related APIs

- [GetDocumentThumbnail](GetDocumentThumbnail.md) — Retrieve the thumbnail image bytes for a document.
- [DeleteDocumentThumbnail](DeleteDocumentThumbnail.md) — Remove the thumbnail image from a document.
- [GetDocument](GetDocument.md) — Get full document properties including the `ThumbnailExists` flag.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | no document at that path - including a folder path, and one the caller may not see |
| `4030` | the caller may not change this document |
| `HTTP 415` | the call was a GET; `thumbnailContent` can only be posted |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

