# ChangeUserPassword1 API

Changes a user's password. **Your own password takes your current password**, checked like a sign-in; another user's password is set by right, as with [ChangeUserPassword](ChangeUserPassword.md).

## Endpoint

```
/srv.asmx/ChangeUserPassword1
```

## Methods

- **GET** `/srv.asmx/ChangeUserPassword1?AuthenticationTicket=...&UserName=...&CurrentPassword=...&NewPassword=...`
- **POST** `/srv.asmx/ChangeUserPassword1` (form data)
- **SOAP** Action: `http://tempuri.org/ChangeUserPassword1`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `UserName` | string | Yes | The login name of the user whose password is to be changed |
| `CurrentPassword` | string | When `UserName` is you | Your current password. Ignored when `UserName` is another user. |
| `NewPassword` | string | Yes | The new password. Must differ from the current password and satisfy the password policy. Empty is accepted only for another user, who must then have an e-mail address. |

## Response

### Success Response

```xml
<root success="true" />
```

### Error Response

```xml
<root success="false" errorCode="4030" error="This action cannot be completed without password verification. ..." />
```

## Required Permissions

**An administrator's account** (the `sysadmin` account or a member of `[Administrators]`) can be changed by administrators only; anyone else is refused with `4030`. See [AdministrativeRoles](AdministrativeRoles.md).

- **Own password:** Any signed-in user, with their current password.
- **Another user's password:** The caller must hold the **User Manager** administrative role, or manage a library the user belongs to. `CurrentPassword` is not used.

## Example

### Request (POST) - a user changing their own password

```
POST /srv.asmx/ChangeUserPassword1 HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=abc123&UserName=jsmith&CurrentPassword=OldSecure!98&NewPassword=NewSecure!99
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/ChangeUserPassword1"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <ChangeUserPassword1 xmlns="http://tempuri.org/">
      <AuthenticationTicket>abc123-def456</AuthenticationTicket>
      <UserName>jsmith</UserName>
      <CurrentPassword>OldSecure!98</CurrentPassword>
      <NewPassword>NewSecure!99</NewPassword>
    </ChangeUserPassword1>
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

The call behind a "change my password" form. A wrong current password answers `4030`, not `4010`:
the session is still good, so do not sign the user out - ask again.

```javascript
await call('ChangeUserPassword1', {
  authenticationTicket: ticket,
  UserName: myUserName,
  CurrentPassword: currentPassword,
  NewPassword: newPassword
});
```

## Notes

- **The current password is checked like a sign-in:** a wrong one is written to the login log as a failed sign-in and waits out the configured login delay, as a failed `AuthenticateUser` does.
- **Windows authentication:** with Windows authentication on there is no infoRouter password to confirm, and `CurrentPassword` is not checked.
- **Only infoRouter passwords:** a user signing in through an external authority (LDAP, Active Directory) has no infoRouter password to change; the call is refused.
- **Same-password restriction and password policy:** as for [ChangeUserPassword](ChangeUserPassword.md).
- **Forgotten password:** a user who cannot sign in uses `ForgotPassword` / `ForgotPasswordByUserName` and then `ChangePasswordUsingSecretText`.

## Related APIs

- [ChangeUserPassword](ChangeUserPassword.md) - **Obsolete**, superseded by this API: sets another user's password and refuses your own
- [ChangePasswordUsingSecretText](ChangePasswordUsingSecretText.md) - Reset password using a one-time email token (no ticket required)
- [GetAuthenticationAndPasswordPolicy](GetAuthenticationAndPasswordPolicy.md) - Retrieve the current password complexity policy

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4030` | `UserName` is you and `CurrentPassword` is wrong or empty |
| `4030` | the caller may not set another account's password - including a caller with no ticket, who is the anonymous user |
| `4010` | `[901]` the ticket is expired or unknown |
