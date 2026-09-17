# GetAccessList API

Returns the current access list (security settings) for a document or folder at the specified path.

## Endpoint

```
/srv.asmx/GetAccessList
```

## Methods

- **GET** `/srv.asmx/GetAccessList?authenticationTicket=...&Path=...`
- **POST** `/srv.asmx/GetAccessList` (form data)
- **SOAP** Action: `http://tempuri.org/GetAccessList`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full path to the document or folder. |

---

## Response

### Success Response

```xml
<response success="true">
  <AccessList DateApplied="2024-06-15T10:30:00" AppliedBy="admin" InheritedSecurity="false">
    <Anonymous Right="0" Description="No Access" />
    <DomainMembers Right="2" Description="Read" />
    <UserGroup DomainName="Finance" GroupName="Managers" Right="6" Description="Full Control" />
    <UserGroup DomainName="" GroupName="AllStaff" Right="4" Description="Add &amp; Read" />
    <User DomainName="Finance" UserName="jsmith" Right="5" Description="Change" />
  </AccessList>
</response>
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

### Access List Element Attributes

| Attribute | Description |
|-----------|-------------|
| `DateApplied` | The date and time when this access list was last applied. |
| `AppliedBy` | The username of the person who last modified the access list. |
| `InheritedSecurity` | `true` if the item inherits security from its parent; `false` if it has a custom access list. |

### Access List Child Elements

| Element | Attributes | Description |
|---------|-----------|-------------|
| `Anonymous` | `Right`, `Description` | Access granted to anonymous (unauthenticated) users. |
| `DomainMembers` | `Right`, `Description` | Access granted to all authenticated domain members. |
| `UserGroup` | `DomainName`, `GroupName`, `Right`, `Description` | Access granted to a specific user group. |
| `User` | `DomainName`, `UserName`, `Right`, `Description` | Access granted to a specific user. |

### Right Values

| Right | Description |
|-------|-------------|
| `0` | No Access |
| `1` | List |
| `2` | Read |
| `3` | Add |
| `4` | Add & Read |
| `5` | Change |
| `6` | Full Control |

---

## Required Permissions

**Read security access list permission** (ActionId 26) on the target document or folder.

---

## Example

### GET Request

```
GET /srv.asmx/GetAccessList
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports/Q4Report.pdf
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetAccessList HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance/Reports/Q4Report.pdf
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetAccessList>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:Path>/Finance/Reports/Q4Report.pdf</tns:Path>
    </tns:GetAccessList>
  </soap:Body>
</soap:Envelope>
```

---

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

Reports who may do what with a folder or a document.

```javascript
const root = await call('GetAccessList', {
  authenticationTicket: ticket,
  Path: '/Finance/Reports'
});

const list = root.querySelector('AccessList');

if (list.getAttribute('InheritedSecurity') === 'true') {
  // the item has no list of its own; this one comes from the folder above
}

for (const entry of list.querySelectorAll('User, UserGroup, Anonymous, DomainMembers')) {
  console.log(entry.tagName,
              entry.getAttribute('UserName') ?? entry.getAttribute('GroupName') ?? '',
              entry.getAttribute('Right'),
              entry.getAttribute('Description'));
}
```

An access list is one `<AccessList>` element carrying the entries as children, and three attributes
about the list itself: `InheritedSecurity` (`true` while the item has no list of its own),
`DateApplied` and `AppliedBy`. A folder that has never been given a list inherits one and says so,
with `DateApplied` empty.

Each entry carries a `Right` and a `Description` - the number and the name of the same thing, the name
in the caller's language. The four kinds of entry are `<Anonymous>`, `<DomainMembers>`, `<UserGroup>`
and `<User>`.

It answers the current list only. Use [GetAccessListHistory](GetAccessListHistory.md) for the ones
before it.

An access list names people, so this is refused to a caller with no ticket even where the item itself
may be read anonymously.

## Notes

- Returns the **current** access list only (no history). To also retrieve historical access list entries, use `GetAccessListHistory`.
- If `InheritedSecurity="true"`, the item does not have a custom access list and inherits from its parent folder.
- Global user groups have an empty `DomainName` attribute.
- To modify the access list, use `SetAccessList`.
- To revert to inherited security, use `ApplyInheritedAccessList`.

---

## Related APIs

- [GetAccessListHistory](GetAccessListHistory.md) - Get the current access list plus historical changes
- [SetAccessList](SetAccessList.md) - Set the access list for a document or folder
- [ApplyInheritedAccessList](ApplyInheritedAccessList.md) - Revert to inherited security
- [GetOwner](GetOwner.md) - Get the owner of a document or folder

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | nothing at that path - including one the caller may not see |
| `4030` | the caller may not read this item's access list |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Path not found | The specified document or folder does not exist. |
| Access denied | The calling user lacks permission to read the security access list. |
| `SystemError:...` | An unexpected server-side error occurred. |

---