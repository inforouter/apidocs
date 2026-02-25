# UpdateDomain API

Updates the properties of an existing domain/library, including its name, anonymous access setting, visibility, and welcome message.

## Endpoint

```
/srv.asmx/UpdateDomain
```

## Methods

- **GET** `/srv.asmx/UpdateDomain?authenticationTicket=...&DomainName=...&NewDomainName=...&Anonymous=...&Hidden=...&WelcomeMessage=...`
- **POST** `/srv.asmx/UpdateDomain` (form data)
- **SOAP** Action: `http://tempuri.org/UpdateDomain`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DomainName` | string | Yes | Current name of the domain/library to update. |
| `NewDomainName` | string | Yes | New name for the domain/library. Pass the same value as `DomainName` to keep the current name. |
| `Anonymous` | bool | Yes | If `true`, enables anonymous (guest) access to the domain. If `false`, requires authenticated membership. |
| `Hidden` | bool | Yes | If `true`, hides the domain from regular library listings. If `false`, the domain appears in listings. |
| `WelcomeMessage` | string | No | New welcome or description message for the domain. Pass empty string or null to clear the existing message. |

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

**Domain manager or system administrator.** The calling user must be a manager of the target domain or a system administrator.

---

## Example

### GET Request (rename domain and update welcome message)

```
GET /srv.asmx/UpdateDomain
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DomainName=Finance
  &NewDomainName=FinanceDepartment
  &Anonymous=false
  &Hidden=false
  &WelcomeMessage=Finance+Department+Document+Repository
HTTP/1.1
```

### GET Request (hide domain without renaming)

```
GET /srv.asmx/UpdateDomain
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DomainName=Finance
  &NewDomainName=Finance
  &Anonymous=false
  &Hidden=true
  &WelcomeMessage=
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/UpdateDomain HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&DomainName=Finance
&NewDomainName=Finance
&Anonymous=false
&Hidden=false
&WelcomeMessage=Updated+welcome+message
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:UpdateDomain>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:DomainName>Finance</tns:DomainName>
      <tns:NewDomainName>FinanceDepartment</tns:NewDomainName>
      <tns:Anonymous>false</tns:Anonymous>
      <tns:Hidden>false</tns:Hidden>
      <tns:WelcomeMessage>Finance Department Document Repository</tns:WelcomeMessage>
    </tns:UpdateDomain>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- To keep the current name unchanged, pass the same value in both `DomainName` and `NewDomainName`.
- If `NewDomainName` is different from `DomainName`, it must not conflict with an existing domain name.
- All parameters (name, anonymous, hidden, welcome message) are updated in a single call -" there is no way to update only one property.
- The `WelcomeMessage` supports multi-line text; newlines are preserved.
- To archive/unarchive a domain, use `ArchiveDomain` and `UnarchiveDomain` instead.

---

## Related APIs

- [GetDomain](GetDomain.md) - Get current properties of the domain
- [CreateDomain](CreateDomain.md) - Create a new domain
- [ArchiveDomain](ArchiveDomain.md) - Archive (deactivate) a domain
- [UnarchiveDomain](UnarchiveDomain.md) - Unarchive a domain

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `[115] Domain not found` | The specified DomainName does not exist. |
| Domain name already exists | The specified NewDomainName conflicts with an existing domain. |
| Access denied | The calling user is not a manager of this domain. |
| `SystemError:...` | An unexpected server-side error occurred. |

---