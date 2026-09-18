# RemoveUserGroupFromDomainMembership API

Removes the specified user group from the specified domain/library member list.

## Endpoint

```
/srv.asmx/RemoveUserGroupFromDomainMembership
```

## Methods

- **GET** `/srv.asmx/RemoveUserGroupFromDomainMembership?authenticationTicket=...&DomainName=...&GroupName=...`
- **POST** `/srv.asmx/RemoveUserGroupFromDomainMembership` (form data)
- **SOAP** Action: `http://tempuri.org/RemoveUserGroupFromDomainMembership`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DomainName` | string | Yes | The name of the domain/library to remove the group from. |
| `GroupName` | string | Yes | The name of the user group to remove from the domain. |

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

**Domain manager or system administrator.** The calling user must be a manager of the target domain or a system administrator.

---

## Example

### GET Request

```
GET /srv.asmx/RemoveUserGroupFromDomainMembership
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DomainName=Finance
  &GroupName=AllStaff
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/RemoveUserGroupFromDomainMembership HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&DomainName=Finance
&GroupName=AllStaff
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:RemoveUserGroupFromDomainMembership>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:DomainName>Finance</tns:DomainName>
      <tns:GroupName>AllStaff</tns:GroupName>
    </tns:RemoveUserGroupFromDomainMembership>
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

Takes a **global** group out of a library's membership.

```javascript
await call('RemoveUserGroupFromDomainMembership', {
  authenticationTicket: ticket, DomainName: 'Finance', GroupName: 'AllStaff'
});
```

> **Either kind of group.** The library's own groups are searched first and then the global
> groups, so a group belonging to the library can be removed from its membership as well as a
> global one that was added to it.

## Notes

- Removes the group's **membership** in the domain. The group itself is not deleted.
- Users who had access to the domain only through this group will lose their access.
- To add a group back, use `AddUserGroupAsDomainMember`.

---

## Related APIs

- [AddUserGroupAsDomainMember](AddUserGroupAsDomainMember.md) - Add a user group to a domain
- [GetDomainMembers](GetDomainMembers.md) - List all member groups and users of a domain
- [DeleteUsergroup](DeleteUsergroup.md) - Permanently delete a user group

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4030` | the caller may not manage groups - including a caller with no ticket at all |
| `4041` | no library by that name, or the group is not a global group |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
