# UploadNewDocumentWidthHandler API

Uploads a **new** document (never an existing-document version) to the specified folder path using a pre-staged upload handler, with extended options via an XML parameters string. The folder path and document name are specified separately, allowing the caller to place the new file independently of any existing document path.

> **Note:** The method name contains a typo ("Width" instead of "With") — this is the original API name and is preserved for backward compatibility.

## Endpoint

```
/srv.asmx/UploadNewDocumentWidthHandler
```

## Methods

- **GET** `/srv.asmx/UploadNewDocumentWidthHandler?authenticationTicket=...&folderPath=...&documentName=...&uploadHandler=...&xmlParameters=...`
- **POST** `/srv.asmx/UploadNewDocumentWidthHandler` (form data)
- **SOAP** Action: `http://tempuri.org/UploadNewDocumentWidthHandler`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `folderPath` | string | Yes | The infoRouter folder path where the new document will be created (e.g. `/Finance/Reports`). The folder must already exist. |
| `documentName` | string | Yes | The file name for the new document including extension (e.g. `Q1-2024-Report.pdf`). |
| `uploadHandler` | string (GUID) | Yes | The upload handler GUID returned by `CreateUploadHandler` after all chunks have been uploaded. |
| `xmlParameters` | string | Yes | XML string with additional upload options. Pass an empty string `""` for default behavior. Supports the same keys as `UploadDocument4`. |

---

## Chunked Upload Workflow

```
1. CreateUploadHandler              → returns UploadHandler GUID + ChunkSize
2. UploadFileChunk                  → repeat until LastChunk=true
3. UploadNewDocumentWidthHandler    → create the new document
```

---

## XML Parameters Format

Same format as `UploadDocument4`:

```xml
<parameters>
  <parameter key="DESCRIPTION">Quarterly financial summary</parameter>
  <parameter key="KEYWORDS">finance quarterly 2024</parameter>
  <parameter key="VERSIONCOMMENT">Initial upload</parameter>
  <parameter key="PUBLISHOPTION">Publish</parameter>
  <parameter key="SENDEMAILS">true</parameter>
</parameters>
```

---

## Response

### Success Response

```xml
<root success="true" DocumentId="12345" VersionId="1000001" />
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
POST /srv.asmx/UploadNewDocumentWidthHandler HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&folderPath=/Finance/Reports
&documentName=Q1-2024-Report.pdf
&uploadHandler=a1b2c3d4-e5f6-7890-abcd-ef1234567890
&xmlParameters=<parameters><parameter key="VERSIONCOMMENT">Initial upload</parameter></parameters>
```

---

## Notes

- This API only creates **new** documents. It does not create new versions of existing documents. To upload a new version, use `UploadDocumentWithHandler3`.
- The `folderPath` must already exist. Use `CreateFolder` to create it first if needed.
- Despite the typo in the name ("Width" vs "With"), this is the correct API name and must be used exactly as shown.

---

## Related APIs

- [CreateUploadHandler](CreateUploadHandler.md) - Create an upload handler for chunked uploads
- [UploadFileChunk](UploadFileChunk.md) - Upload a single chunk
- [UploadDocumentWithHandler3](UploadDocumentWithHandler3.md) - Upload new or versioned document with XML parameters
- [UploadDocument4](UploadDocument4.md) - Direct upload (non-chunked) with XML parameters

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Invalid upload handler.` | The GUID is not a valid or active upload handler. |
| Folder not found | The `folderPath` does not exist. |
| Access denied | The user does not have upload permission on the destination folder. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/UploadNewDocumentWidthHandler*
