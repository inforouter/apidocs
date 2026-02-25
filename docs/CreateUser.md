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

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Username already exists | The specified `UserName` conflicts with an existing user. |
| Access denied | The calling user is not a system administrator. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/CreateUser*
