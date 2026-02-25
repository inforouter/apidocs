# GetNewDocumentsAndFoldersLog API

Returns the log of newly created documents and folders for the specified date range and path filter.

## Endpoint

```
/srv.asmx/GetNewDocumentsAndFoldersLog
```

## Methods

- **GET** `/srv.asmx/GetNewDocumentsAndFoldersLog?AuthenticationTicket=...&StartDate=...&EndDate=...&PathFilter=...`
- **POST** `/srv.asmx/GetNewDocumentsAndFoldersLog` (form data)
- **SOAP** Action: `http://tempuri.org/GetNewDocumentsAndFoldersLog`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `StartDate` | DateTime | No | Start date for the log query range |
| `EndDate` | DateTime | No | End date for the log query range |
| `PathFilter` | string | No | Path filter with optional wildcard (e.g. `\MyLibrary\Reports*`) |

## Response Structure

### Success Response

```xml
<response success="true">
  <logs>
    <log TYPE="DOCUMENT" ID="1234" NAME="Report.docx" DATE="2026-02-01 14:30:00" DOMAINID="1" PATH="\MyLibrary\Reports" USERID="5" FULLNAME="John Smith" />
    <log TYPE="FOLDER" ID="567" NAME="Archive" DATE="2026-01-28 09:15:00" DOMAINID="1" PATH="\MyLibrary" USERID="5" FULLNAME="John Smith" />
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
| `TYPE` | string | Object type: `DOCUMENT` or `FOLDER` |
| `ID` | integer | Object identifier |
| `NAME` | string | Name of the created document or folder |
| `DATE` | DateTime | Date and time of creation |
| `DOMAINID` | integer | Domain/library identifier |
| `PATH` | string | Parent path of the created object |
| `USERID` | integer | User identifier who created the object |
| `FULLNAME` | string | Full name of the user who created the object |

## Required Permissions

- User must be authenticated (valid authentication ticket required)
- User must have `ViewAuditLogs` admin permission

## Example Requests

### Request (GET)

```
GET /srv.asmx/GetNewDocumentsAndFoldersLog?AuthenticationTicket=abc123-def456&StartDate=2026-01-01&EndDate=2026-02-01&PathFilter=\MyLibrary* HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/GetNewDocumentsAndFoldersLog HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=abc123-def456&StartDate=2026-01-01&EndDate=2026-02-01&PathFilter=\MyLibrary*
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetNewDocumentsAndFoldersLog"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetNewDocumentsAndFoldersLog xmlns="http://tempuri.org/">
      <AuthenticationTicket>abc123-def456</AuthenticationTicket>
      <StartDate>2026-01-01</StartDate>
      <EndDate>2026-02-01</EndDate>
      <PathFilter>\MyLibrary*</PathFilter>
    </GetNewDocumentsAndFoldersLog>
  </soap:Body>
</soap:Envelope>
```

## Notes

- Results are ordered by action date descending (most recent first).
- The `PathFilter` parameter supports wildcard matching using `*` (e.g., `\MyLibrary\Reports*`).
- If `StartDate` and `EndDate` are omitted, all available log entries are returned.
- UTC dates are automatically converted to local server time.
- Creation logging must be enabled in the domain policies for entries to be recorded.

## Error Codes

Common error responses:

| Error | Description |
|-------|-------------|
| `[901]Session expired or Invalid ticket` | Invalid or expired authentication ticket |
| Insufficient permissions | Caller does not have `ViewAuditLogs` admin permission |

## Related APIs

- `GetDeleteLog` - Get deletion log entries
- `GetClassificationLogs` - Get classification log entries for a path

## Version History

- **New**: Added to provide programmatic access to new objects log previously only available through the Control Panel UI
