# GetVersionCreateLog API

Returns the version creation log for documents matching the specified date range and path filter. Each entry represents a new version being created for a document.

## Endpoint

```
/srv.asmx/GetVersionCreateLog
```

## Methods

- **GET** `/srv.asmx/GetVersionCreateLog?authenticationTicket=...&startDate=...&endDate=...&pathFilter=...`
- **POST** `/srv.asmx/GetVersionCreateLog` (form data)
- **SOAP** Action: `http://tempuri.org/GetVersionCreateLog`

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
    <log TYPE="DOCUMENT" ID="1234" NAME="Report.docx" DATE="2026-02-01 14:30:00" DOMAINID="1" PATH="\MyLibrary\Reports" USERID="5" FULLNAME="John Smith" VERSION="3" />
    <log TYPE="DOCUMENT" ID="1235" NAME="Invoice.pdf" DATE="2026-01-28 09:15:00" DOMAINID="1" PATH="\MyLibrary\Finance" USERID="8" FULLNAME="Jane Doe" VERSION="2" />
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
| `NAME` | string | Name of the document |
| `DATE` | DateTime | Date and time the version was created |
| `DOMAINID` | integer | Domain/library identifier |
| `PATH` | string | Parent path of the document |
| `USERID` | integer | User identifier who created the version |
| `FULLNAME` | string | Full name of the user who created the version |
| `VERSION` | integer | The version number that was created |

## Required Permissions

- User must be authenticated (valid authentication ticket required)
- User must have `ViewAuditLogs` admin permission

## Example Requests

### Request (GET)

```
GET /srv.asmx/GetVersionCreateLog?authenticationTicket=abc123-def456&startDate=2026-01-01&endDate=2026-02-01&pathFilter=\MyLibrary* HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/GetVersionCreateLog HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&startDate=2026-01-01&endDate=2026-02-01&pathFilter=\MyLibrary*
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetVersionCreateLog"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetVersionCreateLog xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
      <startDate>2026-01-01</startDate>
      <endDate>2026-02-01</endDate>
      <pathFilter>\MyLibrary*</pathFilter>
    </GetVersionCreateLog>
  </soap:Body>
</soap:Envelope>
```

## JavaScript

Every call answers XML with HTTP 200, success or not, so `success` is the thing to branch on and
`errorCode` is the number to report.

```javascript
async function call(action, params) {
  const response = await fetch(`/srv.asmx/${action}?${new URLSearchParams(params)}`);
  const root = new DOMParser()
    .parseFromString(await response.text(), 'text/xml')
    .documentElement;

  if (root.getAttribute('success') !== 'true') {
    throw new Error(`${root.getAttribute('errorCode')}: ${root.getAttribute('error')}`);
  }
  return root;
}
```

Reports which versions were added in a date range. Rows come back as `<log>` inside `<logs>`.

The dates are `yyyy-MM-dd`. They bind as `DateTime`, so a value that is not a date is refused with
HTTP 400 before the operation runs - not with this API's error document. An empty one binds to its
default, which leaves the range open at that end, and a range given backwards is accepted and reports
nothing.

```javascript
const root = await call('GetVersionCreateLog', {
  authenticationTicket: ticket,
  startDate: '2026-01-01',
  endDate: '2026-12-31',
  pathFilter: ''            // empty for everywhere, or a path to narrow it
});

for (const row of root.querySelectorAll('logs > log')) {
  console.log(row.getAttribute('DATE'), row.getAttribute('NAME'));
}
```

Leave `pathFilter` empty to search everywhere.

## Notes

- Results are ordered by action date descending (most recent first).
- The `pathFilter` parameter supports wildcard matching using `*` (e.g., `\MyLibrary\Reports*`).
- If `startDate` and `endDate` are omitted, all available log entries are returned.
- UTC dates are automatically converted to local server time.
- Check-in logging must be enabled in the domain policies for version creation entries to be recorded.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4030` | the caller may not read this log - including a caller with no ticket |
| `HTTP 400` | a date parameter that is not a date; refused by model binding, so there is no error document |


Common error responses:

| Error | Description |
|-------|-------------|
| `[901]Session expired or Invalid ticket` | Invalid or expired authentication ticket |
| Insufficient permissions | Caller does not have `ViewAuditLogs` admin permission |

## Related APIs

- `GetVersionDeleteLog` - Get version deletion log entries
- `GetCheckInLog` - Get check-in log entries
- `GetCheckoutLog` - Get checkout log entries
- `GetDeleteLog` - Get deletion log entries
- `GetNewDocumentsAndFoldersLog` - Get creation log entries for new documents and folders

## Version History

- **New**: Added to provide programmatic access to version creation log previously only available through the Control Panel UI
