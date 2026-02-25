# UpdateUserGroupName API

Updates the name of the specified infoRouter user group.

## Endpoint

```
/srv.asmx/UpdateUserGroupName
```

## Methods

- **GET** `/srv.asmx/UpdateUserGroupName?authenticationTicket=...&DomainName=...&GroupName=...&NewGroupName=...`
- **POST** `/srv.asmx/UpdateUserGroupName` (form data)
- **SOAP** Action: `http://tempuri.org/UpdateUserGroupName`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DomainName` | string | No | The domain/library name if the group is a local group. Pass empty or null for global groups. |
| `GroupName` | string | Yes | The current name of the user group to rename. |
| `NewGroupName` | string | Yes | The new name for the user group. |

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

**Domain manager or system administrator.** The calling user must be a manager of the domain containing the group, or a system administrator for global groups.

---

## Example

### GET Request (rename local group)

```
GET /srv.asmx/UpdateUserGroupName
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DomainName=Finance
  &GroupName=FinanceAdmins
  &NewGroupName=FinanceManagers
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/UpdateUserGroupName HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&DomainName=Finance
&GroupName=FinanceAdmins
&NewGroupName=FinanceManagers
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:UpdateUserGroupName>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:DomainName>Finance</tns:DomainName>
      <tns:GroupName>FinanceAdmins</tns:GroupName>
      <tns:NewGroupName>FinanceManagers</tns:NewGroupName>
    </tns:UpdateUserGroupName>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- This method only renames the group. The member visibility (`public`/`showMembers`) setting is not changed.
- To rename the group and also update the member visibility setting, use `UpdateUserGroupName1`.
- Pass empty `DomainName` or null for global groups.

---

## Related APIs

- [UpdateUserGroupName1](UpdateUserGroupName1.md) - Rename a group and update member visibility
- [GetUserGroup](GetUserGroup.md) - Get current group properties

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Group not found | The specified group does not exist. |
| Group name already exists | The `NewGroupName` conflicts with an existing group. |
| Access denied | The calling user lacks permission to manage this group. |
| `SystemError:...` | An unexpected server-side error occurred. |

---