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

## JavaScript

Every call answers XML with HTTP 200, success or not, so `success` is the thing to branch on and
`errorCode` is the number to report.

```javascript
async function call(action, params) {
  const response = await fetch(`/srv.asmx/${action}?${new URLSearchParams(params)}`);
  const root = new DOMParser()
    .parseFromString(await response.text(), 'text/xml')
    .documentElement;

  if (root.getAttribute('success') !== 'true') {
    throw new Error(`${root.getAttribute('errorCode')}: ${root.getAttribute('error')}`);
  }
  return root;
}
```

Gives every member of a user group access to a library.

```javascript
await call('AddUserGroupAsDomainMember', {
  authenticationTicket: ticket,
  DomainName: 'Finance',
  GroupName: 'AllStaff'
});
```

The group then appears under `<usergroups>` in [GetDomainMembers](GetDomainMembers.md). A group name
nobody has is `4041`.

## Notes

- Only global user groups can be added using this API. Local groups (defined within a specific domain) are inherent members of that domain.
- If the group is already a member of the domain, an error is returned.
- Adding a group grants all current and future members of that group access to the domain.
- Use `GetDomainMembers` to view current user and group members.
- Use `RemoveUserFromDomainMembership` to remove an individual user, or use user group management APIs to remove a group.

---

## Related APIs

- [AddUserAsDomainMember](AddUserAsDomainMember.md) - Add an individual user as domain member
- [GetDomainMembers](GetDomainMembers.md) - Get all members (users and groups) of the domain
- [RemoveUserFromDomainMembership](RemoveUserFromDomainMembership.md) - Remove a user from the domain
- [GetGlobalGroups](GetGlobalGroups.md) - Get list of available global user groups

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4030` | the caller is not a system administrator |
| `4000` | the group is already a member |
| `4041` | no user group by that name |
| `4041` | no library by that name - including one the caller cannot see |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `[115] Domain not found` | The specified DomainName does not exist. |
| Group not found | The specified GroupName does not exist as a global user group. |
| Already a member | The group is already a member of the domain. |
| `SystemError:...` | An unexpected server-side error occurred. |

---