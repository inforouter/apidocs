# CreateDomain API

Creates a new infoRouter domain/library with the specified name and configuration. Domains (also called libraries) are the top-level containers in infoRouter that hold folders, documents, and workflow definitions.

## Endpoint

```
/srv.asmx/CreateDomain
```

## Methods

- **GET** `/srv.asmx/CreateDomain?authenticationTicket=...&DomainName=...&Anonymous=...&Hidden=...&WelcomeMessage=...`
- **POST** `/srv.asmx/CreateDomain` (form data)
- **SOAP** Action: `http://tempuri.org/CreateDomain`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DomainName` | string | Yes | Name for the new domain/library. Must be unique across all domains. |
| `Anonymous` | bool | Yes | If `true`, the domain allows anonymous (guest) access without authentication. If `false`, users must be authenticated members to access the domain. |
| `Hidden` | bool | Yes | If `true`, the domain is hidden from regular library listings and only visible to administrators and members who know the name. |
| `WelcomeMessage` | string | No | Optional welcome or description message for the domain. Pass empty string or null if not needed. |

---

## Response

### Success Response

```xml
<response success="true" error="" />
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

---

## Required Permissions

**System administrator only.** Only the system administrator can create domains/libraries.

---

## Example

### GET Request (public domain with welcome message)

```
GET /srv.asmx/CreateDomain
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DomainName=Finance
  &Anonymous=false
  &Hidden=false
  &WelcomeMessage=Welcome+to+the+Finance+Library
HTTP/1.1
```

### GET Request (hidden anonymous domain)

```
GET /srv.asmx/CreateDomain
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DomainName=PublicResources
  &Anonymous=true
  &Hidden=false
  &WelcomeMessage=
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/CreateDomain HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&DomainName=Finance
&Anonymous=false
&Hidden=false
&WelcomeMessage=Finance department document library
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:CreateDomain>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:DomainName>Finance</tns:DomainName>
      <tns:Anonymous>false</tns:Anonymous>
      <tns:Hidden>false</tns:Hidden>
      <tns:WelcomeMessage>Finance department document library</tns:WelcomeMessage>
    </tns:CreateDomain>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- `DomainName` must be unique; creating a domain with an existing name returns an error.
- After creation, use `AddUserAsDomainMember` or `AddUserGroupAsDomainMember` to populate the domain with members.
- Use `AddManagerToDomain` to assign managers to the new domain.
- The `WelcomeMessage` supports multi-line text; newlines are preserved.
- Use `CreateFolder` to create sub-folders inside the new domain.
- To check if a domain already exists before creating, use `DomainExists`.

---

## Related APIs

- [DeleteDomain](DeleteDomain.md) - Delete a domain/library
- [UpdateDomain](UpdateDomain.md) - Update domain properties (name, visibility, welcome message)
- [DomainExists](DomainExists.md) - Check if a domain exists
- [AddUserAsDomainMember](AddUserAsDomainMember.md) - Add a user to the new domain
- [GetDomain](GetDomain.md) - Get domain properties

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `[1573] Only the system administrator can perform this operation` | The calling user is not a system administrator. |
| Domain already exists | A domain with the specified DomainName already exists. |
| Invalid domain name | The domain name contains invalid characters or is too long. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/CreateDomain*
