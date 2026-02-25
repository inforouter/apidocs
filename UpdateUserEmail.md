# UpdateUserEmail API

Updates the email address of the specified infoRouter user.

## Endpoint

```
/srv.asmx/UpdateUserEmail
```

## Methods

- **GET** `/srv.asmx/UpdateUserEmail?authenticationTicket=...&UserName=...&NewEmailAddress=...`
- **POST** `/srv.asmx/UpdateUserEmail` (form data)
- **SOAP** Action: `http://tempuri.org/UpdateUserEmail`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `UserName` | string | Yes | The username of the account whose email address will be updated. |
| `NewEmailAddress` | string | Yes | The new email address. Pass the existing email to keep it unchanged (no-op). |

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

**System administrator** or the **user themselves.** A user can update their own email address; a system administrator can update any user's email.

---

## Example

### GET Request

```
GET /srv.asmx/UpdateUserEmail
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &UserName=jdoe
  &NewEmailAddress=john.doe%40example.com
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/UpdateUserEmail HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&UserName=jdoe
&NewEmailAddress=john.doe@example.com
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:UpdateUserEmail>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:UserName>jdoe</tns:UserName>
      <tns:NewEmailAddress>john.doe@example.com</tns:NewEmailAddress>
    </tns:UpdateUserEmail>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- If `NewEmailAddress` is the same as the current email, the call is a no-op and returns success.
- The email address is used for notifications, workflow alerts, and password reset emails.
- Use `UpdateUserProfile` to update name and username.

---

## Related APIs

- [GetUser](GetUser) - Get the current email address and other user properties
- [UpdateUserProfile](UpdateUserProfile) - Update the user's name, username, and authentication source
- [UpdateUserPreferences](UpdateUserPreferences) - Update notification and display preferences

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| User not found | The specified username does not exist. |
| Access denied | The calling user lacks permission to update this account. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/UpdateUserEmail*
