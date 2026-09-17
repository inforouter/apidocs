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
1. CreateUploadHandler  -' returns UploadHandler GUID + recommended ChunkSize
2. UploadFileChunk      -' repeat until LastChunk=true (upload all chunks)
3. UploadDocumentWithHandler -' finalize, create/version the document
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

Commits content staged with [UploadFileChunk](UploadFileChunk.md), adding nothing beyond the path.

```javascript
await call('UploadDocumentWithHandler', {
  authenticationTicket: ticket, Path: '/Finance/Reports/Q1.pdf', UploadHandler: handler
});
```

### Staging content

```javascript
// 1. open a handler and read back the chunk size the server chose
const opened = await call('CreateUploadHandler', {
  authenticationTicket: ticket, PreferedChunkSize: 1048576
});
const handler = opened.getAttribute('UploadHandler');
const chunkSize = Number(opened.getAttribute('ChunkSize'));

// 2. send the file a chunk at a time, each with its own CRC32
for (let offset = 0; offset < bytes.length; offset += chunkSize) {
  const chunk = bytes.slice(offset, offset + chunkSize);
  const last = offset + chunkSize >= bytes.length;

  let sent = await post('UploadFileChunk', {
    UploadHandler: handler,
    FileChunk: base64(chunk),
    ChunkHEXCRC: crc32Hex(chunk),        // uppercase hex, no padding
    LastChunk: String(last)
  });

  // a checksum mismatch asks for that chunk again rather than for the whole upload
  while (sent.getAttribute('tryagain') === 'true') {
    sent = await post('UploadFileChunk', { /* the same chunk */ });
  }
}

// 3. commit it - this consumes the handler
await call('UploadDocumentWithHandler', {
  authenticationTicket: ticket, Path: '/Finance/Reports/Q1.pdf', UploadHandler: handler
});
```

**A handler is consumed by the call that commits it.** Committing the same handler twice is `4000`
"upload handler cannot be found". Abandon one that is no longer wanted with
[DeleteUploadHandler](DeleteUploadHandler.md).

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

- The handler GUID is only valid after all chunks have been successfully uploaded with `UploadFileChunk` (final call with `lastChunk=true`).
- The upload handler is automatically deleted after a successful or failed finalization call.
- To add a version comment, use `UploadDocumentWithHandler1`.
- To add manual version numbers (Major.Minor.Revision), use `UploadDocumentWithHandler2`.
- To pass all options as XML parameters, use `UploadDocumentWithHandler3`.

---

## Related APIs

- [CreateUploadHandler](CreateUploadHandler.md) - Create an upload handler for chunked uploads
- [UploadFileChunk](UploadFileChunk.md) - Upload a single file chunk to the handler
- [UploadDocumentWithHandler1](UploadDocumentWithHandler1.md) - Finalize with version comment
- [UploadDocumentWithHandler2](UploadDocumentWithHandler2.md) - Finalize with manual version numbers
- [UploadDocumentWithHandler3](UploadDocumentWithHandler3.md) - Finalize with XML parameters
- [DeleteUploadHandler](DeleteUploadHandler.md) - Discard a handler without creating a document

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4000` | the upload handler is unknown, expired, or has already been committed |
| `4000` | a document is already at that path and is not checked out by the caller |
| `4041` | no folder at the parent of the path |
| `4030` | the caller may not add documents there, or the folder rules forbid the file type |
| `HTTP 400` | a required parameter was empty; refused by model binding, so there is no error document |

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