# UploadTiffAsPDF API

Uploads a TIFF image file and stores it as a PDF document at the specified path. The server converts the TIFF to PDF automatically before storing. If no document exists at the path, a new document is created. If a document already exists, a new version is added.

## Endpoint

```
/srv.asmx/UploadTiffAsPDF
```

## Methods

- **GET** `/srv.asmx/UploadTiffAsPDF?authenticationTicket=...&path=...&fileContent=...`
- **POST** `/srv.asmx/UploadTiffAsPDF` (form data -" recommended for binary content)
- **SOAP** Action: `http://tempuri.org/UploadTiffAsPDF`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full infoRouter destination path including file name and `.pdf` extension (e.g. `/Scans/Invoice-001.pdf`). The file extension must reflect the PDF output, not the TIFF input. |
| `fileContent` | byte[] | Yes | The raw binary content of the TIFF image file, encoded as Base64 when sent over HTTP. |

---

## Response

### Success Response

```xml
<root success="true" DocumentId="12345" VersionId="1000001" />
```

### Error Response

```xml
<root success="false" error="[901] Session expired or Invalid ticket" />
```

---

## Required Permissions

The calling user must have **write** (upload) permission on the destination folder.

---

## Example

### POST Request

```
POST /srv.asmx/UploadTiffAsPDF HTTP/1.1
Content-Type: multipart/form-data; boundary=----FormBoundary

------FormBoundary
Content-Disposition: form-data; name="authenticationTicket"

3f2504e0-4f89-11d3-9a0c-0305e82c3301
------FormBoundary
Content-Disposition: form-data; name="path"

/Scans/Invoice-001.pdf
------FormBoundary
Content-Disposition: form-data; name="fileContent"; filename="invoice.tiff"
Content-Type: image/tiff

[binary TIFF content]
------FormBoundary--
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:UploadTiffAsPDF>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:path>/Scans/Invoice-001.pdf</tns:path>
      <tns:fileContent>SUkqAAgAAAA...</tns:fileContent>
    </tns:UploadTiffAsPDF>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- The PDF conversion is performed server-side. The infoRouter PDF conversion service must be configured and running.
- The `path` should end in `.pdf` to reflect the converted output format.
- For large TIFF files, use the chunked upload approach: `CreateUploadHandler` -' `UploadFileChunk` -' `UploadTiffAsPDFWithHandler`.
- Multi-page TIFF files are converted to multi-page PDFs.

---

## Related APIs

- [UploadTiffAsPDFWithHandler](UploadTiffAsPDFWithHandler.md) - Upload TIFF as PDF using a chunked upload handler
- [UploadDocument](UploadDocument.md) - Upload any document in its original format
- [CreateUploadHandler](CreateUploadHandler.md) - Create a handler for large chunked uploads

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Folder not found | The destination folder in the path does not exist. |
| PDF conversion error | The server-side TIFF-to-PDF conversion failed. |
| Access denied | The user does not have upload permission on the destination folder. |
| `SystemError:...` | An unexpected server-side error occurred. |

---