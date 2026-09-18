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
<response success="false" error="Error message" errorCode="4000" />
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

Deletes a group and every membership of it.

```javascript
await call('DeleteUsergroup', {
  authenticationTicket: ticket, DomainName: 'Finance', GroupName: 'Approvers'
});
```

An empty `DomainName` deletes a global group. Deleting a group that is not there is `4041`.

## Notes

- Deleting a user group removes all its memberships and any folder/document permissions assigned to the group. This action cannot be undone.
- Pass empty `DomainName` or null for global groups.
- `DomainName` is required to delete a *local* group. Group names are only unique within a library, so a name passed without a library name is resolved as a global group; if no global group has that name the call returns "User group not found" even when a local group of that name exists.
- Members of the group are not deleted -" only the group itself is removed.

---

## Related APIs

- [GetUserGroup](GetUserGroup.md) - Get user group properties before deleting
- [GetUserGroupMembers](GetUserGroupMembers.md) - Review members before deleting a group
- [AddUsergroupMember](AddUsergroupMember.md) - Add members to a group

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4030` | the caller may not manage groups - including a caller with no ticket at all |
| `4041` | no group by that name in that library |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
