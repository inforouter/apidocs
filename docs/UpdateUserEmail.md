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

Changes one user's email address.

```javascript
await call('UpdateUserEmail', {
  authenticationTicket: ticket,
  UserName: 'jsmith',
  NewEmailAddress: 'jane.smith@example.com',
});
```

The address is stored as given and is **not** checked - `notanemail` is accepted and read back by
[GetUser](GetUser.md). Validate it before sending.

## Notes

- If `NewEmailAddress` is the same as the current email, the call is a no-op and returns success.
- The email address is used for notifications, workflow alerts, and password reset emails.
- Use `UpdateUserProfile` to update name and username.

---

## Related APIs

- [GetUser](GetUser.md) - Get the current email address and other user properties
- [UpdateUserProfile](UpdateUserProfile.md) - Update the user's name, username, and authentication source
- [UpdateUserPreferences](UpdateUserPreferences.md) - Update notification and display preferences

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4030` | there is no ticket at all |
| `4010` | the ticket is expired or unknown |
| `4041` | no user by that name |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

---
