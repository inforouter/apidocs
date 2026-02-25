# GetMemberDomains API

Returns a list of domains/libraries where the currently authenticated user is a member. Results are sorted alphabetically by domain name.

## Endpoint

```
/srv.asmx/GetMemberDomains
```

## Methods

- **GET** `/srv.asmx/GetMemberDomains?authenticationTicket=...`
- **POST** `/srv.asmx/GetMemberDomains` (form data)
- **SOAP** Action: `http://tempuri.org/GetMemberDomains`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |

---

## Response

### Success Response

Returns a `<domains>` collection with one `<domain>` element per member domain, sorted alphabetically by name.

```xml
<response success="true" error="">
  <domains>
    <domain DomainID="123"
            DomainName="Finance"
            AnonymousDomain="FALSE"
            IsArchive="FALSE"
            IsHidden="FALSE"
            WelcomeMessage="Welcome to the Finance Library" />
    <domain DomainID="456"
            DomainName="HR"
            AnonymousDomain="FALSE"
            IsArchive="FALSE"
            IsHidden="FALSE"
            WelcomeMessage="" />
  </domains>
</response>
```

If the user is not a member of any domain, the `<domains>` element is empty:

```xml
<response success="true" error="">
  <domains />
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

Any **authenticated user** can call this API. Anonymous (unauthenticated) users are rejected.

---

## Example

### GET Request

```
GET /srv.asmx/GetMemberDomains
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetMemberDomains HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetMemberDomains>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
    </tns:GetMemberDomains>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Returns only domains where the **currently authenticated user** is a member — both direct memberships and memberships through user groups are included.
- Archived and hidden domains are included in the results if the user is a member.
- Results are sorted alphabetically by domain name.
- To get domain memberships for a **specific user** (not just the calling user), use `GetDomainMembershipsOfUser`.
- To get all domains in the system regardless of membership, use `GetDomains`.

---

## Related APIs

- [GetDomains](GetDomains.md) - Get all domains in the system
- [GetDomainMembershipsOfUser](GetDomainMembershipsOfUser.md) - Get domain memberships for a specific user
- [AddUserAsDomainMember](AddUserAsDomainMember.md) - Add the user to a domain
- [GetDomain](GetDomain.md) - Get properties of a specific domain

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `[2730] Insufficient rights. Anonymous users cannot perform this action.` | The calling user is not authenticated. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/GetMemberDomains*
