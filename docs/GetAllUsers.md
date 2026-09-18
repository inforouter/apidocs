# GetAllUsers API

Returns a list of all infoRouter users with full detail, sorted alphabetically by first and last name.

## Endpoint

```
/srv.asmx/GetAllUsers
```

## Methods

- **GET** `/srv.asmx/GetAllUsers?authenticationTicket=...`
- **POST** `/srv.asmx/GetAllUsers` (form data)
- **SOAP** Action: `http://tempuri.org/GetAllUsers`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |

---

## Response

### Success Response

Returns a `<users>` collection containing one `<User>` element per user, sorted by first name and last name ascending.

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
    <User exists="true"
          UserID="456"
          FirstName="John"
          LastName="Smith"
          Email="john.smith@example.com"
          Enabled="TRUE"
          UserName="jsmith"
          Domain="HR"
          LastLogonDate="2024-01-12"
          LastPasswordChangeDate="2023-12-01"
          AuthenticationAuthority="native"
          ReadOnlyUser="FALSE">
      <Preferences Language="English"
                   DefaultPortal=""
                   ShowArchives="FALSE"
                   ShowHiddens="FALSE"
                   NotificationType="NONE"
                   NotificationTypeId="0"
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

## User Element Attributes

| Attribute | Description |
|-----------|-------------|
| `UserID` | Unique numeric ID of the user. |
| `FirstName` | User's first name. |
| `LastName` | User's last name. |
| `Email` | User's email address. |
| `Enabled` | `TRUE` if the account is active; `FALSE` if disabled. |
| `UserName` | The user's login name. |
| `Domain` | The user's default domain/library. |
| `LastLogonDate` | Date of the user's most recent login. |
| `LastPasswordChangeDate` | Date the user's password was last changed. |
| `AuthenticationAuthority` | Authentication source (`native`, LDAP/OAuth authority name, Windows domain). |
| `ReadOnlyUser` | `TRUE` if the user is read-only; `FALSE` if an author. |

---

## Required Permissions

**System administrator.** Only system administrators can list all users.

---

## Example

### GET Request

```
GET /srv.asmx/GetAllUsers
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetAllUsers HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetAllUsers>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
    </tns:GetAllUsers>
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

Every user on the instance, in full, unpaged.

```javascript
const root = await call('GetAllUsers', { authenticationTicket: ticket });

for (const user of root.querySelectorAll('User')) {
  console.log(user.getAttribute('UserName'), user.getAttribute('Domain'));
}
```

Each `<User>` carries the whole record, property sets included. There are no paging attributes on
the answer: on an instance with many users prefer [GetAllUsers2](GetAllUsers2.md), which pages and
filters.

## Notes

- Returns **all** users in the system including disabled accounts.
- Results are always sorted alphabetically by first name then last name.
- For large installations, this call may return a very large result set. Use `GetAllUsers1` or `GetAllUsers2` for paged and filtered results.
- Each `<User>` element includes a child `<Preferences>` element with notification and display settings.

---

## Related APIs

- [GetAllUsers1](GetAllUsers1.md) - Paged and filtered user list with sorting
- [GetAllUsers2](GetAllUsers2.md) - Paged and filtered list with user type filter
- [GetAllUsersWithoutDetails](GetAllUsersWithoutDetails.md) - Paged user list without preference details
- [GetCoWorkers](GetCoWorkers.md) - Get co-workers of the current user
- [GetUser](GetUser.md) - Get full properties of a specific user

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4030` | the caller is not a system administrator |

---
