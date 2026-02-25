# GetDomain API

Returns the properties of the specified domain/library, including its ID, name, visibility settings, archive status, and welcome message.

## Endpoint

```
/srv.asmx/GetDomain
```

## Methods

- **GET** `/srv.asmx/GetDomain?authenticationTicket=...&DomainName=...`
- **POST** `/srv.asmx/GetDomain` (form data)
- **SOAP** Action: `http://tempuri.org/GetDomain`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DomainName` | string | Yes | Name of the domain/library whose properties to retrieve. |

---

## Response

### Success Response

Returns a single `<domain>` element nested inside the response.

```xml
<response success="true" error="">
  <domain DomainID="123"
          DomainName="Finance"
          AnonymousDomain="FALSE"
          IsArchive="FALSE"
          IsHidden="FALSE"
          WelcomeMessage="Welcome to the Finance Library" />
</response>
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

---

## Domain Element Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `DomainID` | int | Unique numeric identifier for the domain. |
| `DomainName` | string | The name of the domain/library. |
| `AnonymousDomain` | string | `TRUE` if the domain allows anonymous (unauthenticated) access; `FALSE` otherwise. |
| `IsArchive` | string | `TRUE` if the domain is archived (offline); `FALSE` if active. |
| `IsHidden` | string | `TRUE` if the domain is hidden from regular library listings; `FALSE` otherwise. |
| `WelcomeMessage` | string | The welcome or description message configured for the domain. May be empty. |

---

## Required Permissions

Any **authenticated user** can call this API. The domain does not need to be a member domain of the calling user.

---

## Example

### GET Request

```
GET /srv.asmx/GetDomain
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DomainName=Finance
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetDomain HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&DomainName=Finance
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetDomain>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:DomainName>Finance</tns:DomainName>
    </tns:GetDomain>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- This API returns domain metadata only — it does not return members, managers, or folder/document listings.
- Use `GetDomainMembers` to retrieve the domain's membership list.
- Use `GetManagers` to retrieve the domain's manager list.
- Use `GetDomains` to list all domains and check their archive/hidden status.
- `IsArchive="TRUE"` indicates the domain has been archived using the `ArchiveDomain` API.

---

## Related APIs

- [GetDomains](GetDomains.md) - Get a list of all domains in the system
- [UpdateDomain](UpdateDomain.md) - Update domain properties
- [GetDomainMembers](GetDomainMembers.md) - Get the domain's member list
- [GetManagers](GetManagers.md) - Get the domain's manager list
- [DomainExists](DomainExists.md) - Check if a domain exists

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `[115] Domain not found` | The specified DomainName does not exist. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/GetDomain*
