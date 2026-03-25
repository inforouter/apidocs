# GetDeleteLog API

Returns the deletion audit log for documents, folders, and libraries matching the specified date range and path filter. Each entry records a single delete-related action (recycle, purge, empty recycle bin, or restore) along with who performed it and when.

## Endpoint

```
/srv.asmx/GetDeleteLog
```

## Methods

- **GET** `/srv.asmx/GetDeleteLog?AuthenticationTicket=...&StartDate=...&EndDate=...&PathFilter=...`
- **POST** `/srv.asmx/GetDeleteLog` (form data)
- **SOAP** Action: `http://tempuri.org/GetDeleteLog`

## Parameters

All filter parameters are optional. When all filters are omitted, all deletion log entries in the system are returned (requires system-wide permission — see [Required Permissions](#required-permissions)).

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `StartDate` | DateTime | No | Return entries with an action date on or after this value. Format: `yyyy-MM-dd` or `yyyy-MM-ddTHH:mm:ss`. UTC values are converted to server local time. Leave empty for no lower bound. |
| `EndDate` | DateTime | No | Return entries with an action date on or before this value. Date-only values are automatically extended to `23:59:59`. UTC values are converted to server local time. Leave empty for no upper bound. |
| `PathFilter` | string | No | Path filter scoping the query. Also controls the required permission level — see [Required Permissions](#required-permissions). Supports wildcard `*` at the end (e.g. `\Finance\*`). Leave empty to query all libraries. |

---

## Required Permissions

The required permission level depends on the `PathFilter` value:

| `PathFilter` value | Required permission |
|--------------------|---------------------|
| Empty or omitted | System-wide **ViewAuditLogs** admin permission |
| Unresolvable path (library name not found) | System-wide **ViewAuditLogs** admin permission |
| Starts with a valid library name (e.g. `\Finance` or `\Finance\Reports*`) | **ViewAuditLogs** permission for that library only |

When a library name is resolved from the path, the query is automatically scoped to that library. Library-level audit log administrators can therefore query their own library without system-wide admin rights.

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
  </logs>
</response>
```

### LOGITEM Attribute Reference

| Attribute | Type | Description |
|-----------|------|-------------|
| `TYPE` | string | Object type: `DOCUMENT`, `FOLDER`, or `DOMAIN`. |
| `NAME` | string | Name of the document, folder, or library. |
| `PATH` | string | Full infoRouter path of the item at the time of the action. |
| `DATE` | string | Date and time the action was performed (server local time, `yyyy-MM-dd HH:mm:ss`). |
| `ID` | int | Internal ID of the document, folder, or library. |
| `DOMAINID` | int | Internal ID of the library the item belonged to. |
| `DOMAINNAME` | string | Name of the library (first path segment). |
| `ACTION` | string | Type of delete action performed (see values below). |
| `USERID` | int | Internal user ID of the person who performed the action. |
| `FULLNAME` | string | Full name of the person who performed the action. |

### ACTION Values

| Value | Description |
|-------|-------------|
| `RECYCLE` | Item was moved to the Recycle Bin (soft delete). |
| `PURGE` | Item was permanently deleted from the Recycle Bin. |
| `RECYCLE EMPTIED` | Item was removed when a user emptied their Recycle Bin. |
| `RESTORE` | Item was restored from the Recycle Bin back to the library. |

### Empty Result

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

## Example Requests

### GET — all deletions in June 2024 (system-wide)

```
GET /srv.asmx/GetDeleteLog?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301&StartDate=2024-06-01&EndDate=2024-06-30 HTTP/1.1
Host: server.example.com
```

### GET — all deletions under the Finance library

```
GET /srv.asmx/GetDeleteLog?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301&PathFilter=\Finance\* HTTP/1.1
Host: server.example.com
```

### POST

```
POST /srv.asmx/GetDeleteLog HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301&StartDate=2024-06-01&EndDate=2024-06-30&PathFilter=\Finance\*
```

### SOAP 1.1

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetDeleteLog"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetDeleteLog xmlns="http://tempuri.org/">
      <AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</AuthenticationTicket>
      <StartDate>2024-06-01</StartDate>
      <EndDate>2024-06-30</EndDate>
      <PathFilter>\Finance\*</PathFilter>
    </GetDeleteLog>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- **PathFilter also sets permission scope**: providing a valid library name in the path is not just a filter — it also reduces the required permission to library-level `ViewAuditLogs`. Omitting the path queries all libraries and requires system-wide admin rights.
- **ACTION includes restores**: the log records `RESTORE` and `RECYCLE EMPTIED` events in addition to `RECYCLE` and `PURGE`. Filter by `ACTION` in your client if you want only hard-delete events.
- **PathFilter wildcards**: use `*` as a trailing wildcard. `\Finance\*` matches all items under the Finance library. An exact path is used when no `*` is present.
- **EndDate end-of-day expansion**: a date-only `EndDate` (e.g. `2024-06-30`) is automatically extended to `2024-06-30 23:59:59`, so all events on that day are included.
- **UTC input**: `StartDate` and `EndDate` may be submitted as UTC values; the server converts them to local time before filtering.
- **DATE format**: the `DATE` attribute in the response is server local time in `yyyy-MM-dd HH:mm:ss` format, not UTC.

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Insufficient rights.` | The caller does not have the required `ViewAuditLogs` permission. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

## Related APIs

- [GetCheckInLog](GetCheckInLog.md) - Get check-in log entries
- [GetClassificationLogs](GetClassificationLogs.md) - Get classification level change history
- [GetDispositionLog](GetDispositionLog.md) - Get retention and disposition log entries
- [SearchRecycledItems](SearchRecycledItems.md) - Search for items currently in the Recycle Bin
- [PurgeRecycleBinItem](PurgeRecycleBinItem.md) - Permanently delete a Recycle Bin item
- [RestoreRecycleBinItem](RestoreRecycleBinItem.md) - Restore a Recycle Bin item
