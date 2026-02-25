# AddUserAsDomainMember API

Adds an existing infoRouter user to the member list of the specified domain/library. Once added as a member, the user gains access to the domain's content according to the domain's permissions configuration.

## Endpoint

```
/srv.asmx/AddUserAsDomainMember
```

## Methods

- **GET** `/srv.asmx/AddUserAsDomainMember?authenticationTicket=...&DomainName=...&UserName=...`
- **POST** `/srv.asmx/AddUserAsDomainMember` (form data)
- **SOAP** Action: `http://tempuri.org/AddUserAsDomainMember`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DomainName` | string | Yes | Name of the domain/library to add the user to. |
| `UserName` | string | Yes | Username of the user to add as a domain member. |

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
GET /srv.asmx/AddUserAsDomainMember
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DomainName=Finance
  &UserName=jdoe
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/AddUserAsDomainMember HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&DomainName=Finance
&UserName=jdoe
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:AddUserAsDomainMember>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:DomainName>Finance</tns:DomainName>
      <tns:UserName>jdoe</tns:UserName>
    </tns:AddUserAsDomainMember>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- If the user is already a member of the domain, an error is returned.
- Adding a user as a member gives them access to the domain according to the domain's ACL configuration.
- To add a user group instead of an individual user, use `AddUserGroupAsDomainMember`.
- Use `RemoveUserFromDomainMembership` to remove a user from the domain.
- Use `GetDomainMembers` to retrieve the current member list.

---

## Related APIs

- [RemoveUserFromDomainMembership](RemoveUserFromDomainMembership.md) - Remove a user from domain membership
- [AddUserGroupAsDomainMember](AddUserGroupAsDomainMember.md) - Add a user group as domain member
- [GetDomainMembers](GetDomainMembers.md) - Get all members of the domain
- [AddManagerToDomain](AddManagerToDomain.md) - Designate a member as a domain manager

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `[115] Domain not found` | The specified DomainName does not exist. |
| User not found | The specified UserName does not exist in the system. |
| Already a member | The user is already a member of the domain. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/AddUserAsDomainMember*
