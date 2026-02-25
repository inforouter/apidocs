# DownloadDocument API

Downloads the latest version of a document and returns its content as a raw byte array. This is a single-call download suitable for small to medium-sized files. For large files, use the chunked download workflow (`GetDownloadHandler` → `DownloadFileChunk` → `DeleteDownloadHandler`) instead.

## Endpoint

```
/srv.asmx/DownloadDocument
```

## Methods

- **GET** `/srv.asmx/DownloadDocument?authenticationTicket=...&Path=...`
- **POST** `/srv.asmx/DownloadDocument` (form data)
- **SOAP** Action: `http://tempuri.org/DownloadDocument`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path of the document to download (e.g. `/MyLibrary/Reports/Report.pdf`). |

## Response

### Success Response

The response body contains the raw binary content of the document's latest version.

- **REST (GET/POST)**: Returns raw bytes (`application/octet-stream`).
- **SOAP**: Returns a `base64`-encoded byte array within the SOAP response envelope.

### Error Response

On any error (authentication failure, document not found, offline document, or download failure), an **empty byte array** is returned. There is no XML error message. The caller must check whether the returned byte array is empty to detect failure.

---

## Required Permissions

Any authenticated user with read access to the document may call this API.

---

## Example

### GET Request

```
GET /srv.asmx/DownloadDocument
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/MyLibrary/Reports/Report.pdf
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/DownloadDocument HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/MyLibrary/Reports/Report.pdf
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:DownloadDocument>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:Path>/MyLibrary/Reports/Report.pdf</tns:Path>
    </tns:DownloadDocument>
  </soap:Body>
</soap:Envelope>
```

### SOAP Response (success)

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <DownloadDocumentResponse xmlns="http://tempuri.org/">
      <DownloadDocumentResult>JVBERi0xLjQK...</DownloadDocumentResult>
    </DownloadDocumentResponse>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- This API always downloads the **latest version** of the document. To download a specific version use `DownloadDocumentVersion`.
- If the document is in **Offline** state, an empty byte array is returned.
- On any error (invalid ticket, path not found, permission denied, download failure), the response is an **empty byte array** with no accompanying error message. Use `DocumentExists` to verify the document is accessible before downloading if you need explicit error details.
- For large files, prefer the chunked download workflow to avoid memory and timeout issues: `GetDownloadHandler` → `DownloadFileChunk` → `DeleteDownloadHandler`.
- The downloaded bytes represent the file exactly as stored in the warehouse — no conversion or transformation is applied.

---

## Related APIs

- [DownloadDocumentVersion](DownloadDocumentVersion) - Download a specific version of a document
- [GetDownloadHandler](GetDownloadHandler) - Prepare a document for chunked download (recommended for large files)
- [DownloadFileChunk](DownloadFileChunk) - Download a chunk of a file using a handler
- [DocumentExists](DocumentExists) - Check whether a document exists and retrieve its CRC32 checksums
- [GetDocument](GetDocument) - Get document properties without downloading content

---

## Error Codes

| Condition | Result |
|-----------|--------|
| Invalid or missing authentication ticket | Empty byte array returned |
| Document not found at the specified path | Empty byte array returned |
| Document is in Offline state | Empty byte array returned |
| Download failure | Empty byte array returned |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/DownloadDocument*
