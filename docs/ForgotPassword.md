# ForgotPassword API

Initiates the self-service password-reset flow for the user account(s) registered with the specified email address. The server looks up the account(s), generates a one-time reset token, and sends a password-reset email to the address. The token is then used with `ChangePasswordUsingSecretText` to set a new password.

No authentication ticket is required.

## Endpoint

```
/srv.asmx/ForgotPassword
```

## Methods

- **GET** `/srv.asmx/ForgotPassword?emailAddress=...`
- **POST** `/srv.asmx/ForgotPassword` (form data)
- **SOAP** Action: `http://tempuri.org/ForgotPassword`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `emailAddress` | string | Yes | The email address registered on the user account. Must not be empty. If multiple infoRouter accounts share the same email address, a reset email is sent for each account. |

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
- The SMTP email service must be configured in the application settings for emails to be delivered.

## Example

### Request (GET)

```
GET /srv.asmx/ForgotPassword?emailAddress=jsmith@example.com HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/ForgotPassword HTTP/1.1
Content-Type: application/x-www-form-urlencoded

emailAddress=jsmith@example.com
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/ForgotPassword"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <ForgotPassword xmlns="http://tempuri.org/">
      <emailAddress>jsmith@example.com</emailAddress>
    </ForgotPassword>
  </soap:Body>
</soap:Envelope>
```

## Password Reset Flow

Once the API returns success, the user receives an email containing a reset link in the form:

```
https://yourserver/resetpassword.aspx?username=jsmith&secretText=3f2a1b4c-5d6e-7f8a-9b0c-1d2e3f4a5b6c
```

The `secretText` value from this link (a GUID) is then passed to `ChangePasswordUsingSecretText` together with the `username` and the desired new password to complete the reset.

## Notes

- **Token expiry:** The reset token is valid for **1 hour** from the time the email is sent. After expiry it cannot be used.
- **Multiple accounts per email:** If more than one infoRouter user account is registered with the supplied email address, a separate reset email is sent for each account. The API returns success only after all emails have been dispatched.
- **External-auth users:** For accounts managed by an external authentication source (Windows/NTLM, LDAP, Active Directory), no reset link is generated. Instead, the user receives an informational email stating that their account is managed externally and they should contact their administrator.
- **Email not found returns an error:** Unlike some implementations that silently succeed to avoid email enumeration, this API **returns a failure** when no account is found for the given email address. Applications that wish to hide account existence should handle this error response without exposing it to the end user.
- **Empty email rejected:** Passing an empty or blank `emailAddress` returns an error immediately without any database lookup.
- **Email format:** The reset email is sent in the user's preferred format (HTML or plain text) and in the user's preferred language, both taken from the user's profile settings.
- **Alternative:** Use `ForgotPasswordByUserName` to initiate a reset by login name instead of email address.

## Related APIs

- [ForgotPasswordByUserName](ForgotPasswordByUserName.md) - Initiate password reset using the user's login name instead of email
- [ChangePasswordUsingSecretText](ChangePasswordUsingSecretText.md) - Complete the reset by submitting the token received by email and a new password

## Error Codes

| Error | Description |
|-------|-------------|
| `Please enter your Email address.` | The `emailAddress` parameter was empty or not supplied |
| `No user found with this email` | No infoRouter account has the supplied email address registered |
| Email send failure message | The SMTP service failed to send the email for one or more matched accounts; the error message includes the affected user name(s) |
