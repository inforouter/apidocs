# GetAccessListHistory API

Returns the current access list plus the historical access list records for a document or folder at the specified path.

## Endpoint

```
/srv.asmx/GetAccessListHistory
```

## Methods

- **GET** `/srv.asmx/GetAccessListHistory?authenticationTicket=...&Path=...`
- **POST** `/srv.asmx/GetAccessListHistory` (form data)
- **SOAP** Action: `http://tempuri.org/GetAccessListHistory`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full path to the document or folder. |

---

## Response

### Success Response

The response contains the current access list followed by zero or more historical access list entries, each as a separate `<AccessList>` element ordered from newest to oldest.

```xml
<response success="true">
  <!-- Current access list -->
  <AccessList DateApplied="2024-06-15T10:30:00" AppliedBy="admin" InheritedSecurity="false">
    <Anonymous Right="0" Description="No Access" />
    <DomainMembers Right="2" Description="Read" />
    <UserGroup DomainName="Finance" GroupName="Managers" Right="6" Description="Full Control" />
    <User DomainName="Finance" UserName="jsmith" Right="5" Description="Change" />
  </AccessList>
  <!-- Historical access list (previous version) -->
  <AccessList DateApplied="2024-01-10T08:00:00" AppliedBy="manager1" InheritedSecurity="false">
    <DomainMembers Right="4" Description="Add &amp; Read" />
    <UserGroup DomainName="Finance" GroupName="Managers" Right="6" Description="Full Control" />
  </AccessList>
</response>
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

### Access List Element Attributes

| Attribute | Description |
|-----------|-------------|
| `DateApplied` | The date and time when this access list version was applied. |
| `AppliedBy` | The username of the person who applied this version. |
| `InheritedSecurity` | `true` if this version represented inherited security; `false` if it was a custom access list. |

### Access List Child Elements

| Element | Attributes | Description |
|---------|-----------|-------------|
| `Anonymous` | `Right`, `Description` | Access granted to anonymous (unauthenticated) users. |
| `DomainMembers` | `Right`, `Description` | Access granted to all authenticated domain members. |
| `UserGroup` | `DomainName`, `GroupName`, `Right`, `Description` | Access granted to a specific user group. |
| `User` | `DomainName`, `UserName`, `Right`, `Description` | Access granted to a specific user. |

### Right Values

| Right | Description |
|-------|-------------|
| `0` | No Access |
| `1` | List |
| `2` | Read |
| `3` | Add |
| `4` | Add & Read |
| `5` | Change |
| `6` | Full Control |

---

## Required Permissions

**Read security access list permission** (ActionId 26) on the target document or folder.

---

## Example

### GET Request

```
GET /srv.asmx/GetAccessListHistory
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports/Q4Report.pdf
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetAccessListHistory HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance/Reports/Q4Report.pdf
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetAccessListHistory>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:Path>/Finance/Reports/Q4Report.pdf</tns:Path>
    </tns:GetAccessListHistory>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- The first `<AccessList>` element in the response is always the **current** access list.
- Subsequent `<AccessList>` elements are historical records from previous security changes.
- If there are no historical records, only the current access list is returned.
- To retrieve only the current access list (without history), use `GetAccessList`.
- Global user groups have an empty `DomainName` attribute.

---

## Related APIs

- [GetAccessList](GetAccessList.md) - Get only the current access list
- [SetAccessList](SetAccessList.md) - Set the access list for a document or folder
- [ApplyInheritedAccessList](ApplyInheritedAccessList.md) - Revert to inherited security
- [GetOwner](GetOwner.md) - Get the owner of a document or folder

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Path not found | The specified document or folder does not exist. |
| Access denied | The calling user lacks permission to read the security access list. |
| `SystemError:...` | An unexpected server-side error occurred. |

---