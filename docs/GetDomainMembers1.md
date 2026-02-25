# GetDomainMembers1 API

Returns a list of users and user groups who are members of the specified domain/library, with control over sort order and the level of detail returned for each user.

## Endpoint

```
/srv.asmx/GetDomainMembers1
```

## Methods

- **GET** `/srv.asmx/GetDomainMembers1?authenticationTicket=...&domainName=...&sortBy=...&sortAscending=...&detailMode=...`
- **POST** `/srv.asmx/GetDomainMembers1` (form data)
- **SOAP** Action: `http://tempuri.org/GetDomainMembers1`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `domainName` | string | Yes | Name of the domain/library whose members to retrieve. |
| `sortBy` | int | Yes | Sort field for the user list. Valid values: `0` = default, `1` = USERNAME, `2` = FIRSTNAME_LASTNAME, `3` = LASTNAME_FIRSTNAME, `4` = EMAIL, `5` = STATUS, `6` = AUTHENTICATION_SOURCE, `7` = Library, `8` = UserType. |
| `sortAscending` | bool | Yes | Sort direction. `true` = ascending (A→Z), `false` = descending (Z→A). |
| `detailMode` | bool | Yes | If `true`, returns full user details including domain, logon dates, authentication source, and preferences. If `false`, returns only basic fields (name, email, enabled status). |

---

## Response

### Success Response (detailMode=true)

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
  </users>
  <usergroups>
    <usergroup GroupID="55" GroupName="AccountingTeam" DomainID="123"
               DomainName="Finance" public="True" />
  </usergroups>
</response>
```

### Success Response (detailMode=false)

```xml
<response success="true" error="">
  <users>
    <User exists="true" UserID="101" FirstName="John" LastName="Doe"
          Email="jdoe@example.com" Enabled="TRUE" UserName="jdoe" />
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

### GET Request (sorted by last name, descending, full details)

```
GET /srv.asmx/GetDomainMembers1
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &domainName=Finance
  &sortBy=3
  &sortAscending=false
  &detailMode=true
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetDomainMembers1 HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&domainName=Finance
&sortBy=2
&sortAscending=true
&detailMode=false
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetDomainMembers1>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:domainName>Finance</tns:domainName>
      <tns:sortBy>2</tns:sortBy>
      <tns:sortAscending>true</tns:sortAscending>
      <tns:detailMode>true</tns:detailMode>
    </tns:GetDomainMembers1>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Sorting applies only to the `<users>` list; user groups are returned unsorted.
- The `sortBy=0` value uses the system default sort order.
- `detailMode=false` is faster and reduces response size — use it when only names or IDs are needed.
- This is an enhanced version of `GetDomainMembers` which always returns full detail with default sort.
- The `<users>` list contains only individually-added members. Use `GetDomainUsers1` to include users who are members through group membership.

---

## Related APIs

- [GetDomainMembers](GetDomainMembers.md) - Simplified version with no sort or detail control
- [GetDomainUsers1](GetDomainUsers1.md) - Get all users (including indirect via groups) with sort control
- [AddUserAsDomainMember](AddUserAsDomainMember.md) - Add a user to the domain
- [GetManagers](GetManagers.md) - Get the list of domain managers

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `[2730] Insufficient rights. Anonymous users cannot perform this action.` | The calling user is not authenticated. |
| `[115] Domain not found` | The specified domainName does not exist. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/GetDomainMembers1*
