# LogOut API

Logs out the authenticated user by invalidating their authentication ticket and clearing their server-side session variables. After a successful logout, the ticket can no longer be used for API calls. The call is safe to repeat: a ticket that names no session is answered with success.

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
| `AuthenticationTicket` | string | No | The authentication ticket to invalidate. If not supplied, the server checks the `ticket` HTTP cookie on the request. A ticket that names no session (already signed out, expired, or never issued) is answered with success. |

## Response

### Success Response

```xml
<root success="true" />
```

### Error Response

```xml
<root success="false" error="[ErrorCode] Error message" />
```

An unknown or expired ticket is **not** an error here; see Notes.

## Required Permissions

- None. Any caller may end the session of the ticket it holds; a ticket that names no session is answered with success.

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

## JavaScript

Every call answers XML with HTTP 200, success or not, so `success` is the thing to branch on and
`errorCode` is the number to report. `call` below is used by the sample on every page.

```javascript
async function call(action, params) {
  const response = await fetch(`/srv.asmx/${action}?${new URLSearchParams(params)}`);
  const root = new DOMParser()
    .parseFromString(await response.text(), 'text/xml')
    .documentElement;

  if (root.getAttribute('success') !== 'true') {
    throw new Error(`${root.getAttribute('errorCode')}: ${root.getAttribute('error')}`);
  }
  return root;
}
```

Cancels the ticket. Anything still holding it is signed out.

```javascript
await call('LogOut', { authenticationTicket: ticket });
```

Afterwards `isValidTicket` answers `4010` for it. Calling `LogOut` again with the same ticket succeeds.

## Notes

- **Ticket is removed from memory cache:** The session entry is deleted from the server's in-memory cache. Any subsequent API call using the same ticket will immediately receive a `[901] Session expired or Invalid ticket` error.
- **Cookie fallback:** If `AuthenticationTicket` is not supplied in the request parameters, the server checks for a `ticket` HTTP cookie. This is useful for browser-based clients that store the ticket in a cookie rather than passing it explicitly.
- **Safe to repeat:** A ticket that names no session - signed out already, expired, or never issued - is answered with `success="true"`, since there is nothing left to sign out. The answer is the same in all three cases, so it says nothing about whether a ticket ever existed. Until 9.0 this returned `[901]`.
- **Best practice:** Always call `LogOut` at the end of an integration session to release the server-side session entry and free memory cache resources, rather than simply abandoning the ticket to expire naturally after 30 days.

## Related APIs

- [AuthenticateUser](AuthenticateUser.md) - Obtain a new authentication ticket
- [isValidTicket](isValidTicket.md) - Check whether a ticket is still valid without invalidating it
- [RenewTicket](RenewTicket.md) - Renew a ticket that is about to expire

## Error Codes

This operation has no error of its own. A ticket that names no session is answered with success, not `[901]` / `4010`.
