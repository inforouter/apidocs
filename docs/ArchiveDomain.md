# ArchiveDomain API

Archives a domain/library, changing its status to make it an archived (offline) library. Archived libraries are typically hidden from regular user access and searches, used for long-term storage of inactive projects or historical data.

## Endpoint

```
/srv.asmx/ArchiveDomain
```

## Methods

- **GET** `/srv.asmx/ArchiveDomain?authenticationTicket=...&domainName=...`
- **POST** `/srv.asmx/ArchiveDomain` (form data)
- **SOAP** Action: `http://tempuri.org/ArchiveDomain`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `domainName` | string | Yes | Name of the domain/library to archive. |

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

**Administrator only**. Only the system administrator can archive domains/libraries. Non-administrator users will receive an error even if they are domain managers.

---

## Example

### GET Request

```
GET /srv.asmx/ArchiveDomain
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &domainName=OldProjects
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/ArchiveDomain HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&domainName=OldProjects
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:ArchiveDomain>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:DomainName>OldProjects</tns:DomainName>
    </tns:ArchiveDomain>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- **Administrator Requirement**: Only users with system administrator privileges can archive domains. This operation is restricted even from domain managers.
- **Checked-Out Documents Validation**: The API will **fail** if the domain contains any checked-out documents. All documents must be checked in before archiving.
- **Already Archived Check**: The API will return an error if the specified domain is already archived.
- **Immediate Effect**: Once archived, the domain becomes immediately hidden from regular user searches and may become read-only depending on system configuration.
- **No Data Loss**: Archiving does not delete any documents, folders, or metadata — it only changes the library's visibility and access status.
- **Search Scope**: Archived libraries are excluded from searches when users search with scope set to "InOnlineLibraries". They only appear when explicitly searching "InArchivedLibraries" or "InAllLibraries".
- **Reversible Operation**: Archives can be reversed using the `UnarchiveDomain` API.

---

## Pre-Archive Checklist

Before archiving a domain, ensure:

1. ✅ All documents are checked in (no checked-out documents)
2. ✅ Users are notified of the pending archive
3. ✅ Active workflows are completed or stopped
4. ✅ Backup/export is completed if required for compliance

---

## Use Cases

1. **Project Completion**: Archive project libraries after project completion to reduce clutter in active library lists.
2. **Seasonal Archives**: Archive libraries that are only needed during specific periods (e.g., annual reports after the fiscal year ends).
3. **Data Retention**: Move historical data to archived status for long-term retention while keeping active libraries focused.
4. **System Performance**: Reduce the active library count to improve system performance and search responsiveness.
5. **Compliance Requirements**: Segregate inactive records for regulatory compliance and retention policies.

---

## Related APIs

- [UnarchiveDomain](UnarchiveDomain.md) - Un-archive a domain/library to make it active again
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
| `[1510]` | The domain is already archived. |
| `[1524]` | The domain contains checked-out documents and cannot be archived until all documents are checked in. |
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
         │ ArchiveDomain() ◄── You are here
         ▼
┌─────────────────┐
│ Archived Domain │
│  (IsArchive=1)  │
└────────┬────────┘
         │
         │ UnarchiveDomain()
         ▼
┌─────────────────┐
│  Online Domain  │
│  (IsArchive=0)  │
└─────────────────┘
```

---

## Validation Rules

The API performs the following validations in order:

1. **Authentication**: Valid authentication ticket required
2. **Authorization**: User must be system administrator
3. **Domain Existence**: Domain name must exist
4. **Archive Status**: Domain must not already be archived
5. **Checked-Out Documents**: Domain must have zero checked-out documents

If any validation fails, the operation is rejected with an appropriate error message.

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/ArchiveDomain*
