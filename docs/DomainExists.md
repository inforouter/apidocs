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

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `[115] Domain not found` | The specified DomainName does not exist. |
| `SystemError:...` | An unexpected server-side error occurred. |

---