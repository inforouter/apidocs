# AuthenticateUser API

Authenticates a user against infoRouter using their user name and password, and returns an authentication ticket along with basic profile information. The ticket must be passed to all subsequent API calls as `authenticationTicket`.

## Endpoint

```
/srv.asmx/AuthenticateUser
```

## Methods

- **GET** `/srv.asmx/AuthenticateUser?UID=...&PWD=...`
- **POST** `/srv.asmx/AuthenticateUser` (form data)
- **SOAP** Action: `http://tempuri.org/AuthenticateUser`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `UID` | string | Yes | The user's login name (case-insensitive) |
| `PWD` | string | Yes | The user's password |

> **Note:** This method does not require an `authenticationTicket` — it is the login method that produces one.

## Response

### Success Response

```xml
<root success="true"
      ticket="3f2a1b4c-5d6e-7f8a-9b0c-1d2e3f4a5b6c"
      userid="42"
      username="jsmith"
      firstName="John"
      lastName="Smith"
      fullname="John Smith"
      email="jsmith@example.com"
      expireOn="2026-03-20T14:35:00Z"
      isAuthenticated="True" />
```

### Response Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `success` | boolean | `true` on successful authentication |
| `ticket` | GUID string | Authentication ticket to use in all subsequent API calls |
| `userid` | integer | Internal numeric user ID |
| `username` | string | The user's login name |
| `firstName` | string | User's first name |
| `lastName` | string | User's last name |
| `fullname` | string | User's full display name (`firstName lastName`) |
| `email` | string | User's email address |
| `expireOn` | datetime (UTC) | Ticket expiration timestamp (30-day sliding window) |
| `isAuthenticated` | boolean string | Whether the session is authenticated (`True`/`False`) |

### Error Response

```xml
<root success="false" error="[900] Authentication failed" />
```

## Required Permissions

- No prior authentication is required.
- The user account must exist and be **active** (not disabled or deleted).
- If the application is configured for Windows Authentication, native credential login may be restricted — use `AuthenticateUserViaWindows` instead.

## Example

### Request (GET)

```
GET /srv.asmx/AuthenticateUser?UID=jsmith&PWD=Secret123! HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/AuthenticateUser HTTP/1.1
Content-Type: application/x-www-form-urlencoded

UID=jsmith&PWD=Secret123!
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/AuthenticateUser"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <AuthenticateUser xmlns="http://tempuri.org/">
      <UID>jsmith</UID>
      <PWD>Secret123!</PWD>
    </AuthenticateUser>
  </soap:Body>
</soap:Envelope>
```

## Notes

- The `ticket` value in the response is a GUID and must be stored by the client and passed as `authenticationTicket` in every subsequent API call.
- Tickets use a **30-day sliding expiration** — each successful API call resets the timer.
- The system administrator account (`SysadminAccountName` in config) cannot generate tickets via this method.
- If Windows Authentication is enabled at the IIS/server level, all requests may be pre-authenticated by the OS; use `AuthenticateUserViaWindows` in that configuration.
- Passwords are validated against the configured authentication source (native infoRouter database, LDAP, or an external authority defined in `appsettings.json`).
- Use `LogOut` when the session is finished to release server-side resources.

## Related APIs

- [AuthenticateUser1](AuthenticateUser1.md) - Authenticate and specify a session language
- [AuthenticateUserViaWindows](AuthenticateUserViaWindows.md) - Authenticate using Windows (NTLM/Kerberos) credentials
- [CreateTicketforUser](CreateTicketforUser.md) - Create a ticket for a user via server-to-server trusted password
- [RenewTicket](RenewTicket.md) - Renew a ticket that is about to expire
- [isValidTicket](isValidTicket.md) - Check whether a ticket is still valid
- [LogOut](LogOut.md) - Invalidate the authentication ticket

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | The user name or password is incorrect, the account is disabled, or the account does not exist |
| `[902] Ticket generation not allowed` | The account is not permitted to generate API tickets (e.g. the system admin account) |
