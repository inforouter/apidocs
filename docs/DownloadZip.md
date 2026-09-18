# DownloadZip API

Zips one or more documents and folders and returns the archive as a raw byte array in a single call. This is suitable for small selections. For large archives, use `DownloadZipWithHandler` to stage the file server-side and retrieve it in chunks with `DownloadFileChunk`.

## Endpoint

```

/srv.asmx/DownloadZip

```

## Methods

- **GET** `/srv.asmx/DownloadZip?authenticationTicket=...&Paths=...`

- **POST** `/srv.asmx/DownloadZip` (form data)

- **SOAP** Action: `http://tempuri.org/DownloadZip`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Paths` | string | Yes | Pipe-separated (`\|`) list of infoRouter paths to include in the zip. Each entry can be a full infoRouter path to a document or folder, or a short ID path (`~D{id}` for a document, `~F{id}` for a folder). Paths that cannot be resolved are silently skipped. |

### Paths Format

Multiple items are separated by a pipe character (`|`):

```

/MyLibrary/Reports/Report.pdf|/MyLibrary/Slides|/OtherLibrary/Notes/Note.docx

```

Mix of full paths and short ID paths is also supported:

```

~D4217|~F112|/MyLibrary/Reports/Summary.pdf

```

## Response

### Success Response

The response body contains the raw bytes of a ZIP archive.

- **REST (GET/POST)**: Returns `application/json` - a JSON **string** holding the content as base64,
  not raw bytes. `await response.json()` gives the base64; decode it before use.

- **SOAP**: Returns a `base64`-encoded byte array within the SOAP response envelope.

### Error Response

On any error (authentication failure, no valid paths resolved, zip size/count restriction exceeded, or zip creation failure), an **empty byte array** is returned. There is no XML error message.

---

## Required Permissions

Any authenticated user with read access to the specified documents and folders may call this API. Paths the user cannot access are silently skipped rather than causing an error.

---

## Example

### GET Request

```

GET /srv.asmx/DownloadZip

  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

  &Paths=/MyLibrary/Reports/Report.pdf|/MyLibrary/Slides

HTTP/1.1

```

### POST Request

```

POST /srv.asmx/DownloadZip HTTP/1.1

Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

&Paths=/MyLibrary/Reports/Report.pdf|/MyLibrary/Slides

```

### SOAP Request

```xml

<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"

               xmlns:tns="http://tempuri.org/">

  <soap:Body>

    <tns:DownloadZip>

      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>

      <tns:Paths>/MyLibrary/Reports/Report.pdf|/MyLibrary/Slides</tns:Paths>

    </tns:DownloadZip>

  </soap:Body>

</soap:Envelope>

```

---

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

**The download operations do not answer XML, and over REST they do not answer raw bytes either.**
They are declared to return `byte[]`, and the REST stack serialises that as `application/json`: the
body is a JSON string whose contents are base64. Decode it before writing anything to disk.

```javascript
async function download(action, params) {
  const response = await fetch(`/srv.asmx/${action}?${new URLSearchParams(params)}`);
  const base64 = await response.json();            // a JSON string, not an object

  if (base64 === '') throw new Error('empty - see below');

  return Uint8Array.from(atob(base64), c => c.charCodeAt(0));
}
```

**A failure is reported on the HTTP response.** The body of a byte-returning operation has no room
for an error document, so it is still the empty answer - but the REST response carries the HTTP
status the error code bands to (`404` for a missing document, `403` for a refusal, and so on) and
two headers beside it:

| Header | What it holds |
|---|---|
| `X-InfoRouter-ErrorCode` | the infoRouter error code, e.g. `4041` |
| `X-InfoRouter-Error` | the message, as one line of ASCII |

Until 9.0 every failure was `""` with HTTP 200 and nothing else, so a document that is not there, a
path naming a folder, a version nobody has, a refusal and a file that really is empty were all the
same answer. A SOAP caller still gets the empty array and no status: there is nowhere in a SOAP
envelope to put one.

```javascript
const bytes = await download('DownloadZip', {
  authenticationTicket: ticket,
  Paths: '/Finance/Reports/Q1.pdf|/Finance/Reports/Q2.pdf|/Finance/Archive'
});
```

**The separator is `|`.** Not a semicolon and not a comma: either of those makes the whole string one
path, which resolves to nothing - and that is refused `4000` now rather than answered with an empty
archive. Note that the document filters elsewhere in the API do split on `;`, which is what makes
this worth checking twice.

A folder is packed with everything in it. A path that cannot be resolved is still dropped, so an
archive built from a list with one typo in it is smaller than expected rather than refused; use
[DownloadZipWithHandler](DownloadZipWithHandler.md) with `partialResult=false` when that matters.

## Notes

- Paths are separated by the pipe character (`|`). Each entry is resolved independently -" paths that cannot be found or accessed are silently skipped.

- If none of the provided paths resolve to a valid document or folder, an empty byte array is returned.

- System-configured zip restrictions apply: if the total document count or combined file size exceeds the configured limits, an empty byte array is returned.

- For large archives that may cause memory or timeout issues, use `DownloadZipWithHandler` to stage the zip on the server and retrieve it in chunks via `DownloadFileChunk`.

- On any error, the response is an **empty byte array** -" there is no accompanying XML error message.

- When including a folder in `Paths`, all documents within that folder (and its sub-folders) are added to the archive.

---

## Related APIs

- [DownloadZipWithHandler](DownloadZipWithHandler.md) - Stage a zip archive on the server and obtain a download handler GUID (recommended for large archives)

- [DownloadFileChunk](DownloadFileChunk.md) - Download chunks of a staged zip file using a handler

- [DeleteDownloadHandler](DeleteDownloadHandler.md) - Clean up a download handler after chunked download

- [GetDownloadQue](GetDownloadQue.md) - Get the list of items in the current user's download queue

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `none` | every failure is an empty string with no error document; see above |

| Condition | Result |
|-----------|--------|
| Invalid or missing authentication ticket | Empty byte array returned |
| No valid paths resolved | Empty byte array returned |
| Zip size or count restriction exceeded | Empty byte array returned |
| Zip creation failure | Empty byte array returned |

---

