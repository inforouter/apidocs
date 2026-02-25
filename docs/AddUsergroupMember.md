# AddUsergroupMember API

Adds the specified user to the member list of the specified user group.

## Endpoint

```
/srv.asmx/AddUsergroupMember
```

## Methods

- **GET** `/srv.asmx/AddUsergroupMember?authenticationTicket=...&DomainName=...&GroupName=...&UserName=...`
- **POST** `/srv.asmx/AddUsergroupMember` (form data)
- **SOAP** Action: `http://tempuri.org/AddUsergroupMember`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DomainName` | string | Yes | The domain/library name if the group is a local group. Pass an empty string for global groups. |
| `GroupName` | string | Yes | The name of the user group to add the user to. |
| `UserName` | string | Yes | The username to add to the group. Also accepts the short ID format `ID:userid` (e.g., `ID:123`). |

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

**Domain manager or system administrator.** The calling user must be a manager of the domain containing the group, or a system administrator.

---

## Example

### GET Request (add to local group)

```
GET /srv.asmx/AddUsergroupMember
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DomainName=Finance
  &GroupName=FinanceAdmins
  &UserName=jdoe
HTTP/1.1
```

### GET Request (add to global group)

```
GET /srv.asmx/AddUsergroupMember
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DomainName=
  &GroupName=AllStaff
  &UserName=jdoe
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/AddUsergroupMember HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&DomainName=Finance
&GroupName=FinanceAdmins
&UserName=jdoe
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:AddUsergroupMember>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:DomainName>Finance</tns:DomainName>
      <tns:GroupName>FinanceAdmins</tns:GroupName>
      <tns:UserName>jdoe</tns:UserName>
    </tns:AddUsergroupMember>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- For global groups, pass an empty string for `DomainName`.
- The `UserName` parameter also accepts a short ID reference in the format `ID:userid` (e.g., `ID:123`).
- If the user is already a member of the group, an error is returned.

---

## Related APIs

- [RemoveUsergroupMember](RemoveUsergroupMember.md) - Remove a user from a group
- [GetUserGroupMembers](GetUserGroupMembers.md) - List members of a user group
- [GetUserGroup](GetUserGroup.md) - Get user group properties

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Group not found | The specified group does not exist. |
| User not found | The specified username does not exist. |
| User already a member | The user is already a member of this group. |
| Access denied | The calling user lacks permission to manage this group. |
| `SystemError:...` | An unexpected server-side error occurred. |

---