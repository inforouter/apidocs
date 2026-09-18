# UploadTiffAsPDF API

Uploads a TIFF image and stores it as a PDF. The converted document is created with a `.pdf` name rather than the `.tif` name in `Path`: a new document if that path is free, a new version if it is not.

## Endpoint

```
/srv.asmx/UploadTiffAsPDF
```

## Methods

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

## JavaScript

> **The content must really be a TIFF.** The uploaded bytes are converted to PDF before
> anything is stored, and the document is created with a `.pdf` name rather than the `.tif`
> name in `Path`. Content that is not a TIFF is refused with `4000` and the converter's own
> message, and nothing is stored under either name.

```javascript
// Anything carrying bytes is POST-only: a byte[] cannot be bound from a query string, and a GET is
// answered HTTP 415 before the operation runs.
async function post(action, fields) {
  const response = await fetch(`/srv.asmx/${action}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ authenticationTicket: ticket, ...fields })
  });

  const root = new DOMParser()
    .parseFromString(await response.text(), 'text/xml').documentElement;

  if (root.getAttribute('success') !== 'true') {
    throw new Error(`${root.getAttribute('errorCode')}: ${root.getAttribute('error')}`);
  }
  return root;
}

const base64 = bytes => btoa(String.fromCharCode(...bytes));
```

```javascript
// What it does today: stores the bytes as they are, under the name in Path.
await post('UploadTiffAsPDF', {
  Path: '/Scans/2026/invoice.tif',
  FileContent: base64(tiffBytes)
});
```

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

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4000` | a document is already at that path and is not checked out by the caller |
| `4041` | no folder at the parent of the path |
| `4030` | the caller may not add documents there, or the folder rules forbid the file type |
| `HTTP 415` | the call was a GET; the content can only be posted |
| `HTTP 400` | a required parameter was empty; refused by model binding, so there is no error document |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Folder not found | The destination folder in the path does not exist. |
| PDF conversion error | The server-side TIFF-to-PDF conversion failed. |
| Access denied | The user does not have upload permission on the destination folder. |
| `SystemError:...` | An unexpected server-side error occurred. |

---