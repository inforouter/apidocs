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

Gives one user access to a library.

```javascript
await call('AddUserAsDomainMember', {
  authenticationTicket: ticket,
  DomainName: 'Finance',
  UserName: 'jsmith'
});
```

**Adding somebody who is already a member is `4000`**, not the `4090` a duplicate gets almost
everywhere else in this API. A user name nobody has is `4041`.

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

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4030` | the caller is not a system administrator |
| `4000` | the user is already a member |
| `4041` | no user by that name |
| `4041` | no library by that name - including one the caller cannot see |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `[115] Domain not found` | The specified DomainName does not exist. |
| User not found | The specified UserName does not exist in the system. |
| Already a member | The user is already a member of the domain. |
| `SystemError:...` | An unexpected server-side error occurred. |

---