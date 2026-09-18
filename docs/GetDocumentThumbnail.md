# GetDocumentThumbnail API

Retrieves the thumbnail image bytes for a document. Returns the raw JPEG image data, whether the server generated it from the document or it was uploaded via `UpdateDocumentThumbnail`.

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

Raw JPEG image bytes (`image/jpeg`). The response body contains the binary thumbnail data with no XML wrapper.

Before 9.0 the response was a 50 pixel GIF (`image/gif`). Callers that assumed GIF must be updated; see the 9.0 release notes.

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

> **This returns bytes, not XML.** Like the download operations it is declared to return `byte[]`,
> so over REST the body is `application/json` - a JSON string holding base64 - and a failure is `""`.
> The failure itself is on the HTTP response: the status, `X-InfoRouter-ErrorCode` and
> `X-InfoRouter-Error`. Until 9.0 a document with no thumbnail, a document that does not exist and a
> refusal were all the same two bytes and nothing else; the first two now carry different messages.

```javascript
const response = await fetch('/srv.asmx/GetDocumentThumbnail?' + new URLSearchParams({
  authenticationTicket: ticket,
  documentPath: '/Finance/Reports/Q1.pdf'
}));

const base64 = await response.json();
if (base64 === '') return null;                      // no thumbnail, or no document

const bytes = Uint8Array.from(atob(base64), c => c.charCodeAt(0));
```

Thumbnails are generated for the file types the server renders; an HTML document has none. Clear a
stale one with [DeleteDocumentThumbnail](DeleteDocumentThumbnail.md), which regenerates it on next
use.

## Notes

- Thumbnails are stored as JPEG images, at most 240 pixels on the longest edge, regardless of the source document type. The aspect ratio of the source image is preserved, and an image already smaller than 240 pixels in both dimensions is not enlarged.
- Thumbnails created before 9.0 were 50 pixel GIF images. They were deleted by the 9.0 upgrade and are regenerated as JPEG on the first request, so the first call for a given document may be slower than usual.
- To check whether a document has a thumbnail before calling this API, inspect the `ThumbnailExists` attribute returned by `GetDocument`.
- To upload or replace a thumbnail, use `UpdateDocumentThumbnail`.
- To delete a thumbnail, use `DeleteDocumentThumbnail`.

## Related APIs

- [UpdateDocumentThumbnail](UpdateDocumentThumbnail.md) — Upload a thumbnail image for a document.
- [DeleteDocumentThumbnail](DeleteDocumentThumbnail.md) — Remove the thumbnail image from a document.
- [GetDocument](GetDocument.md) — Get full document properties including the `ThumbnailExists` flag.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4041` | no document at that path, **or** the document has no thumbnail - the message tells them apart |
| `4030` | the caller may not read the document |

Both on the HTTP response rather than in the body; see above.

