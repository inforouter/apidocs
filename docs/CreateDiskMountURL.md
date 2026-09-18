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
| `customExpirationDate` | DateTime | Yes | Expiry date and time for the generated WebDAV session ticket. Pass in ISO 8601 format (e.g. `2026-12-31T23:59:59`). UTC values are automatically converted to server local time. Use a far-future date to create a long-lived mount URL. **Must be in the future**: a date already past is refused with `4000`. |

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

- No additional document or folder permission is required -" the returned URL grants WebDAV access to items the user would normally be permitted to see.

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

## JavaScript

Every call answers XML with HTTP 200, success or not, so `success` is the thing to branch on and
`errorCode` is the number to report.

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

Opens a WebDAV session and returns the path to mount. The answer is a path, not a full URL: prepend
the server address.

```javascript
const root = await call('CreateDiskMountURL', {
  authenticationTicket: ticket,
  customExpirationDate: '2027-01-01'
});

const url = location.origin + root.querySelector('Value').textContent;  // https://host/dav/sid-<guid>/
```

**The expiry is not checked against today.** A date in the past is accepted without complaint and
hands back a mount path that looks exactly like a usable one but is already expired. `customExpirationDate`
binds as a `DateTime`, so a value that is not a date is refused with HTTP 400 before the operation
runs.

## Notes

- The returned URL is **root-level WebDAV** -" it gives access to all domains and folders the user is permitted to browse, not a specific document.

- A **separate DAV session ticket** is created for the URL. This ticket is independent of the caller's authentication ticket and can be handed to a WebDAV client without exposing the original ticket.

- The ticket embedded in the URL expires at `customExpirationDate`. After expiry, the mount URL stops working and a new URL must be requested.

- If `customExpirationDate` is supplied in UTC, the server automatically converts it to local time before creating the ticket.

- To create a URL for editing a **specific document** (e.g. opening a Word file directly in Microsoft Office), use `CreateEditDocumentURL` instead.

- The WebDAV endpoint supports PROPFIND, GET, PUT, LOCK, and UNLOCK operations, enabling full read/write access through compatible clients.

---

## Related APIs

- [CreateEditDocumentURL](CreateEditDocumentURL.md) - Create a WebDAV editing URL for a specific document

- [GetDocument](GetDocument.md) - Retrieve document properties including the document path

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all - the anonymous user is refused |
| `none` | an expiry date in the past is accepted silently |
| `HTTP 400` | `customExpirationDate` was not a date; refused by model binding |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |

---

