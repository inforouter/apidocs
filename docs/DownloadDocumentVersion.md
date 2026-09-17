# DownloadDocumentVersion API

Downloads a specific version of a document and returns its content as a raw byte array. Use this when you need a particular historical version rather than the latest. For large files, use the chunked download workflow (`GetDownloadHandlerByVersion` -' `DownloadFileChunk` -' `DeleteDownloadHandler`) instead.

## Endpoint

```

/srv.asmx/DownloadDocumentVersion

```

## Methods

- **GET** `/srv.asmx/DownloadDocumentVersion?authenticationTicket=...&Path=...&VersionNumber=...`

- **POST** `/srv.asmx/DownloadDocumentVersion` (form data)

- **SOAP** Action: `http://tempuri.org/DownloadDocumentVersion`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path of the document (e.g. `/MyLibrary/Reports/Report.pdf`). |
| `VersionNumber` | int | Yes | Version number to download. Accepts both legacy format (e.g. `1`, `2`, `3`) and modernized format (e.g. `1000000`, `2000000`, `3000000`) -" legacy values are automatically converted internally. Use `GetDocumentVersions` to retrieve valid version numbers. |

## Response

### Success Response

The response body contains the raw binary content of the specified document version.

- **REST (GET/POST)**: Returns `application/json` - a JSON **string** holding the content as base64,
  not raw bytes. `await response.json()` gives the base64; decode it before use.

- **SOAP**: Returns a `base64`-encoded byte array within the SOAP response envelope.

### Error Response

On any error (authentication failure, document not found, version not found, offline document, or download failure), an **empty byte array** is returned. There is no XML error message. The caller must check whether the returned byte array is empty to detect failure.

---

## Required Permissions

Any authenticated user with read access to the document may call this API.

---

## Example

### GET Request

```

GET /srv.asmx/DownloadDocumentVersion

  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

  &Path=/MyLibrary/Reports/Report.pdf

  &VersionNumber=3000000

HTTP/1.1

```

### POST Request

```

POST /srv.asmx/DownloadDocumentVersion HTTP/1.1

Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

&Path=/MyLibrary/Reports/Report.pdf

&VersionNumber=3000000

```

### SOAP Request

```xml

<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"

               xmlns:tns="http://tempuri.org/">

  <soap:Body>

    <tns:DownloadDocumentVersion>

      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>

      <tns:Path>/MyLibrary/Reports/Report.pdf</tns:Path>

      <tns:VersionNumber>3000000</tns:VersionNumber>

    </tns:DownloadDocumentVersion>

  </soap:Body>

</soap:Envelope>

```

### SOAP Response (success)

```xml

<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">

  <soap:Body>

    <DownloadDocumentVersionResponse xmlns="http://tempuri.org/">

      <DownloadDocumentVersionResult>JVBERi0xLjQK...</DownloadDocumentVersionResult>

    </DownloadDocumentVersionResponse>

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

**Failure is an empty string.** There is no error document and no `errorCode`: a document that is not
there, a path naming a folder, a version that does not exist and a refusal all come back as `""`. A
caller cannot tell them apart, and cannot tell any of them from a file that really is empty. Check
with [DocumentExists](DocumentExists.md) first when it matters.

```javascript
const bytes = await download('DownloadDocumentVersion', {
  authenticationTicket: ticket,
  Path: '/Finance/Reports/Q1.pdf',
  VersionNumber: 1000000        // 0 means the published version
});
```

`VersionNumber` is in the large-integer scheme - version 1 is `1000000` - and `0` means whichever
version is published. A version number nothing uses comes back as the empty string like any other
failure.

## Notes

- Both **legacy** version numbers (e.g. `1`, `2`, `3`) and **modernized** version numbers (e.g. `1000000`, `2000000`, `3000000`) are accepted. Legacy values below 1,000,000 are automatically multiplied by 1,000,000 internally before the lookup. Either format will work -" use whatever `GetDocumentVersions` returns.

- If the document is in **Offline** state, an empty byte array is returned.

- On any error, the response is an **empty byte array** with no accompanying error message. Use `GetDocumentVersions` to verify the version exists before downloading if you need explicit error details.

- To download the latest version without specifying a version number, use `DownloadDocument`.

- For large files, prefer the chunked download workflow to avoid memory and timeout issues: `GetDownloadHandlerByVersion` -' `DownloadFileChunk` -' `DeleteDownloadHandler`.

---

## Related APIs

- [DownloadDocument](DownloadDocument.md) - Download the latest version of a document

- [GetDocumentVersions](GetDocumentVersions.md) - List all versions of a document (use to retrieve valid VersionNumber values)

- [GetDownloadHandlerByVersion](GetDownloadHandlerByVersion.md) - Prepare a specific document version for chunked download

- [DownloadFileChunk](DownloadFileChunk.md) - Download a chunk of a file using a handler

- [DeleteDownloadHandler](DeleteDownloadHandler.md) - Clean up a download handler after use

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `none` | every failure is an empty string with no error document; see above |

| Condition | Result |
|-----------|--------|
| Invalid or missing authentication ticket | Empty byte array returned |
| Document not found at the specified path | Empty byte array returned |
| Version not found | Empty byte array returned |
| Document is in Offline state | Empty byte array returned |
| Download failure | Empty byte array returned |

---

