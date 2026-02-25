# GetDeleteLog API

Returns the deletion audit log for documents, folders, and libraries matching the specified date range and path filter. Each log entry records a single delete-related action (recycle, purge, empty recycle bin, or restore) along with who performed it and when. Use this API to audit deletion activity across the system, track data loss events, or verify that purged items were disposed of intentionally.

## Endpoint

```
/srv.asmx/GetDeleteLog
```

## Methods

- **GET** `/srv.asmx/GetDeleteLog?AuthenticationTicket=...&StartDate=...&EndDate=...&PathFilter=...`
- **POST** `/srv.asmx/GetDeleteLog` (form data)
- **SOAP** Action: `http://tempuri.org/GetDeleteLog`

## Parameters

All filter parameters are optional. When all filters are omitted, all deletion log entries in the system are returned.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `StartDate` | DateTime | No | Return entries with an action date on or after this date/time. Format: `yyyy-MM-dd` or `yyyy-MM-ddTHH:mm:ss`. UTC values are automatically converted to server local time. Leave empty for no lower bound. |
| `EndDate` | DateTime | No | Return entries with an action date on or before this date/time. Format: `yyyy-MM-dd` or `yyyy-MM-ddTHH:mm:ss`. If a date-only value is given (time = midnight), the filter is automatically extended to `23:59:59` (end of that day). UTC values are automatically converted to server local time. Leave empty for no upper bound. |
| `PathFilter` | string | No | Filter entries by the path of the deleted item. Supports wildcards using `*` (e.g. `\Finance\*` returns all deletions under the Finance library). An exact path match is performed when no wildcard is present. Leave empty to return entries for any path. |

---

## Response

### Success Response

Returns a `<response>` element with `success="true"` containing a `<logs>` element with zero or more `<LOGITEM>` child elements. Results are ordered by action date **descending** (most recent first).

```xml
<response success="true" error="">
  <logs>
    <LOGITEM
      TYPE="DOCUMENT"
      NAME="Q1-2024-Report.pdf"
      PATH="\Finance\Reports"
      DATE="2024-06-15 14:30:00"
      ID="9871"
      DOMAINID="5"
      DOMAINNAME="Finance"
      ACTION="RECYCLE"
      USERID="12"
      FULLNAME="John Smith" />
    <LOGITEM
      TYPE="FOLDER"
      NAME="OldArchives"
      PATH="\Finance\OldArchives"
      DATE="2024-06-14 10:00:00"
      ID="4312"
      DOMAINID="5"
      DOMAINNAME="Finance"
      ACTION="PURGE"
      USERID="1"
      FULLNAME="Admin User" />
    <LOGITEM
      TYPE="DOCUMENT"
      NAME="Invoice-2023.pdf"
      PATH="\Finance\Invoices"
      DATE="2024-06-13 09:15:00"
      ID="8800"
      DOMAINID="5"
      DOMAINNAME="Finance"
      ACTION="RESTORE"
      USERID="12"
      FULLNAME="John Smith" />
  </logs>
</response>
```

### LOGITEM Attribute Reference

| Attribute | Type | Description |
|-----------|------|-------------|
| `TYPE` | string | Object type that was acted on: `DOCUMENT`, `FOLDER`, or `DOMAIN`. |
| `NAME` | string | Name of the document, folder, or library. |
| `PATH` | string | Full infoRouter path of the item at the time of the action (e.g. `\Finance\Reports`). |
| `DATE` | string | Date and time the action was performed, in server local time format `yyyy-MM-dd HH:mm:ss`. |
| `ID` | int | Internal ID of the document, folder, or library. |
| `DOMAINID` | int | Internal ID of the library/domain the item belonged to. |
| `DOMAINNAME` | string | Name of the library/domain the item belonged to (the first path segment). |
| `ACTION` | string | The type of delete action performed (see values below). |
| `USERID` | int | Internal user ID of the person who performed the action. |
| `FULLNAME` | string | Full name of the person who performed the action. |

### ACTION Values

| Value | Description |
|-------|-------------|
| `RECYCLE` | Item was moved to the Recycle Bin (soft delete). |
| `PURGE` | Item was permanently deleted from the Recycle Bin (hard delete). |
| `RECYCLE EMPTIED` | Item was removed when a user emptied their Recycle Bin. |
| `RESTORE` | Item was restored from the Recycle Bin back to the library. |

### Empty Result Response

When no entries match the filter criteria:

```xml
<response success="true" error="">
  <logs />
</response>
```

### Error Response

```xml
<response success="false" error="Insufficient rights." />
```

---

## Required Permissions

The calling user must be authenticated and must have the **`ViewAuditLogs`** administration permission. This is typically granted to compliance officers, records managers, and system administrators.

---

## Example

### GET Request -" all deletions in June 2024

```
GET /srv.asmx/GetDeleteLog
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &StartDate=2024-06-01
  &EndDate=2024-06-30
HTTP/1.1
```

### GET Request -" all deletions under the Finance library

```
GET /srv.asmx/GetDeleteLog
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &PathFilter=\Finance\*
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetDeleteLog HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&StartDate=2024-06-01
&EndDate=2024-06-30
&PathFilter=\Finance\*
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetDeleteLog>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:StartDate>2024-06-01</tns:StartDate>
      <tns:EndDate>2024-06-30</tns:EndDate>
      <tns:PathFilter>\Finance\*</tns:PathFilter>
    </tns:GetDeleteLog>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- **Sort Order**: Entries are returned in descending `DATE` order (most recent first).
- **ACTION Includes Restores**: The log records not just delete and purge actions but also `RESTORE` events (when items are recovered from the Recycle Bin) and `RECYCLE EMPTIED` (bulk emptying of a bin). Filter by `ACTION` value in your client if you want only hard-delete events.
- **PathFilter Wildcards**: Use `*` as a wildcard character. `\Finance\*` matches all items under the Finance library. An exact path is used when no `*` is present. Path comparison is case-insensitive.
- **EndDate End-of-Day Expansion**: If `EndDate` is provided as a date-only value (e.g. `2024-06-30`), the filter is automatically extended to `2024-06-30 23:59:59`, so all events on that day are included.
- **UTC Input**: `StartDate` and `EndDate` may be submitted as UTC values. The server automatically converts them to local time before filtering.
- **No Filters**: Omitting all filter parameters returns the full deletion history for the entire system. This may return a large result set; apply date and path filters in production usage.
- **DATE Format**: The `DATE` attribute in the response uses server local time in `yyyy-MM-dd HH:mm:ss` format -" this is not UTC.

---

## Related APIs

- [GetClassificationLogs](GetClassificationLogs.md) - Get classification level change history
- [GetDispositionLog](GetDispositionLog.md) - Get retention and disposition log entries
- [GetSecurityChangeLog](GetSecurityChangeLog.md) - Get security change log entries
- [SearchRecycledItems](SearchRecycledItems.md) - Search for items currently in the Recycle Bin
- [PurgeRecycleBinItem](PurgeRecycleBinItem.md) - Permanently delete a Recycle Bin item
- [RestoreRecycleBinItem](RestoreRecycleBinItem.md) - Restore a Recycle Bin item

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Insufficient rights.` | The calling user does not have the `ViewAuditLogs` admin permission. |
| `SystemError:...` | An unexpected server-side error occurred. |

---
