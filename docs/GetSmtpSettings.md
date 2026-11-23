# GetSmtpSettings API

**Available in:** infoRouter 9.0 and later

Returns the SMTP settings in effect: the address infoRouter's email comes from, the SMTP server, its port, encryption and timeout, the account infoRouter signs in with, and who receives the technical status reports. The password is never returned. Administrators only; [SetSmtpSettings](SetSmtpSettings.md) changes them.

## Endpoint

```
/srv.asmx/GetSmtpSettings
```

## Methods

- **GET** `/srv.asmx/GetSmtpSettings?authenticationTicket=...`
- **POST** `/srv.asmx/GetSmtpSettings` (form data)
- **SOAP** Action: `http://tempuri.org/GetSmtpSettings`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |

## Response

### Success Response
```xml
<response success="true" error="">
  <SmtpSettings>
    <SystemEmailAddress>inforouter@example.com</SystemEmailAddress>
    <SmtpServer>smtp.office365.com</SmtpServer>
    <SmtpServerPort>587</SmtpServerPort>
    <SmtpSSL>true</SmtpSSL>
    <SmtpConnectionTimeout>20</SmtpConnectionTimeout>
    <SmtpSendUserName>inforouter@example.com</SmtpSendUserName>
    <PasswordSet>true</PasswordSet>
    <TechnicalContactEmail>it@example.com</TechnicalContactEmail>
  </SmtpSettings>
</response>
```

| Element | Type | Description |
|---------|------|-------------|
| `SystemEmailAddress` | string | The address infoRouter's email comes from. The mail queue's folder is named after it. |
| `SmtpServer` | string | The SMTP server's host name or IP address. Empty: no SMTP server is set, and email is queued but not sent. |
| `SmtpServerPort` | int | The SMTP server's port: usually 25, 587 (STARTTLS) or 465 (TLS from the start). |
| `SmtpSSL` | bool | `true`: the connection must be encrypted, with TLS from the start on port 465 and STARTTLS on any other port. `false`: STARTTLS is used when the server offers it. |
| `SmtpConnectionTimeout` | int | Seconds to wait for the SMTP server. |
| `SmtpSendUserName` | string | The account infoRouter signs in with. Empty: it does not sign in. |
| `PasswordSet` | bool | Whether a password is saved for that account. The password itself is never returned. |
| `TechnicalContactEmail` | string | Who receives the technical status reports. Empty: nobody. |
| `SettingsProblem` | string | Present only when the settings file could not be read (see Notes). Says what is wrong with it; email cannot be sent until it is corrected or the settings are saved. |

### Error Response
```xml
<response success="false" error="[ErrorCode] Error message" errorCode="4030" />
```

| errorCode | When |
|-----------|------|
| 4010 | No authentication ticket, or an invalid or expired one |
| 4030 | The user is not allowed to change application settings |

## Required Permissions

The `UpdateApplicationSettingsAndPolicies` administrative right (system administrators), the same as the other application settings APIs.

## Example

### Request (POST)
```
POST /srv.asmx/GetSmtpSettings HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123
```

## Notes

- The settings are kept in their own file, `config\smtp-setting.json` in infoRouter's application folder, not in `appsettings.json`. The password is stored encrypted. Without that file there is no SMTP server: the values are empty, and email is queued but not sent.
- The answer is what infoRouter is using now: the file as it was last read (at start or by [FlushApplicationCache](FlushApplicationCache.md)), or as SetSmtpSettings last saved it. A change made to the file by hand is used after FlushApplicationCache or a restart.
- infoRouter 8.7 kept these settings in `web.config`; the upgrade to 9.0 moves them to this file and encrypts the password.
- [GetApplicationParameters](getApplicationParameters.md) also returns the system email address to everyone, and the SMTP server, port, timeout and user name to administrators.
