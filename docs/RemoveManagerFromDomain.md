# RemoveManagerFromDomain API

Removes domain manager status from the specified user in the given domain/library. The user remains a member of the domain but loses manager privileges.

## Endpoint

```
/srv.asmx/RemoveManagerFromDomain
```

## Methods

- **GET** `/srv.asmx/RemoveManagerFromDomain?authenticationTicket=...&DomainName=...&UserName=...`
- **POST** `/srv.asmx/RemoveManagerFromDomain` (form data)
- **SOAP** Action: `http://tempuri.org/RemoveManagerFromDomain`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DomainName` | string | Yes | Name of the domain/library from which to remove the manager. |
| `UserName` | string | Yes | Username of the user whose manager status is to be removed. |

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

**System administrator only.** Only the system administrator can remove manager designations from domain/library managers.

---

## Example

### GET Request

```
GET /srv.asmx/RemoveManagerFromDomain
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DomainName=Finance
  &UserName=jdoe
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/RemoveManagerFromDomain HTTP/1.1
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
    <tns:RemoveManagerFromDomain>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:DomainName>Finance</tns:DomainName>
      <tns:UserName>jdoe</tns:UserName>
    </tns:RemoveManagerFromDomain>
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

Takes a user's manager role away from a library.

```javascript
await call('RemoveManagerFromDomain', {
  authenticationTicket: ticket,
  DomainName: 'Finance',
  UserName: 'jsmith'
});
```

**Removing somebody who is not a manager is a success**, so this is safe to call blindly - unlike
[RemoveUserFromDomainMembership](RemoveUserFromDomainMembership.md), which answers `4041` for a user
it does not know. Removing a manager does not remove their membership.

## Notes

- This operation only removes the manager role -" the user remains a member of the domain.
- To remove the user entirely from the domain, use `RemoveUserFromDomainMembership`.
- Use `GetManagers` to verify the current manager list before and after the operation.
- Use `AddManagerToDomain` to re-designate a user as a manager.

---

## Related APIs

- [AddManagerToDomain](AddManagerToDomain.md) - Designate a user as a domain manager
- [RemoveUserFromDomainMembership](RemoveUserFromDomainMembership.md) - Remove a user from the domain entirely
- [GetManagers](GetManagers.md) - Get the list of managers for a domain

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4030` | the caller is not a system administrator |
| `4041` | no user by that name |
| `4041` | no library by that name - including one the caller cannot see |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `[1573] Only the system administrator can perform this operation` | The calling user is not a system administrator. |
| `[115] Domain not found` | The specified DomainName does not exist. |
| User not found | The specified UserName does not exist in the system. |
| User is not a manager | The specified user is not currently a manager of the domain. |
| `SystemError:...` | An unexpected server-side error occurred. |

---