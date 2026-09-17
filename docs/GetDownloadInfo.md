# GetDownloadInfo API

Returns download metadata for the latest version of a document -" file size, MIME content type, modification date, suggested download file name, and CRC32 checksum -" **without** staging the file on the server or creating a download handler. Use this API when you need to inspect a document's download properties before deciding whether to download it, or when you only need file metadata rather than the file content itself.

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

Describes a document without transferring it: how big it is, what type it is and what its checksum
is. Enough to decide whether to download at all.

```javascript
const info = await call('GetDownloadInfo', {
  authenticationTicket: ticket,
  Path: '/Finance/Reports/Q1.pdf'
});

if (info.getAttribute('CRC32') === localChecksum) return;   // nothing has changed

console.log(info.getAttribute('Size'), info.getAttribute('ContentType'));
```

`AlterDocumentName` is the name to save the file under. Nothing is staged and no handler is opened -
use [GetDownloadHandler](GetDownloadHandler.md) when the file is to be read in chunks.

### Four operations, two decisions

| | Published version | A named version |
|---|---|---|
| **Describe only** | [GetDownloadInfo](GetDownloadInfo.md) | [GetDownloadInfoByVersion](GetDownloadInfoByVersion.md) |
| **Describe and open a chunked read** | [GetDownloadHandler](GetDownloadHandler.md) | [GetDownloadHandlerByVersion](GetDownloadHandlerByVersion.md) |

All four answer the same attributes - `Size`, `ContentType`, `ModificationDate`, `VersionNumber`,
`AlterDocumentName` and `CRC32` - and the two that open a read add `ChunkSize` and `downloadhandler`.
`VersionNumber` is echoed back exactly as it was asked for, so a `0` stays `0` rather than resolving
to the number of the published version.

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

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | no document at that path - including a folder path, and one the caller may not see |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

A call with no ticket signs in as the anonymous user, so a document in a library flagged as anonymous
can be read without authenticating.

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Document not found | The specified `Path` does not resolve to an existing document. |
| Offline document error | The document is in an archived/offline library and cannot be queried. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

