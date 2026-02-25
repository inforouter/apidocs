# UploadDocument1 API

Uploads a new document or creates a new version of an existing document at the specified path using a raw byte array, with an optional version comment. This is identical to `UploadDocument` with the addition of a `versionComment` parameter that is recorded in the document's version history.

## Endpoint

```
/srv.asmx/UploadDocument1
```

## Methods

- **GET** `/srv.asmx/UploadDocument1?authenticationTicket=...&path=...&fileContent=...&versionComment=...`
- **POST** `/srv.asmx/UploadDocument1` (form data — recommended for binary content)
- **SOAP** Action: `http://tempuri.org/UploadDocument1`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full infoRouter destination path including file name (e.g. `/Finance/Reports/Q1-Report.pdf`). If a document exists at this path a new version is created. |
| `fileContent` | byte[] | Yes | The raw binary content of the file to upload, encoded as a Base64 string when sent over HTTP. |
| `versionComment` | string | No | A comment describing the changes in this version (e.g. `"Updated figures for Q1"`). Recorded in the version history. |

---

## Response

### Success Response

```xml
<root success="true" DocumentId="12345" VersionId="1000002" />
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
POST /srv.asmx/UploadDocument1 HTTP/1.1
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
Content-Disposition: form-data; name="versionComment"

Updated figures for Q1
------FormBoundary--
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:UploadDocument1>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:path>/Finance/Reports/Q1-2024-Report.pdf</tns:path>
      <tns:fileContent>JVBERi0xLjQ...</tns:fileContent>
      <tns:versionComment>Updated figures for Q1</tns:versionComment>
    </tns:UploadDocument1>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- `versionComment` is optional. Omitting it or passing `null` creates a version with no comment.
- For large files, use the chunked upload approach: `CreateUploadHandler` → `UploadFileChunk` → `UploadDocumentWithHandler1`.
- Use `UploadDocument2` if you need post-upload checkout instead of a version comment.
- Use `UploadDocument3` if you need both a version comment and post-upload checkout.

---

## Related APIs

- [UploadDocument](UploadDocument) - Upload without a version comment
- [UploadDocument2](UploadDocument2) - Upload with post-upload checkout option
- [UploadDocument3](UploadDocument3) - Upload with version comment and checkout
- [UploadDocument4](UploadDocument4) - Upload with extended XML parameters
- [UploadDocumentWithHandler1](UploadDocumentWithHandler1) - Chunked upload with version comment

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Folder not found | The destination folder in the path does not exist. |
| Access denied | The user does not have upload permission on the destination folder. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/UploadDocument1*
