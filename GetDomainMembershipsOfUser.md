# GetDomainMembershipsOfUser API

Returns a list of all domain/library memberships for the specified user. Shows every domain the user has access to as a member, sorted alphabetically by domain name.

## Endpoint

```
/srv.asmx/GetDomainMembershipsOfUser
```

## Methods

- **GET** `/srv.asmx/GetDomainMembershipsOfUser?authenticationTicket=...&userName=...`
- **POST** `/srv.asmx/GetDomainMembershipsOfUser` (form data)
- **SOAP** Action: `http://tempuri.org/GetDomainMembershipsOfUser`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `userName` | string | Yes | Username of the user whose domain memberships to retrieve. |

---

## Response

### Success Response

Returns a `<domains>` collection with one `<domain>` element per membership.

```xml
<response success="true" error="">
  <domains>
    <domain DomainID="123" DomainName="Finance"
            AnonymousDomain="FALSE" IsArchive="FALSE"
            IsHidden="FALSE" WelcomeMessage="Welcome to the Finance Library" />
    <domain DomainID="456" DomainName="HR"
            AnonymousDomain="FALSE" IsArchive="FALSE"
            IsHidden="FALSE" WelcomeMessage="" />
    <domain DomainID="789" DomainName="Projects"
            AnonymousDomain="FALSE" IsArchive="FALSE"
            IsHidden="FALSE" WelcomeMessage="Active project documents" />
  </domains>
</response>
```

If the user has no domain memberships, the `<domains>` element is empty:

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
| `DomainID` | Unique numeric ID of the domain/library. |
| `DomainName` | Name of the domain/library. |
| `AnonymousDomain` | `TRUE` if the domain allows anonymous (guest) access, `FALSE` otherwise. |
| `IsArchive` | `TRUE` if the domain is archived (offline), `FALSE` if it is active. |
| `IsHidden` | `TRUE` if the domain is hidden from regular library listings, `FALSE` otherwise. |
| `WelcomeMessage` | The welcome/description message configured for the domain, or empty string if none. |

---

## Required Permissions

Any **authenticated user** can call this API. A user can retrieve their own memberships as well as other users' memberships.

---

## Example

### GET Request

```
GET /srv.asmx/GetDomainMembershipsOfUser
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &userName=jdoe
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetDomainMembershipsOfUser HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&userName=jdoe
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetDomainMembershipsOfUser>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:userName>jdoe</tns:userName>
    </tns:GetDomainMembershipsOfUser>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Results are sorted alphabetically by domain name.
- Includes both direct memberships and memberships acquired through user group membership.
- Archived (`IsArchive="TRUE"`) and hidden (`IsHidden="TRUE"`) domains are included in the results.
- The `WelcomeMessage` attribute contains the domain's configured welcome/description text, which may be empty.

---

## Related APIs

- [GetDomains](GetDomains) - Get the list of all domains in the system
- [AddUserAsDomainMember](AddUserAsDomainMember) - Add a user to a domain
- [RemoveUserFromDomainMembership](RemoveUserFromDomainMembership) - Remove a user from a domain
- [GetMemberDomains](GetMemberDomains) - Get the current user's member domains

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| User not found | The specified userName does not exist in the system. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/GetDomainMembershipsOfUser*
