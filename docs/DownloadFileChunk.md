# DownloadFileChunk API

Downloads a single chunk of a staged file using an open download handler. Returns the chunk bytes as base64-encoded content inside an XML element, along with metadata about the chunk and the total file. This is the second step in the chunked download workflow.

## Endpoint

```
/srv.asmx/DownloadFileChunk
```

## Methods

- **GET** `/srv.asmx/DownloadFileChunk?authenticationTicket=...&DownloadHandler=...&StartOffset=...&ChunkSize=...`
- **POST** `/srv.asmx/DownloadFileChunk` (form data)
- **SOAP** Action: `http://tempuri.org/DownloadFileChunk`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DownloadHandler` | string (GUID) | Yes | The handler GUID returned by `GetDownloadHandler`, `GetDownloadHandlerByVersion`, or `DownloadZipWithHandler`. Must be a valid GUID string. |
| `StartOffset` | int | Yes | Byte offset within the file at which to begin reading. Use `0` for the first chunk. For each subsequent chunk, increment by the previous chunk's `chunklength` value. |
| `ChunkSize` | int | Yes | Maximum number of bytes to read for this chunk. The actual bytes returned may be less for the final chunk. |

## Response

### Success Response

The chunk bytes are returned as **base64-encoded text** in the XML element body. File metadata and chunk integrity information are provided as attributes.

```xml
<response success="true"
          filelength="1048576"
          chunklength="65536"
          lastchunk="false"
          chunkCRC32="a3f1c29d">
  JVBERi0xLjQKJeLjz9MKNiAwIG9iag==...
</response>
```

| Attribute | Type | Description |
|-----------|------|-------------|
| `success` | bool | `true` if the chunk was read successfully. |
| `filelength` | int | Total size of the staged file in bytes. Use this to calculate the total number of chunks. |
| `chunklength` | int | Actual number of bytes returned in this chunk. May be less than `ChunkSize` for the final chunk. Always use `chunklength` (not `ChunkSize`) when advancing `StartOffset`. |
| `lastchunk` | bool | `"true"` when this is the last chunk of the file (`StartOffset + ChunkSize >= filelength`). Stop iterating when this is `"true"`. |
| `chunkCRC32` | string | CRC32 checksum of this chunk's bytes. Use to verify chunk integrity after decoding from base64. |
| *(body)* | string | Base64-encoded bytes of the chunk content. |

### Error Response

```xml
<response success="false" error="Error message" />
```

---

## Required Permissions

Any authenticated user may call this API. The download handler must have been created by the same authenticated user's session.

---

## Chunked Download Workflow

1. **`GetDownloadHandler`** (or `GetDownloadHandlerByVersion` / `DownloadZipWithHandler`) -" Prepare the file and obtain a `DownloadHandler` GUID and the total file size.
2. **`DownloadFileChunk`** *(this API)* -" Call repeatedly, advancing `StartOffset` by `chunklength` after each response, until `lastchunk="true"`.
3. **`DeleteDownloadHandler`** -" Clean up the handler and its temporary file.

### Iteration Example

```
// First chunk
StartOffset=0, ChunkSize=65536
-' chunklength=65536, lastchunk="false"

// Second chunk
StartOffset=65536, ChunkSize=65536
-' chunklength=65536, lastchunk="false"

// Final chunk (file size = 180000 bytes)
StartOffset=131072, ChunkSize=65536
-' chunklength=48928, lastchunk="true"  --- stop here
```

Always advance `StartOffset` by `chunklength` (not `ChunkSize`) to correctly handle the shorter final chunk.

---

## Example

### GET Request

```
GET /srv.asmx/DownloadFileChunk
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DownloadHandler=a1b2c3d4-e5f6-7890-abcd-ef1234567890
  &StartOffset=0
  &ChunkSize=65536
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/DownloadFileChunk HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&DownloadHandler=a1b2c3d4-e5f6-7890-abcd-ef1234567890
&StartOffset=0
&ChunkSize=65536
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:DownloadFileChunk>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:DownloadHandler>a1b2c3d4-e5f6-7890-abcd-ef1234567890</tns:DownloadHandler>
      <tns:StartOffset>0</tns:StartOffset>
      <tns:ChunkSize>65536</tns:ChunkSize>
    </tns:DownloadFileChunk>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- The chunk content is **base64-encoded** in the XML body -" decode it before writing to the output file.
- Use `chunklength` (not `ChunkSize`) when advancing `StartOffset` to correctly handle the shorter final chunk.
- Check `chunkCRC32` after decoding each chunk to verify it was not corrupted in transit.
- Stop iterating when `lastchunk="true"`. Do not make a further call with the next offset.
- Passing a string that is not a valid GUID for `DownloadHandler` returns an error immediately.
- If the handler file has been deleted or expired, an error is returned.
- After all chunks are collected, call `DeleteDownloadHandler` to free the temporary file on the server.

---

## Related APIs

- [GetDownloadHandler](GetDownloadHandler.md) - Prepare a document for chunked download and obtain the handler GUID
- [GetDownloadHandlerByVersion](GetDownloadHandlerByVersion.md) - Prepare a specific document version for chunked download
- [DownloadZipWithHandler](DownloadZipWithHandler.md) - Prepare a zip archive of folders and documents for chunked download
- [DeleteDownloadHandler](DeleteDownloadHandler.md) - Clean up the download handler after all chunks are retrieved
- [UploadFileChunk](UploadFileChunk.md) - Upload counterpart for chunked uploads

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Invalid download handler. (guid)` | `DownloadHandler` is not a valid GUID string. |
| Handler not found | The handler file does not exist (deleted or expired). |

---
