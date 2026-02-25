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

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Access denied | The calling user is not a system administrator. |
| `SystemError:...` | An unexpected server-side error occurred. |

---