# DocumentExists1 API

Checks whether a named document exists within a specified folder and returns CRC32 checksums for the latest version and the published version. This is an alternative to `DocumentExists` that accepts the folder path and document name as separate parameters instead of a combined full path.

## Endpoint

```
/srv.asmx/DocumentExists1
```

## Methods

- **GET** `/srv.asmx/DocumentExists1?authenticationTicket=...&FolderPath=...&DocumentName=...`
- **POST** `/srv.asmx/DocumentExists1` (form data)
- **SOAP** Action: `http://tempuri.org/DocumentExists1`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `FolderPath` | string | Yes | Full infoRouter path of the folder containing the document (e.g. `/MyLibrary/Reports`). |
| `DocumentName` | string | Yes | Name of the document within the folder (e.g. `Report.pdf`). Do not include a leading slash. |

## Response

### Success Response

```xml
<response success="true" CRC32LASTVERSION="a3f1c29d" CRC32="b7e4d80c" />
```

| Attribute | Description |
|-----------|-------------|
| `success` | `true` if the document was found. |
| `CRC32LASTVERSION` | CRC32 checksum of the latest version's file content. |
| `CRC32` | CRC32 checksum of the published version's file content. Empty string if no version has been published. |

### Error Response

```xml
<response success="false" error="Error message" />
```

---

## Required Permissions

Any authenticated user may call this API. The folder and document must be accessible to the authenticated user.

---

## Example

### GET Request

```
GET /srv.asmx/DocumentExists1
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &FolderPath=/MyLibrary/Reports
  &DocumentName=Report.pdf
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/DocumentExists1 HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&FolderPath=/MyLibrary/Reports
&DocumentName=Report.pdf
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:DocumentExists1>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:FolderPath>/MyLibrary/Reports</tns:FolderPath>
      <tns:DocumentName>Report.pdf</tns:DocumentName>
    </tns:DocumentExists1>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Unlike `DocumentExists`, this variant does **not** accept short document paths (`~D{id}.{ext}`). Both `FolderPath` and `DocumentName` must be plain string values.
- The lookup resolves the folder first, then searches for the document by name within that folder. If either step fails, an error is returned.
- The `CRC32` attribute (published version checksum) is an empty string when no version of the document has been published.
- Use the returned CRC32 checksums to verify document content integrity without downloading the file.

---

## Related APIs

- [DocumentExists](DocumentExists.md) - Check document existence using a single combined path (also supports short `~D` paths)
- [GetDocument](GetDocument.md) - Get full document properties
- [FolderExists](FolderExists.md) - Check whether a folder exists at a given path

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Folder not found` | The `FolderPath` does not refer to an existing folder. |
| `Document not found` | No document named `DocumentName` exists in the specified folder. |

---
