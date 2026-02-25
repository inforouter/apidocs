# AddUserGroupAsDomainMember API

Adds an existing infoRouter global user group to the member list of the specified domain/library. All users in the group gain access to the domain according to its permissions configuration.

## Endpoint

```
/srv.asmx/AddUserGroupAsDomainMember
```

## Methods

- **GET** `/srv.asmx/AddUserGroupAsDomainMember?authenticationTicket=...&DomainName=...&GroupName=...`
- **POST** `/srv.asmx/AddUserGroupAsDomainMember` (form data)
- **SOAP** Action: `http://tempuri.org/AddUserGroupAsDomainMember`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DomainName` | string | Yes | Name of the domain/library to add the group to. |
| `GroupName` | string | Yes | Name of the global user group to add as a domain member. |

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

**Domain manager or system administrator.** The calling user must be a manager of the target domain or a system administrator.

---

## Example

### GET Request

```
GET /srv.asmx/AddUserGroupAsDomainMember
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DomainName=Finance
  &GroupName=AccountingTeam
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/AddUserGroupAsDomainMember HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&DomainName=Finance
&GroupName=AccountingTeam
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:AddUserGroupAsDomainMember>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:DomainName>Finance</tns:DomainName>
      <tns:GroupName>AccountingTeam</tns:GroupName>
    </tns:AddUserGroupAsDomainMember>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Only global user groups can be added using this API. Local groups (defined within a specific domain) are inherent members of that domain.
- If the group is already a member of the domain, an error is returned.
- Adding a group grants all current and future members of that group access to the domain.
- Use `GetDomainMembers` to view current user and group members.
- Use `RemoveUserFromDomainMembership` to remove an individual user, or use user group management APIs to remove a group.

---

## Related APIs

- [AddUserAsDomainMember](AddUserAsDomainMember) - Add an individual user as domain member
- [GetDomainMembers](GetDomainMembers) - Get all members (users and groups) of the domain
- [RemoveUserFromDomainMembership](RemoveUserFromDomainMembership) - Remove a user from the domain
- [GetGlobalGroups](GetGlobalGroups) - Get list of available global user groups

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `[115] Domain not found` | The specified DomainName does not exist. |
| Group not found | The specified GroupName does not exist as a global user group. |
| Already a member | The group is already a member of the domain. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/AddUserGroupAsDomainMember*
