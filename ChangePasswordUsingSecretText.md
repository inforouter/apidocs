# ChangePasswordUsingSecretText API

Changes a user's password using a one-time password-reset token (the "secret text") that was issued by the `ForgotPassword` or `ForgotPasswordByUserName` API and delivered to the user by email.

This method is used to complete the self-service password-reset flow:
1. The user calls `ForgotPassword` (by email) or `ForgotPasswordByUserName` — the server emails them a reset link containing a GUID token.
2. The user (or the application handling the reset link) calls `ChangePasswordUsingSecretText` with that token and the desired new password.

No authentication ticket is required.

## Endpoint

```
/srv.asmx/ChangePasswordUsingSecretText
```

## Methods

- **GET** `/srv.asmx/ChangePasswordUsingSecretText?userName=...&secretText=...&newPassword=...`
- **POST** `/srv.asmx/ChangePasswordUsingSecretText` (form data)
- **SOAP** Action: `http://tempuri.org/ChangePasswordUsingSecretText`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `userName` | string | Yes | The login name of the user whose password is being reset |
| `secretText` | string | Yes | The one-time password-reset token (a GUID string, e.g. `3f2a1b4c-5d6e-7f8a-9b0c-1d2e3f4a5b6c`) that was emailed to the user. Must be in valid GUID format. The token is single-use and expires after a server-configured period. |
| `newPassword` | string | Yes | The new password to set for the account. Must satisfy the application's password complexity policy and must not be identical to the user's current password. |

> **Note:** This method does not require an `authenticationTicket`.

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

- No authentication ticket is required.
- The `secretText` token must have been issued for the specified `userName` by a prior call to `ForgotPassword` or `ForgotPasswordByUserName`.
- Only users with **native infoRouter authentication** can reset their password this way. Users authenticated via an external source (LDAP, Active Directory, OAuth) cannot change their infoRouter password through this API.

## Example

### Request (GET)

```
GET /srv.asmx/ChangePasswordUsingSecretText?userName=jsmith&secretText=3f2a1b4c-5d6e-7f8a-9b0c-1d2e3f4a5b6c&newPassword=NewSecure!99 HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/ChangePasswordUsingSecretText HTTP/1.1
Content-Type: application/x-www-form-urlencoded

userName=jsmith&secretText=3f2a1b4c-5d6e-7f8a-9b0c-1d2e3f4a5b6c&newPassword=NewSecure!99
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/ChangePasswordUsingSecretText"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <ChangePasswordUsingSecretText xmlns="http://tempuri.org/">
      <userName>jsmith</userName>
      <secretText>3f2a1b4c-5d6e-7f8a-9b0c-1d2e3f4a5b6c</secretText>
      <newPassword>NewSecure!99</newPassword>
    </ChangePasswordUsingSecretText>
  </soap:Body>
</soap:Envelope>
```

## Notes

- **`secretText` format:** The token must be a valid GUID string. Any other format (e.g. a plain word or partial GUID) is rejected immediately before any database lookup.
- **Token expiry:** The reset token has a server-defined expiration time. Attempting to use an expired token fails with the same error as an invalid token, to prevent information leakage.
- **Single-use token:** Once the password is changed successfully, the reset token is deleted and cannot be reused.
- **Same-password restriction:** The new password must differ from the user's current password. Attempting to set the same password fails.
- **Password policy enforcement:** The new password is validated against the application's password complexity rules (minimum length, character requirements, etc.) configured in `GetAuthenticationAndPasswordPolicy`. If the new password does not comply, the call fails with a descriptive policy error message.
- **External authentication users:** This API only works for users whose authentication source is the native infoRouter database. Users who authenticate via LDAP, Active Directory, or another external authority cannot change their password through infoRouter and must use their identity provider.
- **Typical integration:** This method is called by the infoRouter password-reset web page when a user clicks the reset link in their email. Applications implementing a custom reset flow should extract the `userName` and `secretText` from the emailed link and pass them to this API.

## Related APIs

- [ForgotPassword](ForgotPassword) - Initiate password reset by sending a reset token to the user's registered email address
- [ForgotPasswordByUserName](ForgotPasswordByUserName) - Initiate password reset by user name
- [ChangeUserPassword](ChangeUserPassword) - Change a user's password when you already have a valid authentication ticket

## Error Codes

| Error | Description |
|-------|-------------|
| `Invalid or expired reset code` | The `secretText` is not a valid GUID, does not match the stored token for the given user, or the token has expired |
| `User not found` | The `userName` does not correspond to any user account in the system |
| `External authentication — password cannot be changed` | The user's account is managed by an external authentication source (LDAP, AD, etc.) and the password cannot be changed via infoRouter |
| `New password cannot be the same as old password` | The supplied `newPassword` is identical to the user's current password |
| Password policy violation message | The `newPassword` does not meet the configured complexity requirements (the exact message describes the unmet rule) |
