# ChangeUserPassword API

> **Obsolete.** Use [ChangeUserPassword1](ChangeUserPassword1.md) instead. `ChangeUserPassword` remains functional for backward compatibility - it still sets another user's password - but it refuses your own, and new integrations should use `ChangeUserPassword1`.

Sets another infoRouter user's password; this requires the **User Manager** administrative role. **Your own password is not changed here:** use [ChangeUserPassword1](ChangeUserPassword1.md), which takes your current password.

## Endpoint

```
/srv.asmx/ChangeUserPassword
```

## Methods

- **GET** `/srv.asmx/ChangeUserPassword?AuthenticationTicket=...&UserName=...&NewPassword=...`
- **POST** `/srv.asmx/ChangeUserPassword` (form data)
- **SOAP** Action: `http://tempuri.org/ChangeUserPassword`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `UserName` | string | Yes | The login name of the user whose password is to be changed |
| `NewPassword` | string | Yes | The new password. Must differ from the current password and must satisfy the application's password complexity policy. |

## Response

### Success Response

```xml
<root success="true" />
```

### Error Response

```xml
<root success="false" error="Error message" />
```

## Required Permissions

**An administrator's account** (the `sysadmin` account or a member of `[Administrators]`) can be changed by administrators only; anyone else is refused with `4030`. See [AdministrativeRoles](AdministrativeRoles.md).

- **Another user's password:** The caller must hold the **User Manager** administrative role, or manage a library the user belongs to.
- **Own password:** Refused with `4000`, naming `CHANGEUSERPASSWORD1`. A ticket alone is not enough to change your own password - a stolen ticket would otherwise become a permanent takeover of the account. With Windows authentication on there is no infoRouter password to confirm, and your own password is still accepted here.

## Example

### Request (POST) - an administrator setting another user's password

```
POST /srv.asmx/ChangeUserPassword HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=admin-ticket-guid&UserName=jsmith&NewPassword=NewSecure!99
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/ChangeUserPassword"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <ChangeUserPassword xmlns="http://tempuri.org/">
      <AuthenticationTicket>abc123-def456</AuthenticationTicket>
      <UserName>jsmith</UserName>
      <NewPassword>NewSecure!99</NewPassword>
    </ChangeUserPassword>
  </soap:Body>
</soap:Envelope>
```

## JavaScript

Every call answers XML with HTTP 200, success or not, so `success` is the thing to branch on and
`errorCode` is the number to report. `call` below is used by the sample on every page.

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

Sets another account's password outright, so it needs a ticket with the rights to do it - this is not
the call a user changes their own password with.

```javascript
await call('ChangeUserPassword', {
  authenticationTicket: ticket,
  UserName: 'jsmith',
  NewPassword: 'the new one'
});
```

The old password stops working immediately, including any session holding a ticket issued under it.

## Notes

- **Same-password restriction:** The new password must differ from the user's current password. Submitting the same password is rejected.
- **Password policy enforcement:** The new password is validated against the application's password complexity rules (minimum length, required character types, etc.) as configured in `GetAuthenticationAndPasswordPolicy`. If the password does not comply, the call fails and the response `error` attribute contains a descriptive message identifying the unmet rule.
- **No current password:** Setting another user's password takes no password of theirs - the caller's right is what decides. Your own password needs your current one, through [ChangeUserPassword1](ChangeUserPassword1.md).
- **Use `ChangePasswordUsingSecretText` for unauthenticated resets:** If the user has forgotten their password and cannot log in, use the `ForgotPassword` / `ForgotPasswordByUserName` + `ChangePasswordUsingSecretText` flow instead.

## Related APIs

- [ChangeUserPassword1](ChangeUserPassword1.md) - Change your own password (takes the current one) or another user's
- [ChangePasswordUsingSecretText](ChangePasswordUsingSecretText.md) - Reset password using a one-time email token (no ticket required)
- [ForgotPassword](ForgotPassword.md) - Initiate a password reset by email address
- [ForgotPasswordByUserName](ForgotPasswordByUserName.md) - Initiate a password reset by user name
- [GetAuthenticationAndPasswordPolicy](GetAuthenticationAndPasswordPolicy.md) - Retrieve the current password complexity policy

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4000` | `UserName` is the caller: your own password is changed with ChangeUserPassword1 |
| `4030` | the caller may not set another account’s password - including a caller with no ticket, who is the anonymous user |
| `4010` | `[901]` the ticket is expired or unknown |


| Error | Description |
|-------|-------------|
| `[901] Session expired or Invalid ticket` | The `AuthenticationTicket` is missing, invalid, or has expired |
| `User not found` | The specified `UserName` does not exist |
| `Insufficient rights` | The caller does not have the User Manager role and is attempting to change another user's password |
| `New password cannot be the same as old password` | The supplied `NewPassword` is identical to the user's current password |
| Password policy violation message | The `NewPassword` does not meet the configured complexity requirements (the exact message describes the unmet rule) |
