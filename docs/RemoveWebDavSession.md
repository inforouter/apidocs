# RemoveWebDavSession API

Removes one of the signed-in user's WebDAV session tickets. A drive mapped with the ticket stops working at once: the next request with it is refused.

## Endpoint

```
/srv.asmx/RemoveWebDavSession
```

## Methods

- **GET** `/srv.asmx/RemoveWebDavSession?authenticationTicket=...&ticket=...`
- **POST** `/srv.asmx/RemoveWebDavSession` (form data)
- **SOAP** Action: `http://tempuri.org/RemoveWebDavSession`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `ticket` | string | Yes | The WebDAV session's ticket, as [GetWebDavSessions](GetWebDavSessions.md) lists it. A `sid-` prefix, as in the mount URL, is accepted. |

## Response

### Success Response

```xml
<response success="true" error="" />
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

## Required Permissions

Any authenticated, non-anonymous user, for their own WebDAV sessions only. Another user's WebDAV session, or one of the caller's ordinary sign-in sessions, is answered as not found (`4041`) and left alone; this API cannot end sessions it does not manage, or tell whether a ticket exists. To end the current sign-in use [LogOut](LogOut.md).

## Example

### Request (POST)
```
POST /srv.asmx/RemoveWebDavSession HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&ticket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
```

### Request (GET)
```
GET /srv.asmx/RemoveWebDavSession?authenticationTicket=abc123&ticket=sid-3f2504e0-4f89-11d3-9a0c-0305e82c3301 HTTP/1.1
```

## Notes

- The caller may remove the WebDAV session it is itself signed in with; the call then ends its own session.

## Related APIs

- [GetWebDavSessions](GetWebDavSessions.md) - List the caller's WebDAV session tickets
- [CreateWebDavSession](CreateWebDavSession.md) - Create a WebDAV session ticket
- [LogOut](LogOut.md) - End the current sign-in

## Error Codes

| `errorCode` | When |
|---:|---|
| `4000` | `ticket` is not a ticket |
| `4010` | the authentication ticket is expired or unknown, or there is none |
| `4030` | the caller is signed in anonymously |
| `4041` | `ticket` is not one of the caller's live WebDAV sessions |
