# ForgotPasswordByUserName API

Initiates the self-service password-reset flow for the infoRouter user with the specified login name. The server generates a one-time reset token and sends a password-reset email to the address registered on that account. The token is then used with `ChangePasswordUsingSecretText` to set a new password.

This is the login-name variant of `ForgotPassword`. Use it when the user knows their user name but not the email address associated with their account, or when the calling application works with user names rather than email addresses.

No authentication ticket is required.

## Endpoint

```
/srv.asmx/ForgotPasswordByUserName
```

## Methods

- **GET** `/srv.asmx/ForgotPasswordByUserName?userName=...`
- **POST** `/srv.asmx/ForgotPasswordByUserName` (form data)
- **SOAP** Action: `http://tempuri.org/ForgotPasswordByUserName`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `userName` | string | Yes | The infoRouter login name of the user requesting a password reset. Must not be empty. |

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

- No authentication required.
- The SMTP email service must be configured in the application settings for the email to be delivered.

## Example

### Request (GET)

```
GET /srv.asmx/ForgotPasswordByUserName?userName=jsmith HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/ForgotPasswordByUserName HTTP/1.1
Content-Type: application/x-www-form-urlencoded

userName=jsmith
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/ForgotPasswordByUserName"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <ForgotPasswordByUserName xmlns="http://tempuri.org/">
      <userName>jsmith</userName>
    </ForgotPasswordByUserName>
  </soap:Body>
</soap:Envelope>
```

## Password Reset Flow

Once the API returns success, the user receives an email at their registered address containing a reset link in the form:

```
https://yourserver/resetpassword.aspx?username=jsmith&secretText=3f2a1b4c-5d6e-7f8a-9b0c-1d2e3f4a5b6c
```

The `secretText` value (a GUID) and the `username` from this link are then passed to `ChangePasswordUsingSecretText` together with the desired new password to complete the reset.

## Notes

- **Token expiry:** The reset token is valid for **1 hour** from the time the email is sent. After expiry, it cannot be used and a new reset must be initiated.
- **Single account:** Because `userName` is unique in infoRouter, exactly one account is processed per call -" unlike `ForgotPassword` which may match multiple accounts sharing the same email address.
- **External-auth users:** For accounts managed by an external authentication source (Windows/NTLM, LDAP, Active Directory), no reset token is generated. Instead, the user receives an informational email stating their account is externally managed and they should contact their administrator.
- **Empty user name rejected:** Passing an empty or blank `userName` returns an error immediately without any database lookup.
- **Returns an error if user not found:** Unlike some implementations that silently succeed, this API returns a failure when the specified `userName` does not exist. Applications wishing to avoid user-name enumeration should suppress this error response before presenting feedback to end users.
- **Email format and language:** The reset email is sent in the user's preferred format (HTML or plain text) and in the user's preferred language, both taken from the user's profile settings.
- **Alternative:** Use `ForgotPassword` to initiate a reset by registered email address instead of login name.

## Related APIs

- [ForgotPassword](ForgotPassword.md) - Initiate password reset by the user's registered email address
- [ChangePasswordUsingSecretText](ChangePasswordUsingSecretText.md) - Complete the reset by submitting the token and new password

## Error Codes

| Error | Description |
|-------|-------------|
| `User name field cannot be empty.` | The `userName` parameter was empty or not supplied |
| `User not found` | No infoRouter account exists with the specified `userName` |
| Email send failure message | The SMTP service failed to deliver the reset email |
