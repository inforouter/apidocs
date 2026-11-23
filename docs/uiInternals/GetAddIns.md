---
search:
  exclude: true
---

# GetAddIns API

**Available in:** infoRouter 9.0 and later

!!! warning "Internal API"
    Made for infoRouter's own user interface. It is not part of the public web API: there is no SOAP
    form and no promise of backward compatibility, and it may change or be removed in any release
    without notice. Do not use it in an integration.

Returns a list of all infoRouter client add-ins available on the server, including name, setup version, DLL version, and description.

## Endpoint

```
/api/UIInternals/GetAddIns
```

## Methods

- **GET** `/api/UIInternals/GetAddIns?authenticationTicket=...`
- **POST** `/api/UIInternals/GetAddIns` (form data)

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |

## Response

### Success

```xml
<root success="true">
  <addins>
    <addin>
      <name>IRCLIENTAPP</name>
      <version>8.2.1</version>
      <dllVersion>8.2.1.0</dllVersion>
      <description>infoRouter Client Application</description>
    </addin>
    <addin>
      <name>WORDADDIN</name>
      <version>8.2.0</version>
      <dllVersion>8.2.0.5</dllVersion>
      <description>infoRouter Word Add-in</description>
    </addin>
  </addins>
</root>
```

| Field | Description |
|-------|-------------|
| `<name>` | Add-in directory name (uppercase) |
| `<version>` | Setup package version read from `info.ini` |
| `<dllVersion>` | DLL version read from `info.ini` |
| `<description>` | Human-readable description read from `info.ini` |

When no add-ins are installed the `<addins>` element is present but empty.

### Error

```xml
<root success="false" error="[901]Session expired or Invalid ticket" />
```

## Required Permissions

- User must be authenticated.

## Example Requests

### Request (GET)

```
GET /api/UIInternals/GetAddIns?authenticationTicket=abc123 HTTP/1.1
```

### Request (POST)

```
POST /api/UIInternals/GetAddIns HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123
```

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |

## JavaScript

Every call answers XML with HTTP 200, success or not, so `success` is the thing to branch on and
`errorCode` is the number to report.

```javascript
async function call(action, params) {
  const response = await fetch(`/api/UIInternals/${action}?${new URLSearchParams(params)}`);
  const root = new DOMParser()
    .parseFromString(await response.text(), 'text/xml')
    .documentElement;

  if (root.getAttribute('success') !== 'true') {
    throw new Error(`${root.getAttribute('errorCode')}: ${root.getAttribute('error')}`);
  }
  return root;
}
```

Lists the client add-ins this server has to offer.

```javascript
const root = await call('GetAddIns', { authenticationTicket: ticket });

for (const addin of root.querySelectorAll('addin')) {
  console.log(addin.querySelector('name').textContent,
              addin.querySelector('version').textContent,
              addin.querySelector('dllVersion').textContent,
              addin.querySelector('description').textContent);
}
```

Read from the folders under `appdir\Add-ins`. A folder with no `Version` in its `info.ini` is
skipped, so every entry listed has one; the shared `Office` folder is passed over by name.

## Notes

- Only add-ins that have a non-empty `Version` entry in their `info.ini` file are included.
- The legacy `office` add-in directory is always excluded from the list.
- Add-in metadata is read from `<ApplicationDirectory>/Add-ins/<AddinName>/info.ini`, section `[info]`, keys `Version`, `DLLVersion`, `Description`.

## Related APIs

- `GetAddInInfo` — Get version and description for a single named add-in
- `GetAddInPart` — Download the installation package for a single named add-in
