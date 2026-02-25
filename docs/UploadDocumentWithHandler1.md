# UploadDocumentWithHandler1 API

Finalizes a chunked file upload and creates a new document or a new version of an existing document at the specified path, with an optional version comment. Extends `UploadDocumentWithHandler` by accepting a `versionComments` parameter that is recorded in the document's version history.

## Endpoint

```
/srv.asmx/UploadDocumentWithHandler1
```

## Methods

- **GET** `/srv.asmx/UploadDocumentWithHandler1?authenticationTicket=...&path=...&uploadHandler=...&versionComments=...`
- **POST** `/srv.asmx/UploadDocumentWithHandler1` (form data)
- **SOAP** Action: `http://tempuri.org/UploadDocumentWithHandler1`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full infoRouter destination path including file name (e.g. `/Finance/Reports/Q1-Report.pdf`). |
| `uploadHandler` | string (GUID) | Yes | The upload handler GUID returned by `CreateUploadHandler` after all chunks have been uploaded. |
| `versionComments` | string | No | A comment describing the changes in this version. Recorded in the version history. |

---

## Chunked Upload Workflow

```
1. CreateUploadHandler      → returns UploadHandler GUID + ChunkSize
2. UploadFileChunk          → repeat until LastChunk=true
3. UploadDocumentWithHandler1 → finalize with version comment
```

---

## Response

### Success Response

```xml
<root success="true" DocumentId="12345" VersionId="1000002" />
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
POST /srv.asmx/UploadDocumentWithHandler1 HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&path=/Finance/Reports/Q1-2024-Report.pdf
&uploadHandler=a1b2c3d4-e5f6-7890-abcd-ef1234567890
&versionComments=Revised Q1 revenue figures
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:UploadDocumentWithHandler1>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:path>/Finance/Reports/Q1-2024-Report.pdf</tns:path>
      <tns:uploadHandler>a1b2c3d4-e5f6-7890-abcd-ef1234567890</tns:uploadHandler>
      <tns:versionComments>Revised Q1 revenue figures</tns:versionComments>
    </tns:UploadDocumentWithHandler1>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- `versionComments` is optional. Omitting it creates a version with no comment.
- Use `UploadDocumentWithHandler2` to set manual version numbers (Major.Minor.Revision) in addition to a version comment.
- Use `UploadDocumentWithHandler3` for all options via an XML parameters string.

---

## Related APIs

- [CreateUploadHandler](CreateUploadHandler.md) - Create an upload handler for chunked uploads
- [UploadFileChunk](UploadFileChunk.md) - Upload a single chunk
- [UploadDocumentWithHandler](UploadDocumentWithHandler.md) - Finalize without version comment
- [UploadDocumentWithHandler2](UploadDocumentWithHandler2.md) - Finalize with manual version numbers
- [UploadDocumentWithHandler3](UploadDocumentWithHandler3.md) - Finalize with XML parameters

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Invalid upload handler.` | The GUID is not a valid or active upload handler. |
| Handler not found | The handler has expired or was already consumed. |
| Folder not found | The destination folder in the path does not exist. |
| Access denied | The user does not have upload permission on the destination folder. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/UploadDocumentWithHandler1*
