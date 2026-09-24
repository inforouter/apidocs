# GetWebDavSessions API

Lists the WebDAV session tickets of the signed-in user. A WebDAV session ticket is what Windows File Explorer (or any WebDAV client) maps a drive with: the ticket travels in the URL, `https://server/dav/sid-{ticket}/`, so the client needs no sign-in of its own. This API, with [CreateWebDavSession](CreateWebDavSession.md) and [RemoveWebDavSession](RemoveWebDavSession.md), replaces the 8.7 *WebDAV sessions* page.

## Endpoint

```
/srv.asmx/GetWebDavSessions
```

## Methods

- **GET** `/srv.asmx/GetWebDavSessions?authenticationTicket=...`
- **POST** `/srv.asmx/GetWebDavSessions` (form data)
- **SOAP** Action: `http://tempuri.org/GetWebDavSessions`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |

## Response

### Success Response

```xml
<response success="true" error="">
  <WebDavSession>
    <Ticket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</Ticket>
    <Url>/dav/sid-3f2504e0-4f89-11d3-9a0c-0305e82c3301/</Url>
    <SessionStartTime>2026-09-24T10:15:02.000Z</SessionStartTime>
    <AccessTime>2026-09-24T12:40:11.000Z</AccessTime>
    <ExpirationDate>2026-10-24T12:40:11.000Z</ExpirationDate>
    <CustomExpiration>false</CustomExpiration>
    <IpAddress>10.0.0.21</IpAddress>
  </WebDavSession>
</response>
```

One `WebDavSession` element per live WebDAV session of the caller, newest first; none when there are none.

| Element | Description |
|---------|-------------|
| `Ticket` | The session ticket. Pass it to `RemoveWebDavSession` to end the session. |
| `Url` | The mount path, relative to the application: `/dav/sid-{ticket}/`. Prepend the server address (and virtual directory) to mount it. |
| `SessionStartTime` | When the ticket was created (UTC, ISO 8601). |
| `AccessTime` | When it was last used (UTC). |
| `ExpirationDate` | When it stops working (UTC). With `CustomExpiration` `false` this is the last use plus the server's WebDAV expiry in days, and moves forward each time the ticket is used. |
| `CustomExpiration` | `true` when the ticket was created with a fixed expiry date. |
| `IpAddress` | The address the ticket was created from. |

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

## Required Permissions

Any authenticated, non-anonymous user. A user sees only their own WebDAV sessions, never another user's, and not their ordinary sign-in sessions.

## Example

### Request (GET)
```
GET /srv.asmx/GetWebDavSessions?authenticationTicket=abc123 HTTP/1.1
```

### Request (POST)
```
POST /srv.asmx/GetWebDavSessions HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123
```

## Notes

- Expired sessions are not listed.
- `CreateDiskMountURL` creates the same kind of session; its tickets are listed here too.

## Related APIs

- [CreateWebDavSession](CreateWebDavSession.md) - Create a WebDAV session ticket
- [RemoveWebDavSession](RemoveWebDavSession.md) - Remove a WebDAV session ticket
- [CreateDiskMountURL](CreateDiskMountURL.md) - Create a WebDAV session and return only its mount path

## Error Codes

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is none |
| `4030` | the caller is signed in anonymously |
