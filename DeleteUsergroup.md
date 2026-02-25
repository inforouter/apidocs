# DeleteUsergroup API

Deletes the specified infoRouter user group.

## Endpoint

```
/srv.asmx/DeleteUsergroup
```

## Methods

- **GET** `/srv.asmx/DeleteUsergroup?authenticationTicket=...&DomainName=...&GroupName=...`
- **POST** `/srv.asmx/DeleteUsergroup` (form data)
- **SOAP** Action: `http://tempuri.org/DeleteUsergroup`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DomainName` | string | No | The domain/library name if the group is a local group. Pass empty or null for global groups. |
| `GroupName` | string | Yes | The name of the user group to delete. |

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

### GET Request (delete local group)

```
GET /srv.asmx/DeleteUsergroup
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DomainName=Finance
  &GroupName=FinanceAdmins
HTTP/1.1
```

### GET Request (delete global group)

```
GET /srv.asmx/DeleteUsergroup
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DomainName=
  &GroupName=OldGlobalGroup
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/DeleteUsergroup HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&DomainName=Finance
&GroupName=FinanceAdmins
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:DeleteUsergroup>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:DomainName>Finance</tns:DomainName>
      <tns:GroupName>FinanceAdmins</tns:GroupName>
    </tns:DeleteUsergroup>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Deleting a user group removes all its memberships and any folder/document permissions assigned to the group. This action cannot be undone.
- Pass empty `DomainName` or null for global groups.
- Members of the group are not deleted — only the group itself is removed.

---

## Related APIs

- [GetUserGroup](GetUserGroup) - Get user group properties before deleting
- [GetUserGroupMembers](GetUserGroupMembers) - Review members before deleting a group
- [AddUsergroupMember](AddUsergroupMember) - Add members to a group

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Group not found | The specified group does not exist. |
| Access denied | The calling user lacks permission to delete this group. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/DeleteUsergroup*
