# isValidTicket API

Checks whether an existing authentication ticket is still valid and returns the session profile associated with it. Unlike `RenewTicket`, this method does not require credentials and does not extend the ticket's expiration — it is a passive, read-only check.

Use this method when a client application needs to confirm that a previously obtained ticket is still alive before making further API calls.

## Endpoint

```
/srv.asmx/isValidTicket
```

## Methods

- **GET** `/srv.asmx/isValidTicket?AuthenticationTicket=...`
- **POST** `/srv.asmx/isValidTicket` (form data)
- **SOAP** Action: `http://tempuri.org/isValidTicket`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | No | The authentication ticket to validate. If not supplied, the server checks the `ticket` HTTP cookie. If neither is present or valid, the call fails with `[901]`. |

## Response

### Success Response

```xml
<root success="true"
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
| `userid` | integer | Internal numeric user ID |
| `username` | string | The user's login name |
| `firstName` | string | User's first name |
| `lastName` | string | User's last name |
| `fullname` | string | User's full display name |
| `email` | string | User's email address |
| `expireOn` | datetime (UTC) | Current ticket expiration timestamp |
| `isAuthenticated` | boolean string | Whether the session is authenticated (`True`/`False`) |

### Error Response

```xml
<root success="false" error="[901] Session expired or Invalid ticket" />
```

## Required Permissions

- No special role is required.
- The ticket must exist in the server's in-memory session cache and not have expired.

## Example

### Request (GET)

```
GET /srv.asmx/isValidTicket?AuthenticationTicket=3f2a1b4c-5d6e-7f8a-9b0c-1d2e3f4a5b6c HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/isValidTicket HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2a1b4c-5d6e-7f8a-9b0c-1d2e3f4a5b6c
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/isValidTicket"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <isValidTicket xmlns="http://tempuri.org/">
      <AuthenticationTicket>3f2a1b4c-5d6e-7f8a-9b0c-1d2e3f4a5b6c</AuthenticationTicket>
    </isValidTicket>
  </soap:Body>
</soap:Envelope>
```

## Notes

- **Passive check only:** This method does not renew or extend the ticket's 30-day sliding expiration. The expiration timestamp returned in `expireOn` reflects the current value, unchanged by this call.
- **Cookie fallback:** If `AuthenticationTicket` is not supplied as a parameter, the server checks for a `ticket` HTTP cookie. Browser-based clients that store the ticket in a cookie can omit the parameter entirely.
- **No credentials required:** Unlike `RenewTicket`, no `UID` or `PWD` need to be supplied — the ticket itself is the only input.
- **Use `RenewTicket` to extend sessions:** If you want to both validate and reset the expiration window, use `RenewTicket` instead.
- **Already-expired tickets return `[901]`:** Once a ticket has expired and been evicted from the session cache, it cannot be recovered. A new login via `AuthenticateUser` is required.

## Related APIs

- [AuthenticateUser](AuthenticateUser.md) - Obtain a new authentication ticket
- [RenewTicket](RenewTicket.md) - Validate credentials and renew a ticket, resetting the expiration
- [LogOut](LogOut.md) - Explicitly invalidate a ticket

## Error Codes

| Error | Description |
|-------|-------------|
| `[901] Session expired or Invalid ticket` | The ticket is missing, already expired, or not found in the session cache |
