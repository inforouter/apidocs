# GetManagers API

Returns a list of users who are designated as managers of the specified domain/library. Domain managers can administer members, workflows, and other domain settings.

## Endpoint

```
/srv.asmx/GetManagers
```

## Methods

- **GET** `/srv.asmx/GetManagers?authenticationTicket=...&DomainName=...`
- **POST** `/srv.asmx/GetManagers` (form data)
- **SOAP** Action: `http://tempuri.org/GetManagers`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DomainName` | string | Yes | Name of the domain/library whose managers to retrieve. |

---

## Response

### Success Response

Returns a `<users>` collection with full user details for each manager.

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

If no managers are assigned, the `<users>` element is empty:

```xml
<response success="true" error="">
  <users />
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
GET /srv.asmx/GetManagers
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DomainName=Finance
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetManagers HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&DomainName=Finance
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetManagers>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:DomainName>Finance</tns:DomainName>
    </tns:GetManagers>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Returns only users with manager status -" regular members are not included. Use `GetDomainMembers` for all members.
- Users are returned in full detail mode (includes domain, logon dates, authentication source, preferences).
- A domain can have multiple managers. An empty `<users>` element is returned if no managers are assigned.
- Domain managers can manage domain membership, configure workflows, set policies, and perform other administrative tasks within the domain.

---

## Related APIs

- [AddManagerToDomain](AddManagerToDomain.md) - Designate a user as a domain manager
- [RemoveManagerFromDomain](RemoveManagerFromDomain.md) - Remove manager status from a user
- [GetDomainMembers](GetDomainMembers.md) - Get all members (users and groups) of the domain
- [GetDomain](GetDomain.md) - Get domain properties

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