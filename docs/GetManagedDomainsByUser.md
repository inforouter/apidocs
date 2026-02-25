# GetManagedDomainsByUser API

Returns the list of domains/libraries that the specified user has management (administration) rights on. If the calling user has the `ListLibrariesForAdministration` system right and is querying themselves, all libraries are returned. Otherwise, only libraries where the specified user is listed as a domain manager are returned.

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
| `userName` | string | Yes | The username of the user whose managed domains to retrieve |

## Response

### Success Response

```xml
<root success="true">
  <domains>
    <domain DomainID="1" DomainName="MyLibrary" AnonymousDomain="FALSE" IsArchive="FALSE" IsHidden="FALSE" WelcomeMessage="Welcome to MyLibrary" />
    <domain DomainID="5" DomainName="HRDocuments" AnonymousDomain="FALSE" IsArchive="TRUE" IsHidden="FALSE" WelcomeMessage="" />
    <!-- ... additional domain elements ... -->
  </domains>
</root>
```

### Response Attributes

Each `<domain>` element contains the following attributes:

| Attribute | Type | Description |
|-----------|------|-------------|
| `DomainID` | int | Unique identifier of the domain/library |
| `DomainName` | string | Name of the domain/library |
| `AnonymousDomain` | string | `TRUE` if anonymous access is enabled, `FALSE` otherwise |
| `IsArchive` | string | `TRUE` if this is an archive domain, `FALSE` otherwise |
| `IsHidden` | string | `TRUE` if the domain is hidden, `FALSE` otherwise |
| `WelcomeMessage` | string | Welcome message configured for the domain (may be empty) |

### Error Response

```xml
<root success="false" error="[ErrorCode] Error message" />
```

## Required Permissions

The caller must be authenticated. The results are scoped based on the caller's privileges:
- If the caller has the **ListLibrariesForAdministration** system right and is querying their own account, all libraries are returned.
- If the caller is querying another user and has the **ListLibrariesForAdministration** right, only libraries where the specified user is a domain manager are returned.
- If the caller is querying another user and does **not** have the **ListLibrariesForAdministration** right, an error is returned.

## Example

### Request (GET)

```
GET /srv.asmx/GetManagedDomainsByUser?authenticationTicket=abc123-def456&userName=jsmith HTTP/1.1
```

### Request (POST)

```
POST /srv.asmx/GetManagedDomainsByUser HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&userName=jsmith
```

### Request (SOAP 1.1)

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

- This API returns only domains of type "library" (not system domains)
- If the user manages no domains, the `<domains>` element will be empty
- When querying another user without the `ListLibrariesForAdministration` right, an error response is returned
- Compare with `GetDomainMembershipsOfUser` which returns domains the user is a **member** of, regardless of management rights
