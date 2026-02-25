# GetDocumentVersion API

Returns the metadata for a specific version of a document, identified by document path and version number. The response includes the version author, size, checksum, creation and publish dates, check-in comment, and approval information.

## Endpoint

```
/srv.asmx/GetDocumentVersion
```

## Methods

- **GET** `/srv.asmx/GetDocumentVersion?authenticationTicket=...&path=...&versionNumber=...`
- **POST** `/srv.asmx/GetDocumentVersion` (form data)
- **SOAP** Action: `http://tempuri.org/GetDocumentVersion`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1-Report.pdf`), or a short document ID path (`~D{id}` or `~D{id}.ext`). |
| `versionNumber` | int | Yes | Version number to retrieve. Pass `0` to retrieve the currently published version. Otherwise use the modern format: version 1 = `1000000`, version 2 = `2000000`, etc. Values between `1` and `999,999` will not match any version and result in an error. |

### Version Number Format

infoRouter stores and returns version numbers in a large-integer format where version 1 = `1000000`, version 2 = `2000000`, and so on. The `Number` attribute in the response always uses this format.

| Intent | Value to pass |
|--------|---------------|
| Published version | `0` |
| Version 1 | `1000000` |
| Version 2 | `2000000` |
| Version N | `N × 1000000` |

---

## Response

### Success Response

Returns a `<response>` root element containing a single `<Version>` element. The version number is an attribute; all other fields are child elements.

```xml
<response success="true" error="">
  <Version Number="2000000">
    <VersionAuthor>jsmith</VersionAuthor>
    <VersionAuthorId>7</VersionAuthorId>
    <VersionSize>204800</VersionSize>
    <CheckSum>a1b2c3d4e5f6...</CheckSum>
    <DateCreated>2024-06-15T10:30:00.000Z</DateCreated>
    <DatePublished>2024-06-16T09:00:00.000Z</DatePublished>
    <Comment>Updated executive summary section</Comment>
    <ApprovalStatus>Approved</ApprovalStatus>
    <ApprovalDate>2024-06-17T08:00:00.000Z</ApprovalDate>
  </Version>
</response>
```

### Version Element

| Field | Type | Description |
|-------|------|-------------|
| `Number` *(attribute)* | int | Version number in modern format (e.g. `1000000` for version 1, `2000000` for version 2). |
| `<VersionAuthor>` | string | Login name of the user who created this version. |
| `<VersionAuthorId>` | int | User ID of the version author. |
| `<VersionSize>` | long | File size of this version in bytes. |
| `<CheckSum>` | string | Checksum of the version file. Empty if checksum is unavailable. |
| `<CheckSumError>` | string | Present only if the checksum could not be computed. Contains the error message. |
| `<DateCreated>` | string | UTC timestamp when this version was created, in ISO 8601 format (`yyyy-MM-ddTHH:mm:ss.fffZ`). Empty if not set. |
| `<DatePublished>` | string | UTC timestamp when this version was published. Empty if the version has never been published. |
| `<Comment>` | string | Check-in comment for this version. Empty if no comment was entered. |
| `<ApprovalStatus>` | string | Approval status (e.g. `Approved`, `Pending`, `Rejected`). |
| `<ApprovalDate>` | string | UTC timestamp when the version was approved. Empty if not approved. |

### Error Response

```xml
<response success="false" error="Specified version cannot be found." />
```

---

## Required Permissions

The calling user must have at least read access to the document.

---

## Example

### GET Request (published version)

```
GET /srv.asmx/GetDocumentVersion
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &path=/Finance/Reports/Q1-2024-Report.pdf
  &versionNumber=0
HTTP/1.1
```

### GET Request (specific version)

```
GET /srv.asmx/GetDocumentVersion
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &path=/Finance/Reports/Q1-2024-Report.pdf
  &versionNumber=2000000
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetDocumentVersion HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&path=/Finance/Reports/Q1-2024-Report.pdf
&versionNumber=1000000
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetDocumentVersion>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:path>/Finance/Reports/Q1-2024-Report.pdf</tns:path>
      <tns:versionNumber>1000000</tns:versionNumber>
    </tns:GetDocumentVersion>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- All date fields use UTC ISO 8601 format (`yyyy-MM-ddTHH:mm:ss.fffZ`). Empty string means the date is not set.
- `<CheckSumError>` is only present in the response when the checksum computation fails; it does not appear on successful checksum retrieval.
- Empty child elements (e.g. `<Comment/>`) are always present in the response even if the value is empty.
- Version numbers between `1` and `999,999` will not match any stored version and return an error. Use `0` or the modern format (≥ `1000000`).
- To retrieve the full list of versions for a document, use `GetDocumentVersions`.

---

## Related APIs

- [GetDocumentVersions](GetDocumentVersions.md) - Get the full version history list for a document
- [GetDocument](GetDocument.md) - Get document properties including current version number
- [DownloadDocumentVersion](DownloadDocumentVersion.md) - Download a specific version as a byte array

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Document not found | The specified path does not resolve to an existing document. |
| Specified version cannot be found | The requested version number does not exist for this document. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/GetDocumentVersion*
