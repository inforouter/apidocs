# CreateUser API

Creates a new infoRouter user account.

## Endpoint

```
/srv.asmx/CreateUser
```

## Methods

- **GET** `/srv.asmx/CreateUser?authenticationTicket=...&DomainName=...&UserName=...&FirstName=...&LastName=...&EmailAddress=...&Password=...&ReadOnlyUser=...&AuthenticationSource=...`
- **POST** `/srv.asmx/CreateUser` (form data)
- **SOAP** Action: `http://tempuri.org/CreateUser`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DomainName` | string | No | The domain/library to add the user to as a member upon creation. Pass empty or null to create the user without a domain membership. |
| `UserName` | string | Yes | The login name for the new user. Must be unique across the system. |
| `FirstName` | string | Yes | The user's first name. |
| `LastName` | string | Yes | The user's last name. |
| `EmailAddress` | string | No | The user's email address. Used for notifications and password reset. |
| `Password` | string | No | The initial password for native authentication users. Do not specify for users authenticated by external systems (LDAP, OAuth, Windows). |
| `ReadOnlyUser` | bool | Yes | If `true`, the user is created as a read-only user (cannot upload or edit documents). If `false`, the user is an author. |
| `AuthenticationSource` | string | Yes | The authentication source. Use `native` for infoRouter built-in authentication, or specify the name of a configured LDAP, OAuth, or Windows domain authority. |

---

## Response

### Success Response

Returns the new user's numeric ID in the `id` attribute.

```xml
<response success="true" id="123" error="" />
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

---

## Required Permissions

**System administrator.** Only system administrators can create user accounts.

---

## Example

### GET Request (native user)

```
GET /srv.asmx/CreateUser
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DomainName=Finance
  &UserName=jdoe
  &FirstName=John
  &LastName=Doe
  &EmailAddress=john.doe%40example.com
  &Password=InitialP%40ss1
  &ReadOnlyUser=false
  &AuthenticationSource=native
HTTP/1.1
```

### GET Request (external/LDAP user, no password)

```
GET /srv.asmx/CreateUser
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DomainName=
  &UserName=jdoe
  &FirstName=John
  &LastName=Doe
  &EmailAddress=john.doe%40example.com
  &Password=
  &ReadOnlyUser=false
  &AuthenticationSource=LDAP_Authority
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/CreateUser HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&DomainName=Finance
&UserName=jdoe
&FirstName=John
&LastName=Doe
&EmailAddress=john.doe@example.com
&Password=InitialP@ss1
&ReadOnlyUser=false
&AuthenticationSource=native
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:CreateUser>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:DomainName>Finance</tns:DomainName>
      <tns:UserName>jdoe</tns:UserName>
      <tns:FirstName>John</tns:FirstName>
      <tns:LastName>Doe</tns:LastName>
      <tns:EmailAddress>john.doe@example.com</tns:EmailAddress>
      <tns:Password>InitialP@ss1</tns:Password>
      <tns:ReadOnlyUser>false</tns:ReadOnlyUser>
      <tns:AuthenticationSource>native</tns:AuthenticationSource>
    </tns:CreateUser>
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

Creates a user.

```javascript
const root = await call('CreateUser', {
  authenticationTicket: ticket,
  DomainName: 'Finance',          // may be empty: the user is then outside every library
  UserName: 'jsmith',
  FirstName: 'Jane',
  LastName: 'Smith',
  EmailAddress: 'jsmith@example.com',
  Password: 'Passw0rd!x',         // may be empty: nothing insists on one
  ReadOnlyUser: false,
  AuthenticationSource: 'INFOROUTER',
});
```

The new user starts enabled. `GetUser` reports `Enabled="TRUE"` and `ReadOnlyUser` in capitals.

## Notes

- The response includes the new user's numeric `id` attribute, which can be used to reference the user in subsequent API calls.
- Do not provide a `Password` for users authenticated by external systems (LDAP, OAuth, Windows domain). Their password is managed by the external authority.
- If `DomainName` is specified, the user is automatically added as a member of that domain upon creation.
- Use `ChangeUserType` to change a user's type (author/read-only) after creation.
- Use `ChangeUserStatus` to disable or re-enable a user after creation.

---

## Related APIs

- [UserExists](UserExists.md) - Check if a username already exists before creating
- [DeleteUser](DeleteUser.md) - Delete a user account
- [UpdateUserProfile](UpdateUserProfile.md) - Update user profile after creation
- [AddUserAsDomainMember](AddUserAsDomainMember.md) - Add an existing user to a domain/library

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4030` | the caller is not a system administrator |
| `4000` | a user of that name already exists - reported as a bad request rather than 4090 |
| `4000` | `AuthenticationSource` names an authority this instance does not have; the message lists the ones it does |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

`EmailAddress` is stored as given and is **not** checked: `notanemail` is accepted and read
back. Validate it before sending if it matters - the welcome email and every later notice go to
whatever was stored.

---
