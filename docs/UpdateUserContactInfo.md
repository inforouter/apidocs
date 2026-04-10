# UpdateUserContactInfo API

Updates the email address and mobile number of the specified infoRouter user in a single call.

## Endpoint

```
/srv.asmx/UpdateUserContactInfo
```

## Methods

- **GET** `/srv.asmx/UpdateUserContactInfo?authenticationTicket=...&userName=...&emailAddress=...&mobileNumber=...`
- **POST** `/srv.asmx/UpdateUserContactInfo` (form data)
- **SOAP** Action: `http://tempuri.org/UpdateUserContactInfo`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `userName` | string | Yes | The username of the account to update. |
| `emailAddress` | string | Yes | The new email address. Pass the existing value to keep it unchanged. |
| `mobileNumber` | string | Yes | The new mobile number. Pass the existing value to keep it unchanged. |

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

**System administrator** or the **user themselves.** A user can update their own contact info; a system administrator can update any user's contact info.

---

## Example

### GET Request

```
GET /srv.asmx/UpdateUserContactInfo
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &userName=jdoe
  &emailAddress=john.doe%40example.com
  &mobileNumber=%2B15551234567
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/UpdateUserContactInfo HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&userName=jdoe
&emailAddress=john.doe@example.com
&mobileNumber=+15551234567
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:UpdateUserContactInfo>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:userName>jdoe</tns:userName>
      <tns:emailAddress>john.doe@example.com</tns:emailAddress>
      <tns:mobileNumber>+15551234567</tns:mobileNumber>
    </tns:UpdateUserContactInfo>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- To update only email without changing the mobile number, use `UpdateUserEmail` instead.
- The email address is used for notifications, workflow alerts, and password reset emails.
- The mobile number is stored as a plain string; no format validation is enforced server-side.
- Passing an empty string `""` for `emailAddress` or `mobileNumber` clears that field. To keep a field unchanged, pass its current value — retrieve it first with `GetUser` (attributes `Email` and `MobileNumber` on the `<User>` element).
- Via SOAP, passing `null` for `emailAddress` or `mobileNumber` preserves the existing value without clearing it. This null-preservation is not available through the HTTP GET/POST endpoints.

---

## Related APIs

- [GetUser](GetUser.md) - Get the current email, mobile number, and other user properties
- [UpdateUserEmail](UpdateUserEmail.md) - Update email address only
- [UpdateUserProfile](UpdateUserProfile.md) - Update the user's name, username, and authentication source
- [UpdateUserPreferences](UpdateUserPreferences.md) - Update notification and display preferences

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
