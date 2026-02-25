# GetSoxLogs API

Returns the complete SOX (Sarbanes-Oxley) compliance review log for the specified document. Each log entry records a single SOX review event -" the version reviewed, the reviewer, the review date, and the review comment. Use this API to programmatically audit the SOX review history of a document, verify that required compliance reviews have been performed, or export SOX log data for audit and financial reporting purposes.

## Endpoint

```
/srv.asmx/GetSoxLogs
```

## Methods

- **GET** `/srv.asmx/GetSoxLogs?AuthenticationTicket=...&DocumentPath=...`
- **POST** `/srv.asmx/GetSoxLogs` (form data)
- **SOAP** Action: `http://tempuri.org/GetSoxLogs`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DocumentPath` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Procedures/FinancialControls.pdf`). The path must resolve to an existing document. |

---

## Response

### Success Response

Returns a `<response>` element with `success="true"` containing a `<Value>` element with zero or more `<SoxLog>` child elements -" one per SOX review event recorded for the document, in the order they were stored.

```xml
<response success="true" error="">
  <Value>
    <SoxLog>
      <DocumentId>9871</DocumentId>
      <VersionNumber>1000000</VersionNumber>
      <ReviewDate>2024-06-15T14:30:00</ReviewDate>
      <Comment>SOX review completed. Financial controls verified. No exceptions noted for Q2 2024.</Comment>
      <UserId>12</UserId>
      <UserName>jsmith</UserName>
    </SoxLog>
    <SoxLog>
      <DocumentId>9871</DocumentId>
      <VersionNumber>1000000</VersionNumber>
      <ReviewDate>2023-06-12T10:00:00</ReviewDate>
      <Comment>Initial SOX review after document publication. Controls effective.</Comment>
      <UserId>8</UserId>
      <UserName>mjones</UserName>
    </SoxLog>
  </Value>
</response>
```

### SoxLog Field Reference

| Field | Type | Description |
|-------|------|-------------|
| `DocumentId` | int | Internal ID of the document. |
| `VersionNumber` | int | Internal version number of the document version that was reviewed. For standard versioning: `1000000` = Version 1, `2000000` = Version 2. For milestone/patch versioning the value encodes major, minor, and patch: e.g. `1001002` = version `1.1.2`. A value of `0` indicates the version was not recorded. |
| `ReviewDate` | DateTime | Date and time the review was recorded, in ISO 8601 format (`yyyy-MM-ddTHH:mm:ss`). |
| `Comment` | string | The SOX review comment text entered by the reviewer. |
| `UserId` | int | Internal user ID of the reviewer who recorded the log entry. |
| `UserName` | string | Username of the reviewer. |

### No Entries Response

When no SOX log entries exist for the document:

```xml
<response success="true" error="">
  <Value />
</response>
```

### Error Response

```xml
<response success="false" error="Insufficient rights." />
```

---

## Required Permissions

The calling user must satisfy **one of** the following conditions:

1. **`DocumentReadSoxLog`** permission on the document (the document-level "Read SOX Log" access right), **or**
2. **`ViewAuditLogs`** system administration permission on the document's library.

Domain managers and document owners typically have `DocumentReadSoxLog`. System administrators with `ViewAuditLogs` can read SOX logs for any document regardless of document-level permissions. Both conditions are checked independently -" either is sufficient.

Additionally, the document must **not** be in an Offline (archived) state.

---

## Example

### GET Request

```
GET /srv.asmx/GetSoxLogs
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DocumentPath=/Finance/Procedures/FinancialControls.pdf
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetSoxLogs HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&DocumentPath=/Finance/Procedures/FinancialControls.pdf
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetSoxLogs>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:DocumentPath>/Finance/Procedures/FinancialControls.pdf</tns:DocumentPath>
    </tns:GetSoxLogs>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- **Documents Only**: This API accepts document paths only. Passing a folder path will return a "Document not found" error.
- **Offline Documents**: If the document is in an Offline (archived) state, the API returns an error. Restore the document to an active library before querying its SOX log.
- **Version Number Format**: `VersionNumber` stores the raw internal version value. For standard documents, Version 1 = `1000000`, Version 2 = `2000000`. For documents using milestone/patch versioning, the value encodes `MMMNNNPPP` (major -- 10--- + minor -- 10³ + patch). A value of `0` means the version was not captured at the time of the review.
- **Dual Permission Check**: Both `DocumentReadSoxLog` and `ViewAuditLogs` are evaluated -" either is sufficient to authorize access. This differs slightly from some other log APIs where only one check succeeds before returning.
- **Adding SOX Logs**: Use `AddSOXComment` to add a new SOX review comment to a document.
- **Relationship to ISO Logs**: SOX logs and ISO logs are independent audit trails. A document may have entries in both. Use `GetISOLogs` for ISO compliance review history.

---

## Related APIs

- [AddSOXComment](AddSOXComment.md) - Record a new SOX review comment on a document
- [GetISOLogs](GetISOLogs.md) - Get the ISO compliance review log for a document
- [GetDocumentViewLog](GetDocumentViewLog.md) - Get the full view/access log for a document
- [GetDeleteLog](GetDeleteLog.md) - Get the deletion audit log

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Document not found.` | The `DocumentPath` does not resolve to an existing document. |
| `Insufficient rights.` | The caller does not have `DocumentReadSoxLog` permission on the document and does not have the `ViewAuditLogs` admin permission. |
| Document is Offline | The document is in an archived/offline state and its SOX log cannot be retrieved. |
| `SystemError:...` | An unexpected server-side error occurred. |

---
