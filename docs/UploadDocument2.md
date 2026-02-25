# UploadDocument2 API

Uploads a new document or creates a new version of an existing document at the specified path using a raw byte array, with a post-upload checkout option. When `checkout=true`, the document is immediately locked (checked out) to the calling user after upload, preventing others from creating new versions.

## Endpoint

```
/srv.asmx/UploadDocument2
```

## Methods

- **GET** `/srv.asmx/UploadDocument2?authenticationTicket=...&path=...&fileContent=...&checkout=...`
- **POST** `/srv.asmx/UploadDocument2` (form data — recommended for binary content)
- **SOAP** Action: `http://tempuri.org/UploadDocument2`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full infoRouter destination path including file name (e.g. `/Finance/Reports/Q1-Report.pdf`). |
| `fileContent` | byte[] | Yes | The raw binary content of the file to upload, encoded as a Base64 string when sent over HTTP. |
| `checkout` | bool | Yes | `true` to lock (check out) the document immediately after upload. `false` to leave it available for other users. |

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
POST /srv.asmx/UploadDocument2 HTTP/1.1
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
Content-Disposition: form-data; name="checkout"

true
------FormBoundary--
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:UploadDocument2>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:path>/Finance/Reports/Q1-2024-Report.pdf</tns:path>
      <tns:fileContent>JVBERi0xLjQ...</tns:fileContent>
      <tns:checkout>true</tns:checkout>
    </tns:UploadDocument2>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- When `checkout=true`, the document is checked out to the calling user immediately after upload. Other users cannot create new versions until the document is unlocked.
- For large files, use the chunked upload approach with `CreateUploadHandler` → `UploadFileChunk` → `UploadDocumentWithHandler`.
- Use `UploadDocument3` if you also need a version comment along with checkout.

---

## Related APIs

- [UploadDocument](UploadDocument.md) - Upload without checkout
- [UploadDocument1](UploadDocument1.md) - Upload with version comment
- [UploadDocument3](UploadDocument3.md) - Upload with both version comment and checkout
- [UploadDocument4](UploadDocument4.md) - Upload with extended XML parameters
- [UnLock](UnLock.md) - Unlock (check in) a document after editing

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

*For detailed documentation visit: https://support.inforouter.com/api-docs/UploadDocument2*
