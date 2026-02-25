# UpdateUserProfile API

Updates the profile of the specified infoRouter user, including their name, username, and authentication source.

## Endpoint

```
/srv.asmx/UpdateUserProfile
```

## Methods

- **GET** `/srv.asmx/UpdateUserProfile?authenticationTicket=...&UserName=...&NewUserName=...&NewFirstName=...&NewLastName=...&AuthenticateSource=...`
- **POST** `/srv.asmx/UpdateUserProfile` (form data)
- **SOAP** Action: `http://tempuri.org/UpdateUserProfile`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `UserName` | string | Yes | The current username of the account to update. |
| `NewUserName` | string | Yes | The new username. Pass the same value as `UserName` to keep the current username. |
| `NewFirstName` | string | Yes | The new first name. |
| `NewLastName` | string | Yes | The new last name. |
| `AuthenticateSource` | string | Yes | The authentication source for the user (e.g., `native`, an LDAP/OAuth authority name, or a Windows domain). |

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

**System administrator.** Only system administrators can update user profiles.

---

## Example

### GET Request (rename user)

```
GET /srv.asmx/UpdateUserProfile
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &UserName=jdoe
  &NewUserName=john.doe
  &NewFirstName=John
  &NewLastName=Doe
  &AuthenticateSource=native
HTTP/1.1
```

### GET Request (update name only, keep username)

```
GET /srv.asmx/UpdateUserProfile
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &UserName=jdoe
  &NewUserName=jdoe
  &NewFirstName=Jonathan
  &NewLastName=Doe
  &AuthenticateSource=native
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/UpdateUserProfile HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&UserName=jdoe
&NewUserName=john.doe
&NewFirstName=John
&NewLastName=Doe
&AuthenticateSource=native
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:UpdateUserProfile>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:UserName>jdoe</tns:UserName>
      <tns:NewUserName>john.doe</tns:NewUserName>
      <tns:NewFirstName>John</tns:NewFirstName>
      <tns:NewLastName>Doe</tns:NewLastName>
      <tns:AuthenticateSource>native</tns:AuthenticateSource>
    </tns:UpdateUserProfile>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- To keep the current username, pass the same value in both `UserName` and `NewUserName`.
- If `NewUserName` differs from `UserName`, it must not conflict with an existing username.
- The `AuthenticateSource` determines how the user authenticates: `native` uses infoRouter's built-in password authentication, other values refer to configured LDAP, OAuth, or Windows domain authorities.
- To update the user's email address, use `UpdateUserEmail`.
- To update notification preferences, use `UpdateUserPreferences`.

---

## Related APIs

- [GetUser](GetUser.md) - Get current user profile properties
- [UpdateUserEmail](UpdateUserEmail.md) - Update the user's email address
- [UpdateUserPreferences](UpdateUserPreferences.md) - Update notification and display preferences
- [CreateUser](CreateUser.md) - Create a new user

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| User not found | The specified username does not exist. |
| Username already exists | The specified `NewUserName` conflicts with an existing user. |
| Access denied | The calling user is not a system administrator. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/UpdateUserProfile*
