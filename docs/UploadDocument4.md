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

The `xmlParameters` value is an XML string. The root element is `<xmlparameters>` and each option is an `<item>` element with `NAME` and `VALUE` attributes:

```xml
<xmlparameters>
  <item NAME="TEXTONLYCONTENT" VALUE="lorem dolor sit amet.."/>
  <item NAME="DESCRIPTION" VALUE="this is the sample description of this document"/>
  <item NAME="VERSIONCOMMENT" VALUE="sample version comment from the author."/>
  <item NAME="CHECKOUT" VALUE="TRUE"/>
  <item NAME="MPVERSIONMAJOR" VALUE="1"/>
  <item NAME="MPVERSIONMINOR" VALUE="0"/>
  <item NAME="MPVERSIONREVISION" VALUE="0"/>
  <item NAME="PUBLISHOPTION" VALUE="Publish"/>
  <item NAME="KEYWORDS" VALUE="finance quarterly 2024"/>
  <item NAME="SENDEMAILS" VALUE="true"/>
  <item NAME="CREATIONDATE" VALUE="2024-01-15"/>
  <item NAME="MODIFICATIONDATE" VALUE="2024-03-31"/>
</xmlparameters>
```

All `NAME` values are case-insensitive. If `VALUE` is omitted the element's inner text is used instead.

### Supported XML Parameter Keys

| Key | Type | Description |
|-----|------|-------------|
| `TEXTONLYCONTENT` | string | Plain-text content for full-text indexing (useful for image-only documents). |
| `DESCRIPTION` | string | Document description. |
| `KEYWORDS` | string | Space- or comma-separated keywords. |
| `VERSIONCOMMENT` | string | Version comment recorded in version history. |
| `CHECKOUT` | bool (`true`/`false`) | Lock document immediately after upload. |
| `PUBLISHOPTION` | enum | Publishing behavior: `ServerDefault`, `Publish`, `DontPublish`. |
| `SENDEMAILS` | bool (`true`/`false`) | Whether to send notification emails on upload. Default: `true`. |
| `CREATIONDATE` | DateTime | Override the document creation date (e.g. `2024-01-15`). |
| `MODIFICATIONDATE` | DateTime | Override the document modification date (e.g. `2024-03-31`). |
| `MPVERSIONMAJOR` | short | Major component of the manual version number (e.g. `2` for v2.0.1). Range: 1–2400. |
| `MPVERSIONMINOR` | short | Minor component of the manual version number (e.g. `0` for v2.0.1). Range: 0–999. |
| `MPVERSIONREVISION` | short | Revision component of the manual version number (e.g. `1` for v2.0.1). Range: 0–999. |

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

<xmlparameters><item NAME="VERSIONCOMMENT" VALUE="Revised Q1 figures"/><item NAME="KEYWORDS" VALUE="finance quarterly 2024"/><item NAME="PUBLISHOPTION" VALUE="Publish"/></xmlparameters>
------FormBoundary--
```

---

## Notes

- Passing an empty string `""` for `xmlParameters` uses server defaults for all options.
- `PUBLISHOPTION` values: `ServerDefault` (use the domain's publishing setting), `Publish` (publish immediately), `DontPublish` (do not publish).
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
