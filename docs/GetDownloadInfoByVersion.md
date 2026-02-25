# GetDownloadInfoByVersion API

Returns download metadata for a **specific version** of a document — file size, MIME content type, modification date, suggested download file name, and CRC32 checksum — **without** staging the file on the server or creating a download handler. This is the version-aware counterpart to `GetDownloadInfo`, which always queries the latest version.

To download the actual file content, use `GetDownloadHandlerByVersion` (chunked) or `DownloadDocumentVersion` (single call). To query the latest version without specifying a version number, use `GetDownloadInfo`.

## Endpoint

```
/srv.asmx/GetDownloadInfoByVersion
```

## Methods

- **GET** `/srv.asmx/GetDownloadInfoByVersion?AuthenticationTicket=...&Path=...&VersionNumber=...`
- **POST** `/srv.asmx/GetDownloadInfoByVersion` (form data)
- **SOAP** Action: `http://tempuri.org/GetDownloadInfoByVersion`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1-Report.pdf`), or a short document ID path (`~D{id}` or `~D{id}.ext`). |
| `VersionNumber` | int | Yes | **Internal version number** of the version to query, as returned in the `Number` attribute of `GetDocumentVersions` (e.g. `1000000` for version 1, `2000000` for version 2). Values between 1 and 999,999 are invalid and will return an error. Pass `0` to query the latest version (equivalent to `GetDownloadInfo`). |

### Version Number Format

infoRouter stores version numbers internally as multiples of 1,000,000:

| User-visible version | VersionNumber to pass |
|----------------------|-----------------------|
| Version 1 | `1000000` |
| Version 2 | `2000000` |
| Version 3 | `3000000` |
| Latest version | `0` |

Always use the `Number` attribute from `GetDocumentVersions` to obtain the correct value.

---

## Response

### Success Response

Returns file metadata for the specified version. No temporary file is created on the server and no handler GUID is issued.

```xml
<response success="true"
          Size="102400"
          ContentType="application/pdf"
          ModificationDate="2024-03-10"
          VersionNumber="1000000"
          AlterDocumentName="Q1-Report.pdf"
          RenderedContent="false"
          CRC32="a3f1c29d" />
```

### Response Attributes

| Attribute | Description |
|-----------|-------------|
| `success` | `true` if the metadata was retrieved successfully. |
| `Size` | Total file size of the specified version in bytes. |
| `ContentType` | MIME type of the document version (e.g. `application/pdf`). |
| `ModificationDate` | Modification date of the specified version in `yyyy-MM-dd` format. |
| `VersionNumber` | The internal version number that was queried, echoed from the request parameter. |
| `AlterDocumentName` | The file name to use when saving a downloaded copy on the client side. |
| `RenderedContent` | `true` if the file would be served as a server-rendered temporary representation; `false` if the original stored file would be served. |
| `CRC32` | CRC32 checksum of the version file for integrity verification. Empty string when `RenderedContent` is `true`. |

> **Note:** This response never contains `ChunkSize` or `downloadhandler` attributes because no file is staged and no handler is created.

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
GET /srv.asmx/GetDownloadInfoByVersion
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports/Q1-Report.pdf
  &VersionNumber=1000000
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetDownloadInfoByVersion HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance/Reports/Q1-Report.pdf
&VersionNumber=1000000
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetDownloadInfoByVersion>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:Path>/Finance/Reports/Q1-Report.pdf</tns:Path>
      <tns:VersionNumber>1000000</tns:VersionNumber>
    </tns:GetDownloadInfoByVersion>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- This API is a **metadata-only** call. No file is read from disk, no temporary file is created, and no download handler GUID is issued.
- `VersionNumber` must be in the **internal format** (a multiple of 1,000,000). Use the `Number` attribute from `GetDocumentVersions` to obtain the correct value. Values between 1 and 999,999 are explicitly rejected and will return an error.
- Passing `VersionNumber=0` queries the latest version, which is equivalent to calling `GetDownloadInfo`.
- Both full infoRouter paths and short document ID paths (`~D{id}` or `~D{id}.ext`) are accepted for the `Path` parameter.
- Offline (archived) documents cannot be queried and will return an error.
- When `RenderedContent` is `true`, the `CRC32` attribute will be an empty string.

---

## Related APIs

- [GetDownloadInfo](GetDownloadInfo.md) - Get download metadata for the latest version of a document
- [GetDocumentVersions](GetDocumentVersions.md) - Get the version list to obtain valid VersionNumber values
- [GetDownloadHandlerByVersion](GetDownloadHandlerByVersion.md) - Stage a specific version and return a handler GUID for chunked download
- [DownloadDocumentVersion](DownloadDocumentVersion.md) - Download a specific version as a raw byte array in a single call
- [GetDocument](GetDocument.md) - Get the full metadata properties of a document

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Document not found | The specified `Path` does not resolve to an existing document. |
| Invalid version number | `VersionNumber` is between 1 and 999,999 (not a valid internal version number). |
| Offline document error | The document is in an archived/offline library and cannot be queried. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/GetDownloadInfoByVersion*
