# RenewTicket API

Validates the user's credentials and either renews an existing authentication ticket or issues a new one. This is useful for long-running client applications that need to keep a session alive without requiring a full login cycle.

The caller always supplies their credentials (`UID` / `PWD`). If a valid `OldTicket` is provided, it is renewed and its expiration window is reset. If the old ticket has already expired, the credentials are used to authenticate normally and a fresh ticket is returned.

No prior authentication ticket is required — this method acts as a combined validate-and-refresh login.

## Endpoint

```
/srv.asmx/RenewTicket
```

## Methods

- **GET** `/srv.asmx/RenewTicket?UID=...&PWD=...&Lang=...&OldTicket=...`
- **POST** `/srv.asmx/RenewTicket` (form data)
- **SOAP** Action: `http://tempuri.org/RenewTicket`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `UID` | string | Yes | The user's login name. Always validated against the database regardless of ticket status. |
| `PWD` | string | Yes | The user's password. Always validated regardless of ticket status. |
| `Lang` | string | No | Language code for the session (e.g. `en`, `de`, `fr`, `tr`). If omitted or empty, the user's preferred language from their profile is used. |
| `OldTicket` | string | No | The existing ticket GUID to renew. If omitted or empty, the server checks the `ticket` HTTP cookie. If no cookie is present either, a completely fresh session is created. Must be a valid GUID string if supplied — an invalid format returns an error immediately. |

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
| `success` | boolean | `true` on success |
| `ticket` | GUID string | The renewed or newly issued authentication ticket |
| `userid` | integer | Internal numeric user ID |
| `username` | string | The user's login name |
| `firstName` | string | User's first name |
| `lastName` | string | User's last name |
| `fullname` | string | User's full display name |
| `email` | string | User's email address |
| `expireOn` | datetime (UTC) | New ticket expiration timestamp (30-day sliding window from this call) |
| `isAuthenticated` | boolean string | Whether the session is authenticated (`True`/`False`) |

### Error Response

```xml
<root success="false" error="[ErrorCode] Error message" />
```

## Required Permissions

- No prior authentication ticket is required.
- The user account must exist and be active.

## Example

### Request (GET) — renewing an existing ticket

```
GET /srv.asmx/RenewTicket?UID=jsmith&PWD=Secret123!&Lang=en&OldTicket=3f2a1b4c-5d6e-7f8a-9b0c-1d2e3f4a5b6c HTTP/1.1
Host: server.example.com
```

### Request (GET) — fresh login (no old ticket)

```
GET /srv.asmx/RenewTicket?UID=jsmith&PWD=Secret123!&Lang=en HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/RenewTicket HTTP/1.1
Content-Type: application/x-www-form-urlencoded

UID=jsmith&PWD=Secret123!&Lang=en&OldTicket=3f2a1b4c-5d6e-7f8a-9b0c-1d2e3f4a5b6c
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/RenewTicket"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <RenewTicket xmlns="http://tempuri.org/">
      <UID>jsmith</UID>
      <PWD>Secret123!</PWD>
      <Lang>en</Lang>
      <OldTicket>3f2a1b4c-5d6e-7f8a-9b0c-1d2e3f4a5b6c</OldTicket>
    </RenewTicket>
  </soap:Body>
</soap:Envelope>
```

## Notes

- **Credentials are always validated:** Unlike some renew patterns that skip credential checks when the old ticket is still valid, `RenewTicket` always authenticates `UID` and `PWD` against the database. If the credentials are wrong, the call fails even if `OldTicket` is currently valid.
- **`OldTicket` fallback to cookie:** If `OldTicket` is not supplied as a parameter, the server checks the `ticket` HTTP cookie. Browser-based clients that store the ticket in a cookie can omit `OldTicket` entirely.
- **Fresh login when no old ticket:** If neither `OldTicket` nor the cookie is present, the call behaves identically to `AuthenticateUser1` — a brand-new session is created.
- **`OldTicket` format:** If `OldTicket` is supplied it must be a valid GUID string. Any other format is rejected immediately with `invalid ticket format` before any credential validation occurs.
- **Expiration reset:** On success the ticket's 30-day sliding expiration is reset from the current time, regardless of whether the old ticket was still valid or has expired.
- **`Lang` overrides session language:** Supplying `Lang` changes the session language for this ticket; the user's stored profile preference is not permanently changed.
- **Use `isValidTicket` for passive checks:** If you only need to verify whether a ticket is still alive without re-authenticating, use `isValidTicket` instead — it does not require credentials.

## Related APIs

- [AuthenticateUser](AuthenticateUser.md) - Standard login returning a new ticket and full profile info
- [AuthenticateUser1](AuthenticateUser1.md) - Login with explicit session language
- [isValidTicket](isValidTicket.md) - Check ticket validity without supplying credentials
- [LogOut](LogOut.md) - Explicitly invalidate a ticket

## Error Codes

| Error | Description |
|-------|-------------|
| `invalid ticket format` | `OldTicket` was supplied but is not a valid GUID string |
| `[900] Authentication failed` | The `UID` or `PWD` is incorrect, or the account is disabled or does not exist |
| `[902] Ticket generation are not allowed for this user.` | The account is not permitted to generate API tickets |
