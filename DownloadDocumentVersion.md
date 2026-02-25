# DownloadDocumentVersion API

Downloads a specific version of a document and returns its content as a raw byte array. Use this when you need a particular historical version rather than the latest. For large files, use the chunked download workflow (`GetDownloadHandlerByVersion` → `DownloadFileChunk` → `DeleteDownloadHandler`) instead.

## Endpoint

```
/srv.asmx/DownloadDocumentVersion
```

## Methods

- **GET** `/srv.asmx/DownloadDocumentVersion?authenticationTicket=...&Path=...&VersionNumber=...`
- **POST** `/srv.asmx/DownloadDocumentVersion` (form data)
- **SOAP** Action: `http://tempuri.org/DownloadDocumentVersion`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path of the document (e.g. `/MyLibrary/Reports/Report.pdf`). |
| `VersionNumber` | int | Yes | Version number to download. Accepts both legacy format (e.g. `1`, `2`, `3`) and modernized format (e.g. `1000000`, `2000000`, `3000000`) — legacy values are automatically converted internally. Use `GetDocumentVersions` to retrieve valid version numbers. |

## Response

### Success Response

The response body contains the raw binary content of the specified document version.

- **REST (GET/POST)**: Returns raw bytes (`application/octet-stream`).
- **SOAP**: Returns a `base64`-encoded byte array within the SOAP response envelope.

### Error Response

On any error (authentication failure, document not found, version not found, offline document, or download failure), an **empty byte array** is returned. There is no XML error message. The caller must check whether the returned byte array is empty to detect failure.

---

## Required Permissions

Any authenticated user with read access to the document may call this API.

---

## Example

### GET Request

```
GET /srv.asmx/DownloadDocumentVersion
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/MyLibrary/Reports/Report.pdf
  &VersionNumber=3000000
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/DownloadDocumentVersion HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/MyLibrary/Reports/Report.pdf
&VersionNumber=3000000
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:DownloadDocumentVersion>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:Path>/MyLibrary/Reports/Report.pdf</tns:Path>
      <tns:VersionNumber>3000000</tns:VersionNumber>
    </tns:DownloadDocumentVersion>
  </soap:Body>
</soap:Envelope>
```

### SOAP Response (success)

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <DownloadDocumentVersionResponse xmlns="http://tempuri.org/">
      <DownloadDocumentVersionResult>JVBERi0xLjQK...</DownloadDocumentVersionResult>
    </DownloadDocumentVersionResponse>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Both **legacy** version numbers (e.g. `1`, `2`, `3`) and **modernized** version numbers (e.g. `1000000`, `2000000`, `3000000`) are accepted. Legacy values below 1,000,000 are automatically multiplied by 1,000,000 internally before the lookup. Either format will work — use whatever `GetDocumentVersions` returns.
- If the document is in **Offline** state, an empty byte array is returned.
- On any error, the response is an **empty byte array** with no accompanying error message. Use `GetDocumentVersions` to verify the version exists before downloading if you need explicit error details.
- To download the latest version without specifying a version number, use `DownloadDocument`.
- For large files, prefer the chunked download workflow to avoid memory and timeout issues: `GetDownloadHandlerByVersion` → `DownloadFileChunk` → `DeleteDownloadHandler`.

---

## Related APIs

- [DownloadDocument](DownloadDocument) - Download the latest version of a document
- [GetDocumentVersions](GetDocumentVersions) - List all versions of a document (use to retrieve valid VersionNumber values)
- [GetDownloadHandlerByVersion](GetDownloadHandlerByVersion) - Prepare a specific document version for chunked download
- [DownloadFileChunk](DownloadFileChunk) - Download a chunk of a file using a handler
- [DeleteDownloadHandler](DeleteDownloadHandler) - Clean up a download handler after use

---

## Error Codes

| Condition | Result |
|-----------|--------|
| Invalid or missing authentication ticket | Empty byte array returned |
| Document not found at the specified path | Empty byte array returned |
| Version not found | Empty byte array returned |
| Document is in Offline state | Empty byte array returned |
| Download failure | Empty byte array returned |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/DownloadDocumentVersion*
