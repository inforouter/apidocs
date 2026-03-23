# GetCheckoutLog API

Returns the checkout log for documents matching the specified date range and path filter.

## Endpoint

```
/srv.asmx/GetCheckoutLog
```

## Methods

- **GET** `/srv.asmx/GetCheckoutLog?AuthenticationTicket=...&StartDate=...&EndDate=...&PathFilter=...`
- **POST** `/srv.asmx/GetCheckoutLog` (form data)
- **SOAP** Action: `http://tempuri.org/GetCheckoutLog`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `StartDate` | DateTime | No | Start date for the log query range |
| `EndDate` | DateTime | No | End date for the log query range |
| `PathFilter` | string | No | Path filter to restrict results to a specific library or folder path (e.g. `\MyLibrary` or `\MyLibrary\Reports*`). Also determines the required privilege level — see **Required Permissions** below. |

## Response Structure

### Success Response

```xml
<response success="true">
  <logs>
    <log TYPE="DOCUMENT" ID="1234" NAME="Report.docx" DATE="2026-02-01 14:30:00" DOMAINID="1" PATH="\MyLibrary\Reports" USERID="5" FULLNAME="John Smith" />
    <log TYPE="DOCUMENT" ID="1235" NAME="Invoice.pdf" DATE="2026-01-28 09:15:00" DOMAINID="1" PATH="\MyLibrary\Finance" USERID="8" FULLNAME="Jane Doe" />
  </logs>
</response>
```

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

## Log Entry Attributes

Each `<log>` element contains:

| Attribute | Type | Description |
|-----------|------|-------------|
| `TYPE` | string | Object type (typically `DOCUMENT`) |
| `ID` | integer | Document identifier |
| `NAME` | string | Name of the checked out document |
| `DATE` | DateTime | Date and time of the checkout action |
| `DOMAINID` | integer | Domain/library identifier |
| `PATH` | string | Parent path of the document |
| `USERID` | integer | User identifier who performed the checkout |
| `FULLNAME` | string | Full name of the user who performed the checkout |

## Required Permissions

- User must be authenticated (valid authentication ticket required)
- The required privilege depends on the value of `PathFilter`:

| `PathFilter` value | Required permission |
|--------------------|---------------------|
| Empty / omitted | System-wide `ViewAuditLogs` admin permission |
| Domain name only (e.g. `\MyLibrary`) | `ViewAuditLogs` permission on that specific library/domain |
| Full path (e.g. `\MyLibrary\Reports*`) | `ViewAuditLogs` permission on the library/domain that contains the path |

When `PathFilter` includes a domain name or path, the system resolves the domain from the first path segment and performs the access check against that domain only. Callers who are library-level audit log administrators can therefore scope queries to their own library without needing system-wide admin rights.

## Example Requests

### Request (GET)

```
GET /srv.asmx/GetCheckoutLog?AuthenticationTicket=abc123-def456&StartDate=2026-01-01&EndDate=2026-02-01&PathFilter=\MyLibrary* HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/GetCheckoutLog HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=abc123-def456&StartDate=2026-01-01&EndDate=2026-02-01&PathFilter=\MyLibrary*
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetCheckoutLog"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetCheckoutLog xmlns="http://tempuri.org/">
      <AuthenticationTicket>abc123-def456</AuthenticationTicket>
      <StartDate>2026-01-01</StartDate>
      <EndDate>2026-02-01</EndDate>
      <PathFilter>\MyLibrary*</PathFilter>
    </GetCheckoutLog>
  </soap:Body>
</soap:Envelope>
```

## Notes

- Results are ordered by action date descending (most recent first).
- The `PathFilter` parameter supports wildcard matching using `*` (e.g., `\MyLibrary\Reports*`).
- When `PathFilter` is just a domain/library name (e.g. `\MyLibrary`), all checkouts within that domain are returned and the path portion of the filter is cleared internally.
- When `PathFilter` contains a sub-path (e.g. `\MyLibrary\Reports*`), the domain is derived from the first path segment and the remainder is used as the path filter.
- Omitting `PathFilter` returns system-wide results, but requires system-wide `ViewAuditLogs` admin permission.
- If `StartDate` and `EndDate` are omitted, all available log entries are returned.
- UTC dates are automatically converted to local server time.
- Checkout logging must be enabled in the domain policies for entries to be recorded.

## Error Codes

Common error responses:

| Error | Description |
|-------|-------------|
| `[901]Session expired or Invalid ticket` | Invalid or expired authentication ticket |
| Access denied | Caller lacks the required `ViewAuditLogs` permission — system-wide when `PathFilter` is omitted, or domain-level for the resolved library when `PathFilter` is supplied |

## Related APIs

- `GetCheckinLog` - Get checkin log entries
- `GetDeleteLog` - Get deletion log entries
- `GetNewDocumentsAndFoldersLog` - Get creation log entries for new documents and folders

## Version History

- **New**: Added to provide programmatic access to checkout log previously only available through the Control Panel UI
