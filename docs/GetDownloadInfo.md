# GetDownloadInfo API

Returns download metadata for the latest version of a document — file size, MIME content type, modification date, suggested download file name, and CRC32 checksum — **without** staging the file on the server or creating a download handler. Use this API when you need to inspect a document's download properties before deciding whether to download it, or when you only need file metadata rather than the file content itself.

To download the actual file content, use `GetDownloadHandler` (chunked) or `DownloadDocument` (single call). To query metadata for a specific version, use `GetDownloadInfoByVersion`.

## Endpoint

```
/srv.asmx/GetDownloadInfo
```

## Methods

- **GET** `/srv.asmx/GetDownloadInfo?AuthenticationTicket=...&Path=...`
- **POST** `/srv.asmx/GetDownloadInfo` (form data)
- **SOAP** Action: `http://tempuri.org/GetDownloadInfo`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1-Report.pdf`), or a short document ID path (`~D{id}` or `~D{id}.ext`). |

---

## Response

### Success Response

Returns file metadata for the latest version. No temporary file is created on the server and no handler GUID is issued.

```xml
<response success="true"
          Size="2097152"
          ContentType="application/pdf"
          ModificationDate="2024-06-15"
          VersionNumber="0"
          AlterDocumentName="Q1-Report.pdf"
          RenderedContent="false"
          CRC32="a3f1c29d" />
```

### Response Attributes

| Attribute | Description |
|-----------|-------------|
| `success` | `true` if the metadata was retrieved successfully. |
| `Size` | Total file size of the latest version in bytes. |
| `ContentType` | MIME type of the document (e.g. `application/pdf`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document`). |
| `ModificationDate` | Last modification date of the latest document version in `yyyy-MM-dd` format. |
| `VersionNumber` | Always `0` for this API, indicating the latest version. Use `GetDownloadInfoByVersion` to query a specific version. |
| `AlterDocumentName` | The file name to use when saving a downloaded copy on the client side. |
| `RenderedContent` | `true` if the file would be served as a server-rendered temporary representation (e.g. a converted format); `false` if the original stored file would be served. |
| `CRC32` | CRC32 checksum of the file for integrity verification. Empty string when `RenderedContent` is `true`. |

> **Note:** Unlike `GetDownloadHandler`, this response never contains `ChunkSize` or `downloadhandler` attributes because no file is staged and no handler is created.

### Error Response

```xml
<response success="false" error="[901] Session expired or Invalid ticket" />
```

---

## Required Permissions

The calling user must have at least **read** access to the document. Offline (archived) documents cannot be queried and return an error.

---

## Example

### GET Request

```
GET /srv.asmx/GetDownloadInfo
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports/Q1-Report.pdf
HTTP/1.1
```

### GET Request (short ID path)

```
GET /srv.asmx/GetDownloadInfo
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=~D1051
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetDownloadInfo HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301&Path=/Finance/Reports/Q1-Report.pdf
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetDownloadInfo>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:Path>/Finance/Reports/Q1-Report.pdf</tns:Path>
    </tns:GetDownloadInfo>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- This API is a **metadata-only** call. No file is read from disk, no temporary file is created on the server, and no download handler GUID is issued. It is significantly cheaper than `GetDownloadHandler` for inspecting file properties.
- `VersionNumber` is always `0` in the response, indicating the latest version was queried. To query metadata for a specific version use `GetDownloadInfoByVersion`.
- Both full infoRouter paths and short document ID paths (`~D{id}` or `~D{id}.ext`) are accepted for the `Path` parameter.
- Offline (archived) documents cannot be queried and will return an error response.
- When `RenderedContent` is `true`, the `CRC32` attribute will be an empty string because the checksum applies to the original stored file, not the rendered output.
- Use `Size` to pre-calculate download progress bars or to determine whether chunked downloading is necessary before calling `GetDownloadHandler`.

---

## Related APIs

- [GetDownloadInfoByVersion](GetDownloadInfoByVersion.md) - Get download metadata for a specific version of a document
- [GetDownloadHandler](GetDownloadHandler.md) - Stage the latest version and return a download handler GUID for chunked retrieval
- [GetDownloadHandlerByVersion](GetDownloadHandlerByVersion.md) - Stage a specific version and return a download handler GUID for chunked retrieval
- [DownloadDocument](DownloadDocument.md) - Download the latest version as a raw byte array in a single call
- [GetDocument](GetDocument.md) - Get the full metadata properties of a document

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Document not found | The specified `Path` does not resolve to an existing document. |
| Offline document error | The document is in an archived/offline library and cannot be queried. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/GetDownloadInfo*
