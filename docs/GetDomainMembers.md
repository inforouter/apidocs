# GetDomainMembers API

Returns a list of all users and user groups who are members of the specified domain/library. Both directly-added individual users and member user groups are returned.

## Endpoint

```
/srv.asmx/GetDomainMembers
```

## Methods

- **GET** `/srv.asmx/GetDomainMembers?authenticationTicket=...&DomainName=...`
- **POST** `/srv.asmx/GetDomainMembers` (form data)
- **SOAP** Action: `http://tempuri.org/GetDomainMembers`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DomainName` | string | Yes | Name of the domain/library whose members to retrieve. |

---

## Response

### Success Response

Returns a `<users>` collection and a `<usergroups>` collection. Users are returned in full detail mode (including domain, logon dates, preferences).

```xml
<response success="true" error="">
  <users>
    <User exists="true" UserID="101" FirstName="John" LastName="Doe"
          Email="jdoe@example.com" Enabled="TRUE" UserName="jdoe"
          Domain="Finance" LastLogonDate="2024-01-15T10:30:00"
          LastPasswordChangeDate="2023-06-01T08:00:00"
          AuthenticationAuthority="Native" ReadOnlyUser="FALSE">
      <Preferences>
        <Language>en-US</Language>
        <DefaultPortal />
        <ShowArchives>FALSE</ShowArchives>
        <ShowHiddens>FALSE</ShowHiddens>
        <NotificationType>None</NotificationType>
        <NotificationTypeId>0</NotificationTypeId>
        <EmailType>0</EmailType>
        <AttachDocumentToEmail>FALSE</AttachDocumentToEmail>
      </Preferences>
    </User>
    <User exists="true" UserID="102" FirstName="Jane" LastName="Smith"
          Email="jsmith@example.com" Enabled="TRUE" UserName="jsmith"
          Domain="Finance" LastLogonDate="2024-02-10T14:15:00"
          LastPasswordChangeDate="2023-09-01T09:00:00"
          AuthenticationAuthority="Native" ReadOnlyUser="FALSE">
      <Preferences>...</Preferences>
    </User>
  </users>
  <usergroups>
    <usergroup GroupID="55" GroupName="AccountingTeam" DomainID="123"
               DomainName="Finance" public="True" />
  </usergroups>
</response>
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

---

## Required Permissions

Any **authenticated user** can call this API. Anonymous (unauthenticated) users are rejected.

---

## Example

### GET Request

```
GET /srv.asmx/GetDomainMembers
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DomainName=Finance
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetDomainMembers HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&DomainName=Finance
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetDomainMembers>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:DomainName>Finance</tns:DomainName>
    </tns:GetDomainMembers>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Returns both direct user members and user group members.
- Users are always returned in full detail mode (includes domain, logon dates, authentication source, preferences).
- The `<users>` list contains only individually-added users, not users who are members indirectly through groups. Use `GetDomainUsers` to get all users including those from groups.
- For sorting and detail-mode control, use `GetDomainMembers1`.
- The `public` attribute on `<usergroup>` elements indicates whether the group's member list is visible to non-managers.

---

## Related APIs

- [GetDomainMembers1](GetDomainMembers1.md) - Get members with sort and detail-mode control
- [GetDomainUsers](GetDomainUsers.md) - Get all users including indirect group members
- [AddUserAsDomainMember](AddUserAsDomainMember.md) - Add a user to the domain
- [AddUserGroupAsDomainMember](AddUserGroupAsDomainMember.md) - Add a user group to the domain
- [GetManagers](GetManagers.md) - Get the domain managers list

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `[2730] Insufficient rights. Anonymous users cannot perform this action.` | The calling user is not authenticated. |
| `[115] Domain not found` | The specified DomainName does not exist. |
| `SystemError:...` | An unexpected server-side error occurred. |

---