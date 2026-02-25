# GetUserGroup API

Returns information on the specified infoRouter user group.

## Endpoint

```
/srv.asmx/GetUserGroup
```

## Methods

- **GET** `/srv.asmx/GetUserGroup?authenticationTicket=...&DomainName=...&GroupName=...`
- **POST** `/srv.asmx/GetUserGroup` (form data)
- **SOAP** Action: `http://tempuri.org/GetUserGroup`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DomainName` | string | No | The domain/library name if the group is a local group. Pass empty or null for global groups. |
| `GroupName` | string | Yes | The name of the user group to retrieve. |

---

## Response

### Success Response

Returns a `<usergroup>` element nested inside the `<response>` element.

```xml
<response success="true" error="">
  <usergroup GroupID="55"
             GroupName="FinanceAdmins"
             DomainID="123"
             DomainName="Finance"
             public="True" />
</response>
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

---

## Usergroup Element Attributes

| Attribute | Description |
|-----------|-------------|
| `GroupID` | Unique numeric ID of the user group. |
| `GroupName` | Name of the user group. |
| `DomainID` | `0` for global groups; the domain's numeric ID for local groups. |
| `DomainName` | Empty for global groups; the domain name for local groups. |
| `public` | `True` if group membership is visible to all users; `False` if membership is private. |

---

## Required Permissions

Any **authenticated user** can call this API. Anonymous users are rejected.

---

## Example

### GET Request (local group)

```
GET /srv.asmx/GetUserGroup
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DomainName=Finance
  &GroupName=FinanceAdmins
HTTP/1.1
```

### GET Request (global group)

```
GET /srv.asmx/GetUserGroup
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DomainName=
  &GroupName=AllStaff
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetUserGroup HTTP/1.1
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
    <tns:GetUserGroup>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:DomainName>Finance</tns:DomainName>
      <tns:GroupName>FinanceAdmins</tns:GroupName>
    </tns:GetUserGroup>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- For global groups, pass an empty string or null for `DomainName`.
- For local groups, specify both the `DomainName` and `GroupName`.
- To get the members of a group, use `GetUserGroupMembers` or `GetUserGroupMembers1`.

---

## Related APIs

- [GetUserGroupMembers](GetUserGroupMembers) - Get members of a user group
- [GetDomainGroups](GetDomainGroups) - List all groups for a domain
- [GetGlobalGroups](GetGlobalGroups) - List all global groups
- [GetLocalGroups](GetLocalGroups) - List local groups of a domain

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `[2730] Insufficient rights. Anonymous users cannot perform this action.` | The calling user is not authenticated. |
| Group not found | The specified group does not exist. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/GetUserGroup*
