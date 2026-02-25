# UploadFileChunk API

Uploads a single binary chunk to a server-side upload handler as part of a chunked large-file upload workflow. Each chunk is verified against its CRC32 checksum before being appended. When `lastChunk=true`, the handler is marked as complete and ready for finalization.

## Endpoint

```
/srv.asmx/UploadFileChunk
```

## Methods

- **GET** `/srv.asmx/UploadFileChunk?authenticationTicket=...&uploadHandler=...&fileChunk=...&chunkHEXCRC=...&lastChunk=...`
- **POST** `/srv.asmx/UploadFileChunk` (form data — recommended for binary content)
- **SOAP** Action: `http://tempuri.org/UploadFileChunk`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `uploadHandler` | string (GUID) | Yes | The upload handler GUID returned by `CreateUploadHandler`. |
| `fileChunk` | byte[] | Yes | The binary chunk data, encoded as Base64 when sent over HTTP. The recommended chunk size is returned by `CreateUploadHandler` (256 KB minimum, 32 MB maximum). |
| `chunkHEXCRC` | string | Yes | The CRC32 checksum of this chunk, expressed as a hexadecimal string (e.g. `A3F2B1C0`). The server verifies the checksum before appending the chunk. |
| `lastChunk` | bool | Yes | `true` if this is the final chunk of the file. `false` for all intermediate chunks. Setting `true` marks the handler as ready for finalization. |

---

## Chunked Upload Workflow

```
1. CreateUploadHandler  → returns UploadHandler GUID + recommended ChunkSize
2. UploadFileChunk      → upload chunk 1 (lastChunk=false)
3. UploadFileChunk      → upload chunk 2 (lastChunk=false)
   ...
N. UploadFileChunk      → upload last chunk (lastChunk=true)
N+1. UploadDocumentWithHandler[X] → finalize and create the document
```

---

## Response

### Success Response (non-final chunk)

```xml
<root success="true" tryagain="false" />
```

### Success Response (final chunk)

```xml
<root success="true" tryagain="false" />
```

### Checksum Mismatch (retry this chunk)

```xml
<root success="true" tryagain="true" />
```

> When `tryagain="true"` is returned, the chunk was NOT appended — resend the same chunk.

### Error Response

```xml
<root success="false" error="Invalid upload handler." />
```

---

## Required Permissions

The calling user must be authenticated. The handler must have been created by the same authenticated session.

---

## Example

### POST Request (chunk upload)

```
POST /srv.asmx/UploadFileChunk HTTP/1.1
Content-Type: multipart/form-data; boundary=----FormBoundary

------FormBoundary
Content-Disposition: form-data; name="authenticationTicket"

3f2504e0-4f89-11d3-9a0c-0305e82c3301
------FormBoundary
Content-Disposition: form-data; name="uploadHandler"

a1b2c3d4-e5f6-7890-abcd-ef1234567890
------FormBoundary
Content-Disposition: form-data; name="fileChunk"; filename="chunk"
Content-Type: application/octet-stream

[binary chunk bytes]
------FormBoundary
Content-Disposition: form-data; name="chunkHEXCRC"

A3F2B1C0
------FormBoundary
Content-Disposition: form-data; name="lastChunk"

false
------FormBoundary--
```

---

## Notes

- Always check the `tryagain` attribute in the response. If `tryagain="true"`, the chunk checksum did not match — resend the same chunk without advancing.
- The recommended chunk size is returned by `CreateUploadHandler` and is between 256 KB and 32 MB.
- Chunk sizes below 256 KB are automatically raised to 256 KB by the server.
- CRC32 is computed over the raw binary chunk bytes before Base64 encoding.

---

## Related APIs

- [CreateUploadHandler](CreateUploadHandler.md) - Create the upload handler before calling this API
- [UploadDocumentWithHandler](UploadDocumentWithHandler.md) - Finalize the upload after all chunks are sent
- [UploadDocumentWithHandler3](UploadDocumentWithHandler3.md) - Finalize with XML parameters
- [DeleteUploadHandler](DeleteUploadHandler.md) - Discard the handler without creating a document
- [DownloadFileChunk](DownloadFileChunk.md) - Download a file in chunks

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Invalid upload handler.` | The GUID is not a valid GUID format. |
| Handler not found / expired | The handler file does not exist — it may have expired or been deleted. |
| `tryagain="true"` | Chunk checksum mismatch — resend the chunk. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/UploadFileChunk*
