# GetGroupMembershipsOfUser API

Returns the user group memberships of the specified user, including both global and domain-level groups.

## Endpoint

```
/srv.asmx/GetGroupMembershipsOfUser
```

## Methods

- **GET** `/srv.asmx/GetGroupMembershipsOfUser?authenticationTicket=...&userName=...`
- **POST** `/srv.asmx/GetGroupMembershipsOfUser` (form data)
- **SOAP** Action: `http://tempuri.org/GetGroupMembershipsOfUser`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `userName` | string | Yes | The username of the user whose group memberships to retrieve |

## Response

### Success Response

```xml
<response success="true">
  <UserGroups>
    <usergroup GroupID="1" GroupName="Editors" DomainID="0" DomainName="" public="True" />
    <usergroup GroupID="5" GroupName="Reviewers" DomainID="3" DomainName="MyLibrary" public="False" />
    <!-- ... additional usergroup elements ... -->
  </UserGroups>
</response>
```

### Response Attributes

Each `<usergroup>` element contains the following attributes:

| Attribute | Type | Description |
|-----------|------|-------------|
| `GroupID` | int | Unique identifier of the user group |
| `GroupName` | string | Name of the user group |
| `DomainID` | int | Domain/library ID. `0` indicates a global group. |
| `DomainName` | string | Domain/library name. Empty string for global groups. |
| `public` | boolean | Whether group members are visible to other users |

### Error Response

```xml
<response success="false" error="Error message" errorCode="4000" />
```

## Required Permissions

The caller must have **ListingGroupMembershipOfUser** permission for the specified user.

## Example

### Request (GET)

```
GET /srv.asmx/GetGroupMembershipsOfUser?authenticationTicket=abc123-def456&userName=jsmith HTTP/1.1
```

### Request (POST)

```
POST /srv.asmx/GetGroupMembershipsOfUser HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&userName=jsmith
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetGroupMembershipsOfUser"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetGroupMembershipsOfUser xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
      <userName>jsmith</userName>
    </GetGroupMembershipsOfUser>
  </soap:Body>
</soap:Envelope>
```

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

Lists the groups a user is in.

```javascript
const root = await call('GetGroupMembershipsOfUser', {
  authenticationTicket: ticket, userName: 'jsmith'
});

for (const group of root.querySelectorAll('UserGroups > usergroup')) {
  console.log(group.getAttribute('GroupName'), group.getAttribute('DomainName'));
}
```

A user in no group answers an empty `<UserGroups />`. A user nobody is answers **`4000`**, where the
rest of the family answers `4041` for the same condition with the same message.

## Notes

- The response includes both global groups (`DomainID="0"`) and domain-level (local) groups
- If the user has no group memberships, the `<UserGroups>` element will be empty
- The `public` attribute corresponds to the `showMembers` setting configured when the group was created

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4000` | no user by that name - its neighbours call this `4041` |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
