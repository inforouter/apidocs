# DownloadDocument API

Downloads the latest version of a document and returns its content as a raw byte array. This is a single-call download suitable for small to medium-sized files. For large files, use the chunked download workflow (`GetDownloadHandler` -' `DownloadFileChunk` -' `DeleteDownloadHandler`) instead.

## Endpoint

```

/srv.asmx/DownloadDocument

```

## Methods

- **GET** `/srv.asmx/DownloadDocument?authenticationTicket=...&Path=...`

- **POST** `/srv.asmx/DownloadDocument` (form data)

- **SOAP** Action: `http://tempuri.org/DownloadDocument`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path of the document to download (e.g. `/MyLibrary/Reports/Report.pdf`). |

## Response

### Success Response

The response body contains the raw binary content of the document's latest version.

- **REST (GET/POST)**: Returns `application/json` - a JSON **string** holding the content as base64,
  not raw bytes. `await response.json()` gives the base64; decode it before use.

- **SOAP**: Returns a `base64`-encoded byte array within the SOAP response envelope.

### Error Response

On any error (authentication failure, document not found, offline document, or download failure), an **empty byte array** is returned. There is no XML error message. The caller must check whether the returned byte array is empty to detect failure.

---

## Required Permissions

Any authenticated user with read access to the document may call this API.

---

## Example

### GET Request

```

GET /srv.asmx/DownloadDocument

  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

  &Path=/MyLibrary/Reports/Report.pdf

HTTP/1.1

```

### POST Request

```

POST /srv.asmx/DownloadDocument HTTP/1.1

Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

&Path=/MyLibrary/Reports/Report.pdf

```

### SOAP Request

```xml

<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"

               xmlns:tns="http://tempuri.org/">

  <soap:Body>

    <tns:DownloadDocument>

      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>

      <tns:Path>/MyLibrary/Reports/Report.pdf</tns:Path>

    </tns:DownloadDocument>

  </soap:Body>

</soap:Envelope>

```

### SOAP Response (success)

```xml

<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">

  <soap:Body>

    <DownloadDocumentResponse xmlns="http://tempuri.org/">

      <DownloadDocumentResult>JVBERi0xLjQK...</DownloadDocumentResult>

    </DownloadDocumentResponse>

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
const bytes = await download('DownloadDocument', {
  authenticationTicket: ticket,
  Path: '/Finance/Reports/Q1.pdf'
});
```

For a document too large to hold in memory, stage it with
[DownloadZipWithHandler](DownloadZipWithHandler.md) and read it with
[DownloadFileChunk](DownloadFileChunk.md) instead.

## Notes

- This API always downloads the **latest version** of the document. To download a specific version use `DownloadDocumentVersion`.

- If the document is in **Offline** state, an empty byte array is returned.

- On any error (invalid ticket, path not found, permission denied, download failure), the response is an **empty byte array** with no accompanying error message. Use `DocumentExists` to verify the document is accessible before downloading if you need explicit error details.

- For large files, prefer the chunked download workflow to avoid memory and timeout issues: `GetDownloadHandler` -' `DownloadFileChunk` -' `DeleteDownloadHandler`.

- The downloaded bytes represent the file exactly as stored in the warehouse -" no conversion or transformation is applied.

---

## Related APIs

- [DownloadDocumentVersion](DownloadDocumentVersion.md) - Download a specific version of a document

- [GetDownloadHandler](GetDownloadHandler.md) - Prepare a document for chunked download (recommended for large files)

- [DownloadFileChunk](DownloadFileChunk.md) - Download a chunk of a file using a handler

- [DocumentExists](DocumentExists.md) - Check whether a document exists and retrieve its CRC32 checksums

- [GetDocument](GetDocument.md) - Get document properties without downloading content

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4041` | no document at that path, including a folder path |
| `4030` | the caller may not read it |
| `4010` | the ticket is expired or unknown |

All of them on the HTTP response rather than in the body; see above.

| Condition | Result |
|-----------|--------|
| Invalid or missing authentication ticket | Empty byte array returned |
| Document not found at the specified path | Empty byte array returned |
| Document is in Offline state | Empty byte array returned |
| Download failure | Empty byte array returned |

---

