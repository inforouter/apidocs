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

Renames a user and sets their first and last name.

```javascript
await call('UpdateUserProfile', {
  authenticationTicket: ticket,
  UserName: 'jsmith',          // who to change
  NewUserName: 'jsmith2',      // send the same name again to change only the rest
  NewFirstName: 'Jane',
  NewLastName: 'Smith-Garcia',
  AuthenticateSource: 'INFOROUTER',
});
```

`NewUserName` is the account name, and changing it takes effect at once: the old name stops
resolving and every later call has to use the new one. Send the existing name to leave it alone.

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

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4030` | there is no ticket at all |
| `4010` | the ticket is expired or unknown |
| `4041` | no user by that name |
| `4090` | `NewUserName` is a name another account already has |
| `4000` | `AuthenticateSource` names an authority this instance does not have |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

---
