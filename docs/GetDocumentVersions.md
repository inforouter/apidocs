# GetDocumentVersions API

Returns the full version history list for a document. Each version entry includes the version author, file size, checksum, creation and publish dates, check-in comment, and approval information.

## Endpoint

```
/srv.asmx/GetDocumentVersions
```

## Methods

- **GET** `/srv.asmx/GetDocumentVersions?AuthenticationTicket=...&Path=...`
- **POST** `/srv.asmx/GetDocumentVersions` (form data)
- **SOAP** Action: `http://tempuri.org/GetDocumentVersions`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1-Report.pdf`), or a short document ID path (`~D{id}` or `~D{id}.ext`). |

---

## Response

### Success Response

Returns a `<response>` root element containing a `<Versions>` element with one `<Version>` child per version. The list includes all versions ordered as stored. If the document has no versions, `<Versions>` is present but empty.

```xml
<response success="true" error="">
  <Versions>
    <Version Number="1000000">
      <VersionAuthor>jsmith</VersionAuthor>
      <VersionAuthorId>7</VersionAuthorId>
      <VersionSize>102400</VersionSize>
      <CheckSum>a1b2c3d4e5f6...</CheckSum>
      <DateCreated>2024-03-10T08:15:00.000Z</DateCreated>
      <DatePublished>2024-03-11T09:00:00.000Z</DatePublished>
      <Comment>Initial upload</Comment>
      <ApprovalStatus>Approved</ApprovalStatus>
      <ApprovalDate>2024-03-12T10:00:00.000Z</ApprovalDate>
    </Version>
    <Version Number="2000000">
      <VersionAuthor>jsmith</VersionAuthor>
      <VersionAuthorId>7</VersionAuthorId>
      <VersionSize>204800</VersionSize>
      <CheckSum>b2c3d4e5f6a1...</CheckSum>
      <DateCreated>2024-06-15T10:30:00.000Z</DateCreated>
      <DatePublished>2024-06-16T09:00:00.000Z</DatePublished>
      <Comment>Updated executive summary section</Comment>
      <ApprovalStatus>Approved</ApprovalStatus>
      <ApprovalDate>2024-06-17T08:00:00.000Z</ApprovalDate>
    </Version>
  </Versions>
</response>
```

### Version Element

Each `<Version>` element has one attribute and several child elements:

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
| `<Comment>` | string | Check-in comment for this version. Empty if no comment was entered. If the comment could not be retrieved, contains `N/A error:{message}`. |
| `<ApprovalStatus>` | string | Approval status (e.g. `Approved`, `Pending`, `Rejected`). |
| `<ApprovalDate>` | string | UTC timestamp when the version was approved. Empty if not approved. |

### Error Response

```xml
<response success="false" error="Document not found." />
```

---

## Required Permissions

The calling user must have at least read access to the document.

---

## Example

### GET Request

```
GET /srv.asmx/GetDocumentVersions
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports/Q1-2024-Report.pdf
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetDocumentVersions HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance/Reports/Q1-2024-Report.pdf
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetDocumentVersions>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:Path>/Finance/Reports/Q1-2024-Report.pdf</tns:Path>
    </tns:GetDocumentVersions>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- All date fields use UTC ISO 8601 format (`yyyy-MM-ddTHH:mm:ss.fffZ`). An empty string means the date is not set.
- `<CheckSumError>` is only present in a `<Version>` element when the checksum computation fails; it does not appear on successful checksum retrieval.
- All child elements are always present in each `<Version>` even when their value is empty.
- Version numbers in the `Number` attribute use the modern format: version 1 = `1000000`, version 2 = `2000000`, etc.
- To retrieve a single specific version, use `GetDocumentVersion`.

---

## Related APIs

- [GetDocumentVersion](GetDocumentVersion.md) - Get metadata for a single specific version
- [GetDocument](GetDocument.md) - Get document properties including current version number
- [DownloadDocumentVersion](DownloadDocumentVersion.md) - Download a specific version as a byte array
- [DeleteDocumentVersion](DeleteDocumentVersion.md) - Permanently delete a specific version

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Document not found | The specified path does not resolve to an existing document. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/GetDocumentVersions*
