# CreateWebDavSession API

Creates a WebDAV session ticket for the signed-in user, to map infoRouter as a drive in Windows File Explorer or any WebDAV client. The ticket travels in the URL, `https://server/dav/sid-{ticket}/`, so the client needs no sign-in of its own, and the caller's own authentication ticket is not exposed. Answers with the new session as [GetWebDavSessions](GetWebDavSessions.md) lists it.

## Endpoint

```
/srv.asmx/CreateWebDavSession
```

## Methods

- **GET** `/srv.asmx/CreateWebDavSession?authenticationTicket=...&customExpirationDate=...`
- **POST** `/srv.asmx/CreateWebDavSession` (form data)
- **SOAP** Action: `http://tempuri.org/CreateWebDavSession`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `customExpirationDate` | DateTime | No | When the ticket stops working, ISO 8601 (e.g. `2026-12-31T23:59:59`). A UTC value is converted to server local time. Must be in the future (`4000` otherwise). Omitted, the ticket expires the server's WebDAV expiry in days after its last use, a date each use moves forward. |

## Response

### Success Response

```xml
<response success="true" error="">
  <WebDavSession>
    <Ticket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</Ticket>
    <Url>/dav/sid-3f2504e0-4f89-11d3-9a0c-0305e82c3301/</Url>
    <SessionStartTime>2026-09-24T10:15:02.000Z</SessionStartTime>
    <AccessTime>2026-09-24T10:15:02.000Z</AccessTime>
    <ExpirationDate>2026-12-31T20:59:59.000Z</ExpirationDate>
    <CustomExpiration>true</CustomExpiration>
    <IpAddress>10.0.0.21</IpAddress>
  </WebDavSession>
</response>
```

The elements are described in [GetWebDavSessions](GetWebDavSessions.md). Mount `Url` with the server address prepended:

```
net use Z: "https://yourserver.example.com/dav/sid-3f2504e0-4f89-11d3-9a0c-0305e82c3301/"
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

## Required Permissions

Any authenticated, non-anonymous user. The ticket grants WebDAV access to what the user may see anyway; no further permission is needed.

## Example

### Request (POST)
```
POST /srv.asmx/CreateWebDavSession HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&customExpirationDate=2026-12-31T23:59:59
```

### Request (GET, sliding expiry)
```
GET /srv.asmx/CreateWebDavSession?authenticationTicket=abc123 HTTP/1.1
```

### SOAP Request
```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:CreateWebDavSession>
      <tns:authenticationTicket>abc123</tns:authenticationTicket>
      <tns:customExpirationDate>2026-12-31T23:59:59</tns:customExpirationDate>
    </tns:CreateWebDavSession>
  </soap:Body>
</soap:Envelope>
```

## Notes

- `CreateDiskMountURL` creates the same session and answers only its mount path.
- End a session with [RemoveWebDavSession](RemoveWebDavSession.md); the drive mapped with it stops working at once.

## Related APIs

- [GetWebDavSessions](GetWebDavSessions.md) - List the caller's WebDAV session tickets
- [RemoveWebDavSession](RemoveWebDavSession.md) - Remove a WebDAV session ticket
- [CreateDiskMountURL](CreateDiskMountURL.md) - Create a WebDAV session and return only its mount path

## Error Codes

| `errorCode` | When |
|---:|---|
| `4000` | `customExpirationDate` is not in the future |
| `4010` | the ticket is expired or unknown, or there is none |
| `4030` | the caller is signed in anonymously |
| `HTTP 400` | `customExpirationDate` is not a date; refused by model binding |
