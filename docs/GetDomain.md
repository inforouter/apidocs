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

Reports one library.

```javascript
const root = await call('GetDomain', { authenticationTicket: ticket, DomainName: 'Finance' });
const domain = root.querySelector('domain');

console.log(domain.getAttribute('DomainID'),
            domain.getAttribute('AnonymousDomain'),   // "TRUE" or "FALSE"
            domain.getAttribute('IsArchive'),
            domain.getAttribute('IsHidden'));
```

A **library** and a **domain** are the same thing. The operations are named Domain, the messages say
library, and the XML element is `<domain>`. Its flags come back as the words `TRUE` and `FALSE` rather
than `true`/`false`.

A library the caller cannot see is `4041`, the same as one that does not exist - so an unticketed
caller asking about a library that is not flagged anonymous is told it is missing rather than that it
is private.

## Notes

- This API returns domain metadata only -" it does not return members, managers, or folder/document listings.
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

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | no library by that name - including one the caller cannot see |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `[115] Domain not found` | The specified DomainName does not exist. |
| `SystemError:...` | An unexpected server-side error occurred. |

---