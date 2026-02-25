# DeleteUploadHandler API

Deletes an upload handler and discards its staged temporary file on the server. Use this to clean up if a chunked upload is cancelled or if an error occurs before the upload is finalized with `UploadDocumentWithHandler`.

## Endpoint

```
/srv.asmx/DeleteUploadHandler
```

## Methods

- **GET** `/srv.asmx/DeleteUploadHandler?authenticationTicket=...&UploadHandler=...`
- **POST** `/srv.asmx/DeleteUploadHandler` (form data)
- **SOAP** Action: `http://tempuri.org/DeleteUploadHandler`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `UploadHandler` | string (GUID) | Yes | The handler GUID returned by `CreateUploadHandler`. Must be a valid GUID string. |

## Response

### Success Response

```xml
<response success="true" error="" />
```

### Error Response

```xml
<response success="false" error="Error message" />
```

---

## Required Permissions

Any authenticated user may call this API.

---

## Chunked Upload Workflow

Upload handlers stage large files on the server before they are committed to the document library. `DeleteUploadHandler` is the cleanup step:

1. **`CreateUploadHandler`** — Allocate a handler and obtain the `UploadHandler` GUID and `ChunkSize`.
2. **`UploadFileChunk`** — Send the file in sequential chunks using the handler GUID.
3. **`UploadDocumentWithHandler`** (or `UploadDocumentWithHandler1` / `UploadNewDocumentWidthHandler`) — Finalize the upload and create the document or new version.
4. **`DeleteUploadHandler`** — Call this **only if the upload is cancelled or fails** before step 3 completes. After a successful `UploadDocumentWithHandler` call the handler is consumed automatically and does not need to be deleted manually.

---

## Example

### GET Request

```
GET /srv.asmx/DeleteUploadHandler
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &UploadHandler=a1b2c3d4-e5f6-7890-abcd-ef1234567890
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/DeleteUploadHandler HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&UploadHandler=a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:DeleteUploadHandler>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:UploadHandler>a1b2c3d4-e5f6-7890-abcd-ef1234567890</tns:UploadHandler>
    </tns:DeleteUploadHandler>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- If the handler's temporary file does not exist (e.g. already cleaned up or never fully written), the call still returns success — no error is raised.
- Passing a string that is not a valid GUID format returns an error immediately without performing any authentication check.
- Do **not** call `DeleteUploadHandler` after a successful `UploadDocumentWithHandler` — the handler is consumed by the finalization step and the temporary file is already removed.
- Call `DeleteUploadHandler` if an error occurs at any point during `UploadFileChunk` or before `UploadDocumentWithHandler` is called, to free the temporary server storage.

---

## Related APIs

- [CreateUploadHandler](CreateUploadHandler.md) - Allocate an upload handler and obtain the GUID and chunk size
- [UploadFileChunk](UploadFileChunk.md) - Upload a single chunk of a file to an open handler
- [UploadDocumentWithHandler](UploadDocumentWithHandler.md) - Finalize the upload and create or update a document
- [DeleteDownloadHandler](DeleteDownloadHandler.md) - Delete a download handler and discard its temporary file

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `bad Request` | `UploadHandler` is not a valid GUID string. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/DeleteUploadHandler*
