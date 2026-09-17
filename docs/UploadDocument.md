# UploadDocument API

Uploads a new document or creates a new version of an existing document at the specified path using a raw byte array. If no document exists at the path, a new document is created. If a document already exists, a new version is added. This is the base upload method; use numbered variants (`UploadDocument1` through `UploadDocument4`) for additional options such as version comments, post-upload checkout, and extended XML parameters.

## Endpoint

```
/srv.asmx/UploadDocument
```

## Methods

- **POST** `/srv.asmx/UploadDocument` (form data -" recommended for binary content)
- **SOAP** Action: `http://tempuri.org/UploadDocument`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full infoRouter destination path including file name (e.g. `/Finance/Reports/Q1-Report.pdf`). If the document already exists at this path a new version is created. |
| `fileContent` | byte[] | Yes | The raw binary content of the file to upload, encoded as a Base64 string when sent over HTTP. |

---

## Response

### Success Response

```xml
<root success="true" DocumentId="12345" VersionId="1000001" />
```

| Attribute | Description |
|-----------|-------------|
| `success` | `"true"` on success. |
| `DocumentId` | The numeric ID of the created or updated document. |
| `VersionId` | The internal version ID of the newly created version. |

### Error Response

```xml
<root success="false" error="[901] Session expired or Invalid ticket" />
```

---

## Required Permissions

The calling user must have **write** (upload) permission on the destination folder.

---

## Example

### POST Request (recommended for binary files)

```
POST /srv.asmx/UploadDocument HTTP/1.1
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
------FormBoundary--
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:UploadDocument>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:path>/Finance/Reports/Q1-2024-Report.pdf</tns:path>
      <tns:fileContent>JVBERi0xLjQ...</tns:fileContent>
    </tns:UploadDocument>
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

**POST only.** The content is a `byte[]`, which model binding cannot read from a query string: a GET is
answered **HTTP 415 Unsupported Media Type** before the operation runs. Post it as a form field
holding base64.

```javascript
async function upload(path, bytes) {
  const body = new URLSearchParams({
    authenticationTicket: ticket,
    Path: path,
    FileContent: btoa(String.fromCharCode(...bytes))
  });

  const response = await fetch('/srv.asmx/UploadDocument', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body
  });

  const root = new DOMParser()
    .parseFromString(await response.text(), 'text/xml').documentElement;

  if (root.getAttribute('success') !== 'true') {
    throw new Error(`${root.getAttribute('errorCode')}: ${root.getAttribute('error')}`);
  }
  return root.getAttribute('DocumentID');
}
```

**Uploading over a document that already exists needs it checked out first.** The second upload to a
path is a new version, and only whoever holds the checkout may create one - so without
[Lock](Lock.md) the answer is `4000` "this document is not checked out", which is not the
duplicate-name error a caller might expect:

```javascript
await call('Lock', { authenticationTicket: ticket, Path: path });
try {
  await upload(path, newBytes);          // now it becomes version 1000001
} finally {
  await call('UnLock', { authenticationTicket: ticket, Path: path, force: false });
}
```

An empty `FileContent` is refused by model binding with HTTP 400 - there is no way to upload an empty
file this way.

## Notes

- For large files, use the chunked upload approach: `CreateUploadHandler` -' `UploadFileChunk` (repeat) -' `UploadDocumentWithHandler`.
- The file extension in `path` determines the document's MIME type and thumbnail behavior.
- If a document already exists at the path, a new version is created automatically. The document ID remains the same.
- The folder path component of `path` must already exist. Use `CreateFolder` to create missing folders first.
- For uploads with version comments, use `UploadDocument1`. For post-upload checkout, use `UploadDocument2`. For all options in XML, use `UploadDocument4`.

---

## Related APIs

- [UploadDocument1](UploadDocument1.md) - Upload with a version comment
- [UploadDocument2](UploadDocument2.md) - Upload with post-upload checkout option
- [UploadDocument3](UploadDocument3.md) - Upload with version comment and checkout
- [UploadDocument4](UploadDocument4.md) - Upload with extended XML parameters
- [CreateUploadHandler](CreateUploadHandler.md) - Create a handler for large chunked uploads
- [UploadFileChunk](UploadFileChunk.md) - Upload a single chunk to a handler
- [UploadDocumentWithHandler](UploadDocumentWithHandler.md) - Finalize a chunked upload

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4000` | the document already exists and is not checked out by the caller |
| `4041` | no folder at the parent of `Path` |
| `4030` | the caller may not add documents there, or the folder rules forbid the file type |
| `HTTP 415` | the call was a GET; `FileContent` can only be posted |
| `HTTP 400` | `FileContent` or `Path` was empty |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Folder not found | The destination folder in the path does not exist. |
| Access denied | The user does not have upload permission on the destination folder. |
| `SystemError:...` | An unexpected server-side error occurred. |

---