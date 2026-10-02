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

**HTTP 200 with an empty body**, as every infoRouter API answers a call it handled. There is no XML
error envelope, because the body is the image. Over REST the empty body is the empty JSON string `""`;
over SOAP it is an empty byte array.

An empty body is returned when:
- the document has no thumbnail (see [Which documents have a thumbnail](#which-documents-have-a-thumbnail));
- the document does not exist at the path, or the caller may not read it;
- the ticket is invalid;
- the document is unpublished or offline, or the thumbnail cannot be read.

Treat an empty body as "no thumbnail to show". To know why, read the two response headers (REST only):

```
HTTP/1.1 200 OK
Content-Type: application/json
X-InfoRouter-ErrorCode: 4041
X-InfoRouter-Error: There is no thumbnail for this document.

""
```

| Header | Content |
|---|---|
| `X-InfoRouter-ErrorCode` | the infoRouter error code, see [Error Codes](#error-codes) |
| `X-InfoRouter-Error` | the message, as one line of ASCII |

### Which documents have a thumbnail

- **Images** (`bmp`, `jpg`, `jpeg`, `gif`, `png`): generated automatically from the published version
  on the first request.
- **Every other document** (PDF, Office, HTML, ...): only when one was uploaded with
  [UpdateDocumentThumbnail](UpdateDocumentThumbnail.md). Otherwise the answer is the empty body.

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
> so over REST the body is `application/json` - a JSON string holding base64 - and a failure is `""`
> with HTTP 200. The reason is in the `X-InfoRouter-ErrorCode` and `X-InfoRouter-Error` headers.

```javascript
const response = await fetch('/srv.asmx/GetDocumentThumbnail?' + new URLSearchParams({
  authenticationTicket: ticket,
  documentPath: '/Finance/Reports/Q1.pdf'
}));

const base64 = await response.json();
if (base64 === '') {                                 // show the placeholder icon
  console.debug(response.headers.get('X-InfoRouter-ErrorCode'), response.headers.get('X-InfoRouter-Error'));
  return null;
}

const bytes = Uint8Array.from(atob(base64), c => c.charCodeAt(0));
```

Only images get a thumbnail generated automatically; an HTML, PDF or Office document has one only if it
was uploaded. Clear a stale one with [DeleteDocumentThumbnail](DeleteDocumentThumbnail.md); for an image
it is regenerated on next use.

## Notes

- Thumbnails are stored as JPEG images, at most 240 pixels on the longest edge, regardless of the source document type. The aspect ratio of the source image is preserved, and an image already smaller than 240 pixels in both dimensions is not enlarged.
- Thumbnails created before 9.0 were 50 pixel GIF images. They were deleted by the 9.0 upgrade and are regenerated as JPEG on the first request, so the first call for a given document may be slower than usual.
- There is no flag on `GetDocument` that says whether a thumbnail exists; call this API and treat an empty body as "none".
- To upload or replace a thumbnail, use `UpdateDocumentThumbnail`.
- To delete a thumbnail, use `DeleteDocumentThumbnail`.

## Related APIs

- [UpdateDocumentThumbnail](UpdateDocumentThumbnail.md) — Upload a thumbnail image for a document.
- [DeleteDocumentThumbnail](DeleteDocumentThumbnail.md) — Remove the thumbnail image from a document.
- [GetDocument](GetDocument.md) — Get full document properties.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

In the `X-InfoRouter-ErrorCode` header, with HTTP 200 and an empty body:

| `errorCode` | When |
|---:|---|
| `4041` | no document at that path, **or** the document has no thumbnail - `X-InfoRouter-Error` tells them apart |
| `4030` | the caller may not read the document |
| `4000` | the document is unpublished, or its thumbnail file is missing |
| `4010` | the ticket is expired or unknown |
| `4230` | the document is offline |

Before 9.0 this API answered an empty body for every failure, with HTTP 200 and nothing else.

