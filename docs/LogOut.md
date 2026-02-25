# LogOut API

Logs out the authenticated user by invalidating their authentication ticket and clearing their server-side session variables. After a successful logout, the ticket can no longer be used for API calls.

## Endpoint

```
/srv.asmx/LogOut
```

## Methods

- **GET** `/srv.asmx/LogOut?AuthenticationTicket=...`
- **POST** `/srv.asmx/LogOut` (form data)
- **SOAP** Action: `http://tempuri.org/LogOut`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | No | The authentication ticket to invalidate. If not supplied, the server checks the `ticket` HTTP cookie on the request. If neither is present or valid, the call fails with `[901]`. |

## Response

### Success Response

```xml
<root success="true" />
```

### Error Response

```xml
<root success="false" error="[901] Session expired or Invalid ticket" />
```

## Required Permissions

- Only a valid, currently active authentication ticket can be logged out.

## Example

### Request (GET)

```
GET /srv.asmx/LogOut?AuthenticationTicket=3f2a1b4c-5d6e-7f8a-9b0c-1d2e3f4a5b6c HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/LogOut HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2a1b4c-5d6e-7f8a-9b0c-1d2e3f4a5b6c
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/LogOut"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <LogOut xmlns="http://tempuri.org/">
      <AuthenticationTicket>3f2a1b4c-5d6e-7f8a-9b0c-1d2e3f4a5b6c</AuthenticationTicket>
    </LogOut>
  </soap:Body>
</soap:Envelope>
```

## Notes

- **Ticket is removed from memory cache:** The session entry is deleted from the server's in-memory cache. Any subsequent API call using the same ticket will immediately receive a `[901] Session expired or Invalid ticket` error.
- **Cookie fallback:** If `AuthenticationTicket` is not supplied in the request parameters, the server checks for a `ticket` HTTP cookie. This is useful for browser-based clients that store the ticket in a cookie rather than passing it explicitly.
- **Already-expired tickets return an error:** If the ticket has already expired before `LogOut` is called, the server cannot find the session to remove and returns `[901]`. This is expected behaviour — the session was already gone. Callers should not treat this as a critical failure during cleanup.
- **Best practice:** Always call `LogOut` at the end of an integration session to release the server-side session entry and free memory cache resources, rather than simply abandoning the ticket to expire naturally after 30 days.

## Related APIs

- [AuthenticateUser](AuthenticateUser.md) - Obtain a new authentication ticket
- [isValidTicket](isValidTicket.md) - Check whether a ticket is still valid without invalidating it
- [RenewTicket](RenewTicket.md) - Renew a ticket that is about to expire

## Error Codes

| Error | Description |
|-------|-------------|
| `[901] Session expired or Invalid ticket` | The ticket is missing, already expired, or not found in the session cache |
