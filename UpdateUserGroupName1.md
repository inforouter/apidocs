# UpdateUserGroupName1 API

Updates the name and member visibility setting of the specified infoRouter user group.

## Endpoint

```
/srv.asmx/UpdateUserGroupName1
```

## Methods

- **GET** `/srv.asmx/UpdateUserGroupName1?authenticationTicket=...&DomainName=...&GroupName=...&NewGroupName=...&showMembers=...`
- **POST** `/srv.asmx/UpdateUserGroupName1` (form data)
- **SOAP** Action: `http://tempuri.org/UpdateUserGroupName1`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DomainName` | string | No | The domain/library name if the group is a local group. Pass empty or null for global groups. |
| `GroupName` | string | Yes | The current name of the user group to update. |
| `NewGroupName` | string | Yes | The new name for the user group. Pass the same value as `GroupName` to keep the current name. |
| `showMembers` | bool | Yes | If `true`, group membership is publicly visible to all users. If `false`, membership is private (hidden from non-members). |

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

### GET Request (rename and make membership public)

```
GET /srv.asmx/UpdateUserGroupName1
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DomainName=Finance
  &GroupName=FinanceAdmins
  &NewGroupName=FinanceManagers
  &showMembers=true
HTTP/1.1
```

### GET Request (keep name, make membership private)

```
GET /srv.asmx/UpdateUserGroupName1
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DomainName=Finance
  &GroupName=FinanceAdmins
  &NewGroupName=FinanceAdmins
  &showMembers=false
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/UpdateUserGroupName1 HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&DomainName=Finance
&GroupName=FinanceAdmins
&NewGroupName=FinanceManagers
&showMembers=true
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:UpdateUserGroupName1>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:DomainName>Finance</tns:DomainName>
      <tns:GroupName>FinanceAdmins</tns:GroupName>
      <tns:NewGroupName>FinanceManagers</tns:NewGroupName>
      <tns:ShowMembers>true</tns:ShowMembers>
    </tns:UpdateUserGroupName1>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- To keep the current name unchanged, pass the same value in both `GroupName` and `NewGroupName`.
- The `showMembers` parameter corresponds to the `public` attribute in user group responses: `true` maps to `public="True"`.
- To rename the group without changing the member visibility setting, use `UpdateUserGroupName`.
- Pass empty `DomainName` or null for global groups.

---

## Related APIs

- [UpdateUserGroupName](UpdateUserGroupName) - Rename a group (without changing visibility)
- [GetUserGroup](GetUserGroup) - Get current group properties including `public` setting

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

*For detailed documentation visit: https://support.inforouter.com/api-docs/UpdateUserGroupName1*
