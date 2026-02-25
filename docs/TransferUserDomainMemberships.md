# TransferUserDomainMemberships API

Transfers domain/library memberships from one user to another. The target user is added as a member of all domains where the source user is currently a member.

## Endpoint

```
/srv.asmx/TransferUserDomainMemberships
```

## Methods

- **GET** `/srv.asmx/TransferUserDomainMemberships?authenticationTicket=...&fromUserName=...&toUserName=...`
- **POST** `/srv.asmx/TransferUserDomainMemberships` (form data)
- **SOAP** Action: `http://tempuri.org/TransferUserDomainMemberships`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `fromUserName` | string | Yes | The username whose domain memberships will be transferred. |
| `toUserName` | string | Yes | The username who will receive the domain memberships. |

---

## Response

### Success Response

```xml
<root success="true" />
```

### Success Response (with warnings)

```xml
<root success="true" warnings="Some memberships could not be transferred." />
```

### Error Response

```xml
<root success="false" error="[ErrorCode] Error message" />
```

---

## Required Permissions

**System administrator.** Only system administrators can transfer user data between accounts.

---

## Example

### GET Request

```
GET /srv.asmx/TransferUserDomainMemberships
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &fromUserName=jdoe
  &toUserName=jsmith
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/TransferUserDomainMemberships HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&fromUserName=jdoe
&toUserName=jsmith
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:TransferUserDomainMemberships>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:FromUserName>jdoe</tns:FromUserName>
      <tns:ToUserName>jsmith</tns:ToUserName>
    </tns:TransferUserDomainMemberships>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- The `toUserName` is added as a member of each domain/library where `fromUserName` is a direct member.
- Domains where `toUserName` is already a member are skipped without error.
- The response root element is `<root>`, not `<response>`.
- Typically used as part of a user offboarding process before deleting the source user.

---

## Related APIs

- [TransferUserGroupMemberships](TransferUserGroupMemberships.md) - Transfer user group memberships
- [TransferUserDomainManagerRoles](TransferUserDomainManagerRoles.md) - Transfer domain manager roles
- [AddUserAsDomainMember](AddUserAsDomainMember.md) - Add a user to a domain manually
- [DeleteUser](DeleteUser.md) - Delete a user after transferring their data

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| User not found | The specified `fromUserName` or `toUserName` does not exist. |
| Access denied | The calling user is not a system administrator. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/TransferUserDomainMemberships*
