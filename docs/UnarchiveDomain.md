# UnarchiveDomain API

Un-archives a previously archived domain/library, making it an active online library again. This operation changes the library's archive status flag, allowing regular user access and document operations to resume.

## Endpoint

```
/srv.asmx/UnarchiveDomain
```

## Methods

- **GET** `/srv.asmx/UnarchiveDomain?authenticationTicket=...&domainName=...`
- **POST** `/srv.asmx/UnarchiveDomain` (form data)
- **SOAP** Action: `http://tempuri.org/UnarchiveDomain`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `domainName` | string | Yes | Name of the domain/library to un-archive. |

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

**Administrator only**. Only the system administrator can un-archive domains/libraries. Non-administrator users will receive an error even if they are domain managers.

---

## Example

### GET Request

```
GET /srv.asmx/UnarchiveDomain
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &domainName=Finance
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/UnarchiveDomain HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&domainName=Finance
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:UnarchiveDomain>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:DomainName>Finance</tns:DomainName>
    </tns:UnarchiveDomain>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- **Administrator Requirement**: Only users with system administrator privileges can un-archive domains. This operation is restricted even from domain managers.
- **Archive Status Check**: The API will return an error if the specified domain is not currently archived (attempting to un-archive an already active domain).
- **Immediate Effect**: Once un-archived, the domain becomes immediately visible and accessible to users who are members of that library.
- **No Data Loss**: Archiving and un-archiving do not delete or modify any documents, folders, or metadata — they only change the library's visibility and access status.
- **Search Scope**: After un-archiving, the library will appear in search results when users search with scope set to "InOnlineLibraries" or "InAllLibraries".
- **User Access**: All existing permissions and memberships remain intact — members can access the library immediately after un-archiving.

---

## Use Cases

1. **Seasonal Access**: Un-archive libraries for active business periods (e.g., tax libraries during tax season).
2. **Project Reactivation**: Restore access to archived project libraries when projects are reopened.
3. **Audit Preparation**: Temporarily un-archive historical libraries for compliance audits.
4. **Data Recovery**: Make archived content accessible again for reference or recovery purposes.

---

## Related APIs

- [ArchiveDomain](ArchiveDomain.md) - Archive a domain/library to make it read-only or hidden
- [GetDomain](GetDomain.md) - Get properties of a domain/library including archive status
- [GetDomains](GetDomains.md) - Get list of all domains/libraries with their archive status
- [UpdateDomain](UpdateDomain.md) - Update other domain properties
- [GetMemberDomains](GetMemberDomains.md) - Get list of member domains (excludes archived by default)

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `[1573] Only the system administrator can perform this operation` | The calling user is not a system administrator. |
| `[1521]` | The domain is not currently archived (cannot un-archive an active domain). |
| `[115] Domain not found` | The specified domainName does not exist. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

## Archive Status Workflow

```
┌─────────────────┐
│  Online Domain  │
│  (IsArchive=0)  │
└────────┬────────┘
         │
         │ ArchiveDomain()
         ▼
┌─────────────────┐
│ Archived Domain │
│  (IsArchive=1)  │
└────────┬────────┘
         │
         │ UnarchiveDomain() ◄── You are here
         ▼
┌─────────────────┐
│  Online Domain  │
│  (IsArchive=0)  │
└─────────────────┘
```

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/UnarchiveDomain*
