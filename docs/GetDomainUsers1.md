# GetDomainUsers1 API

Returns a list of all users who are members of the specified domain/library (directly or indirectly through group membership), with control over sort order and the level of user detail returned.

## Endpoint

```
/srv.asmx/GetDomainUsers1
```

## Methods

- **GET** `/srv.asmx/GetDomainUsers1?authenticationTicket=...&domainName=...&sortBy=...&sortAscending=...&detailMode=...`
- **POST** `/srv.asmx/GetDomainUsers1` (form data)
- **SOAP** Action: `http://tempuri.org/GetDomainUsers1`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `domainName` | string | Yes | Name of the domain/library whose users to retrieve. |
| `sortBy` | int | Yes | Sort field for the user list. Valid values: `0` = default, `1` = USERNAME, `2` = FIRSTNAME_LASTNAME, `3` = LASTNAME_FIRSTNAME, `4` = EMAIL, `5` = STATUS, `6` = AUTHENTICATION_SOURCE, `7` = Library, `8` = UserType. |
| `sortAscending` | bool | Yes | Sort direction. `true` = ascending (A-'Z), `false` = descending (Z-'A). |
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
</response>
```

### Success Response (detailMode=false)

```xml
<response success="true" error="">
  <users>
    <User exists="true" UserID="101" FirstName="John" LastName="Doe"
          Email="jdoe@example.com" Enabled="TRUE" UserName="jdoe" />
    <User exists="true" UserID="102" FirstName="Jane" LastName="Smith"
          Email="jsmith@example.com" Enabled="TRUE" UserName="jsmith" />
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

### GET Request (sorted by username, ascending, basic detail)

```
GET /srv.asmx/GetDomainUsers1
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &domainName=Finance
  &sortBy=1
  &sortAscending=true
  &detailMode=false
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetDomainUsers1 HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&domainName=Finance
&sortBy=2
&sortAscending=true
&detailMode=true
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetDomainUsers1>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:domainName>Finance</tns:domainName>
      <tns:sortBy>1</tns:sortBy>
      <tns:sortAscending>true</tns:sortAscending>
      <tns:detailMode>false</tns:detailMode>
    </tns:GetDomainUsers1>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Includes both directly-added users and users who are domain members through group memberships (local or global).
- Use `detailMode=false` for faster response when only names or IDs are needed.
- `sortBy=0` uses the system default sort (typically by name).
- This is the enhanced version of `GetDomainUsers`, which always uses default sort and full detail mode.
- For large domains, use `detailMode=false` to reduce response size and improve performance.

---

## Related APIs

- [GetDomainUsers](GetDomainUsers.md) - Simplified version with default sort and full detail
- [GetDomainMembers1](GetDomainMembers1.md) - Get direct members (users and groups separately) with sort control
- [GetLocalUsers](GetLocalUsers.md) - Get only users local to the domain
- [GetDomainMembers](GetDomainMembers.md) - Get direct members without sort control

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `[115] Domain not found` | The specified domainName does not exist. |
| `SystemError:...` | An unexpected server-side error occurred. |

---