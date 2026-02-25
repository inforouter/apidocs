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
<root success="true">
  <UserGroups>
    <usergroup GroupID="1" GroupName="Editors" DomainID="0" DomainName="" public="True" />
    <usergroup GroupID="5" GroupName="Reviewers" DomainID="3" DomainName="MyLibrary" public="False" />
    <!-- ... additional usergroup elements ... -->
  </UserGroups>
</root>
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
<root success="false" error="[ErrorCode] Error message" />
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

## Notes

- The response includes both global groups (`DomainID="0"`) and domain-level (local) groups
- If the user has no group memberships, the `<UserGroups>` element will be empty
- The `public` attribute corresponds to the `showMembers` setting configured when the group was created
