# AddUsergroupMember API

Adds the specified user to the member list of the specified user group.

## Endpoint

```
/srv.asmx/AddUsergroupMember
```

## Methods

- **GET** `/srv.asmx/AddUsergroupMember?authenticationTicket=...&DomainName=...&GroupName=...&UserName=...`
- **POST** `/srv.asmx/AddUsergroupMember` (form data)
- **SOAP** Action: `http://tempuri.org/AddUsergroupMember`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DomainName` | string | No | The library name if the group is a local group. Leave it empty for a global group. Until 9.0 it was declared without a question mark on the REST action, so an empty one was refused with HTTP 400 - and nobody could be added to a global group through the API at all. [RemoveUsergroupMember](RemoveUsergroupMember.md) never had the problem. |
| `GroupName` | string | Yes | The name of the user group to add the user to. |
| `UserName` | string | Yes | The username to add to the group. Also accepts the short ID format `ID:userid` (e.g., `ID:123`). |

---

## Response

### Success Response

```xml
<response success="true" error="" />
```

### Error Response

```xml
<response success="false" error="Error message" errorCode="4000" />
```

---

## Required Permissions

**Domain manager or system administrator.** The calling user must be a manager of the domain containing the group, or a system administrator.

---

## Example

### GET Request (add to local group)

```
GET /srv.asmx/AddUsergroupMember
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DomainName=Finance
  &GroupName=FinanceAdmins
  &UserName=jdoe
HTTP/1.1
```

### GET Request (add to global group)

```
GET /srv.asmx/AddUsergroupMember
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DomainName=
  &GroupName=AllStaff
  &UserName=jdoe
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/AddUsergroupMember HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&DomainName=Finance
&GroupName=FinanceAdmins
&UserName=jdoe
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:AddUsergroupMember>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:DomainName>Finance</tns:DomainName>
      <tns:GroupName>FinanceAdmins</tns:GroupName>
      <tns:UserName>jdoe</tns:UserName>
    </tns:AddUsergroupMember>
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

Puts a user in a group. Adding somebody who is already in it is accepted and does not duplicate the
membership.

```javascript
await call('AddUsergroupMember', {
  authenticationTicket: ticket,
  DomainName: 'Finance',
  GroupName: 'Approvers',
  UserName: 'jsmith'
});
```

## Notes

- For global groups, pass an empty string for `DomainName`.
- The `UserName` parameter also accepts a short ID reference in the format `ID:userid` (e.g., `ID:123`).
- If the user is already a member of the group, an error is returned.

---

## Related APIs

- [RemoveUsergroupMember](RemoveUsergroupMember.md) - Remove a user from a group
- [GetUserGroupMembers](GetUserGroupMembers.md) - List members of a user group
- [GetUserGroup](GetUserGroup.md) - Get user group properties

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4030` | the caller may not manage groups - including a caller with no ticket at all |
| `4041` | no group by that name in that library, or no user by that name |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
