# GetSecurityChangeLog API

Returns the security change log for a library, folder, or document. This API merges the functionality of the library-wide security audit log and the object-specific security history into a single endpoint.

From 9.0 the security history is always kept; it is no longer a library policy. It is kept as one entry per operation, on the item the change was made on, plus one entry for each item whose own list or parent that operation changed. An item that merely inherits a change has no entry of its own for it: its history is read from its own entries with the history of the folders it was following spliced in. So a document that has never been given a list of its own still answers with every change of the folders it has been under, each marked `isInherited="true"`, and a list applied to a tree of fifty thousand items is one entry, not fifty thousand.

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

- **Library path** (e.g. `/corporate/`): Returns the security changes made in the library, one `<change>` per operation. A list set on a folder and applied to its tree is one entry: `objectType`, `objectId`, `objectName` and `objectPath` name the folder it was set on and `itemCount` says how many folders and documents it reached. A folder move, restore or copy that gave the folder's contents a list is one entry on that folder, counting what came along; a move or restore is made by the system account, a copy by the user copying. The list a library's root starts with is its first entry. Until 9.0 every item reached was an entry of its own, so one change on a large tree filled the whole result or went over its limit.
- **Folder path** (e.g. `/corporate/accounting/`): Returns the folder's own history - what its list was, and every change that reached it from a folder above - together with every change made on an item under it, one entry per operation with `itemCount`. `objectType`, `objectId`, `objectName` and `objectPath` name the item each entry was made on. Until 9.0 a folder answered its own history alone.
- **Document path** (e.g. `/corporate/accounting/report.docx`): Returns the document's history: the lists it was given, and the changes of the folders it was following while it had no list of its own, each as an entry on the document with `isInherited="true"`.

## Response Structure

### Success Response

```xml
<response success="true">
  <securitychanges>
    <change objectType="DOCUMENT" objectId="123" objectName="report.docx" objectPath="\corporate\accounting"
            appliedById="5" appliedByName="John Smith" dateApplied="2026-02-01T14:30:00.000Z" itemCount="1"
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
            appliedById="5" appliedByName="John Smith" dateApplied="2026-01-15T09:00:00.000Z" itemCount="38"
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
| `objectType` | string | Object type: `DOCUMENT` or `FOLDER`. For a library query, the item the change was made on |
| `objectId` | integer | Object identifier |
| `objectName` | string | Name of the document or folder |
| `objectPath` | string | Parent path of the object |
| `appliedById` | integer | User ID of who applied the security change |
| `appliedByName` | string | Full name of who applied the security change |
| `dateApplied` | DateTime | Date and time the security change was applied, ISO 8601 in UTC (`yyyy-MM-ddTHH:mm:ss.fffZ`). Until 9.0 it was the server's local time in the server's own culture, e.g. `16.10.2026 09:12:00` on a Turkish server. |
| `itemCount` | integer | How many folders and documents the change reached, counting the one it was made on. `1` for an entry recorded before 9.0, which stands for one item. New in 9.0. |
| `isInherited` | boolean | Whether the item took its parent's list by this change (`true`), or was given a list of its own (`false`). On an entry a document or folder has because it was following a folder, always `true`. For an entry recorded before 9.0, whether the item inherits now. |
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

- **Library-level queries** (the path is a library's root): an administrator, a member of `[Audit Managers]`, or a manager of that library. Up to 8.7 library managers were refused here, though allowed on the library's subfolders.
- **Document/Folder queries**: the `ReadSecurityAccessList` right on the object; otherwise an administrator, a member of `[Audit Managers]`, or a manager of the object's library. The right on a folder covers the changes made under it.

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

- Results are ordered by date applied, newest first, for every scope. Until 9.0 a library-level query answered oldest first.
- A library-level or folder-level query answers at most 10,000 changes. The limit is fixed, not a setting. Above it the call fails with `4000` and a message asking to narrow the query. Until 9.0 the limit counted the items reached rather than the changes, so one list applied to a tree of more than 10,000 items could not be read at all, and a smaller one was expanded item by item.
- UTC dates are automatically converted to local server time.
- From 9.0 the security history is always recorded. The `SecurityChange` policy's `LogAction` ([SetDomainPolicies](SetDomainPolicies.md)) has no effect on it any more. Until 9.0 nothing was recorded where that policy was off.
- An item's entries name the folder it was under when each change was made. A document or folder that inherits follows the folder it is under: the changes of the folder it was moved out of up to the move, and of the one it was moved into from then on, which is an entry of its own by the system account.
- Both document and folder security changes are included in library-level and folder-level queries.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4000` | `path` was left empty - it is required despite being declared optional |
| `4030` | the caller may not read the security change log (see Required Permissions) |


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
- **9.0**: A library query answers one `<change>` per operation, with `itemCount`, rather than one per item reached; the limit counts changes
