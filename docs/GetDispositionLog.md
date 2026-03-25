# GetDispositionLog API

Returns the disposition log for documents, folders, and libraries matching the specified date range and path filter. Each entry represents a retention and disposition action performed on an object.

## Endpoint

```
/srv.asmx/GetDispositionLog
```

## Methods

- **GET** `/srv.asmx/GetDispositionLog?authenticationTicket=...&startDate=...&endDate=...&pathFilter=...`
- **POST** `/srv.asmx/GetDispositionLog` (form data)
- **SOAP** Action: `http://tempuri.org/GetDispositionLog`

## Parameters

All filter parameters are optional. When all filters are omitted, all disposition log entries in the system are returned (requires system-wide permission — see [Required Permissions](#required-permissions)).

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `startDate` | DateTime | No | Return entries with an action date on or after this value. Format: `yyyy-MM-dd` or `yyyy-MM-ddTHH:mm:ss`. UTC values are converted to server local time. Leave empty for no lower bound. |
| `endDate` | DateTime | No | Return entries with an action date on or before this value. Date-only values are automatically extended to `23:59:59`. UTC values are converted to server local time. Leave empty for no upper bound. |
| `pathFilter` | string | No | Path filter scoping the query. Also controls the required permission level — see [Required Permissions](#required-permissions). Supports wildcard `*` at the end (e.g. `\MyLibrary\*`). Leave empty to query all libraries. |

---

## Required Permissions

The required permission level depends on the `pathFilter` value:

| `pathFilter` value | Required permission |
|--------------------|---------------------|
| Empty or omitted | System-wide **ViewAuditLogs** admin permission |
| Unresolvable path (library name not found) | System-wide **ViewAuditLogs** admin permission |
| Starts with a valid library name (e.g. `\MyLibrary` or `\MyLibrary\Policies*`) | **ViewAuditLogs** permission for that library only |

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
      NAME="Policy_2024.docx"
      PATH="\MyLibrary\Policies"
      DATE="2026-02-01 14:30:00"
      ID="1234"
      DOMAINID="1"
      DOMAINNAME="MyLibrary"
      COMMENTS="Retention period expired. Document disposed per schedule."
      USERID="5"
      FULLNAME="John Smith" />
    <LOGITEM
      TYPE="DOCUMENT"
      NAME="Contract_Old.pdf"
      PATH="\MyLibrary\Contracts"
      DATE="2026-01-15 10:00:00"
      ID="1235"
      DOMAINID="1"
      DOMAINNAME="MyLibrary"
      COMMENTS="Manual disposition approved by records manager."
      USERID="8"
      FULLNAME="Jane Doe" />
  </logs>
</response>
```

### LOGITEM Attribute Reference

| Attribute | Type | Description |
|-----------|------|-------------|
| `TYPE` | string | Object type: `DOCUMENT`, `FOLDER`, or `DOMAIN`. |
| `NAME` | string | Name of the disposed object. |
| `PATH` | string | Full infoRouter path of the object at the time of the action. |
| `DATE` | string | Date and time the action was performed (server local time, `yyyy-MM-dd HH:mm:ss`). |
| `ID` | int | Internal ID of the object. |
| `DOMAINID` | int | Internal ID of the library the object belonged to. |
| `DOMAINNAME` | string | Name of the library (first path segment). |
| `COMMENTS` | string | Disposition reason or notes recorded at the time of the action. |
| `USERID` | int | Internal user ID of the person who performed the action. |
| `FULLNAME` | string | Full name of the person who performed the action. |

### Empty Result

```xml
<response success="true" error="">
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
GET /srv.asmx/GetDispositionLog?authenticationTicket=abc123-def456&startDate=2026-01-01&endDate=2026-02-01 HTTP/1.1
Host: server.example.com
```

### GET — scoped to a library

```
GET /srv.asmx/GetDispositionLog?authenticationTicket=abc123-def456&startDate=2026-01-01&endDate=2026-02-01&pathFilter=\MyLibrary* HTTP/1.1
Host: server.example.com
```

### POST

```
POST /srv.asmx/GetDispositionLog HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&startDate=2026-01-01&endDate=2026-02-01&pathFilter=\MyLibrary*
```

### SOAP 1.1

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetDispositionLog"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetDispositionLog xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
      <startDate>2026-01-01</startDate>
      <endDate>2026-02-01</endDate>
      <pathFilter>\MyLibrary*</pathFilter>
    </GetDispositionLog>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- **pathFilter also sets permission scope**: providing a valid library name in the path is not just a filter — it also reduces the required permission to library-level `ViewAuditLogs`. Omitting the path queries all libraries and requires system-wide admin rights.
- **pathFilter wildcards**: use `*` as a trailing wildcard. `\MyLibrary\*` matches all items under MyLibrary. An exact path is used when no `*` is present.
- **UTC input**: `startDate` and `endDate` may be submitted as UTC values; the server converts them to local time before filtering.
- **DATE format**: the `DATE` attribute in the response is server local time in `yyyy-MM-dd HH:mm:ss` format, not UTC.
- **COMMENTS**: contains the disposition reason or notes recorded at the time of the action. May be empty if no comments were provided.

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
- [GetCheckInLog](GetCheckInLog.md) - Get check-in log entries
- [GetNewDocumentsAndFoldersLog](GetNewDocumentsAndFoldersLog.md) - Get creation log entries for new documents and folders
- [GetRetentionSourceAuthorities](GetRetentionSourceAuthorities.md) - List all retention source authorities
