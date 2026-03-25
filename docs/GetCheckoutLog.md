# GetCheckoutLog API

Returns the checkout log for documents matching the specified date range and path filter.

## Endpoint

```
/srv.asmx/GetCheckoutLog
```

## Methods

- **GET** `/srv.asmx/GetCheckoutLog?authenticationTicket=...&startDate=...&endDate=...&pathFilter=...`
- **POST** `/srv.asmx/GetCheckoutLog` (form data)
- **SOAP** Action: `http://tempuri.org/GetCheckoutLog`

## Parameters

All filter parameters are optional. When all filters are omitted, all checkout log entries in the system are returned (requires system-wide permission — see [Required Permissions](#required-permissions)).

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

Returns a `<response>` element with `success="true"` containing a `<logs>` element with zero or more `<log>` child elements. Results are ordered by action date **descending** (most recent first).

```xml
<response success="true">
  <logs>
    <log TYPE="DOCUMENT" ID="1234" NAME="Report.docx" DATE="2026-02-01 14:30:00"
         DOMAINID="1" DOMAINNAME="MyLibrary" PATH="\MyLibrary\Reports"
         USERID="5" FULLNAME="John Smith" />
    <log TYPE="DOCUMENT" ID="1235" NAME="Invoice.pdf" DATE="2026-01-28 09:15:00"
         DOMAINID="1" DOMAINNAME="MyLibrary" PATH="\MyLibrary\Finance"
         USERID="8" FULLNAME="Jane Doe" />
  </logs>
</response>
```

### Log Entry Attribute Reference

| Attribute | Type | Description |
|-----------|------|-------------|
| `TYPE` | string | Object type — always `DOCUMENT`. |
| `ID` | int | Document identifier. |
| `NAME` | string | Name of the checked out document. |
| `DATE` | string | Date and time of the checkout action (server local time, `yyyy-MM-dd HH:mm:ss`). |
| `DOMAINID` | int | Internal ID of the library the document belongs to. |
| `DOMAINNAME` | string | Name of the library (first path segment). |
| `PATH` | string | Full parent path of the document. |
| `USERID` | int | Internal user ID of the person who performed the checkout. |
| `FULLNAME` | string | Full name of the person who performed the checkout. |

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
GET /srv.asmx/GetCheckoutLog?authenticationTicket=abc123-def456&startDate=2026-01-01&endDate=2026-02-01 HTTP/1.1
Host: server.example.com
```

### GET — scoped to a library

```
GET /srv.asmx/GetCheckoutLog?authenticationTicket=abc123-def456&startDate=2026-01-01&endDate=2026-02-01&pathFilter=\MyLibrary* HTTP/1.1
Host: server.example.com
```

### POST

```
POST /srv.asmx/GetCheckoutLog HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&startDate=2026-01-01&endDate=2026-02-01&pathFilter=\MyLibrary*
```

### SOAP 1.1

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetCheckoutLog"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetCheckoutLog xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
      <startDate>2026-01-01</startDate>
      <endDate>2026-02-01</endDate>
      <pathFilter>\MyLibrary*</pathFilter>
    </GetCheckoutLog>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- **pathFilter also sets permission scope**: providing a valid library name in the path is not just a filter — it also reduces the required permission to library-level `ViewAuditLogs`. Omitting the path queries all libraries and requires system-wide admin rights.
- **pathFilter wildcards**: use `*` as a trailing wildcard. `\MyLibrary\Reports*` matches all checkouts under that folder. An exact path is used when no `*` is present.
- **Library-only path**: when `pathFilter` is exactly a library name (e.g. `\MyLibrary`), the path filter is cleared internally and all checkout records within that library are returned.
- **UTC input**: `startDate` and `endDate` may be submitted as UTC values; the server converts them to local time before filtering.
- **DATE format**: the `DATE` attribute in the response is server local time, not UTC.
- Checkout logging must be enabled in the domain policies for entries to be recorded.

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
- [GetDeleteLog](GetDeleteLog.md) - Get deletion log entries
- [GetNewDocumentsAndFoldersLog](GetNewDocumentsAndFoldersLog.md) - Get creation log entries for new documents and folders
