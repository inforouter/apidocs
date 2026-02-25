# CreateDiskMountURL API

Creates a time-limited WebDAV disk mount URL for the currently authenticated user. The returned URL points to the root of the infoRouter WebDAV share and can be used to mount infoRouter as a network drive in Windows Explorer or any WebDAV-capable client. A dedicated DAV session ticket is generated for the URL; the calling user's normal authentication ticket is not embedded in it.

## Endpoint

```
/srv.asmx/CreateDiskMountURL
```

## Methods

- **GET** `/srv.asmx/CreateDiskMountURL?authenticationTicket=...&customExpirationDate=...`
- **POST** `/srv.asmx/CreateDiskMountURL` (form data)
- **SOAP** Action: `http://tempuri.org/CreateDiskMountURL`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `customExpirationDate` | DateTime | Yes | Expiry date and time for the generated WebDAV session ticket. Pass in ISO 8601 format (e.g. `2026-12-31T23:59:59`). UTC values are automatically converted to server local time. Use a far-future date to create a long-lived mount URL. |

## Response

### Success Response

```xml
<response success="true">
  <Value>/dav/sid-3f2504e0-4f89-11d3-9a0c-0305e82c3301/</Value>
</response>
```

| Element / Attribute | Description |
|---------------------|-------------|
| `success` | `true` on success. |
| `Value` | The WebDAV mount path. Prepend the server base URL to form a full mount URL (e.g. `https://yourserver/dav/sid-{ticket}/`). |

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

---

## Required Permissions

- Any **authenticated user** with a valid ticket may call this API.
- No additional document or folder permission is required — the returned URL grants WebDAV access to items the user would normally be permitted to see.
- Anonymous users cannot obtain a WebDAV mount URL.

---

## Example

### GET Request

```
GET /srv.asmx/CreateDiskMountURL?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301&customExpirationDate=2026-12-31T23:59:59 HTTP/1.1
```

### POST Request

```
POST /srv.asmx/CreateDiskMountURL HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&customExpirationDate=2026-12-31T23:59:59
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:CreateDiskMountURL>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:customExpirationDate>2026-12-31T23:59:59</tns:customExpirationDate>
    </tns:CreateDiskMountURL>
  </soap:Body>
</soap:Envelope>
```

### Using the Returned URL

Construct the full mount URL by prepending your server's base address to the `Value` returned in the response:

```
https://yourserver.example.com/dav/sid-3f2504e0-4f89-11d3-9a0c-0305e82c3301/
```

This URL can be mapped as a network drive on Windows:

```
net use Z: "https://yourserver.example.com/dav/sid-3f2504e0-4f89-11d3-9a0c-0305e82c3301/"
```

---

## Notes

- The returned URL is **root-level WebDAV** — it gives access to all domains and folders the user is permitted to browse, not a specific document.
- A **separate DAV session ticket** is created for the URL. This ticket is independent of the caller's authentication ticket and can be handed to a WebDAV client without exposing the original ticket.
- The ticket embedded in the URL expires at `customExpirationDate`. After expiry, the mount URL stops working and a new URL must be requested.
- If `customExpirationDate` is supplied in UTC, the server automatically converts it to local time before creating the ticket.
- To create a URL for editing a **specific document** (e.g. opening a Word file directly in Microsoft Office), use `CreateEditDocumentURL` instead.
- The WebDAV endpoint supports PROPFIND, GET, PUT, LOCK, and UNLOCK operations, enabling full read/write access through compatible clients.

---

## Related APIs

- [CreateEditDocumentURL](CreateEditDocumentURL) - Create a WebDAV editing URL for a specific document
- [GetDocument](GetDocument) - Retrieve document properties including the document path

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/CreateDiskMountURL*
