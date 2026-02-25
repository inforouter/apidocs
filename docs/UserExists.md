# UserExists API

Determines whether the given user name refers to an existing infoRouter user.

## Endpoint

```
/srv.asmx/UserExists
```

## Methods

- **GET** `/srv.asmx/UserExists?authenticationTicket=...&UserName=...`
- **POST** `/srv.asmx/UserExists` (form data)
- **SOAP** Action: `http://tempuri.org/UserExists`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `UserName` | string | Yes | The username to check for existence. |

---

## Response

### Success Response (user exists)

```xml
<response success="true" error="" />
```

### Error Response (user not found or access denied)

```xml
<response success="false" error="[ErrorCode] Error message" />
```

---

## Required Permissions

Any **authenticated user** can call this API. Anonymous (unauthenticated) users are rejected.

---

## Example

### GET Request

```
GET /srv.asmx/UserExists
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &UserName=jdoe
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/UserExists HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&UserName=jdoe
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:UserExists>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:UserName>jdoe</tns:UserName>
    </tns:UserExists>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Returns `success="true"` if the user exists; returns an error response if the user is not found.
- Anonymous (unauthenticated) callers receive error `[2730]`.
- The check is case-insensitive for the username.

---

## Related APIs

- [GetUser](GetUser.md) - Get full properties of an existing user
- [CreateUser](CreateUser.md) - Create a new user
- [DeleteUser](DeleteUser.md) - Delete an existing user

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `[2730] Insufficient rights. Anonymous users cannot perform this action.` | The calling user is not authenticated. |
| User not found | The specified username does not exist. |
| `SystemError:...` | An unexpected server-side error occurred. |

---