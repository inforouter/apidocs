# GetGlobalGroups API

Returns a list of all infoRouter global user groups, sorted alphabetically by group name.

## Endpoint

```
/srv.asmx/GetGlobalGroups
```

## Methods

- **GET** `/srv.asmx/GetGlobalGroups?authenticationTicket=...`
- **POST** `/srv.asmx/GetGlobalGroups` (form data)
- **SOAP** Action: `http://tempuri.org/GetGlobalGroups`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |

---

## Response

### Success Response

Returns a `<usergroups>` collection with one `<usergroup>` element per global group, sorted alphabetically by group name.

```xml
<response success="true" error="">
  <usergroups>
    <usergroup GroupID="10"
               GroupName="AllStaff"
               DomainID="0"
               DomainName=""
               public="True" />
    <usergroup GroupID="11"
               GroupName="Managers"
               DomainID="0"
               DomainName=""
               public="False" />
  </usergroups>
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
| `DomainID` | Always `0` for global groups (not tied to a domain). |
| `DomainName` | Always empty for global groups. |
| `public` | `True` if group membership is visible to all users; `False` if membership is private. |

---

## Required Permissions

Any **authenticated user** can call this API. Anonymous users are rejected.

---

## Example

### GET Request

```
GET /srv.asmx/GetGlobalGroups
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetGlobalGroups HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetGlobalGroups>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
    </tns:GetGlobalGroups>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Global groups are not tied to a specific domain/library and can be added as members of any domain.
- To get only local groups for a specific domain, use `GetLocalGroups`.
- To get all groups (local and global) for a domain, use `GetDomainGroups`.

---

## Related APIs

- [GetLocalGroups](GetLocalGroups.md) - Get local user groups of a domain/library
- [GetDomainGroups](GetDomainGroups.md) - Get all groups (local and global) for a domain
- [GetUserGroup](GetUserGroup.md) - Get properties of a specific user group

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `[2730] Insufficient rights. Anonymous users cannot perform this action.` | The calling user is not authenticated. |
| `SystemError:...` | An unexpected server-side error occurred. |

---