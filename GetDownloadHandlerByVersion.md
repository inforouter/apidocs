# GetDownloadHandlerByVersion API

Stages a specific version of a document as a temporary server-side file and returns a download handler GUID along with file metadata and the negotiated chunk size. This is the version-aware counterpart to `GetDownloadHandler`, which always stages the latest version. Use `DownloadFileChunk` to retrieve the file data in sequential chunks, then `DeleteDownloadHandler` to clean up the temporary file when done.

## Endpoint

```
/srv.asmx/GetDownloadHandlerByVersion
```

## Methods

- **GET** `/srv.asmx/GetDownloadHandlerByVersion?AuthenticationTicket=...&Path=...&PreferedChunkSize=...&VersionNumber=...`
- **POST** `/srv.asmx/GetDownloadHandlerByVersion` (form data)
- **SOAP** Action: `http://tempuri.org/GetDownloadHandlerByVersion`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1-Report.pdf`), or a short document ID path (`~D{id}` or `~D{id}.ext`). |
| `PreferedChunkSize` | int | Yes | Preferred byte size for each chunk when calling `DownloadFileChunk`. The server clamps this value between **262,144 bytes (256 KB)** minimum and **33,554,432 bytes (32 MB)** maximum. The actual chunk size used is returned in the `ChunkSize` attribute of the response. |
| `VersionNumber` | int | Yes | **Internal version number** of the version to stage. This is the `Number` attribute value returned by `GetDocumentVersions` (e.g. `1000000` for version 1, `2000000` for version 2). Values between 1 and 999,999 are invalid and will return an error. Pass `0` to stage the latest version (equivalent to `GetDownloadHandler`). |

### Version Number Format

infoRouter stores version numbers internally as multiples of 1,000,000:

| User-visible version | VersionNumber to pass |
|----------------------|-----------------------|
| Version 1 | `1000000` |
| Version 2 | `2000000` |
| Version 3 | `3000000` |
| Latest version | `0` |

Always use the `Number` attribute from `GetDocumentVersions` to obtain the correct value — do not multiply the sequential version number yourself, as the internal numbering may not always follow this simple pattern.

---

## Response

### Success Response

The server stages the specified document version, creates a temporary handler, and returns file metadata along with the handler GUID.

```xml
<response success="true"
          Size="102400"
          ContentType="application/pdf"
          ModificationDate="2024-03-10"
          VersionNumber="1000000"
          AlterDocumentName="Q1-Report.pdf"
          RenderedContent="false"
          CRC32="a3f1c29d"
          ChunkSize="1048576"
          downloadhandler="7f3a1b2c-d4e5-6789-abcd-ef0123456789" />
```

### Response Attributes

| Attribute | Description |
|-----------|-------------|
| `success` | `true` if the handler was created successfully. |
| `Size` | Total size of the staged file in bytes. Use this with `ChunkSize` to calculate the total number of chunks needed. |
| `ContentType` | MIME type of the document version (e.g. `application/pdf`). |
| `ModificationDate` | Modification date of the staged document version in `yyyy-MM-dd` format. |
| `VersionNumber` | The internal version number that was staged, echoed from the request parameter. |
| `AlterDocumentName` | The file name to use when saving the downloaded file on the client side. |
| `RenderedContent` | `true` if the file is a server-rendered temporary representation (e.g. a converted format); `false` if it is the original stored file. |
| `CRC32` | CRC32 checksum of the full file for integrity verification. Empty string when `RenderedContent` is `true`. |
| `ChunkSize` | The actual chunk size in bytes to use with `DownloadFileChunk`. This is the `PreferedChunkSize` value clamped to the allowed range (256 KB – 32 MB). |
| `downloadhandler` | GUID identifying the staged temporary file on the server. Pass this to `DownloadFileChunk` to retrieve file data in chunks, and to `DeleteDownloadHandler` to clean up after the download completes. |

### Error Response

```xml
<response success="false" error="[901] Session expired or Invalid ticket" />
```

---

## Required Permissions

The calling user must have at least **read** access to the document. Offline (archived) documents cannot be downloaded and return an error.

---

## Chunked Download Workflow

```
1. GetDocumentVersions              →  list versions, obtain VersionNumber for the desired version
2. GetDownloadHandlerByVersion      →  stage that version, obtain downloadhandler GUID + ChunkSize + Size
3. DownloadFileChunk (×N)           →  download chunks sequentially until lastchunk="true"
4. DeleteDownloadHandler            →  clean up the temporary staged file on the server
```

**Chunk iteration pattern:**

```
chunkSize   = response/@ChunkSize
totalSize   = response/@Size
handler     = response/@downloadhandler
offset      = 0

