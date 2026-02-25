# GetDomains API

Returns a list of all infoRouter domains/libraries in the system, sorted alphabetically by domain name. Includes all domains regardless of archive or hidden status.

## Endpoint

```
/srv.asmx/GetDomains
```

## Methods

- **GET** `/srv.asmx/GetDomains?authenticationTicket=...`
- **POST** `/srv.asmx/GetDomains` (form data)
- **SOAP** Action: `http://tempuri.org/GetDomains`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |

---

## Response

### Success Response

Returns a `<domains>` collection with one `<domain>` element per domain, sorted alphabetically by name.

```xml
<response success="true" error="">
  <domains>
    <domain DomainID="123"
            DomainName="Finance"
            AnonymousDomain="FALSE"
            IsArchive="FALSE"
            IsHidden="FALSE"
            WelcomeMessage="Finance department documents" />
    <domain DomainID="456"
            DomainName="HR"
            AnonymousDomain="FALSE"
            IsArchive="FALSE"
            IsHidden="FALSE"
            WelcomeMessage="" />
    <domain DomainID="789"
            DomainName="OldProjects"
            AnonymousDomain="FALSE"
            IsArchive="TRUE"
            IsHidden="FALSE"
            WelcomeMessage="Archived project files" />
  </domains>
</response>
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

---

## Domain Element Attributes

| Attribute | Description |
|-----------|-------------|
| `DomainID` | Unique numeric ID of the domain. |
| `DomainName` | Name of the domain/library. |
| `AnonymousDomain` | `TRUE` if anonymous (guest) access is allowed; `FALSE` otherwise. |
| `IsArchive` | `TRUE` if the domain is archived (offline); `FALSE` if active. |
| `IsHidden` | `TRUE` if the domain is hidden from regular library listings; `FALSE` otherwise. |
| `WelcomeMessage` | The domain's configured welcome/description message. May be empty. |

---

## Required Permissions

Any **authenticated user** can call this API.

---

## Example

### GET Request

```
GET /srv.asmx/GetDomains
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetDomains HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetDomains>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
    </tns:GetDomains>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Returns **all** domains including archived (`IsArchive="TRUE"`) and hidden (`IsHidden="TRUE"`) domains.
- Results are sorted alphabetically by domain name.
- To get only the domains where the calling user is a member, use `GetMemberDomains`.
- To get the memberships of a specific user, use `GetDomainMembershipsOfUser`.
- For large installations with many domains, this call may return a substantial list.

---

## Related APIs

- [GetMemberDomains](GetMemberDomains.md) - Get domains where the current user is a member
- [GetDomain](GetDomain.md) - Get properties of a single domain
- [DomainExists](DomainExists.md) - Check if a specific domain exists
- [CreateDomain](CreateDomain.md) - Create a new domain
- [ArchiveDomain](ArchiveDomain.md) - Archive a domain

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `SystemError:...` | An unexpected server-side error occurred. |

---