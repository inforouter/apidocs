# UploadDocument1 API

Uploads a new document or creates a new version of an existing document at the specified path using a raw byte array, with an optional version comment. This is identical to `UploadDocument` with the addition of a `versionComment` parameter that is recorded in the document's version history.

## Endpoint

```
/srv.asmx/UploadDocument1
```

## Methods

- **POST** `/srv.asmx/UploadDocument1` (form data -" recommended for binary content)
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

## JavaScript

```javascript
// Anything carrying bytes is POST-only: a byte[] cannot be bound from a query string, and a GET is
// answered HTTP 415 before the operation runs.
async function post(action, fields) {
  const response = await fetch(`/srv.asmx/${action}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ authenticationTicket: ticket, ...fields })
  });

  const root = new DOMParser()
    .parseFromString(await response.text(), 'text/xml').documentElement;

  if (root.getAttribute('success') !== 'true') {
    throw new Error(`${root.getAttribute('errorCode')}: ${root.getAttribute('error')}`);
  }
  return root;
}

const base64 = bytes => btoa(String.fromCharCode(...bytes));
```

```javascript
await post('UploadDocument1', {
  Path: '/Finance/Reports/Q1.pdf',
  FileContent: base64(bytes),
  VersionComment: 'Figures corrected after review'
});
```

The comment is attached to the version this upload creates, and reads back as the `<Comment>` element
of that version in [GetDocumentVersions](GetDocumentVersions.md).

### The upload family

Two ways in. Either the bytes travel with the call, or they are staged first and the call names the
handler that holds them.

| Bytes with the call | Staged, by handler | Adds |
|---|---|---|
| [UploadDocument](UploadDocument.md) | [UploadDocumentWithHandler](UploadDocumentWithHandler.md) | nothing |
| [UploadDocument1](UploadDocument1.md) | [UploadDocumentWithHandler1](UploadDocumentWithHandler1.md) | a version comment |
| [UploadDocument2](UploadDocument2.md) | | the `Checkout` flag |
| [UploadDocument3](UploadDocument3.md) | [UploadDocumentWithHandler2](UploadDocumentWithHandler2.md) | a comment, and a checkout flag or a version number |
| [UploadDocument4](UploadDocument4.md) | [UploadDocumentWithHandler3](UploadDocumentWithHandler3.md) | a parameter document |
| | [UploadNewDocumentWidthHandler](UploadNewDocumentWidthHandler.md) | a folder and a name instead of one path |

**Uploading over a document that already exists is a new version, and only whoever holds the checkout
may make one.** Without a checkout the answer is `4000` "this document is not checked out". The
`Checkout` flag means *check it out for me if it is not already*: the operation then checks out,
uploads and checks back in, leaving the document free. It does not mean "leave it checked out".

## Notes

- `versionComment` is optional. Omitting it or passing `null` creates a version with no comment.
- For large files, use the chunked upload approach: `CreateUploadHandler` -' `UploadFileChunk` -' `UploadDocumentWithHandler1`.
- Use `UploadDocument2` if you need post-upload checkout instead of a version comment.
- Use `UploadDocument3` if you need both a version comment and post-upload checkout.

---

## Related APIs

- [UploadDocument](UploadDocument.md) - Upload without a version comment
- [UploadDocument2](UploadDocument2.md) - Upload with post-upload checkout option
- [UploadDocument3](UploadDocument3.md) - Upload with version comment and checkout
- [UploadDocument4](UploadDocument4.md) - Upload with extended XML parameters
- [UploadDocumentWithHandler1](UploadDocumentWithHandler1.md) - Chunked upload with version comment

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4000` | a document is already at that path and is not checked out by the caller |
| `4041` | no folder at the parent of the path |
| `4030` | the caller may not add documents there, or the folder rules forbid the file type |
| `HTTP 415` | the call was a GET; the content can only be posted |
| `HTTP 400` | a required parameter was empty; refused by model binding, so there is no error document |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Folder not found | The destination folder in the path does not exist. |
| Access denied | The user does not have upload permission on the destination folder. |
| `SystemError:...` | An unexpected server-side error occurred. |

---