# DeleteDomain API

Permanently deletes the specified domain/library and all of its contents, including all folders, documents, versions, and associated data. This operation is irreversible.

## Endpoint

```
/srv.asmx/DeleteDomain
```

## Methods

- **GET** `/srv.asmx/DeleteDomain?authenticationTicket=...&DomainName=...`
- **POST** `/srv.asmx/DeleteDomain` (form data)
- **SOAP** Action: `http://tempuri.org/DeleteDomain`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DomainName` | string | Yes | Name of the domain/library to permanently delete. |

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

**System administrator only.** Only the system administrator can delete domains/libraries.

---

## Example

### GET Request

```
GET /srv.asmx/DeleteDomain
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DomainName=OldProjects
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/DeleteDomain HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&DomainName=OldProjects
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:DeleteDomain>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:DomainName>OldProjects</tns:DomainName>
    </tns:DeleteDomain>
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

Removes a library and everything in it.

```javascript
await call('DeleteDomain', { authenticationTicket: ticket, DomainName: 'Finance' });
```

Deleting one that is not there is `4041`, so a delete that runs twice reports the second attempt.

> **A library must keep a member.** Removing the last one is refused with `4000`: a library
> is visible only to its members, so one with nobody in it cannot be reached by anyone, a
> system administrator included, and no operation on it - `DeleteDomain` among them - would
> work again. A member group counts only for the people in it.

## Notes

- **Irreversible**: Deletion permanently removes all documents, folders, versions, workflow definitions, memberships, and all other data inside the domain. There is no undo.
- **Recycle Bin**: Deleted domain contents do not go to the recycle bin.
- For a non-destructive alternative, consider archiving the domain with `ArchiveDomain` instead of deleting it.
- It is recommended to verify the domain exists with `DomainExists` before attempting deletion.

---

## Related APIs

- [CreateDomain](CreateDomain.md) - Create a new domain/library
- [ArchiveDomain](ArchiveDomain.md) - Archive (deactivate) a domain without deleting it
- [DomainExists](DomainExists.md) - Check if a domain exists before deleting
- [GetDomains](GetDomains.md) - List all domains

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4030` | the caller is not a system administrator |
| `4041` | no library by that name - including one the caller cannot see |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `[1573] Only the system administrator can perform this operation` | The calling user is not a system administrator. |
| `[115] Domain not found` | The specified DomainName does not exist. |
| `SystemError:...` | An unexpected server-side error occurred. |

---