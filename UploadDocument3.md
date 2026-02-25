# UploadDocument3 API

Uploads a new document or creates a new version of an existing document at the specified path using a raw byte array, with both a version comment and a post-upload checkout option. This combines the features of `UploadDocument1` (version comment) and `UploadDocument2` (checkout).

## Endpoint

```
/srv.asmx/UploadDocument3
```

## Methods

- **GET** `/srv.asmx/UploadDocument3?authenticationTicket=...&path=...&fileContent=...&versionComment=...&checkout=...`
- **POST** `/srv.asmx/UploadDocument3` (form data — recommended for binary content)
- **SOAP** Action: `http://tempuri.org/UploadDocument3`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full infoRouter destination path including file name (e.g. `/Finance/Reports/Q1-Report.pdf`). |
| `fileContent` | byte[] | Yes | The raw binary content of the file, encoded as Base64 when sent over HTTP. |
| `versionComment` | string | No | A comment describing this version. Recorded in the version history. |
| `checkout` | bool | Yes | `true` to lock the document immediately after upload. `false` to leave it available for other users. |

---

## Response

### Success Response

```xml
<root success="true" DocumentId="12345" VersionId="1000003" />
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
POST /srv.asmx/UploadDocument3 HTTP/1.1
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

Revised revenue figures
------FormBoundary
Content-Disposition: form-data; name="checkout"

true
------FormBoundary--
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:UploadDocument3>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:path>/Finance/Reports/Q1-2024-Report.pdf</tns:path>
      <tns:fileContent>JVBERi0xLjQ...</tns:fileContent>
      <tns:versionComment>Revised revenue figures</tns:versionComment>
      <tns:checkout>true</tns:checkout>
    </tns:UploadDocument3>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- For large files, use the chunked upload approach: `CreateUploadHandler` → `UploadFileChunk` → `UploadDocumentWithHandler1` (with version comment).
- Use `UploadDocument4` for additional options (publish option, send emails, custom dates) via an XML parameters string.

---

## Related APIs

- [UploadDocument](UploadDocument) - Upload without extra options
- [UploadDocument1](UploadDocument1) - Upload with version comment only
- [UploadDocument2](UploadDocument2) - Upload with checkout only
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

*For detailed documentation visit: https://support.inforouter.com/api-docs/UploadDocument3*
