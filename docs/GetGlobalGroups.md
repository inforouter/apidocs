# GetGlobalGroups API

Returns a list of all infoRouter global user groups, sorted alphabetically by group name.

## Endpoint

```
/srv.asmx/GetGlobalGroups
```

## Methods

- **GET** `/srv.asmx/GetGlobalGroups?authenticationTicket=...`
- **POST** `/srv.asmx/GetGlobalGroups` (form data)
- **SOAP** Action: `http://tempuri.org/GetGlobalGroups`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |

---

## Response

### Success Response

Returns a `<usergroups>` collection with one `<usergroup>` element per global group, sorted alphabetically by group name.

```xml
<response success="true" error="">
  <usergroups>
    <usergroup GroupID="10"
               GroupName="AllStaff"
               DomainID="0"
               DomainName=""
               public="True" />
    <usergroup GroupID="11"
               GroupName="Managers"
               DomainID="0"
               DomainName=""
               public="False" />
  </usergroups>
</response>
```

### Error Response

```xml
<response success="false" error="Error message" errorCode="4000" />
```

---

## Usergroup Element Attributes

| Attribute | Description |
|-----------|-------------|
| `GroupID` | Unique numeric ID of the user group. |
| `GroupName` | Name of the user group. |
| `DomainID` | Always `0` for global groups (not tied to a domain). |
| `DomainName` | Always empty for global groups. |
| `public` | `True` if group membership is visible to all users; `False` if membership is private. |

---

## Required Permissions

Any **authenticated user** can call this API. Anonymous users are rejected.

---

## Example

### GET Request

```
GET /srv.asmx/GetGlobalGroups
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetGlobalGroups HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetGlobalGroups>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
    </tns:GetGlobalGroups>
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

Lists the global groups: the ones created with an empty `DomainName`, and the built-in roles, whose
names are in square brackets.

```javascript
const root = await call('GetGlobalGroups', { authenticationTicket: ticket });

for (const group of root.querySelectorAll('usergroups > usergroup')) {
  const name = group.getAttribute('GroupName');
  const builtIn = name.startsWith('[');   // [Administrators], [User Managers], ...
  console.log(name, builtIn ? '(built in)' : '');
}
```

A global group answers `DomainID="0"` and `DomainName="*"`.

## Notes

- Global groups are not tied to a specific domain/library and can be added as members of any domain.
- To get only local groups for a specific domain, use `GetLocalGroups`.
- To get all groups (local and global) for a domain, use `GetDomainGroups`.

---

## Related APIs

- [GetLocalGroups](GetLocalGroups.md) - Get local user groups of a domain/library
- [GetDomainGroups](GetDomainGroups.md) - Get all groups (local and global) for a domain
- [GetUserGroup](GetUserGroup.md) - Get properties of a specific user group

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
