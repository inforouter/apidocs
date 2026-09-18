# GetLocalGroups API

Returns a list of local user groups defined within the specified domain/library, sorted alphabetically by group name.

## Endpoint

```
/srv.asmx/GetLocalGroups
```

## Methods

- **GET** `/srv.asmx/GetLocalGroups?authenticationTicket=...&DomainName=...`
- **POST** `/srv.asmx/GetLocalGroups` (form data)
- **SOAP** Action: `http://tempuri.org/GetLocalGroups`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DomainName` | string | Yes | The name of the domain/library whose local groups will be returned. |

---

## Response

### Success Response

Returns a `<usergroups>` collection with one `<usergroup>` element per local group, sorted alphabetically by group name.

```xml
<response success="true" error="">
  <usergroups>
    <usergroup GroupID="55"
               GroupName="FinanceAdmins"
               DomainID="123"
               DomainName="Finance"
               public="True" />
    <usergroup GroupID="56"
               GroupName="FinanceReaders"
               DomainID="123"
               DomainName="Finance"
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
| `DomainID` | Numeric ID of the domain this local group belongs to. |
| `DomainName` | Name of the domain this local group belongs to. |
| `public` | `True` if group membership is visible to all users; `False` if membership is private. |

---

## Required Permissions

Any **authenticated user** can call this API. Anonymous users are rejected.

---

## Example

### GET Request

```
GET /srv.asmx/GetLocalGroups
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DomainName=Finance
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetLocalGroups HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&DomainName=Finance
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetLocalGroups>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:DomainName>Finance</tns:DomainName>
    </tns:GetLocalGroups>
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

Lists the groups that belong to a library - the same list
[GetDomainGroups](GetDomainGroups.md) answers, under a second name.

```javascript
const root = await call('GetLocalGroups', {
  authenticationTicket: ticket, DomainName: 'Finance'
});
```

## Notes

- Returns only **local** groups defined specifically for the given domain. Global groups that are members of the domain are not included.
- To get all groups (both local and global) that are members of a domain, use `GetDomainGroups`.
- To get all global groups in the system, use `GetGlobalGroups`.

---

## Related APIs

- [GetDomainGroups](GetDomainGroups.md) - Get all groups (local and global) for a domain
- [GetGlobalGroups](GetGlobalGroups.md) - Get all global user groups in the system
- [GetUserGroup](GetUserGroup.md) - Get properties of a specific user group

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | no library by that name |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
