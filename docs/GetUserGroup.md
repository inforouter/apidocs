# GetUserGroup API

Returns information on the specified infoRouter user group.

## Endpoint

```
/srv.asmx/GetUserGroup
```

## Methods

- **GET** `/srv.asmx/GetUserGroup?authenticationTicket=...&DomainName=...&GroupName=...`
- **POST** `/srv.asmx/GetUserGroup` (form data)
- **SOAP** Action: `http://tempuri.org/GetUserGroup`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DomainName` | string | No | The domain/library name if the group is a local group. Pass empty or null for global groups. |
| `GroupName` | string | Yes | The name of the user group to retrieve. |

---

## Response

### Success Response

Returns a `<usergroup>` element nested inside the `<response>` element.

```xml
<response success="true" error="">
  <usergroup GroupID="55"
             GroupName="FinanceAdmins"
             DomainID="123"
             DomainName="Finance"
             public="True" />
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
| `DomainID` | `0` for global groups; the domain's numeric ID for local groups. |
| `DomainName` | Empty for global groups; the domain name for local groups. |
| `public` | `True` if group membership is visible to all users; `False` if membership is private. |

---

## Required Permissions

Any **authenticated user** can call this API. Anonymous users are rejected.

---

## Example

### GET Request (local group)

```
GET /srv.asmx/GetUserGroup
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DomainName=Finance
  &GroupName=FinanceAdmins
HTTP/1.1
```

### GET Request (global group)

```
GET /srv.asmx/GetUserGroup
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DomainName=
  &GroupName=AllStaff
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetUserGroup HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&DomainName=Finance
&GroupName=FinanceAdmins
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetUserGroup>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:DomainName>Finance</tns:DomainName>
      <tns:GroupName>FinanceAdmins</tns:GroupName>
    </tns:GetUserGroup>
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

Reads one group.

```javascript
const root = await call('GetUserGroup', {
  authenticationTicket: ticket, DomainName: 'Finance', GroupName: 'Approvers'
});

const group = root.querySelector('usergroup');
console.log(group.getAttribute('GroupID'),
            group.getAttribute('DomainName'),   // "*" for a global group
            group.getAttribute('public'));      // the showMembers flag, inverted - see CreateUserGroup1
```

> **`DomainName` cannot be left empty here.** It is declared optional and every other operation in
> the family takes an empty one, but this one answers a bare **HTTP 500** with no error document -
> so there is no code or message to read. To read a global group, list them with
> `GetGlobalGroups` instead.

## Notes

- For global groups, pass an empty string or null for `DomainName`.
- For local groups, specify both the `DomainName` and `GroupName`.
- To get the members of a group, use `GetUserGroupMembers` or `GetUserGroupMembers1`.

---

## Related APIs

- [GetUserGroupMembers](GetUserGroupMembers.md) - Get members of a user group
- [GetDomainGroups](GetDomainGroups.md) - List all groups for a domain
- [GetGlobalGroups](GetGlobalGroups.md) - List all global groups
- [GetLocalGroups](GetLocalGroups.md) - List local groups of a domain

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | no group by that name in that library |
| `HTTP 500` | `DomainName` was empty; a bare Internal Server Error with no error document |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
