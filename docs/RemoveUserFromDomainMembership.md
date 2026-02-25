# RemoveUserFromDomainMembership API

Removes the specified user from the member list of the given domain/library. The user loses access to the domain's content after removal.

## Endpoint

```
/srv.asmx/RemoveUserFromDomainMembership
```

## Methods

- **GET** `/srv.asmx/RemoveUserFromDomainMembership?authenticationTicket=...&DomainName=...&Username=...`
- **POST** `/srv.asmx/RemoveUserFromDomainMembership` (form data)
- **SOAP** Action: `http://tempuri.org/RemoveUserFromDomainMembership`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DomainName` | string | Yes | Name of the domain/library from which to remove the user. |
| `Username` | string | Yes | Username of the user to remove from the domain membership. |

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
GET /srv.asmx/RemoveUserFromDomainMembership
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DomainName=Finance
  &Username=jdoe
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/RemoveUserFromDomainMembership HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&DomainName=Finance
&Username=jdoe
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:RemoveUserFromDomainMembership>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:DomainName>Finance</tns:DomainName>
      <tns:Username>jdoe</tns:Username>
    </tns:RemoveUserFromDomainMembership>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- If the user is also a manager of the domain, their manager role is also removed upon membership removal.
- This operation removes individual user membership only -" it does not affect user group memberships. If the user is a member of a group that is also a domain member, they may retain indirect access.
- Use `GetDomainMembers` to verify the member list after removal.

---

## Related APIs

- [AddUserAsDomainMember](AddUserAsDomainMember.md) - Add a user to the domain membership
- [RemoveManagerFromDomain](RemoveManagerFromDomain.md) - Remove manager status only (keep membership)
- [GetDomainMembers](GetDomainMembers.md) - Get all members of the domain
- [GetDomainMembershipsOfUser](GetDomainMembershipsOfUser.md) - Get all domain memberships of a user

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `[115] Domain not found` | The specified DomainName does not exist. |
| User not found | The specified Username does not exist in the system. |
| User is not a member | The specified user is not a member of this domain. |
| `SystemError:...` | An unexpected server-side error occurred. |

---