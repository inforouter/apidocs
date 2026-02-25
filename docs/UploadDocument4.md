# UploadDocument4 API

Uploads a new document or creates a new version of an existing document at the specified path using a raw byte array, with extended options supplied through an XML parameters string. This is the most flexible direct-upload variant and supports all upload options including version comment, checkout, publish option, keywords, text-only content, custom dates, and more.

## Endpoint

```
/srv.asmx/UploadDocument4
```

## Methods

- **GET** `/srv.asmx/UploadDocument4?authenticationTicket=...&path=...&fileContent=...&xmlParameters=...`
- **POST** `/srv.asmx/UploadDocument4` (form data — recommended for binary content)
- **SOAP** Action: `http://tempuri.org/UploadDocument4`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full infoRouter destination path including file name (e.g. `/Finance/Reports/Q1-Report.pdf`). |
| `fileContent` | byte[] | Yes | The raw binary content of the file, encoded as Base64 when sent over HTTP. |
| `xmlParameters` | string | Yes | XML string containing additional upload options. See the XML Parameters section below. Pass an empty string `""` for default behavior. |

---

## XML Parameters Format

The `xmlParameters` value is an XML string with key-value pairs. All keys are case-insensitive uppercase:

```xml
<parameters>
  <parameter key="DESCRIPTION">Quarterly financial summary</parameter>
  <parameter key="KEYWORDS">finance quarterly 2024</parameter>
  <parameter key="VERSIONCOMMENT">Updated figures</parameter>
  <parameter key="CHECKOUT">true</parameter>
  <parameter key="PUBLISHOPTION">Publish</parameter>
  <parameter key="SENDEMAILS">true</parameter>
  <parameter key="TEXTONLYCONTENT">Plain text version of the document</parameter>
  <parameter key="CREATIONDATE">2024-01-15</parameter>
  <parameter key="MODIFICATIONDATE">2024-03-31</parameter>
  <parameter key="MPVERSIONMAJOR">2</parameter>
  <parameter key="MPVERSIONMINOR">0</parameter>
  <parameter key="MPVERSIONREVISION">1</parameter>
</parameters>
```

### Supported XML Parameter Keys

| Key | Type | Description |
|-----|------|-------------|
| `DESCRIPTION` | string | Document description. |
| `KEYWORDS` | string | Space- or comma-separated keywords. |
| `VERSIONCOMMENT` | string | Version comment recorded in version history. |
| `CHECKOUT` | bool (`true`/`false`) | Lock document immediately after upload. |
| `PUBLISHOPTION` | enum | Publishing behavior: `ServerDefault`, `Publish`, `DoNotPublish`. |
| `SENDEMAILS` | bool (`true`/`false`) | Whether to send notification emails on upload. Default: `true`. |
| `TEXTONLYCONTENT` | string | Plain-text content for full-text indexing. |
| `CREATIONDATE` | DateTime | Override the document creation date (yyyy-MM-dd). |
| `MODIFICATIONDATE` | DateTime | Override the document modification date (yyyy-MM-dd). |
| `MPVERSIONMAJOR` | short | Major component of the manual version number (e.g. `2` for v2.0.1). |
| `MPVERSIONMINOR` | short | Minor component of the manual version number (e.g. `0` for v2.0.1). |
| `MPVERSIONREVISION` | short | Revision component of the manual version number (e.g. `1` for v2.0.1). |

---

## Response

### Success Response

```xml
<root success="true" DocumentId="12345" VersionId="1000004" />
```

### Error Response

```xml
<root success="false" error="[901] Session expired or Invalid ticket" />
```

---

## Required Permissions

The calling user must have **write** (upload) permission on the destination folder.

---

## Example

### POST Request

```
POST /srv.asmx/UploadDocument4 HTTP/1.1
Content-Type: multipart/form-data; boundary=----FormBoundary

------FormBoundary
Content-Disposition: form-data; name="authenticationTicket"

3f2504e0-4f89-11d3-9a0c-0305e82c3301
------FormBoundary
Content-Disposition: form-data; name="path"

/Finance/Reports/Q1-2024-Report.pdf
------FormBoundary
Content-Disposition: form-data; name="fileContent"; filename="Q1-2024-Report.pdf"
Content-Type: application/octet-stream

[binary file content]
------FormBoundary
Content-Disposition: form-data; name="xmlParameters"

<parameters><parameter key="VERSIONCOMMENT">Revised Q1 figures</parameter><parameter key="KEYWORDS">finance quarterly 2024</parameter><parameter key="PUBLISHOPTION">Publish</parameter></parameters>
------FormBoundary--
```

---

## Notes

- Passing an empty string `""` for `xmlParameters` uses server defaults for all options.
- `PUBLISHOPTION` values: `ServerDefault` (use the domain's publishing setting), `Publish` (publish immediately), `DoNotPublish` (do not publish).
- Manual version numbers (`MPVERSIONMAJOR`, `MPVERSIONMINOR`, `MPVERSIONREVISION`) set the human-readable version label (e.g. `2.0.1`) independently of the internal version ID.
- For large files, use the chunked handler approach with `UploadDocumentWithHandler3` which accepts the same XML parameters format.

---

## Related APIs

- [UploadDocument](UploadDocument.md) - Basic upload
- [UploadDocument3](UploadDocument3.md) - Upload with version comment and checkout (no XML)
- [UploadDocumentWithHandler3](UploadDocumentWithHandler3.md) - Chunked upload with XML parameters
- [CreateUploadHandler](CreateUploadHandler.md) - Create a handler for chunked large file uploads

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Folder not found | The destination folder in the path does not exist. |
| Invalid parameter value | An XML parameter key has an invalid value (e.g. bad enum or non-boolean for `CHECKOUT`). |
| Access denied | The user does not have upload permission on the destination folder. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/UploadDocument4*
