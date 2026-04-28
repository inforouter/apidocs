# GetAddIns API

Returns a list of all infoRouter client add-ins available on the server, including name, setup version, DLL version, and description.

## Endpoint

```
/srv.asmx/GetAddIns
```

## Methods

- **GET** `/srv.asmx/GetAddIns?authenticationTicket=...`
- **POST** `/srv.asmx/GetAddIns` (form data)
- **SOAP** Action: `http://tempuri.org/GetAddIns`

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
GET /srv.asmx/GetAddIns?authenticationTicket=abc123 HTTP/1.1
```

### Request (POST)

```
POST /srv.asmx/GetAddIns HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetAddIns"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetAddIns xmlns="http://tempuri.org/">
      <authenticationTicket>abc123</authenticationTicket>
    </GetAddIns>
  </soap:Body>
</soap:Envelope>
```

## Error Codes

| Error | Description |
|-------|-------------|
| `[901] Session expired or Invalid ticket` | Invalid or expired authentication ticket |

## Notes

- Only add-ins that have a non-empty `Version` entry in their `info.ini` file are included.
- The legacy `office` add-in directory is always excluded from the list.
- Add-in metadata is read from `<ApplicationDirectory>/Add-ins/<AddinName>/info.ini`, section `[info]`, keys `Version`, `DLLVersion`, `Description`.

## Related APIs

- `GetAddInInfo` — Get version and description for a single named add-in
- `GetAddInPart` — Download the installation package for a single named add-in
