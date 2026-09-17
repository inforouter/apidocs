# UploadNewDocumentWidthHandler API

Uploads a **new** document (never an existing-document version) to the specified folder path using a pre-staged upload handler, with extended options via an XML parameters string. The folder path and document name are specified separately, allowing the caller to place the new file independently of any existing document path.

> **Note:** The method name contains a typo ("Width" instead of "With") -" this is the original API name and is preserved for backward compatibility.

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
1. CreateUploadHandler              -' returns UploadHandler GUID + ChunkSize
2. UploadFileChunk                  -' repeat until LastChunk=true
3. UploadNewDocumentWidthHandler    -' create the new document
```

---

## XML Parameters Format

The root element is `<xmlparameters>` and each option is an `<item>` element with `NAME` and `VALUE` attributes (same format as `UploadDocument4`):

```xml
<xmlparameters>
  <item NAME="DESCRIPTION" VALUE="Quarterly financial summary"/>
  <item NAME="KEYWORDS" VALUE="finance quarterly 2024"/>
  <item NAME="VERSIONCOMMENT" VALUE="Initial upload"/>
  <item NAME="PUBLISHOPTION" VALUE="Publish"/>
  <item NAME="SENDEMAILS" VALUE="true"/>
</xmlparameters>
```

See [UploadDocument4](UploadDocument4.md) for the full list of supported keys and valid values.

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
&xmlParameters=<xmlparameters><item NAME="VERSIONCOMMENT" VALUE="Initial upload"/></xmlparameters>
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

Commits staged content as a **new** document, taking the folder and the name separately rather than
as one path.

```javascript
await call('UploadNewDocumentWidthHandler', {
  authenticationTicket: ticket,
  FolderPath: '/Finance/Reports',
  DocumentName: 'Q1.pdf',
  UploadHandler: handler,
  xmlParameters: '<parameters />'
});
```

> **The operation name is misspelled: `Width`, not `With`.** It has always been, and correcting it
> would break every caller, so it stays. Spell it the way the server does.

This is the safer shape of the family - a folder and a name cannot be confused the way a single path
can - and the only one that offers it.

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

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4000` | the upload handler is unknown, expired, or has already been committed |
| `4090` | a document of that name is already in the folder |
| `4041` | no folder at `FolderPath` |
| `4030` | the caller may not add documents there, or the folder rules forbid the file type |
| `HTTP 400` | a required parameter was empty; refused by model binding, so there is no error document |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Invalid upload handler.` | The GUID is not a valid or active upload handler. |
| Folder not found | The `folderPath` does not exist. |
| Access denied | The user does not have upload permission on the destination folder. |
| `SystemError:...` | An unexpected server-side error occurred. |

---