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
<response success="false" error="Error message" errorCode="4000" />
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

`UpdateUserGroupName` with the `showMembers` flag, which it sets as well as renaming. Sending the
same name for both is the way to change only the flag.

```javascript
await call('UpdateUserGroupName1', {
  authenticationTicket: ticket,
  DomainName: 'Finance',
  GroupName: 'Approvers',
  NewGroupName: 'Approvers',
  showMembers: true
});
```

> **The flag is stored inverted**, the same way `CreateUserGroup1` stores it: `showMembers=false`
> reads back as `public="True"`. Send the opposite of what you mean until this is fixed.

## Notes

- To keep the current name unchanged, pass the same value in both `GroupName` and `NewGroupName`.
- The `showMembers` parameter corresponds to the `public` attribute in user group responses: `true` maps to `public="True"`.
- To rename the group without changing the member visibility setting, use `UpdateUserGroupName`.
- Pass empty `DomainName` or null for global groups.

---

## Related APIs

- [UpdateUserGroupName](UpdateUserGroupName.md) - Rename a group (without changing visibility)
- [GetUserGroup](GetUserGroup.md) - Get current group properties including `public` setting

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4030` | the caller may not manage groups - including a caller with no ticket at all |
| `4041` | no group by that name in that library |
| `4090` | the new name is already another group's |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
