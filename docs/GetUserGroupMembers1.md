# GetUserGroupMembers1 API

Returns a list of members of the specified user group with configurable sort order and detail level.

## Endpoint

```
/srv.asmx/GetUserGroupMembers1
```

## Methods

- **GET** `/srv.asmx/GetUserGroupMembers1?authenticationTicket=...&domainName=...&groupName=...&sortBy=...&sortAscending=...&detailMode=...`
- **POST** `/srv.asmx/GetUserGroupMembers1` (form data)
- **SOAP** Action: `http://tempuri.org/GetUserGroupMembers1`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `domainName` | string | No | The domain/library name if the group is a local group. Pass empty or null for global groups. |
| `groupName` | string | Yes | The name of the user group whose members will be returned. |
| `sortBy` | int | Yes | Sort field. Valid values: `1` = username, `2` = first name + last name, `3` = last name + first name, `4` = email, `5` = status, `6` = authentication source, `7` = domain/library, `8` = user type. |
| `sortAscending` | bool | Yes | If `true`, sort in ascending order; if `false`, sort in descending order. |
| `detailMode` | bool | Yes | If `true`, returns full user details including the `<Preferences>` child element. If `false`, returns basic identity attributes only (UserID, FirstName, LastName, Email, Enabled, UserName). |

---

## Response

### Success Response (detailMode=true)

```xml
<response success="true" error="">
  <users>
    <User exists="true"
          UserID="123"
          FirstName="Jane"
          LastName="Doe"
          Email="jane.doe@example.com"
          Enabled="TRUE"
          UserName="janedoe"
          Domain="Finance"
          LastLogonDate="2024-01-10"
          LastPasswordChangeDate="2024-01-01"
          AuthenticationAuthority="native"
          ReadOnlyUser="FALSE">
      <Preferences Language="English"
                   DefaultPortal=""
                   ShowArchives="FALSE"
                   ShowHiddens="FALSE"
                   NotificationType="INSTANT"
                   NotificationTypeId="1"
                   EmailType="HTML"
                   AttachDocumentToEmail="FALSE" />
    </User>
  </users>
</response>
```

### Success Response (detailMode=false)

```xml
<response success="true" error="">
  <users>
    <User exists="true"
          UserID="123"
          FirstName="Jane"
          LastName="Doe"
          Email="jane.doe@example.com"
          Enabled="TRUE"
          UserName="janedoe" />
  </users>
</response>
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

---

## Required Permissions

Any **authenticated user** can call this API.

---

## Example

### GET Request (sorted by last name, basic detail)

```
GET /srv.asmx/GetUserGroupMembers1
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &domainName=Finance
  &groupName=FinanceAdmins
  &sortBy=3
  &sortAscending=true
  &detailMode=false
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetUserGroupMembers1 HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&domainName=Finance
&groupName=FinanceAdmins
&sortBy=2
&sortAscending=true
&detailMode=true
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetUserGroupMembers1>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:DomainName>Finance</tns:DomainName>
      <tns:GroupName>FinanceAdmins</tns:GroupName>
      <tns:SortBy>2</tns:SortBy>
      <tns:SortAscending>true</tns:SortAscending>
      <tns:DetailMode>false</tns:DetailMode>
    </tns:GetUserGroupMembers1>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Use `detailMode=false` for a lighter response when only basic user identity is needed.
- Pass empty `domainName` for global groups.
- For a simpler call with fixed sort (first+last name ascending) and full detail, use `GetUserGroupMembers`.

---

## Related APIs

- [GetUserGroupMembers](GetUserGroupMembers.md) - Members with fixed sort and full detail
- [GetUserGroup](GetUserGroup.md) - Get user group properties
- [AddUsergroupMember](AddUsergroupMember.md) - Add a member to a group
- [RemoveUsergroupMember](RemoveUsergroupMember.md) - Remove a member from a group

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Group not found | The specified group does not exist. |
| `SystemError:...` | An unexpected server-side error occurred. |

---