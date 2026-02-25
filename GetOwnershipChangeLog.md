# GetOwnershipChangeLog API

Returns the ownership change log for documents matching the specified date range and path filter. Each entry represents a change in document or folder ownership.

## Endpoint

```
/srv.asmx/GetOwnershipChangeLog
```

## Methods

- **GET** `/srv.asmx/GetOwnershipChangeLog?authenticationTicket=...&startDate=...&endDate=...&pathFilter=...`
- **POST** `/srv.asmx/GetOwnershipChangeLog` (form data)
- **SOAP** Action: `http://tempuri.org/GetOwnershipChangeLog`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `startDate` | DateTime | No | Start date for the log query range |
| `endDate` | DateTime | No | End date for the log query range |
| `pathFilter` | string | No | Path filter with optional wildcard (e.g. `\MyLibrary\Reports*`) |

## Response Structure

### Success Response

```xml
<response success="true">
  <logs>
    <LOGITEM TYPE="DOCUMENT" NAME="Report_2025.docx" PATH="\MyLibrary\Reports" DATE="2026-02-01 14:30:00" ID="1234" DOMAINID="1" USERID="5" FULLNAME="John Smith" COMMENTS="Ownership transferred from Jane Doe to John Smith." />
    <LOGITEM TYPE="FOLDER" NAME="Archive" PATH="\MyLibrary\Archive" DATE="2026-01-15 10:00:00" ID="1235" DOMAINID="1" USERID="8" FULLNAME="Jane Doe" COMMENTS="Ownership reassigned during department restructuring." />
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

Each log element contains:

| Attribute | Type | Description |
|-----------|------|-------------|
| `TYPE` | string | Object type: `DOCUMENT`, `FOLDER`, or `DOMAIN` |
| `ID` | integer | Object identifier |
| `NAME` | string | Name of the object whose ownership changed |
| `DATE` | DateTime | Date and time of the ownership change |
| `DOMAINID` | integer | Domain/library identifier |
| `PATH` | string | Path of the object |
| `USERID` | integer | User identifier of the new owner |
| `FULLNAME` | string | Full name of the new owner |
| `COMMENTS` | string | Comments associated with the ownership change |

## Required Permissions

- User must be authenticated (valid authentication ticket required)
- User must have `ViewAuditLogs` admin permission

## Example Requests

### Request (GET)

```
GET /srv.asmx/GetOwnershipChangeLog?authenticationTicket=abc123-def456&startDate=2026-01-01&endDate=2026-02-01&pathFilter=\MyLibrary* HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/GetOwnershipChangeLog HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&startDate=2026-01-01&endDate=2026-02-01&pathFilter=\MyLibrary*
```

### Request (SOAP 1.1)

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

## Notes

- Results are ordered by action date descending (most recent first).
- The `pathFilter` parameter supports wildcard matching using `*` (e.g., `\MyLibrary\Reports*`).
- If `startDate` and `endDate` are omitted, all available log entries are returned.
- UTC dates are automatically converted to local server time.
- The `COMMENTS` attribute contains details about the ownership transfer.

## Error Codes

Common error responses:

| Error | Description |
|-------|-------------|
| `[901]Session expired or Invalid ticket` | Invalid or expired authentication ticket |
| Insufficient permissions | Caller does not have `ViewAuditLogs` admin permission |

## Related APIs

- `GetDeleteLog` - Get deletion log entries
- `GetNewDocumentsAndFoldersLog` - Get creation log entries for new documents and folders
- `GetDispositionLog` - Get disposition log entries

## Version History

- **New**: Added to provide programmatic access to ownership change log previously only available through the Control Panel UI
