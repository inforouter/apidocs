# AuthenticateUserViaWindows API

Authenticates the currently logged-in Windows user against infoRouter using the HTTP request's Windows identity (NTLM/Kerberos), and returns an authentication ticket. No user name or password is passed in the request — the Windows account is determined automatically from the authenticated HTTP context.

Use this method when the infoRouter server is deployed behind IIS or Kestrel with Windows Authentication enabled, and you want seamless single-sign-on for domain users.

## Endpoint

```
/srv.asmx/AuthenticateUserViaWindows
```

## Methods

- **GET** `/srv.asmx/AuthenticateUserViaWindows?language=...&oldTicket=...`
- **POST** `/srv.asmx/AuthenticateUserViaWindows` (form data)
- **SOAP** Action: `http://tempuri.org/AuthenticateUserViaWindows`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `language` | string | No | Language code for the session (e.g. `en`, `de`, `fr`, `tr`). If omitted or empty, the user's preferred language from their profile is used. |
| `oldTicket` | string | No | An existing infoRouter ticket GUID to renew. If omitted or empty, the server checks the request's `ticket` cookie. If neither is present, a fresh session is created. Must be a valid GUID string if supplied; an invalid format returns an error. |

> **Note:** This method does not require an `authenticationTicket` parameter — it is a login method that produces one. The caller's Windows identity is read directly from the HTTP request context.

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
| `username` | string | The user's infoRouter login name |
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

- No infoRouter credentials are required in the request.
- **The server must have Windows Authentication enabled** at the IIS or Kestrel host level.
- The Windows domain account (`DOMAIN\username`) must be mapped to an active infoRouter user account.
- The calling HTTP client must supply a valid Windows Negotiate/NTLM/Kerberos challenge-response (this happens automatically in browsers and .NET `HttpClient` when Windows Authentication is configured).

## Example

### Request (GET) — fresh session

```
GET /srv.asmx/AuthenticateUserViaWindows?language=en HTTP/1.1
Host: server.example.com
Authorization: Negotiate <kerberos-token>
```

### Request (GET) — renewing an existing ticket

```
GET /srv.asmx/AuthenticateUserViaWindows?language=en&oldTicket=3f2a1b4c-5d6e-7f8a-9b0c-1d2e3f4a5b6c HTTP/1.1
Host: server.example.com
Authorization: Negotiate <kerberos-token>
```

### Request (POST)

```
POST /srv.asmx/AuthenticateUserViaWindows HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Authorization: Negotiate <kerberos-token>

language=en&oldTicket=
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/AuthenticateUserViaWindows"
Authorization: Negotiate <kerberos-token>

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <AuthenticateUserViaWindows xmlns="http://tempuri.org/">
      <language>en</language>
      <oldTicket></oldTicket>
    </AuthenticateUserViaWindows>
  </soap:Body>
</soap:Envelope>
```

## Notes

- **`oldTicket` fallback to cookie:** If `oldTicket` is not supplied in the request parameters, the server automatically checks for a cookie named `ticket` on the incoming request. If found, that value is used as the old ticket. If neither is present, a completely new session is created.
- **`oldTicket` format:** If `oldTicket` is provided it must be a valid GUID string (e.g. `3f2a1b4c-5d6e-7f8a-9b0c-1d2e3f4a5b6c`). A malformed value returns an error immediately: `invalid ticket format`.
- **Windows identity resolution:** The server reads `context.User.Identity.Name`, which is set by the IIS/Kestrel Windows Authentication middleware. The value is typically in `DOMAIN\username` format; the domain portion is parsed separately to identify the authentication source.
- **Account mapping:** The Windows account must correspond to an active infoRouter user. If no matching user is found, authentication fails with `[900] Authentication failed`.
- **Not for non-Windows deployments:** This method only works when the hosting environment supports Windows Authentication. On Linux/Docker or when anonymous authentication is used exclusively, calls will fail with an unauthenticated user error.
- **Language behaviour:** `language` overrides the session language only — it does not permanently change the user's profile preference.

## Related APIs

- [AuthenticateUser](AuthenticateUser) - Authenticate with explicit user name and password
- [AuthenticateUser1](AuthenticateUser1) - Authenticate with user name, password, and session language
- [RenewTicket](RenewTicket) - Renew a ticket using credentials
- [isValidTicket](isValidTicket) - Check whether an existing ticket is still valid
- [LogOut](LogOut) - Invalidate the authentication ticket

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed — Unauthenticated User.` | The HTTP request was not authenticated by Windows Authentication (no `Authorization` header or authentication not enabled on the server) |
| `[900] Authentication failed` | The Windows account could not be mapped to an active infoRouter user |
| `invalid ticket format` | The `oldTicket` parameter was supplied but is not a valid GUID string |
