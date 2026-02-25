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
1. CreateUploadHandler         → returns UploadHandler GUID + ChunkSize
2. UploadFileChunk             → repeat until LastChunk=true (upload all TIFF chunks)
3. UploadTiffAsPDFWithHandler  → finalize: convert TIFF to PDF and store
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

*For detailed documentation visit: https://support.inforouter.com/api-docs/UploadTiffAsPDFWithHandler*
