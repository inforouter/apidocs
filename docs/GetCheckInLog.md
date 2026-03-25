# GetCheckInLog API

Returns the check-in log for documents matching the specified date range and path filter.

## Endpoint

```
/srv.asmx/GetCheckInLog
```

## Methods

- **GET** `/srv.asmx/GetCheckInLog?authenticationTicket=...&startDate=...&endDate=...&pathFilter=...`
- **POST** `/srv.asmx/GetCheckInLog` (form data)
- **SOAP** Action: `http://tempuri.org/GetCheckInLog`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `startDate` | DateTime | No | Start date for the log query range |
| `endDate` | DateTime | No | End date for the log query range |
| `pathFilter` | string | No | Path filter scoping the query (see [Required Permissions](#required-permissions) for how this affects access control). Supports wildcard `*` at the end (e.g. `\MyLibrary\Reports*`). |

## Response Structure

### Success Response

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
| `TYPE` | string | Object type — always `DOCUMENT` |
| `ID` | integer | Document identifier |
| `NAME` | string | Name of the checked-in document |
| `DATE` | DateTime | Date and time of the check-in action |
| `DOMAINID` | integer | Library/domain identifier |
| `DOMAINNAME` | string | Library name (first path segment of the document path) |
| `PATH` | string | Full parent path of the document |
| `USERID` | integer | Identifier of the user who performed the check-in |
| `FULLNAME` | string | Full name of the user who performed the check-in |

## Required Permissions

The required permission level depends on the `pathFilter` value:

| `pathFilter` value | Required permission |
|--------------------|---------------------|
| Empty or omitted | System-wide **ViewAuditLogs** admin permission |
| Unresolvable path (library name not found) | System-wide **ViewAuditLogs** admin permission |
| Starts with a valid library name (e.g. `\MyLibrary` or `\MyLibrary\Reports*`) | **ViewAuditLogs** permission for that library only |

When a library name is resolved from the path, the query is automatically scoped to that library. Library-level audit log administrators can therefore query their own library without system-wide admin rights.

## Example Requests

### Request (GET) — system-wide query

```
GET /srv.asmx/GetCheckInLog?authenticationTicket=abc123-def456&startDate=2026-01-01&endDate=2026-02-01 HTTP/1.1
Host: server.example.com
```

### Request (GET) — scoped to a library

```
GET /srv.asmx/GetCheckInLog?authenticationTicket=abc123-def456&startDate=2026-01-01&endDate=2026-02-01&pathFilter=\MyLibrary* HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/GetCheckInLog HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&startDate=2026-01-01&endDate=2026-02-01&pathFilter=\MyLibrary*
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetCheckInLog"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetCheckInLog xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
      <startDate>2026-01-01</startDate>
      <endDate>2026-02-01</endDate>
      <pathFilter>\MyLibrary*</pathFilter>
    </GetCheckInLog>
  </soap:Body>
</soap:Envelope>
```

## Notes

- Results are ordered by action date descending (most recent first).
- When `pathFilter` begins with a valid library name, the query is scoped to that library and `DomainId` is set automatically — you do not need to specify the domain separately.
- If `pathFilter` is exactly a library name with no sub-path (e.g. `\MyLibrary`), the path filter is cleared internally and all check-in records within that library are returned.
- If `startDate` and `endDate` are omitted, all available log entries matching the path filter are returned.
- Check-in logging must be enabled in the domain policies for entries to be recorded.

## Error Codes

| Error | Description |
|-------|-------------|
| `[901] Session expired or Invalid ticket` | Invalid or expired authentication ticket |
| Access denied | Caller does not have the required `ViewAuditLogs` permission (see [Required Permissions](#required-permissions)) |
| Folder not found / Document not found | The path or ID specified in the filter does not exist |

## Related APIs

- `GetCheckoutLog` - Get checkout log entries
- `GetDeleteLog` - Get deletion log entries
- `GetNewDocumentsAndFoldersLog` - Get creation log entries for new documents and folders
- `GetVersionCreateLog` - Get version creation log entries

## Version History

- **Updated**: `pathFilter` now controls both query scope and required permission level. `DOMAINNAME` attribute added to each log entry.
- **New**: Added to provide programmatic access to check-in log previously only available through the Control Panel UI
