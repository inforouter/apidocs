# GetDownloadHandler API

Stages the latest version of a document as a temporary server-side file and returns a download handler GUID along with file metadata and the negotiated chunk size. This is the first step in the chunked download workflow for large files. Use `DownloadFileChunk` to retrieve the file data in sequential chunks, then `DeleteDownloadHandler` to clean up the temporary file when done.

To download a specific version rather than the latest, use `GetDownloadHandlerByVersion`.

## Endpoint

```
/srv.asmx/GetDownloadHandler
```

## Methods

- **GET** `/srv.asmx/GetDownloadHandler?AuthenticationTicket=...&Path=...&PreferedChunkSize=...`
- **POST** `/srv.asmx/GetDownloadHandler` (form data)
- **SOAP** Action: `http://tempuri.org/GetDownloadHandler`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1-Report.pdf`), or a short document ID path (`~D{id}` or `~D{id}.ext`). |
| `PreferedChunkSize` | int | Yes | Preferred byte size for each chunk when calling `DownloadFileChunk`. The server clamps this value between **262,144 bytes (256 KB)** minimum and **33,554,432 bytes (32 MB)** maximum. The actual chunk size used is returned in the `ChunkSize` attribute of the response. |

---

## Response

### Success Response

The server stages the document file, creates a temporary handler, and returns file metadata along with the handler GUID.

```xml
<response success="true"
          Size="2097152"
          ContentType="application/pdf"
          ModificationDate="2024-06-15"
          VersionNumber="0"
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
| `ContentType` | MIME type of the document (e.g. `application/pdf`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document`). |
| `ModificationDate` | Last modification date of the document version in `yyyy-MM-dd` format. |
| `VersionNumber` | Always `0` for this API (indicating the latest version was staged). Use `GetDownloadHandlerByVersion` to stage a specific version. |
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
1. GetDownloadHandler        →  stage file, obtain downloadhandler GUID + ChunkSize + Size
2. DownloadFileChunk (×N)    →  download chunks sequentially until lastchunk="true"
3. DeleteDownloadHandler     →  clean up the temporary staged file on the server
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
GET /srv.asmx/GetDownloadHandler
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports/Q1-Report.pdf
  &PreferedChunkSize=1048576
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetDownloadHandler HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance/Reports/Q1-Report.pdf
&PreferedChunkSize=1048576
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetDownloadHandler>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:Path>/Finance/Reports/Q1-Report.pdf</tns:Path>
      <tns:PreferedChunkSize>1048576</tns:PreferedChunkSize>
    </tns:GetDownloadHandler>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- The `PreferedChunkSize` value is clamped server-side: values below 262,144 bytes (256 KB) are raised to 262,144; values above 33,554,432 bytes (32 MB) are lowered to 33,554,432. Always read the actual `ChunkSize` from the response.
- The staged file is stored as a temporary server-side file. Always call `DeleteDownloadHandler` after completing (or abandoning) a download to free disk space.
- Both full infoRouter paths and short document ID paths (`~D{id}` or `~D{id}.ext`) are accepted for the `Path` parameter.
- Offline (archived) documents cannot be staged and will return an error response.
- The handler is tied to the authenticated session. Do not share handler GUIDs across different user sessions.
- To download a specific version of a document use `GetDownloadHandlerByVersion`.
- To download small documents without chunking use `DownloadDocument` (returns raw bytes directly).

---

## Related APIs

- [GetDownloadHandlerByVersion](GetDownloadHandlerByVersion) - Create a download handler for a specific version of a document
- [DownloadFileChunk](DownloadFileChunk) - Download a single chunk of a staged file using a handler GUID
- [DeleteDownloadHandler](DeleteDownloadHandler) - Delete a download handler and discard the staged temporary file
- [GetDownloadInfo](GetDownloadInfo) - Get download metadata without staging a handler
- [DownloadDocument](DownloadDocument) - Download the latest version of a document as a raw byte array (no chunking)

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Document not found | The specified `Path` does not resolve to an existing document. |
| Offline document error | The document is in an archived/offline library and cannot be downloaded. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/GetDownloadHandler*
