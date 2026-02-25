# ChangeUserPassword API

Changes the password of the specified infoRouter user. A user may change their own password; changing another user's password requires the **User Manager** administrative role.

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

- **Own password:** Any authenticated user may change their own password (where `UserName` matches the caller's own login name).
- **Another user's password:** The caller must hold the **User Manager** administrative role.

## Example

### Request (GET) -" user changing their own password

```
GET /srv.asmx/ChangeUserPassword?AuthenticationTicket=abc123&UserName=jsmith&NewPassword=NewSecure!99 HTTP/1.1
Host: server.example.com
```

### Request (POST) -" admin changing another user's password

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

## Notes

- **Same-password restriction:** The new password must differ from the user's current password. Submitting the same password is rejected.
- **Password policy enforcement:** The new password is validated against the application's password complexity rules (minimum length, required character types, etc.) as configured in `GetAuthenticationAndPasswordPolicy`. If the password does not comply, the call fails and the response `error` attribute contains a descriptive message identifying the unmet rule.
- **No old password required:** Unlike typical self-service password-change forms, this API does not require the user to supply their current password -" only the authentication ticket is used to verify the caller's identity. Administrative tooling or trusted integrations should therefore protect this endpoint accordingly.
- **Use `ChangePasswordUsingSecretText` for unauthenticated resets:** If the user has forgotten their password and cannot log in, use the `ForgotPassword` / `ForgotPasswordByUserName` + `ChangePasswordUsingSecretText` flow instead.

## Related APIs

- [ChangePasswordUsingSecretText](ChangePasswordUsingSecretText.md) - Reset password using a one-time email token (no ticket required)
- [ForgotPassword](ForgotPassword.md) - Initiate a password reset by email address
- [ForgotPasswordByUserName](ForgotPasswordByUserName.md) - Initiate a password reset by user name
- [GetAuthenticationAndPasswordPolicy](GetAuthenticationAndPasswordPolicy.md) - Retrieve the current password complexity policy

## Error Codes

| Error | Description |
|-------|-------------|
| `[901] Session expired or Invalid ticket` | The `AuthenticationTicket` is missing, invalid, or has expired |
| `User not found` | The specified `UserName` does not exist |
| `Insufficient rights` | The caller does not have the User Manager role and is attempting to change another user's password |
| `New password cannot be the same as old password` | The supplied `NewPassword` is identical to the user's current password |
| Password policy violation message | The `NewPassword` does not meet the configured complexity requirements (the exact message describes the unmet rule) |
