---
search:
  exclude: true
---

# SetSmtpSettings API

**Available in:** infoRouter 9.0 and later

!!! warning "Internal API"
    Made for infoRouter's own user interface. It is not part of the public web API: there is no SOAP
    form and no promise of backward compatibility, and it may change or be removed in any release
    without notice. Do not use it in an integration.

Replaces the SMTP settings and applies them at once, without restarting infoRouter. Then connects and signs in to the SMTP server with them, sending nothing, and returns whether that worked. Administrators only; [GetSmtpSettings](GetSmtpSettings.md) reads them.

## Endpoint

```
/api/UIInternals/SetSmtpSettings
```

## Methods

- **GET** `/api/UIInternals/SetSmtpSettings?authenticationTicket=...&systemEmailAddress=...&smtpServer=...&smtpServerPort=...&smtpSSL=...&smtpConnectionTimeout=...&smtpSendUserName=...&smtpSendPassword=...&technicalContactEmail=...`
- **POST** `/api/UIInternals/SetSmtpSettings` (form data)

Prefer POST: a GET puts the password in the address, where proxies and server logs can keep it.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `systemEmailAddress` | string | Yes | The address infoRouter's email comes from. Must be a valid email address |
| `smtpServer` | string | Yes | The SMTP server's host name or IP address |
| `smtpServerPort` | int | Yes | The SMTP server's port, 1 to 65535: usually 25, 587 (STARTTLS) or 465 (TLS from the start) |
| `smtpSSL` | bool | No | `true`: the connection must be encrypted, with TLS from the start on port 465 and STARTTLS on any other port. `false` (default): STARTTLS is used when the server offers it |
| `smtpConnectionTimeout` | int | Yes | Seconds to wait for the SMTP server, 1 to 600 |
| `smtpSendUserName` | string | No | The account to sign in with. Empty: infoRouter does not sign in, and the saved password is cleared |
| `smtpSendPassword` | string | No | The account's password. Empty or left out: the saved password is kept |
| `technicalContactEmail` | string | No | Who receives the technical status reports. Empty: nobody. Otherwise a valid email address |

All settings are replaced. To change one, send the others as GetSmtpSettings returned them; leave `smtpSendPassword` empty to keep the password. The text values are trimmed.

## Response

### Success Response
```xml
<response success="true" error="">
  <Connection>
    <Connected>true</Connected>
  </Connection>
</response>
```

The settings are saved and in use. `Connection` says whether infoRouter could connect and sign in with them:

| Element | Type | Description |
|---------|------|-------------|
| `Connected` | bool | `true`: the SMTP server answered, and accepted the sign-in when there was one. No email was sent |
| `Error` | string | Why not; only when it did not |

An SMTP server that does not answer, or refuses the sign-in, does not stop the save:

```xml
<response success="true" error="">
  <Connection>
    <Connected>false</Connected>
    <Error>535: 5.7.139 Authentication unsuccessful</Error>
  </Connection>
</response>
```

### Error Response
```xml
<response success="false" error="[ErrorCode] Error message" errorCode="4000" />
```

| errorCode | When |
|-----------|------|
| 4000 | `systemEmailAddress` is not a valid email address |
| 4000 | `smtpServer` is empty, or not a host name or IP address |
| 4000 | `smtpServerPort` is not between 1 and 65535, or `smtpConnectionTimeout` not between 1 and 600 |
| 4000 | `technicalContactEmail` is neither empty nor a valid email address |
| 4010 | No authentication ticket, or an invalid or expired one |
| 4030 | The user is not allowed to change application settings |

Nothing is changed when the call fails.

## Required Permissions

The `UpdateApplicationSettingsAndPolicies` administrative right (system administrators), the same as the other application settings APIs.

## Example

### Request (POST)
```
POST /api/UIInternals/SetSmtpSettings HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&systemEmailAddress=inforouter%40example.com&smtpServer=smtp.office365.com&smtpServerPort=587&smtpSSL=true&smtpConnectionTimeout=20&smtpSendUserName=inforouter%40example.com&smtpSendPassword=&technicalContactEmail=it%40example.com
```

## Notes

- The settings are saved to `config\smtp-setting.json` in infoRouter's application folder, the password encrypted, and email sent from then on uses them.
- infoRouter queues its email in a folder named after the system email address. When the address changes, email still queued under the previous one is moved to the new address's folder by the next run of the email job, and sent with the new settings. Email that failed before stays in the previous address's Exceptions folder.
- To change the file by hand instead, edit it and call [FlushApplicationCache](FlushApplicationCache.md); infoRouter reads it again without a restart. A password typed into the file in plain text is encrypted in the file when infoRouter reads it.
- [GetApplicationParameters](../getApplicationParameters.md) shows the new values at once.
