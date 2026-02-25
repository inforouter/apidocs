# UploadDocumentWithHandler3 API

Finalizes a chunked file upload and creates a new document or a new version of an existing document at the specified path, with extended options supplied through an XML parameters string. This is the most flexible handler-finalization method and supports all upload options including version comment, publish option, checkout, keywords, text-only content, manual version numbers, custom dates, and email notifications.

## Endpoint

```
/srv.asmx/UploadDocumentWithHandler3
```

## Methods

- **GET** `/srv.asmx/UploadDocumentWithHandler3?authenticationTicket=...&path=...&uploadHandler=...&xmlParameters=...`
- **POST** `/srv.asmx/UploadDocumentWithHandler3` (form data)
- **SOAP** Action: `http://tempuri.org/UploadDocumentWithHandler3`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full infoRouter destination path including file name (e.g. `/Finance/Reports/Q1-Report.pdf`). |
| `uploadHandler` | string (GUID) | Yes | The upload handler GUID returned by `CreateUploadHandler` after all chunks have been uploaded. |
| `xmlParameters` | string | Yes | XML string with additional upload options. Pass an empty string `""` for default behavior. See XML Parameters section below. |

---

## XML Parameters Format

The `xmlParameters` is an XML string with key-value pairs (same format as `UploadDocument4`):

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

See `UploadDocument4` for the full list of supported XML parameter keys and their valid values.

---

## Chunked Upload Workflow

```
1. CreateUploadHandler        → returns UploadHandler GUID + ChunkSize
2. UploadFileChunk            → repeat until LastChunk=true
3. UploadDocumentWithHandler3 → finalize with XML parameters
```

---

## Response

### Success Response

```xml
<root success="true" DocumentId="12345" VersionId="1000004" />
```

### Error Response

```xml
<root success="false" error="Invalid upload handler." />
```

---

## Required Permissions

The calling user must have **write** (upload) permission on the destination folder.

---

## Example

### POST Request

```
POST /srv.asmx/UploadDocumentWithHandler3 HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&path=/Finance/Reports/Q1-2024-Report.pdf
&uploadHandler=a1b2c3d4-e5f6-7890-abcd-ef1234567890
&xmlParameters=<parameters><parameter key="VERSIONCOMMENT">Revised figures</parameter><parameter key="PUBLISHOPTION">Publish</parameter></parameters>
```

---

## Notes

- Passing an empty string for `xmlParameters` uses server defaults.
- This is the recommended approach for large file uploads requiring full metadata control.
- See `UploadDocument4` for the complete XML parameter reference.

---

## Related APIs

- [CreateUploadHandler](CreateUploadHandler.md) - Create an upload handler for chunked uploads
- [UploadFileChunk](UploadFileChunk.md) - Upload a single chunk
- [UploadDocumentWithHandler](UploadDocumentWithHandler.md) - Basic handler finalization
- [UploadDocumentWithHandler1](UploadDocumentWithHandler1.md) - Finalize with version comment
- [UploadDocumentWithHandler2](UploadDocumentWithHandler2.md) - Finalize with manual version numbers
- [UploadDocument4](UploadDocument4.md) - Direct byte-array upload with the same XML parameters

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Invalid upload handler.` | The GUID is not a valid or active upload handler. |
| Invalid parameter value | An XML parameter key has an invalid value. |
| Folder not found | The destination folder in the path does not exist. |
| Access denied | The user does not have upload permission on the destination folder. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/UploadDocumentWithHandler3*
