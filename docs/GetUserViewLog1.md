# GetUserViewLog1 API

Returns the read/view log history for a specified user filtered by a date range. This API retrieves document access entries from both the current view log (VIEWLOG table) and historical read logs (HISTORY_READ table) that fall within the specified date range.

## Endpoint

```
/srv.asmx/GetUserViewLog1
```

## Methods

- **GET** `/srv.asmx/GetUserViewLog1?authenticationTicket=...&userName=...&startdate=...&endDate=...`
- **POST** `/srv.asmx/GetUserViewLog1` (form data)
- **SOAP** Action: `http://tempuri.org/GetUserViewLog1`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `userName` | string | Yes | Login name of the user whose view log history should be retrieved. |
| `startdate` | DateTime | No | Start date for filtering results. Format: `yyyy-MM-ddTHH:mm:ss` or `yyyy-MM-dd`. If omitted or null, no lower date boundary is applied. |
| `endDate` | DateTime | No | End date for filtering results. Format: `yyyy-MM-ddTHH:mm:ss` or `yyyy-MM-dd`. If omitted or null, no upper date boundary is applied. |

### Date Parameter Format

The date parameters accept multiple formats:
- **ISO 8601**: `2024-06-15T10:30:00` or `2024-06-15T10:30:00Z` (UTC)
- **Date only**: `2024-06-15` (assumes 00:00:00 local time)
- **Null/Empty**: No filtering on that boundary

If UTC dates are provided (ending with 'Z'), they are automatically converted to local server time for querying.

---

## Response

### Success Response

Returns a `<response>` root element containing a `<viewlogs>` element, which holds zero or more `<viewlog>` child elements. Each element represents a document view/read event within the specified date range.

```xml
<response success="true" error="">
  <viewlogs>
    <viewlog DocumentId="1523" 
             UserId="7" 
             UserFullname="John Smith" 
             DocumentName="Q1-Report.pdf" 
             VersionNumber="2.0.0" 
             ViewDate="2024-06-15T10:30:00.000Z" 
             DomainName="Finance" 
             Path="/Finance/Reports" />
    <viewlog DocumentId="1489" 
             UserId="7" 
             UserFullname="John Smith" 
             DocumentName="Budget-2024.xlsx" 
             VersionNumber="1.0.0" 
             ViewDate="2024-06-14T14:20:00.000Z" 
             DomainName="Finance" 
             Path="/Finance/Planning" />
  </viewlogs>
</response>
```

### Viewlog Element Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `DocumentId` | int | Unique identifier of the document that was accessed. |
| `UserId` | int | User ID of the user who accessed the document (matches the queried user). |
| `UserFullname` | string | Full name of the user who accessed the document. |
| `DocumentName` | string | Name of the document file (including extension). |
| `VersionNumber` | string | Version number in multi-part format (e.g. `"2.0.0"` for version 2). |
| `ViewDate` | string | UTC timestamp when the document was accessed, in ISO 8601 format (`yyyy-MM-ddTHH:mm:ss.fffZ`). Empty if not set. |
| `DomainName` | string | Name of the domain/library containing the document. |
| `Path` | string | Full folder path where the document resides (not including the document name). |

### Error Response

```xml
<response success="false" error="User not found." />
```

---

## Required Permissions

The calling user must be authenticated. Any authenticated user can retrieve view logs for **any user** -" there is no permission check restricting this to administrators or the user themselves.

---

## Example

### GET Request (Date Range Filter)

```
GET /srv.asmx/GetUserViewLog1
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &userName=jsmith
  &startdate=2024-06-01
  &endDate=2024-06-30
HTTP/1.1
```

### GET Request (Start Date Only)

```
GET /srv.asmx/GetUserViewLog1
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &userName=jsmith
  &startdate=2024-06-15T00:00:00
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetUserViewLog1 HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&userName=jsmith
&startdate=2024-06-01T00:00:00
&endDate=2024-06-30T23:59:59
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetUserViewLog1>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:userName>jsmith</tns:userName>
      <tns:startdate>2024-06-01T00:00:00</tns:startdate>
      <tns:endDate>2024-06-30T23:59:59</tns:endDate>
    </tns:GetUserViewLog1>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- **Date Filtering**: This API is identical to `GetUserViewLog` but adds optional date range filtering. If both `startdate` and `endDate` are omitted or null, it behaves exactly like `GetUserViewLog`.
- **Inclusive Range**: The date range is inclusive on both ends. A `ViewDate` matching exactly `startdate` or `endDate` will be included in results.
- **Time Zone Handling**: 
  - If dates are provided in UTC format (with 'Z' suffix), they are converted to local server time before querying.
  - Date-only values (e.g., `2024-06-15`) are interpreted as midnight local time.
- **Combined Data Sources**: The response combines entries from both the active view log (VIEWLOG table) and the historical read log (HISTORY_READ table).
- **Duplicate Removal**: Duplicate entries (same user, document, version, and timestamp) are automatically removed from the combined result set.
- **Sorting**: Results are sorted by `ViewDate` in ascending order (oldest first).
- **Empty Results**: If no documents were accessed within the date range, an empty `<viewlogs/>` element is returned (not an error).
- **Date Format**: All `ViewDate` attributes in the response use UTC ISO 8601 format (`yyyy-MM-ddTHH:mm:ss.fffZ`).
- **Version Number Format**: The `VersionNumber` attribute shows the multi-part format (`major.minor.revision`) rather than the internal integer format.

---

## Use Cases

1. **Audit Reports**: Generate access reports for a specific user over a fiscal quarter or year.
2. **Compliance Auditing**: Track which documents a user accessed during a compliance review period.
3. **Activity Analysis**: Analyze user document access patterns within specific timeframes.
4. **Performance Reviews**: Review employee document access history for performance evaluations.

---

## Related APIs

- [GetUserViewLog](GetUserViewLog.md) - Get complete user view log history without date filtering
- [GetDocumentViewLog](GetDocumentViewLog.md) - Get the view log for a specific document (all users who accessed it)
- [GetDocumentReadLogHistory](GetDocumentReadLogHistory.md) - Get detailed read log history for a specific document and user

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| User not found | The specified userName does not exist in the system. |
| `SystemError:...` | An unexpected server-side error occurred. |

---