loop:
    GET /srv.asmx/DownloadFileChunk
        ?DownloadHandler={handler}
        &StartOffset={offset}
        &ChunkSize={chunkSize}

    append base64-decoded chunk bytes to output file
    offset += chunk/@chunklength

    if chunk/@lastchunk == "true": break

GET /srv.asmx/DeleteDownloadHandler?DownloadHandler={handler}
```

> Always use `chunklength` from the `DownloadFileChunk` response (not the requested `ChunkSize`) when advancing `StartOffset`, because the final chunk may be smaller.

---

## Example

### GET Request

```
GET /srv.asmx/GetDownloadHandlerByVersion
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports/Q1-Report.pdf
  &PreferedChunkSize=1048576
  &VersionNumber=1000000
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetDownloadHandlerByVersion HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance/Reports/Q1-Report.pdf
&PreferedChunkSize=1048576
&VersionNumber=1000000
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetDownloadHandlerByVersion>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:Path>/Finance/Reports/Q1-Report.pdf</tns:Path>
      <tns:PreferedChunkSize>1048576</tns:PreferedChunkSize>
      <tns:VersionNumber>1000000</tns:VersionNumber>
    </tns:GetDownloadHandlerByVersion>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- `VersionNumber` must be in the **internal format** (a multiple of 1,000,000). Use the `Number` attribute from `GetDocumentVersions` to obtain the correct value. Values between 1 and 999,999 are explicitly rejected by the server and will return an error.
- Passing `VersionNumber=0` stages the latest version, which is equivalent to calling `GetDownloadHandler`.
- The `PreferedChunkSize` value is clamped server-side: values below 262,144 bytes (256 KB) are raised to 262,144; values above 33,554,432 bytes (32 MB) are lowered to 33,554,432. Always read the actual `ChunkSize` from the response.
- The staged file is stored as a temporary server-side file. Always call `DeleteDownloadHandler` after completing (or abandoning) a download to free disk space.
- Both full infoRouter paths and short document ID paths (`~D{id}` or `~D{id}.ext`) are accepted for the `Path` parameter.
- Offline (archived) documents cannot be staged and will return an error.
- The handler is tied to the authenticated session. Do not share handler GUIDs across different user sessions.
- To download a version without chunking use `DownloadDocumentVersion` (returns raw bytes directly).

---

## Related APIs

- [GetDocumentVersions](GetDocumentVersions) - Get the version list for a document to obtain valid VersionNumber values
- [GetDownloadHandler](GetDownloadHandler) - Create a download handler for the latest version of a document
- [DownloadFileChunk](DownloadFileChunk) - Download a single chunk of a staged file using a handler GUID
- [DeleteDownloadHandler](DeleteDownloadHandler) - Delete a download handler and discard the staged temporary file
- [GetDownloadInfo](GetDownloadInfo) - Get download metadata without staging a handler
- [DownloadDocumentVersion](DownloadDocumentVersion) - Download a specific version as a raw byte array (no chunking)

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Document not found | The specified `Path` does not resolve to an existing document. |
| Invalid version number | `VersionNumber` is between 1 and 999,999 (not a valid internal version number). |
| Offline document error | The document is in an archived/offline library and cannot be downloaded. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/GetDownloadHandlerByVersion*
