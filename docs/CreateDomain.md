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

## JavaScript

Every call answers XML with HTTP 200, success or not, so `success` is the thing to branch on and
`errorCode` is the number to report.

```javascript
async function call(action, params) {
  const response = await fetch(`/srv.asmx/${action}?${new URLSearchParams(params)}`);
  const root = new DOMParser()
    .parseFromString(await response.text(), 'text/xml')
    .documentElement;

  if (root.getAttribute('success') !== 'true') {
    throw new Error(`${root.getAttribute('errorCode')}: ${root.getAttribute('error')}`);
  }
  return root;
}
```

Makes a library.

```javascript
await call('CreateDomain', {
  authenticationTicket: ticket,
  DomainName: 'Finance',
  Anonymous: false,      // readable without signing in
  Hidden: false,         // hidden from the library list
  WelcomeMessage: 'Finance department documents'
});
```

**Whoever creates a library is a member of it**, without being added - which matters, because a
library with no members is unreachable. Creating one is an administrator's job: a caller without those
rights is refused `4030`, not `4010`.

A name carrying a special character is **refused** with `4000`, unlike a folder name, which is
silently cleaned up.

A **library** and a **domain** are the same thing. The operations are named Domain, the messages say
library, and the XML element is `<domain>`. Its flags come back as the words `TRUE` and `FALSE` rather
than `true`/`false`.

> **A library must keep a member.** Removing the last one is refused with `4000`: a library
> is visible only to its members, so one with nobody in it cannot be reached by anyone, a
> system administrator included, and no operation on it - `DeleteDomain` among them - would
> work again. A member group counts only for the people in it.

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

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4030` | the caller is not a system administrator |
| `4090` | a library of that name already exists |
| `4000` | `DomainName` carries a character a library name may not |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `[1573] Only the system administrator can perform this operation` | The calling user is not a system administrator. |
| Domain already exists | A domain with the specified DomainName already exists. |
| Invalid domain name | The domain name contains invalid characters or is too long. |
| `SystemError:...` | An unexpected server-side error occurred. |

---