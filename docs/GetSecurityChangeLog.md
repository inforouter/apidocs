# GetSecurityChangeLog API

Returns the security change log for a library, folder, or document. This API merges the functionality of the library-wide security audit log and the object-specific security history into a single endpoint.

## Endpoint

```
/srv.asmx/GetSecurityChangeLog
```

## Methods

- **GET** `/srv.asmx/GetSecurityChangeLog?authenticationTicket=...&path=...&userName=...&startDate=...&endDate=...`
- **POST** `/srv.asmx/GetSecurityChangeLog` (form data)
- **SOAP** Action: `http://tempuri.org/GetSecurityChangeLog`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `path` | string | Yes | Path to a library (e.g. `/corporate/`), folder (e.g. `/corporate/accounting/`), or document (e.g. `/corporate/accounting/report.docx`) |
| `userName` | string | No | Filter by the user who applied the security change (empty for all users) |
| `startDate` | DateTime | No | Start date for the log query range |
| `endDate` | DateTime | No | End date for the log query range |

## Path Parameter Behavior

The `path` parameter determines the scope of the security change log:

- **Library path** (e.g. `/corporate/`): Returns all security changes for documents and folders within the library
- **Folder path** (e.g. `/corporate/accounting/`): Returns security changes for that specific folder
- **Document path** (e.g. `/corporate/accounting/report.docx`): Returns security changes for that specific document

## Response Structure

### Success Response

```xml
<response success="true">
  <securitychanges>
    <change objectType="DOCUMENT" objectId="123" objectName="report.docx" objectPath="\corporate\accounting"
            appliedById="5" appliedByName="John Smith" dateApplied="2026-02-01 14:30:00"
            isInherited="false" allowAnonymous="false">
      <everyone access="2" accessDescription="Read" />
      <usergroups>
        <usergroup groupId="10" groupName="Managers" access="5" accessDescription="Change" />
      </usergroups>
      <users>
        <user userId="20" fullName="Jane Smith" userName="jsmith" access="6" accessDescription="Full Control" />
      </users>
    </change>
    <change objectType="FOLDER" objectId="456" objectName="accounting" objectPath="\corporate\accounting"
            appliedById="5" appliedByName="John Smith" dateApplied="2026-01-15 09:00:00"
            isInherited="false" allowAnonymous="false">
      <everyone access="2" accessDescription="Read" />
      <usergroups>
        <usergroup groupId="10" groupName="Managers" access="6" accessDescription="Full Control" />
      </usergroups>
      <users />
    </change>
  </securitychanges>
</response>
```

### Empty Result

```xml
<response success="true">
  <securitychanges />
</response>
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

## Change Entry Attributes

Each `<change>` element contains:

| Attribute | Type | Description |
|-----------|------|-------------|
| `objectType` | string | Object type: `DOCUMENT` or `FOLDER` |
| `objectId` | integer | Object identifier |
| `objectName` | string | Name of the document or folder |
| `objectPath` | string | Parent path of the object |
| `appliedById` | integer | User ID of who applied the security change |
| `appliedByName` | string | Full name of who applied the security change |
| `dateApplied` | DateTime | Date and time the security change was applied |
| `isInherited` | boolean | Whether security is inherited from parent |
| `allowAnonymous` | boolean | Whether anonymous access is allowed |

### Child Elements

**`<everyone>`** (optional, present when everyone access is set):

| Attribute | Description |
|-----------|-------------|
| `access` | Numeric access level |
| `accessDescription` | Human-readable access description (e.g. "Read", "Change", "Full Control") |

**`<usergroups>` / `<usergroup>`**:

| Attribute | Description |
|-----------|-------------|
| `groupId` | User group identifier |
| `groupName` | User group name |
| `access` | Numeric access level |
| `accessDescription` | Human-readable access description |

**`<users>` / `<user>`**:

| Attribute | Description |
|-----------|-------------|
| `userId` | User identifier |
| `fullName` | User's full name |
| `userName` | User's login name |
| `access` | Numeric access level |
| `accessDescription` | Human-readable access description |

## Access Level Values

### Document Access Levels

| Value | Description |
|-------|-------------|
| 0 | No Access |
| 2 | Read |
| 5 | Change |
| 6 | Full Control |

### Folder Access Levels

| Value | Description |
|-------|-------------|
| 0 | No Access |
| 1 | List |
| 2 | Read |
| 3 | Add |
| 4 | Add + Read |
| 5 | Change |
| 6 | Full Control |

## Required Permissions

- **Library-level queries**: User must have `ViewAuditLogs` admin permission
- **Document/Folder queries**: User must have `ReadSecurityAccessList` permission on the object, or `ViewAuditLogs` admin permission

## Example Requests

### Request (GET) - Library scope

```
GET /srv.asmx/GetSecurityChangeLog?authenticationTicket=abc123-def456&path=/corporate/&startDate=2026-01-01&endDate=2026-02-01 HTTP/1.1
Host: server.example.com
```

### Request (GET) - Document scope with user filter

```
GET /srv.asmx/GetSecurityChangeLog?authenticationTicket=abc123-def456&path=/corporate/accounting/report.docx&userName=jsmith HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/GetSecurityChangeLog HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&path=/corporate/accounting/&startDate=2026-01-01&endDate=2026-02-01&userName=jsmith
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetSecurityChangeLog"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetSecurityChangeLog xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
      <path>/corporate/</path>
      <userName></userName>
      <startDate>2026-01-01</startDate>
      <endDate>2026-02-01</endDate>
    </GetSecurityChangeLog>
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

What has been changed about who may do what.

The dates are `yyyy-MM-dd`. They bind as `DateTime`, so a value that is not a date is refused with
HTTP 400 before the operation runs - not with this API's error document. An empty one binds to its
default, which leaves the range open at that end, and a range given backwards is accepted and reports
nothing.

```javascript
const root = await call('GetSecurityChangeLog', {
  authenticationTicket: ticket,
  path: '/Public/ApiTests',     // required, even though it is declared as optional
  userName: '',                 // empty for anybody
  startDate: '2026-01-01',
  endDate: '2026-12-31'
});
```

**`path` is required in practice.** It is declared as an optional string, so an empty one reaches the
operation rather than being refused by model binding - and the operation then answers `4000`, "Path
parameter is required." `userName` really is optional; leave it empty for anybody.

## Notes

- Results are ordered by date applied.
- For library-level queries, a maximum record count is enforced (configured in system settings). If exceeded, an error is returned asking to narrow the query.
- UTC dates are automatically converted to local server time.
- Security change logging must be enabled in the domain policies for entries to be recorded.
- Both document and folder security changes are included in library-level queries.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4000` | `path` was left empty - it is required despite being declared optional |
| `4030` | the caller may not read the security change log |


Common error responses:

| Error | Description |
|-------|-------------|
| `[901]Session expired or Invalid ticket` | Invalid or expired authentication ticket |
| Insufficient permissions | Caller does not have required permissions |
| Path not found | The specified path does not resolve to a valid library, folder, or document |
| Maximum log count exceeded | Too many records; narrow the date range or path |

## Related APIs

- `GetCheckInLog` - Get check-in log entries
- `GetCheckoutLog` - Get checkout log entries
- `GetOwnershipChangeLog` - Get ownership change log entries
- `GetNewDocumentsAndFoldersLog` - Get creation log entries for new documents and folders

## Version History

- **New**: Added to provide programmatic access to security change history, merging library-wide and object-specific security audit logs
