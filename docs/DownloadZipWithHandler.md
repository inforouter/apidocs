# DownloadZipWithHandler API

Stages a zip archive of specified documents and folders on the server and returns a download handler GUID for subsequent chunked retrieval via `DownloadFileChunk`. Unlike `DownloadZip`, this API returns XML (not raw bytes), supports partial results, and provides log details when items cannot be included.

## Endpoint

```
/srv.asmx/DownloadZipWithHandler
```

## Methods

- **GET** `/srv.asmx/DownloadZipWithHandler?authenticationTicket=...&Paths=...&partialResult=...`
- **POST** `/srv.asmx/DownloadZipWithHandler` (form data)
- **SOAP** Action: `http://tempuri.org/DownloadZipWithHandler`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Paths` | string | Yes | Pipe-separated (`\|`) list of infoRouter paths to include in the zip. Each entry can be a full path to a document or folder, or a short ID path (`~D{id}` for a document, `~F{id}` for a folder). Paths that cannot be resolved are silently skipped. |
| `partialResult` | bool | Yes | Controls behavior when some items cannot be included in the archive. `false` — fails if any errors occur during zip creation (strict mode). `true` — succeeds and returns a handler even if some items were skipped, as long as the archive was created (partial mode). |

### Paths Format

Multiple items are separated by a pipe character (`|`):

```
/MyLibrary/Reports/Report.pdf|/MyLibrary/Slides|/OtherLibrary/Notes/Note.docx
```

## Response

### Success Response

```xml
<Response success="true" downloadhandler="a1b2c3d4-e5f6-7890-abcd-ef1234567890" error="" />
```

If some items were skipped during a partial result zip, `error` is set to `"[log]"` and child log elements describe which items were excluded:

```xml
<Response success="true" downloadhandler="a1b2c3d4-e5f6-7890-abcd-ef1234567890" error="[log]">
  <!-- log entries describing skipped items -->
</Response>
```

| Attribute | Description |
|-----------|-------------|
| `success` | `true` if the zip archive was created and the handler is ready. |
| `downloadhandler` | GUID identifying the staged zip file. Pass this to `DownloadFileChunk` to retrieve the archive in chunks, then to `DeleteDownloadHandler` to clean up. |
| `error` | Empty string if no errors occurred. `"[log]"` if child log elements are present describing items that could not be included. |

### Error Response

```xml
<Response success="false" error="[log]" downloadhandler="">
  <!-- log entries describing the failure -->
</Response>
```

---

## Required Permissions

Any authenticated user with read access to the specified documents and folders may call this API.

---

## Chunked Download Workflow

1. **`DownloadZipWithHandler`** *(this API)* — Stage the zip archive and obtain a `downloadhandler` GUID.
2. **`DownloadFileChunk`** — Download the archive in sequential chunks using the handler GUID, advancing `StartOffset` by `chunklength` after each call, until `lastchunk="true"`.
3. **`DeleteDownloadHandler`** — Clean up the handler and the temporary zip file on the server.

---

## Example

### GET Request (strict mode)

```
GET /srv.asmx/DownloadZipWithHandler
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Paths=/MyLibrary/Reports/Report.pdf|/MyLibrary/Slides
  &partialResult=false
HTTP/1.1
```

### GET Request (partial mode)

```
GET /srv.asmx/DownloadZipWithHandler
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Paths=/MyLibrary/Reports|/Archive/OldDocs
  &partialResult=true
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/DownloadZipWithHandler HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Paths=/MyLibrary/Reports/Report.pdf|/MyLibrary/Slides
&partialResult=false
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:DownloadZipWithHandler>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:Paths>/MyLibrary/Reports/Report.pdf|/MyLibrary/Slides</tns:Paths>
      <tns:partialResult>false</tns:partialResult>
    </tns:DownloadZipWithHandler>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Unlike `DownloadZip`, this API returns **XML** — the zip archive is not returned directly. Use the `downloadhandler` GUID to retrieve the zip in chunks via `DownloadFileChunk`.
- The `error="[log]"` value is a literal signal that child log elements are present in the response body describing which items were skipped or failed.
- With `partialResult=false` (strict mode), if any document or folder cannot be added to the archive, the entire operation fails and no handler is returned.
- With `partialResult=true` (partial mode), the operation succeeds as long as the zip file was created, even if some items were excluded. Check for `error="[log]"` and inspect log entries to see what was skipped.
- System-configured zip restrictions apply: if the total document count or combined file size exceeds the configured limits, the operation fails.
- When including a folder path, all documents within that folder and its sub-folders are included in the archive.
- Always call `DeleteDownloadHandler` after finishing the chunked download to free temporary server storage.

---

## Related APIs

- [DownloadFileChunk](DownloadFileChunk.md) - Download chunks of the staged zip archive using the handler GUID
- [DeleteDownloadHandler](DeleteDownloadHandler.md) - Clean up the download handler after all chunks are retrieved
- [DownloadZip](DownloadZip.md) - Download a zip of documents and folders as a raw byte array in one call (suitable for small archives)
- [GetDownloadQue](GetDownloadQue.md) - Get the list of items in the current user's download queue

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| No valid paths | None of the provided paths resolved to a document or folder. |
| Zip size or count restriction exceeded | The selection exceeds system-configured zip limits. |
| `[log]` (with `success="false"`) | Zip creation failed; inspect child log elements for details. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/DownloadZipWithHandler*
