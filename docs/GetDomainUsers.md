# GetDomainUsers API

Returns a list of all users who are members of the specified domain/library, including both directly-added users and users who are members indirectly through user group membership. Returns full user detail for each user.

## Endpoint

```
/srv.asmx/GetDomainUsers
```

## Methods

- **GET** `/srv.asmx/GetDomainUsers?authenticationTicket=...&DomainName=...`
- **POST** `/srv.asmx/GetDomainUsers` (form data)
- **SOAP** Action: `http://tempuri.org/GetDomainUsers`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DomainName` | string | Yes | Name of the domain/library whose users to retrieve. |

---

## Response

### Success Response

Returns a `<users>` collection with full user details. Includes both direct and indirect (via group) members.

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
GET /srv.asmx/GetDomainUsers
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DomainName=Finance
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetDomainUsers HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&DomainName=Finance
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetDomainUsers>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:DomainName>Finance</tns:DomainName>
    </tns:GetDomainUsers>
  </soap:Body>
</soap:Envelope>
```

---

## JavaScript

Every call answers XML with HTTP 200, success or not, so `success` is the thing to branch on and
`errorCode` is the number to report.

```javascript
async function call(action, params) {
  const response = await fetch(`/srv.asmx/${action}?${new URLSearchParams(params)}`);
  const root = new DOMParser()
    .parseFromString(await response.text(), 'text/xml')
    .documentElement;

  if (root.getAttribute('success') !== 'true') {
    throw new Error(`${root.getAttribute('errorCode')}: ${root.getAttribute('error')}`);
  }
  return root;
}
```

Lists the users that belong **to** a library - its local users, not the ones with access to it.

```javascript
const root = await call('GetDomainUsers', { authenticationTicket: ticket, DomainName: 'Finance' });
```

Not the same question as [GetDomainMembers](GetDomainMembers.md), which lists who may reach the
library. A new library has no local users while already having its creator as a member.

## Notes

- Unlike `GetDomainMembers`, this API includes users who are members indirectly through group membership (locally or globally).
- Always returns results in default sort order with full user detail mode.
- For sort and detail-mode control, use `GetDomainUsers1`.
- `GetDomainMembers` returns users and groups separately; `GetDomainUsers` flattens groups and returns only individual users.
- Large domains may return a significant number of users -" consider using `GetDomainUsers1` with `detailMode=false` for performance-sensitive scenarios.

---

## Related APIs

- [GetDomainUsers1](GetDomainUsers1.md) - Get all domain users with sort and detail-mode control
- [GetDomainMembers](GetDomainMembers.md) - Get direct members (users and groups separately)
- [GetLocalUsers](GetLocalUsers.md) - Get only local users of the domain (not global group members)
- [GetManagers](GetManagers.md) - Get the domain managers list

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | no library by that name - including one the caller cannot see |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `[115] Domain not found` | The specified DomainName does not exist. |
| `SystemError:...` | An unexpected server-side error occurred. |

---