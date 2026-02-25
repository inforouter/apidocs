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
<response success="false" error="[ErrorCode] Error message" />
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

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Group not found | The specified group does not exist. |
| User not found | The specified username does not exist. |
| User not a member | The user is not a member of this group. |
| Access denied | The calling user lacks permission to manage this group. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/RemoveUsergroupMember*
