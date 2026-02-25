# GetUserGroupMembers API

Returns a list of members of the specified user group with full detail, sorted by first name and last name ascending.

## Endpoint

```
/srv.asmx/GetUserGroupMembers
```

## Methods

- **GET** `/srv.asmx/GetUserGroupMembers?authenticationTicket=...&DomainName=...&GroupName=...`
- **POST** `/srv.asmx/GetUserGroupMembers` (form data)
- **SOAP** Action: `http://tempuri.org/GetUserGroupMembers`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DomainName` | string | No | The domain/library name if the group is a local group. Pass empty or null for global groups. |
| `GroupName` | string | Yes | The name of the user group whose members will be returned. |

---

## Response

### Success Response

Returns a `<users>` collection with one `<User>` element per member with full user detail.

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

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

---

## Required Permissions

Any **authenticated user** can call this API.

---

## Example

### GET Request

```
GET /srv.asmx/GetUserGroupMembers
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DomainName=Finance
  &GroupName=FinanceAdmins
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetUserGroupMembers HTTP/1.1
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
    <tns:GetUserGroupMembers>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:DomainName>Finance</tns:DomainName>
      <tns:GroupName>FinanceAdmins</tns:GroupName>
    </tns:GetUserGroupMembers>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Returns members sorted by first name then last name, ascending. Full user detail including `<Preferences>` is always returned.
- For configurable sort order and detail mode, use `GetUserGroupMembers1`.
- Pass empty `DomainName` for global groups.

---

## Related APIs

- [GetUserGroupMembers1](GetUserGroupMembers1.md) - Members with configurable sort and detail level
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

*For detailed documentation visit: https://support.inforouter.com/api-docs/GetUserGroupMembers*
