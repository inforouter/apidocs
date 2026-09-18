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

Enables or disables a user.

```javascript
await call('ChangeUserStatus', { authenticationTicket: ticket, UserName: 'jsmith', StatusCode: 0 }); // disable
await call('ChangeUserStatus', { authenticationTicket: ticket, UserName: 'jsmith', StatusCode: 1 }); // enable
```

`StatusCode` is `0` for disabled and `1` for enabled; anything else is refused with a message
naming the two. The change is visible immediately on `GetUser` as `Enabled="TRUE"` or `"FALSE"`.

## Notes

- A disabled user cannot log in to infoRouter.
- Disabling a user does not delete the account or remove any of their data, permissions, or memberships.
- Use `StatusCode=1` to re-enable a previously disabled account.

---

## Related APIs

- [GetUser](GetUser.md) - Get current user properties including enabled/disabled status
- [ChangeUserType](ChangeUserType.md) - Change the user type (author vs read-only)
- [DeleteUser](DeleteUser.md) - Permanently delete a user account

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4030` | the caller is not a system administrator |
| `4041` | no user by that name |
| `4000` | `StatusCode` is neither 0 nor 1 |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

---
