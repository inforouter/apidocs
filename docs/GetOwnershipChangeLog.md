# GetOwnershipChangeLog API

Returns the ownership change log for documents and folders matching the specified date range and path filter. Each entry records a transfer of ownership, including the previous owner, the new owner, and who performed the change.

## Endpoint

```
/srv.asmx/GetOwnershipChangeLog
```

## Methods

- **GET** `/srv.asmx/GetOwnershipChangeLog?authenticationTicket=...&startDate=...&endDate=...&pathFilter=...`
- **POST** `/srv.asmx/GetOwnershipChangeLog` (form data)
- **SOAP** Action: `http://tempuri.org/GetOwnershipChangeLog`

## Parameters

All filter parameters are optional. When all filters are omitted, all ownership change log entries in the system are returned (requires system-wide permission — see [Required Permissions](#required-permissions)).

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `startDate` | DateTime | No | Return entries with an action date on or after this value. Format: `yyyy-MM-dd` or `yyyy-MM-ddTHH:mm:ss`. UTC values are converted to server local time. Leave empty for no lower bound. |
| `endDate` | DateTime | No | Return entries with an action date on or before this value. UTC values are converted to server local time. Leave empty for no upper bound. |
| `pathFilter` | string | No | Path filter scoping the query. Also controls the required permission level — see [Required Permissions](#required-permissions). Supports wildcard `*` at the end (e.g. `\MyLibrary\Reports*`). Leave empty to query all libraries. |

---

## Required Permissions

The required permission level depends on the `pathFilter` value:

| `pathFilter` value | Required permission |
|--------------------|---------------------|
| Empty or omitted | System-wide **ViewAuditLogs** admin permission |
| Unresolvable path (library name not found) | System-wide **ViewAuditLogs** admin permission |
| Starts with a valid library name (e.g. `\MyLibrary` or `\MyLibrary\Reports*`) | **ViewAuditLogs** permission for that library only |

When a library name is resolved from the path, the query is automatically scoped to that library. Library-level audit log administrators can therefore query their own library without system-wide admin rights.

---

## Response

### Success Response

Returns a `<response>` element with `success="true"` containing a `<logs>` element with zero or more `<LOGITEM>` child elements. Results are ordered by action date **descending** (most recent first).

```xml
<response success="true">
  <logs>
    <LOGITEM
      TYPE="DOCUMENT"
      NAME="Report_2025.docx"
      PATH="\MyLibrary\Reports"
      PARENTID="42"
      ID="1234"
      DOMAINID="1"
      DOMAINNAME="MyLibrary"
      BEFORE_PLAYERID="8"
      BEFORE_PLAYERNAME="Jane Doe"
      AFTER_PLAYERID="5"
      AFTER_PLAYERNAME="John Smith"
      DATE="2026-02-01 14:30:00"
      USERID="1"
      FULLNAME="Admin User" />
    <LOGITEM
      TYPE="FOLDER"
      NAME="Archive"
      PATH="\MyLibrary\Archive"
      PARENTID="10"
      ID="567"
      DOMAINID="1"
      DOMAINNAME="MyLibrary"
      BEFORE_PLAYERID="5"
      BEFORE_PLAYERNAME="John Smith"
      AFTER_PLAYERID="8"
      AFTER_PLAYERNAME="Jane Doe"
      DATE="2026-01-15 10:00:00"
      USERID="1"
      FULLNAME="Admin User" />
  </logs>
</response>
```

### LOGITEM Attribute Reference

| Attribute | Type | Description |
|-----------|------|-------------|
| `TYPE` | string | Object type: `DOCUMENT` or `FOLDER`. |
| `NAME` | string | Name of the object whose ownership changed. |
| `PATH` | string | Full infoRouter path of the object (library name prepended). |
| `PARENTID` | int | Internal ID of the parent folder. |
| `ID` | int | Internal ID of the object. |
| `DOMAINID` | int | Internal ID of the library the object belongs to. |
| `DOMAINNAME` | string | Name of the library. |
| `BEFORE_PLAYERID` | int | Internal user ID of the previous owner. |
| `BEFORE_PLAYERNAME` | string | Full name of the previous owner. |
| `AFTER_PLAYERID` | int | Internal user ID of the new owner. |
| `AFTER_PLAYERNAME` | string | Full name of the new owner. |
| `DATE` | string | Date and time the ownership change was performed (server local time, `yyyy-MM-dd HH:mm:ss`). |
| `USERID` | int | Internal user ID of the person who performed the ownership change. |
| `FULLNAME` | string | Full name of the person who performed the ownership change. |

### Empty Result

```xml
<response success="true">
  <logs />
</response>
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

---

## Example Requests

### GET — system-wide query

```
GET /srv.asmx/GetOwnershipChangeLog?authenticationTicket=abc123-def456&startDate=2026-01-01&endDate=2026-02-01 HTTP/1.1
Host: server.example.com
```

### GET — scoped to a library

```
GET /srv.asmx/GetOwnershipChangeLog?authenticationTicket=abc123-def456&startDate=2026-01-01&endDate=2026-02-01&pathFilter=\MyLibrary* HTTP/1.1
Host: server.example.com
```

### POST

```
POST /srv.asmx/GetOwnershipChangeLog HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&startDate=2026-01-01&endDate=2026-02-01&pathFilter=\MyLibrary*
```

### SOAP 1.1

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetOwnershipChangeLog"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetOwnershipChangeLog xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
      <startDate>2026-01-01</startDate>
      <endDate>2026-02-01</endDate>
      <pathFilter>\MyLibrary*</pathFilter>
    </GetOwnershipChangeLog>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- **pathFilter also sets permission scope**: providing a valid library name in the path is not just a filter — it also reduces the required permission to library-level `ViewAuditLogs`. Omitting the path queries all libraries and requires system-wide admin rights.
- **pathFilter wildcards**: use `*` as a trailing wildcard. `\MyLibrary\Reports*` matches all objects under that folder. An exact path is used when no `*` is present.
- **USERID vs AFTER_PLAYERID**: `USERID`/`FULLNAME` identify the person who *performed* the ownership change (e.g. an administrator). `AFTER_PLAYERID`/`AFTER_PLAYERNAME` identify the *new owner* assigned to the object.
- **UTC input**: `startDate` and `endDate` may be submitted as UTC values; the server converts them to local time before filtering.
- **DATE format**: the `DATE` attribute in the response is server local time, not UTC.

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

- [GetDeleteLog](GetDeleteLog.md) - Get deletion log entries
- [GetNewDocumentsAndFoldersLog](GetNewDocumentsAndFoldersLog.md) - Get creation log entries for new documents and folders
- [GetDispositionLog](GetDispositionLog.md) - Get disposition log entries
- [GetClassificationLogs](GetClassificationLogs.md) - Get classification log entries for a specific path
