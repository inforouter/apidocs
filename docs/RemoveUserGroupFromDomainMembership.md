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
<response success="false" error="[ErrorCode] Error message" />
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

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `[115] Domain not found` | The specified domain/library does not exist. |
| Group not found | The specified group does not exist. |
| Group not a member | The group is not a member of this domain. |
| Access denied | The calling user is not a manager of this domain. |
| `SystemError:...` | An unexpected server-side error occurred. |

---