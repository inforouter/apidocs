# RemoveUsergroupMember API

Removes a member from the specified user group.

## Endpoint

```
/srv.asmx/RemoveUsergroupMember
```

## Methods

- **GET** `/srv.asmx/RemoveUsergroupMember?authenticationTicket=...&DomainName=...&GroupName=...&UserName=...`
- **POST** `/srv.asmx/RemoveUsergroupMember` (form data)
- **SOAP** Action: `http://tempuri.org/RemoveUsergroupMember`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DomainName` | string | No | The domain/library name if the group is a local group. Pass empty or null for global groups. |
| `GroupName` | string | Yes | The name of the user group to remove the user from. |
| `UserName` | string | Yes | The username to remove from the group. |

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

### GET Request (remove from local group)

```
GET /srv.asmx/RemoveUsergroupMember
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DomainName=Finance
  &GroupName=FinanceAdmins
  &UserName=jdoe
HTTP/1.1
```

### GET Request (remove from global group)

```
GET /srv.asmx/RemoveUsergroupMember
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DomainName=
  &GroupName=AllStaff
  &UserName=jdoe
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/RemoveUsergroupMember HTTP/1.1
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
    <tns:RemoveUsergroupMember>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:DomainName>Finance</tns:DomainName>
      <tns:GroupName>FinanceAdmins</tns:GroupName>
      <tns:UserName>jdoe</tns:UserName>
    </tns:RemoveUsergroupMember>
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

Takes a user back out of a group. It is safe to repeat - somebody who is not in it is a success.

```javascript
await call('RemoveUsergroupMember', {
  authenticationTicket: ticket,
  DomainName: 'Finance',
  GroupName: 'Approvers',
  UserName: 'jsmith'
});
```

## Notes

- Pass empty `DomainName` or null for global groups.
- If the user is not a member of the group, an error is returned.

---

## Related APIs

- [AddUsergroupMember](AddUsergroupMember.md) - Add a user to a group
- [GetUserGroupMembers](GetUserGroupMembers.md) - List members of a user group
- [DeleteUsergroup](DeleteUsergroup.md) - Delete an entire user group

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4030` | the caller may not manage groups - including a caller with no ticket at all |
| `4041` | no group by that name in that library, or no user by that name |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
