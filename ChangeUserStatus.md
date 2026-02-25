# ChangeUserStatus API

Changes the status (enabled/disabled) of the specified infoRouter user account.

## Endpoint

```
/srv.asmx/ChangeUserStatus
```

## Methods

- **GET** `/srv.asmx/ChangeUserStatus?authenticationTicket=...&UserName=...&StatusCode=...`
- **POST** `/srv.asmx/ChangeUserStatus` (form data)
- **SOAP** Action: `http://tempuri.org/ChangeUserStatus`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `UserName` | string | Yes | The username of the account whose status will be changed. |
| `StatusCode` | int | Yes | The new status to apply. Valid values: `0` = disable the account, `1` = enable the account. |

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

**System administrator.** Only system administrators can change user account status.

---

## Example

### GET Request (disable a user)

```
GET /srv.asmx/ChangeUserStatus
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &UserName=jdoe
  &StatusCode=0
HTTP/1.1
```

### GET Request (enable a user)

```
GET /srv.asmx/ChangeUserStatus
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &UserName=jdoe
  &StatusCode=1
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/ChangeUserStatus HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&UserName=jdoe
&StatusCode=0
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:ChangeUserStatus>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:UserName>jdoe</tns:UserName>
      <tns:StatusCode>0</tns:StatusCode>
    </tns:ChangeUserStatus>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- A disabled user cannot log in to infoRouter.
- Disabling a user does not delete the account or remove any of their data, permissions, or memberships.
- Use `StatusCode=1` to re-enable a previously disabled account.

---

## Related APIs

- [GetUser](GetUser) - Get current user properties including enabled/disabled status
- [ChangeUserType](ChangeUserType) - Change the user type (author vs read-only)
- [DeleteUser](DeleteUser) - Permanently delete a user account

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| User not found | The specified username does not exist. |
| Access denied | The calling user is not a system administrator. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/ChangeUserStatus*
