# DomainExists API

Determines whether a domain/library with the given name exists in the infoRouter system. Returns success if the domain exists, or an error if it does not.

## Endpoint

```
/srv.asmx/DomainExists
```

## Methods

- **GET** `/srv.asmx/DomainExists?authenticationTicket=...&DomainName=...`
- **POST** `/srv.asmx/DomainExists` (form data)
- **SOAP** Action: `http://tempuri.org/DomainExists`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DomainName` | string | Yes | Name of the domain/library to check for existence. |

---

## Response

### Success Response (domain exists)

```xml
<response success="true" error="" />
```

### Error Response (domain does not exist)

```xml
<response success="false" error="[115] Domain not found" />
```

---

## Required Permissions

Any **authenticated user** can call this API.

---

## Example

### GET Request

```
GET /srv.asmx/DomainExists
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DomainName=Finance
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/DomainExists HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&DomainName=Finance
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:DomainExists>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:DomainName>Finance</tns:DomainName>
    </tns:DomainExists>
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

Asks whether a library exists.

```javascript
async function libraryExists(name) {
  const response = await fetch('/srv.asmx/DomainExists?' + new URLSearchParams({
    authenticationTicket: ticket, DomainName: name
  }));
  const root = new DOMParser().parseFromString(await response.text(), 'text/xml').documentElement;

  if (root.getAttribute('success') === 'true') return true;
  if (root.getAttribute('errorCode') === '4000') return false;   // note: 4000, not 4041

  throw new Error(root.getAttribute('error'));
}
```

It answers by succeeding or failing rather than with a boolean. **The code for "no such library" is
`4000` here and `4041` from [GetDomain](GetDomain.md)**, although both carry the same message - so a
client checking both has to accept either.

A library the caller cannot see is reported the same way as one that does not exist.

A **library** and a **domain** are the same thing. The operations are named Domain, the messages say
library, and the XML element is `<domain>`. Its flags come back as the words `TRUE` and `FALSE` rather
than `true`/`false`.

## Notes

- The check is **case-insensitive** -" `Finance` and `finance` are treated as the same domain name.
- This API does not check whether the calling user has access to the domain -" it only checks for existence.
- Archived and hidden domains are found by this check -" `success="true"` is returned for them as well.
- To get the full properties of the domain, use `GetDomain`.

---

## Related APIs

- [GetDomain](GetDomain.md) - Get full properties of the specified domain
- [GetDomains](GetDomains.md) - Get the list of all domains in the system
- [CreateDomain](CreateDomain.md) - Create a new domain if it doesn't exist

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4000` | no library by that name - note this is `4000`, where `GetDomain` answers `4041` |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `[115] Domain not found` | The specified DomainName does not exist. |
| `SystemError:...` | An unexpected server-side error occurred. |

---