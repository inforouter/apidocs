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

Takes one user's access to a library away.

```javascript
await call('RemoveUserFromDomainMembership', {
  authenticationTicket: ticket,
  DomainName: 'Finance',
  Username: 'jsmith'         // note the lower-case n, unlike UserName elsewhere
});
```

Note the spelling of the parameter: `Username`, where its neighbours use `UserName`.

> **A library must keep a member.** Removing the last one is refused with `4000`: a library
> is visible only to its members, so one with nobody in it cannot be reached by anyone, a
> system administrator included, and no operation on it - `DeleteDomain` among them - would
> work again. A member group counts only for the people in it.

There is no guard against it: the operation will remove the last member of a library, and will remove
the caller's own membership, and reports success either way. Check
[GetDomainMembers](GetDomainMembers.md) before removing anybody who might be the last, and never
remove yourself from a library you still need to administer.

A user name nobody has is `4041`.

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

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4030` | the caller is not a system administrator |
| `4041` | no user by that name |
| `4041` | no library by that name - including one the caller cannot see |
| `none` | removing the last member, or the caller's own membership, succeeds and makes the library unreachable |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `[115] Domain not found` | The specified DomainName does not exist. |
| User not found | The specified Username does not exist in the system. |
| User is not a member | The specified user is not a member of this domain. |
| `SystemError:...` | An unexpected server-side error occurred. |

---