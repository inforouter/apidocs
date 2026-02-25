# CreateTicketforUser API

Creates an authentication ticket for any specified infoRouter user without requiring that user's password. Instead, a server-side **trusted user password** (configured in the application settings) is presented by the calling application. This enables secure server-to-server impersonation and integration scenarios.

A typical use case is a trusted back-end service that needs to act on behalf of different users without storing or knowing individual passwords.

## Endpoint

```
/srv.asmx/CreateTicketforUser
```

## Methods

- **GET** `/srv.asmx/CreateTicketforUser?TrustedUserPwd=...&UserName=...`
- **POST** `/srv.asmx/CreateTicketforUser` (form data)
- **SOAP** Action: `http://tempuri.org/CreateTicketforUser`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `TrustedUserPwd` | string | Yes | The trusted user password configured in the infoRouter server's application settings (`appsettings.json`). This is a shared server-side secret, not the target user's password. |
| `UserName` | string | Yes | The login name of the infoRouter user for whom the ticket is created. The system administrator account cannot be impersonated via this method. |

> **Note:** This method does not require an `authenticationTicket`. Access is controlled solely by the `TrustedUserPwd` server secret.

## Response

### Success Response

```xml
<root success="true" ticket="3f2a1b4c-5d6e-7f8a-9b0c-1d2e3f4a5b6c" />
```

### Response Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `success` | boolean | `true` on success |
| `ticket` | GUID string | Authentication ticket to use in subsequent API calls on behalf of `UserName` |

> **Note:** Unlike `AuthenticateUser`, this response returns **only** `ticket` — it does not include `userid`, `username`, `firstName`, `lastName`, `email`, `expireOn`, or `isAuthenticated`.

### Error Response

```xml
<root success="false" error="[ErrorCode] Error message" />
```

## Required Permissions

- No infoRouter authentication ticket is required.
- The caller must know the **trusted user password** configured on the server.
- The system administrator account (configured as `SysadminAccountName` in `appsettings.json`) **cannot** be impersonated — attempting to do so always returns `[902]`.

## Example

### Request (GET)

```
GET /srv.asmx/CreateTicketforUser?TrustedUserPwd=MyServerSecret&UserName=jsmith HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/CreateTicketforUser HTTP/1.1
Content-Type: application/x-www-form-urlencoded

TrustedUserPwd=MyServerSecret&UserName=jsmith
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/CreateTicketforUser"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <CreateTicketforUser xmlns="http://tempuri.org/">
      <TrustedUserPwd>MyServerSecret</TrustedUserPwd>
      <UserName>jsmith</UserName>
    </CreateTicketforUser>
  </soap:Body>
</soap:Envelope>
```

## Notes

- **Trusted password is a server secret:** The `TrustedUserPwd` value is set in `appsettings.json` on the infoRouter server. It is not a user password and is not stored in the user database. Treat it like an API key — rotate it periodically and never expose it in client-side code.
- **Sysadmin is always blocked:** Creating a ticket for the system administrator account is explicitly prevented regardless of the trusted password. This is a hardcoded security constraint.
- **Ticket privileges:** The returned ticket carries the full permissions of the impersonated user. Any subsequent API call using this ticket is indistinguishable from the user having logged in normally.
- **Ticket expiry:** The created ticket uses the standard 30-day sliding expiration.
- **Reduced response:** This method returns only `ticket` on success, unlike `AuthenticateUser` which also returns `userid`, `username`, `firstName`, `lastName`, `email`, `expireOn`, and `isAuthenticated`. If profile information is needed, call `GetCurrentUser` using the returned ticket.
- **Transport security:** Because `TrustedUserPwd` grants impersonation of any user, always transmit it over HTTPS. Never pass it in query string parameters in production environments — use POST instead.

## Related APIs

- [AuthenticateUser](AuthenticateUser.md) - Standard username/password login returning full profile info
- [AuthenticateUser1](AuthenticateUser1.md) - Standard login with explicit session language
- [GetCurrentUser](GetCurrentUser.md) - Retrieve profile information of the currently authenticated user
- [LogOut](LogOut.md) - Invalidate the authentication ticket

## Error Codes

| Error | Description |
|-------|-------------|
| `[902] Ticket generation are not allowed for this user.` | The specified `UserName` is the system administrator account, which cannot be impersonated |
| `[900] Authentication failed` | The `TrustedUserPwd` is incorrect, the user does not exist, or the user account is inactive |
