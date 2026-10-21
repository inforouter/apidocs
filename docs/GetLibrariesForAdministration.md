# GetLibrariesForAdministration API

Returns the domains/libraries the calling user may administer, whether or not they belong to them: every library in the system, hidden and archived ones included, for an administrator, a member of `[User Managers]` or a member of `[Policy Managers]`; the libraries they manage for a library manager; an empty list for anyone else. Sorted alphabetically by domain name. New in 9.0.

[GetDomains](GetDomains.md) answers only the libraries the caller belongs to, whatever their role, so a User Manager had no way to list the libraries they can put users into, make someone a manager of, or set the policies of. This is that list.

## Endpoint

```
/srv.asmx/GetLibrariesForAdministration
```

## Methods

- **GET** `/srv.asmx/GetLibrariesForAdministration?authenticationTicket=...`
- **POST** `/srv.asmx/GetLibrariesForAdministration` (form data)
- **SOAP** Action: `http://tempuri.org/GetLibrariesForAdministration`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |

---

## Response

### Success Response

Returns a `<domains>` collection with one `<domain>` element per library, the same element [GetDomains](GetDomains.md) writes, sorted alphabetically by name.

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
            DomainName="Management"
            AnonymousDomain="FALSE"
            IsArchive="FALSE"
            IsHidden="TRUE"
            WelcomeMessage="" />
  </domains>
</response>
```

A caller with nothing to administer gets an empty collection, not an error:

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

Any **authenticated user** can call this API; what it answers depends on who calls:

| Caller | Answer |
|---|---|
| An administrator, a member of `[User Managers]`, a member of `[Policy Managers]` | every library |
| A manager of one or more libraries | the libraries they manage |
| Anyone else | an empty list |

Anonymous (unauthenticated) callers are refused. See [AdministrativeRoles](AdministrativeRoles.md) for the roles.

---

## Example

### GET Request

```
GET /srv.asmx/GetLibrariesForAdministration
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetLibrariesForAdministration HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetLibrariesForAdministration>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
    </tns:GetLibrariesForAdministration>
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

The list for a page that manages users, memberships, managers or policies: the libraries the signed-in
user may act on, rather than the ones they happen to belong to.

```javascript
const root = await call('GetLibrariesForAdministration', { authenticationTicket: ticket });
const libraries = [...root.querySelectorAll('domain')].map(d => d.getAttribute('DomainName'));
```

An empty list means the caller has no library to administer; it is not an error.

## Notes

- Membership plays no part. A User Manager who belongs to no library at all still gets every library.
- Archived and hidden libraries are included; the recycle bin's internal domain is not.
- Library managers are not a role group: a user is a manager of a particular library ([AddManagerToDomain](AddManagerToDomain.md)), and gets those libraries here.
- Which action the caller may then take on a library is still decided call by call; see [AdministrativeRoles](AdministrativeRoles.md).

---

## Related APIs

- [GetDomains](GetDomains.md) - The libraries the caller belongs to, plus the ones open to anonymous users
- [GetMemberDomains](GetMemberDomains.md) - The libraries the caller belongs to
- [GetManagedDomainsByUser](GetManagedDomainsByUser.md) - The libraries a named user manages
- [AdministrativeRoles](AdministrativeRoles.md) - The role groups and what each unlocks

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
