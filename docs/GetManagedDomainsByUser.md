# GetManagedDomainsByUser API

Returns the list of domains/libraries that a user has management (administration) rights on. Omitting `userName` retrieves the managed domains of the currently authenticated user. Querying another user's managed domains requires system administrator role.

## Endpoint

```
/srv.asmx/GetManagedDomainsByUser
```

## Methods

- **GET** `/srv.asmx/GetManagedDomainsByUser?authenticationTicket=...&userName=...`
- **POST** `/srv.asmx/GetManagedDomainsByUser` (form data)
- **SOAP** Action: `http://tempuri.org/GetManagedDomainsByUser`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `userName` | string | No | Username whose managed domains to retrieve. Leave empty or omit to retrieve the authenticated user's own managed domains. |

## Response

### Success Response

```xml
<root success="true">
  <domains>
    <domain
      DomainID="1"
      DomainName="Corporate"
      AnonymousDomain="FALSE"
      IsArchive="FALSE"
      IsHidden="FALSE"
      WelcomeMessage="Welcome to the Corporate library" />
    <domain
      DomainID="5"
      DomainName="HRDocuments"
      AnonymousDomain="FALSE"
      IsArchive="FALSE"
      IsHidden="FALSE"
      WelcomeMessage="" />
  </domains>
</root>
```

When the user manages no domains the `<domains>` element is empty:

```xml
<root success="true">
  <domains />
</root>
```

### Error Response

```xml
<root success="false" error="[ErrorCode] Error message" />
```

## Domain Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `DomainID` | int | Unique numeric identifier of the domain/library |
| `DomainName` | string | Name of the domain/library |
| `AnonymousDomain` | TRUE/FALSE | Whether anonymous (unauthenticated) access is enabled on this library |
| `IsArchive` | TRUE/FALSE | Whether this library is an archived (offline) library |
| `IsHidden` | TRUE/FALSE | Whether this library is hidden from the library listing |
| `WelcomeMessage` | string | Welcome message configured for the library (may be empty) |

## Required Permissions

- Any authenticated user may retrieve their **own** managed domains (omit `userName` or pass their own username).
- Retrieving **another user's** managed domains requires **system administrator** role; a non-administrator querying another user receives an access-denied error.

## Example Requests

### Get own managed domains (GET)

```
GET /srv.asmx/GetManagedDomainsByUser?authenticationTicket=abc123-def456 HTTP/1.1
Host: yourserver
```

### Get another user's managed domains (GET)

```
GET /srv.asmx/GetManagedDomainsByUser?authenticationTicket=abc123-def456&userName=jsmith HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/GetManagedDomainsByUser HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&userName=jsmith
```

### SOAP 1.1 Request

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetManagedDomainsByUser"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetManagedDomainsByUser xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
      <userName>jsmith</userName>
    </GetManagedDomainsByUser>
  </soap:Body>
</soap:Envelope>
```

## Notes

- Omitting `userName` (or passing an empty string) returns the managed domains of the currently authenticated user — no elevated permissions required.
- The `userName` field in the SOAP contract is non-nullable; pass an empty string `""` to retrieve the current user's own managed domains via SOAP.
- Compare with [GetDomainMembershipsOfUser](GetDomainMembershipsOfUser.md) which returns domains the user is a **member** of, regardless of management rights.
- Compare with [GetManagers](GetManagers.md) which returns the managers of a specific domain.

## Error Codes

| Error | Description |
|-------|-------------|
| `[901]` | Session expired or invalid authentication ticket |
| `[2840]` | Access denied — system administrator role required to query another user |
| User not found | The specified `userName` does not exist |
