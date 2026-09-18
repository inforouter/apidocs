# UploadTiffAsPDFWithHandler API

Uploads a TIFF image using a pre-staged chunked upload handler and stores it as a PDF document at the specified path. The server converts the TIFF to PDF automatically before storing. Use this API for large TIFF files that need to be uploaded in chunks.

## Endpoint

```
/srv.asmx/UploadTiffAsPDFWithHandler
```

## Methods

- **GET** `/srv.asmx/UploadTiffAsPDFWithHandler?authenticationTicket=...&path=...&uploadHandler=...`
- **POST** `/srv.asmx/UploadTiffAsPDFWithHandler` (form data)
- **SOAP** Action: `http://tempuri.org/UploadTiffAsPDFWithHandler`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full infoRouter destination path including file name and `.pdf` extension (e.g. `/Scans/Invoice-001.pdf`). |
| `uploadHandler` | string (GUID) | Yes | The upload handler GUID returned by `CreateUploadHandler` after all TIFF chunks have been uploaded via `UploadFileChunk`. |

---

## Chunked Upload Workflow

```
1. CreateUploadHandler         -' returns UploadHandler GUID + ChunkSize
2. UploadFileChunk             -' repeat until LastChunk=true (upload all TIFF chunks)
3. UploadTiffAsPDFWithHandler  -' finalize: convert TIFF to PDF and store
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
POST /srv.asmx/UploadTiffAsPDFWithHandler HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&path=/Scans/Invoice-001.pdf
&uploadHandler=a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:UploadTiffAsPDFWithHandler>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:path>/Scans/Invoice-001.pdf</tns:path>
      <tns:uploadHandler>a1b2c3d4-e5f6-7890-abcd-ef1234567890</tns:uploadHandler>
    </tns:UploadTiffAsPDFWithHandler>
  </soap:Body>
</soap:Envelope>
```

---

## JavaScript

> **The staged content must really be a TIFF.** The bytes are converted to PDF before anything
> is stored, and the document is created with a `.pdf` name rather than the `.tif` name in
> `Path`. Content that is not a TIFF is refused with `4000` and the converter's own message.

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

```javascript
await call('UploadTiffAsPDFWithHandler', {
  authenticationTicket: ticket,
  Path: '/Scans/2026/invoice.tif',
  UploadHandler: handler
});
```

The staged equivalent of [UploadTiffAsPDF](UploadTiffAsPDF.md), and it converts exactly as much:
nothing.

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

## Notes

- The PDF conversion is performed server-side after all chunks are assembled. The infoRouter PDF conversion service must be configured and running.
- The `path` should end in `.pdf` to reflect the converted output format.
- Multi-page TIFF files are converted to multi-page PDFs.
- For small TIFF files that fit in a single request, use `UploadTiffAsPDF` instead.

---

## Related APIs

- [UploadTiffAsPDF](UploadTiffAsPDF.md) - Upload TIFF as PDF in a single request
- [CreateUploadHandler](CreateUploadHandler.md) - Create an upload handler for chunked uploads
- [UploadFileChunk](UploadFileChunk.md) - Upload a single chunk
- [UploadDocumentWithHandler](UploadDocumentWithHandler.md) - Finalize a generic chunked upload

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
| Handler not found / expired | The handler file does not exist or has expired. |
| PDF conversion error | The server-side TIFF-to-PDF conversion failed. |
| Folder not found | The destination folder in the path does not exist. |
| Access denied | The user does not have upload permission on the destination folder. |
| `SystemError:...` | An unexpected server-side error occurred. |

---