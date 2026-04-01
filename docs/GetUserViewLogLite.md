# GetUserViewLogLite API

Returns a paginated read/view log history for a specified user filtered by a date range, along with the total matching record count. This is the paginated version of `GetUserViewLog1` — suited for large result sets where you want to retrieve records in pages rather than all at once.

## Endpoint

```
/srv.asmx/GetUserViewLogLite
```

## Methods

- **GET** `/srv.asmx/GetUserViewLogLite?authenticationTicket=...&userName=...&startdate=...&endDate=...&startingRow=...&rowCount=...`
- **POST** `/srv.asmx/GetUserViewLogLite` (form data)
- **SOAP** Action: `http://tempuri.org/GetUserViewLogLite`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `userName` | string | Yes | Login name of the user whose view log history should be retrieved. |
| `startdate` | DateTime | No | Start date for filtering results. Format: `yyyy-MM-ddTHH:mm:ss` or `yyyy-MM-dd`. If omitted or null, no lower date boundary is applied. |
| `endDate` | DateTime | No | End date for filtering results. Format: `yyyy-MM-ddTHH:mm:ss` or `yyyy-MM-dd`. If omitted or null, no upper date boundary is applied. |
| `startingRow` | int | Yes | Zero-based row offset for pagination. Pass `0` to start from the first matching record. |
| `rowCount` | int | Yes | Maximum number of records to return in this page. |

### Date Parameter Format

The date parameters accept multiple formats:

- **ISO 8601**: `2024-06-15T10:30:00` or `2024-06-15T10:30:00Z` (UTC)
- **Date only**: `2024-06-15` (assumes 00:00:00 local time)
- **Null/Empty**: No filtering on that boundary

If UTC dates are provided (ending with `Z`), they are automatically converted to local server time for querying.

---

## Response

### Success Response

Returns a `<response>` root element with pagination attributes and an optional `<viewlogs>` child element containing zero or more `<viewlog>` entries.

```xml
<response success="true"
          recordCount="47"
          startingRow="0"
          rowCount="10">
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

### Root Element Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `success` | string | `"true"` on success, `"false"` on failure. |
| `recordCount` | int | Total number of matching records across all pages (useful for calculating total page count). |
| `startingRow` | int | The `startingRow` value from the request (echo). |
| `rowCount` | int | Actual number of `<viewlog>` records returned in this response (may be less than the requested `rowCount` on the last page). |

### Viewlog Element Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `DocumentId` | int | Unique identifier of the document that was accessed. |
| `UserId` | int | User ID of the user who accessed the document. |
| `UserFullname` | string | Full name of the user who accessed the document. |
| `DocumentName` | string | Name of the document file (including extension). |
| `VersionNumber` | string | Version number in multi-part format (e.g. `"2.0.0"` for version 2). |
| `ViewDate` | string | UTC timestamp when the document was accessed, in ISO 8601 format (`yyyy-MM-ddTHH:mm:ss.fffZ`). |
| `DomainName` | string | Name of the domain/library containing the document. |
| `Path` | string | Full folder path where the document resides (not including the document name). |

### Error Response

```xml
<response success="false" error="User not found." />
```

---

## Required Permissions

The calling user must be authenticated. Any authenticated user can retrieve view logs for **any user** — there is no permission check restricting this to administrators or the user themselves.

---

## Example

### GET Request

```
GET /srv.asmx/GetUserViewLogLite
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &userName=jsmith
  &startdate=2024-06-01
  &endDate=2024-06-30
  &startingRow=0
  &rowCount=10
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetUserViewLogLite HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&userName=jsmith
&startdate=2024-06-01T00:00:00
&endDate=2024-06-30T23:59:59
&startingRow=20
&rowCount=10
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetUserViewLogLite>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:userName>jsmith</tns:userName>
      <tns:startdate>2024-06-01T00:00:00</tns:startdate>
      <tns:endDate>2024-06-30T23:59:59</tns:endDate>
      <tns:startingRow>0</tns:startingRow>
      <tns:rowCount>10</tns:rowCount>
    </tns:GetUserViewLogLite>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- **Pagination**: Use `recordCount` in the response together with your requested `rowCount` to calculate the total number of pages. Increment `startingRow` by `rowCount` on each subsequent request to walk through all pages.
- **Empty Page**: If `recordCount` is `0`, the `<viewlogs>` element is omitted from the response entirely.
- **Date Filtering**: If both `startdate` and `endDate` are omitted or null, all available records for the user are considered (subject to pagination).
- **Inclusive Range**: The date range is inclusive on both ends.
- **Time Zone Handling**: UTC dates (with `Z` suffix) are converted to local server time before querying. Date-only values are interpreted as midnight local time.
- **Combined Data Sources**: Results are drawn from both the active view log (VIEWLOG table) and the historical read log (HISTORY_READ table).
- **Duplicate Removal**: Duplicate entries (same user, document, version, and timestamp) are automatically removed.
- **Version Number Format**: The `VersionNumber` attribute uses multi-part format (`major.minor.revision`).

---

## Use Cases

1. **Paginated Audit UI**: Display a scrollable/paginated table of document access history for a user in a control panel.
2. **Large-Scale Compliance Reports**: Retrieve millions of log entries in manageable chunks without timeout risk.
3. **Server-Side Paging**: Power data grids with server-side pagination for user activity dashboards.

---

## Related APIs

- [GetUserViewLog](GetUserViewLog.md) - Get complete user view log history without date filtering
- [GetUserViewLog1](GetUserViewLog1.md) - Get user view log filtered by date range (non-paginated)
- [GetDocumentViewLog](GetDocumentViewLog.md) - Get the view log for a specific document (all users who accessed it)

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| User not found | The specified `userName` does not exist in the system. |
| `SystemError:...` | An unexpected server-side error occurred. |
