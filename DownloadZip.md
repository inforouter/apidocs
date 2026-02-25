# DownloadZip API

Zips one or more documents and folders and returns the archive as a raw byte array in a single call. This is suitable for small selections. For large archives, use `DownloadZipWithHandler` to stage the file server-side and retrieve it in chunks with `DownloadFileChunk`.

## Endpoint

```
/srv.asmx/DownloadZip
```

## Methods

- **GET** `/srv.asmx/DownloadZip?authenticationTicket=...&Paths=...`
- **POST** `/srv.asmx/DownloadZip` (form data)
- **SOAP** Action: `http://tempuri.org/DownloadZip`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Paths` | string | Yes | Pipe-separated (`\|`) list of infoRouter paths to include in the zip. Each entry can be a full infoRouter path to a document or folder, or a short ID path (`~D{id}` for a document, `~F{id}` for a folder). Paths that cannot be resolved are silently skipped. |

### Paths Format

Multiple items are separated by a pipe character (`|`):

```
/MyLibrary/Reports/Report.pdf|/MyLibrary/Slides|/OtherLibrary/Notes/Note.docx
```

Mix of full paths and short ID paths is also supported:

```
~D4217|~F112|/MyLibrary/Reports/Summary.pdf
```

## Response

### Success Response

The response body contains the raw bytes of a ZIP archive.

- **REST (GET/POST)**: Returns raw bytes (`application/octet-stream`).
- **SOAP**: Returns a `base64`-encoded byte array within the SOAP response envelope.

### Error Response

On any error (authentication failure, no valid paths resolved, zip size/count restriction exceeded, or zip creation failure), an **empty byte array** is returned. There is no XML error message.

---

## Required Permissions

Any authenticated user with read access to the specified documents and folders may call this API. Paths the user cannot access are silently skipped rather than causing an error.

---

## Example

### GET Request

```
GET /srv.asmx/DownloadZip
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Paths=/MyLibrary/Reports/Report.pdf|/MyLibrary/Slides
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/DownloadZip HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Paths=/MyLibrary/Reports/Report.pdf|/MyLibrary/Slides
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:DownloadZip>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:Paths>/MyLibrary/Reports/Report.pdf|/MyLibrary/Slides</tns:Paths>
    </tns:DownloadZip>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Paths are separated by the pipe character (`|`). Each entry is resolved independently — paths that cannot be found or accessed are silently skipped.
- If none of the provided paths resolve to a valid document or folder, an empty byte array is returned.
- System-configured zip restrictions apply: if the total document count or combined file size exceeds the configured limits, an empty byte array is returned.
- For large archives that may cause memory or timeout issues, use `DownloadZipWithHandler` to stage the zip on the server and retrieve it in chunks via `DownloadFileChunk`.
- On any error, the response is an **empty byte array** — there is no accompanying XML error message.
- When including a folder in `Paths`, all documents within that folder (and its sub-folders) are added to the archive.

---

## Related APIs

- [DownloadZipWithHandler](DownloadZipWithHandler) - Stage a zip archive on the server and obtain a download handler GUID (recommended for large archives)
- [DownloadFileChunk](DownloadFileChunk) - Download chunks of a staged zip file using a handler
- [DeleteDownloadHandler](DeleteDownloadHandler) - Clean up a download handler after chunked download
- [GetDownloadQue](GetDownloadQue) - Get the list of items in the current user's download queue

---

## Error Codes

| Condition | Result |
|-----------|--------|
| Invalid or missing authentication ticket | Empty byte array returned |
| No valid paths resolved | Empty byte array returned |
| Zip size or count restriction exceeded | Empty byte array returned |
| Zip creation failure | Empty byte array returned |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/DownloadZip*
