# GetDomainGroups API

Returns a list of all user groups (both local and global) that are members of the specified domain/library.

## Endpoint

```
/srv.asmx/GetDomainGroups
```

## Methods

- **GET** `/srv.asmx/GetDomainGroups?authenticationTicket=...&DomainName=...`
- **POST** `/srv.asmx/GetDomainGroups` (form data)
- **SOAP** Action: `http://tempuri.org/GetDomainGroups`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DomainName` | string | Yes | The name of the domain/library whose groups will be returned. |

---

## Response

### Success Response

Returns a `<usergroups>` collection with one `<usergroup>` element per group (both local and global members of the domain).

```xml
<response success="true" error="">
  <usergroups>
    <usergroup GroupID="10"
               GroupName="AllStaff"
               DomainID="0"
               DomainName=""
               public="True" />
    <usergroup GroupID="55"
               GroupName="FinanceAdmins"
               DomainID="123"
               DomainName="Finance"
               public="True" />
    <usergroup GroupID="56"
               GroupName="FinanceReaders"
               DomainID="123"
               DomainName="Finance"
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
| `DomainID` | `0` for global groups; the domain's numeric ID for local groups. |
| `DomainName` | Empty for global groups; the domain name for local groups. |
| `public` | `True` if group membership is visible to all users; `False` if membership is private. |

---

## Required Permissions

Any **authenticated user** can call this API. Anonymous users are rejected.

---

## Example

### GET Request

```
GET /srv.asmx/GetDomainGroups
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DomainName=Finance
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetDomainGroups HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&DomainName=Finance
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetDomainGroups>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:DomainName>Finance</tns:DomainName>
    </tns:GetDomainGroups>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Returns both **local** groups (defined specifically for this domain) and **global** groups that have been added as members of the domain.
- To get only local groups, use `GetLocalGroups`.
- To get all global groups in the system regardless of domain membership, use `GetGlobalGroups`.

---

## Related APIs

- [GetLocalGroups](GetLocalGroups.md) - Get only local groups of a domain
- [GetGlobalGroups](GetGlobalGroups.md) - Get all global user groups in the system
- [AddUserGroupAsDomainMember](AddUserGroupAsDomainMember.md) - Add a global group as a domain member

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `[115] Domain not found` | The specified domain/library does not exist. |
| `[2730] Insufficient rights. Anonymous users cannot perform this action.` | The calling user is not authenticated. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/GetDomainGroups*
