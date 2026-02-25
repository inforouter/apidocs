# GetAccessList API

Returns the current access list (security settings) for a document or folder at the specified path.

## Endpoint

```
/srv.asmx/GetAccessList
```

## Methods

- **GET** `/srv.asmx/GetAccessList?authenticationTicket=...&Path=...`
- **POST** `/srv.asmx/GetAccessList` (form data)
- **SOAP** Action: `http://tempuri.org/GetAccessList`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full path to the document or folder. |

---

## Response

### Success Response

```xml
<response success="true">
  <AccessList DateApplied="2024-06-15T10:30:00" AppliedBy="admin" InheritedSecurity="false">
    <Anonymous Right="0" Description="No Access" />
    <DomainMembers Right="2" Description="Read" />
    <UserGroup DomainName="Finance" GroupName="Managers" Right="6" Description="Full Control" />
    <UserGroup DomainName="" GroupName="AllStaff" Right="4" Description="Add &amp; Read" />
    <User DomainName="Finance" UserName="jsmith" Right="5" Description="Change" />
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
| `DateApplied` | The date and time when this access list was last applied. |
| `AppliedBy` | The username of the person who last modified the access list. |
| `InheritedSecurity` | `true` if the item inherits security from its parent; `false` if it has a custom access list. |

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
GET /srv.asmx/GetAccessList
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports/Q4Report.pdf
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetAccessList HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance/Reports/Q4Report.pdf
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetAccessList>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:Path>/Finance/Reports/Q4Report.pdf</tns:Path>
    </tns:GetAccessList>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Returns the **current** access list only (no history). To also retrieve historical access list entries, use `GetAccessListHistory`.
- If `InheritedSecurity="true"`, the item does not have a custom access list and inherits from its parent folder.
- Global user groups have an empty `DomainName` attribute.
- To modify the access list, use `SetAccessList`.
- To revert to inherited security, use `ApplyInheritedAccessList`.

---

## Related APIs

- [GetAccessListHistory](GetAccessListHistory.md) - Get the current access list plus historical changes
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

*For detailed documentation visit: https://support.inforouter.com/api-docs/GetAccessList*
