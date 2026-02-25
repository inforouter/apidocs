# UploadDocumentWithHandler API

Finalizes a chunked file upload and creates a new document or a new version of an existing document at the specified path. The file content must have been uploaded in chunks beforehand using `CreateUploadHandler` and `UploadFileChunk`. This is the base handler-finalization method; use `UploadDocumentWithHandler1` through `UploadDocumentWithHandler3` for additional options.

## Endpoint

```
/srv.asmx/UploadDocumentWithHandler
```

## Methods

- **GET** `/srv.asmx/UploadDocumentWithHandler?authenticationTicket=...&path=...&uploadHandler=...`
- **POST** `/srv.asmx/UploadDocumentWithHandler` (form data)
- **SOAP** Action: `http://tempuri.org/UploadDocumentWithHandler`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full infoRouter destination path including file name (e.g. `/Finance/Reports/Q1-Report.pdf`). |
| `uploadHandler` | string (GUID) | Yes | The upload handler GUID returned by `CreateUploadHandler` after all chunks have been uploaded via `UploadFileChunk`. |

---

## Chunked Upload Workflow

```
1. CreateUploadHandler  → returns UploadHandler GUID + recommended ChunkSize
2. UploadFileChunk      → repeat until LastChunk=true (upload all chunks)
3. UploadDocumentWithHandler → finalize, create/version the document
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
POST /srv.asmx/UploadDocumentWithHandler HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&path=/Finance/Reports/Q1-2024-Report.pdf
&uploadHandler=a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:UploadDocumentWithHandler>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:path>/Finance/Reports/Q1-2024-Report.pdf</tns:path>
      <tns:uploadHandler>a1b2c3d4-e5f6-7890-abcd-ef1234567890</tns:uploadHandler>
    </tns:UploadDocumentWithHandler>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- The handler GUID is only valid after all chunks have been successfully uploaded with `UploadFileChunk` (final call with `lastChunk=true`).
- The upload handler is automatically deleted after a successful or failed finalization call.
- To add a version comment, use `UploadDocumentWithHandler1`.
- To add manual version numbers (Major.Minor.Revision), use `UploadDocumentWithHandler2`.
- To pass all options as XML parameters, use `UploadDocumentWithHandler3`.

---

## Related APIs

- [CreateUploadHandler](CreateUploadHandler) - Create an upload handler for chunked uploads
- [UploadFileChunk](UploadFileChunk) - Upload a single file chunk to the handler
- [UploadDocumentWithHandler1](UploadDocumentWithHandler1) - Finalize with version comment
- [UploadDocumentWithHandler2](UploadDocumentWithHandler2) - Finalize with manual version numbers
- [UploadDocumentWithHandler3](UploadDocumentWithHandler3) - Finalize with XML parameters
- [DeleteUploadHandler](DeleteUploadHandler) - Discard a handler without creating a document

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

*For detailed documentation visit: https://support.inforouter.com/api-docs/UploadDocumentWithHandler*
