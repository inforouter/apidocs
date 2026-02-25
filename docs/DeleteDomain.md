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

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `[1573] Only the system administrator can perform this operation` | The calling user is not a system administrator. |
| `[115] Domain not found` | The specified DomainName does not exist. |
| `SystemError:...` | An unexpected server-side error occurred. |

---