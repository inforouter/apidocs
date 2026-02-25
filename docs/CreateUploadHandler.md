# CreateUploadHandler API

Creates a server-side temporary upload handler that enables large file uploads to be sent in smaller chunks. Returns a handler GUID and the negotiated chunk size to use for subsequent `UploadFileChunk` calls.

This is the first step in the chunked upload workflow. The handler acts as a staging area on the server until the upload is finalized by `UploadDocumentWithHandler`.

## Endpoint

```
/srv.asmx/CreateUploadHandler
```

## Methods

- **GET** `/srv.asmx/CreateUploadHandler?authenticationTicket=...&PreferedChunkSize=...`
- **POST** `/srv.asmx/CreateUploadHandler` (form data)
- **SOAP** Action: `http://tempuri.org/CreateUploadHandler`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `PreferedChunkSize` | int | Yes | Preferred chunk size in bytes for subsequent `UploadFileChunk` calls. Pass `0` to use the system default. The server enforces a minimum of **262,144 bytes (256 KB)** and a maximum of **33,554,432 bytes (32 MB)**; values outside this range are silently clamped to the nearest limit. |

## Response

### Success Response

```xml
<response success="true" error="" UploadHandler="a1b2c3d4-e5f6-7890-abcd-ef1234567890" ChunkSize="1048576" />
```

| Attribute | Description |
|-----------|-------------|
| `success` | `true` if the handler was created successfully. |
| `UploadHandler` | GUID string identifying the upload handler. Pass this value to every subsequent `UploadFileChunk` and `UploadDocumentWithHandler` call. |
| `ChunkSize` | The actual chunk size in bytes the server has accepted (after clamping). Split the file into chunks of exactly this size (the last chunk may be smaller) when calling `UploadFileChunk`. |

### Error Response

```xml
<response success="false" error="Error message" />
```

---

## Required Permissions

Any authenticated user may call this API.

---

## Chunked Upload Workflow

Use the following sequence to upload a large file in chunks:

1. **`CreateUploadHandler`** -" Allocate a handler and obtain the `UploadHandler` GUID and `ChunkSize`.
2. **`UploadFileChunk`** -" Send the file in sequential chunks of `ChunkSize` bytes, passing `LastChunk=true` on the final chunk.
3. **`UploadDocumentWithHandler`** (or `UploadDocumentWithHandler1` / `UploadNewDocumentWidthHandler`) -" Finalize the upload: move the staged file into the document library and create the document or new version.
4. **`DeleteUploadHandler`** -" Clean up the handler if the upload is cancelled or if an error occurs before step 3 completes.

---

## Example

### GET Request

```
GET /srv.asmx/CreateUploadHandler
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &PreferedChunkSize=1048576
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/CreateUploadHandler HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&PreferedChunkSize=1048576
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:CreateUploadHandler>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:PreferedChunkSize>1048576</tns:PreferedChunkSize>
    </tns:CreateUploadHandler>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Pass `PreferedChunkSize=0` to let the server select the default chunk size configured in the application settings.
- The server silently clamps the chunk size: values below **256 KB** (262,144 bytes) are raised to 256 KB; values above **32 MB** (33,554,432 bytes) are reduced to 32 MB.
- Always use the `ChunkSize` value returned in the response -" not the value you requested -" when splitting the file into chunks for `UploadFileChunk`.
- The handler exists only for the duration of the upload session. If the upload is not completed, call `DeleteUploadHandler` to free the temporary storage.
- Upload handlers are tied to the authenticated user's session. A handler created with one ticket cannot be used with a different user's ticket.

---

## Related APIs

- [UploadFileChunk](UploadFileChunk.md) - Upload a single chunk of a file to an open handler
- [UploadDocumentWithHandler](UploadDocumentWithHandler.md) - Finalize the upload and create or update a document
- [DeleteUploadHandler](DeleteUploadHandler.md) - Delete an upload handler and discard its staged data
- [UploadDocument](UploadDocument.md) - Upload a complete document in a single call (no handler required)

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |

---
