# AddManagerToDomain API

Adds an existing infoRouter user as a domain/library manager. The user must already be a member of the domain/library before being designated as a manager.

## Endpoint

```
/srv.asmx/AddManagerToDomain
```

## Methods

- **GET** `/srv.asmx/AddManagerToDomain?authenticationTicket=...&DomainName=...&UserName=...`
- **POST** `/srv.asmx/AddManagerToDomain` (form data)
- **SOAP** Action: `http://tempuri.org/AddManagerToDomain`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DomainName` | string | Yes | Name of the domain/library to add the manager to. |
| `UserName` | string | Yes | Username of the user to be designated as domain manager. The user must already be a member of the domain. |

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

**System administrator only.** Only the system administrator can designate users as domain managers. The target user must already be a member of the domain/library.

---

## Example

### GET Request

```
GET /srv.asmx/AddManagerToDomain
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DomainName=Finance
  &UserName=jdoe
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/AddManagerToDomain HTTP/1.1
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
    <tns:AddManagerToDomain>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:DomainName>Finance</tns:DomainName>
      <tns:UserName>jdoe</tns:UserName>
    </tns:AddManagerToDomain>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- The user must be an existing member of the domain/library before being made a manager. Use `AddUserAsDomainMember` first if the user is not yet a member.
- A domain can have multiple managers.
- Domain managers can manage members, workflows, and other domain settings.
- Use `RemoveManagerFromDomain` to revoke manager status without removing domain membership.
- Use `GetManagers` to retrieve the current list of managers for a domain.

---

## Related APIs

- [RemoveManagerFromDomain](RemoveManagerFromDomain.md) - Remove manager status from a user
- [AddUserAsDomainMember](AddUserAsDomainMember.md) - Add a user as a domain member
- [GetManagers](GetManagers.md) - Get the list of managers for a domain
- [GetDomainMembers](GetDomainMembers.md) - Get all members of a domain

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `[1573] Only the system administrator can perform this operation` | The calling user is not a system administrator. |
| `[115] Domain not found` | The specified DomainName does not exist. |
| User not found | The specified UserName does not exist in the system. |
| User is not a member | The user must be a domain member before being made a manager. |
| `SystemError:...` | An unexpected server-side error occurred. |

---