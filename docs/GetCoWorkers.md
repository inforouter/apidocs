# GetCoWorkers API

Returns the co-workers of the currently authenticated user. Co-workers are all users who share at least one domain/library membership with the current user.

## Endpoint

```
/srv.asmx/GetCoWorkers
```

## Methods

- **GET** `/srv.asmx/GetCoWorkers?authenticationTicket=...`
- **POST** `/srv.asmx/GetCoWorkers` (form data)
- **SOAP** Action: `http://tempuri.org/GetCoWorkers`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |

---

## Response

### Success Response

Returns a `<users>` collection with one `<User>` element per co-worker, sorted by first name and last name ascending with full user detail.

```xml
<response success="true" error="">
  <users>
    <User exists="true"
          UserID="456"
          FirstName="Jane"
          LastName="Smith"
          Email="jane.smith@example.com"
          Enabled="TRUE"
          UserName="jsmith"
          Domain="Finance"
          LastLogonDate="2024-01-10"
          LastPasswordChangeDate="2023-12-01"
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
GET /srv.asmx/GetCoWorkers
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetCoWorkers HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetCoWorkers>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
    </tns:GetCoWorkers>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Returns users from all domains/libraries where the calling user is a member.
- Results are sorted by first name then last name, ascending.
- Each `<User>` element includes a child `<Preferences>` element with notification and display settings.
- For a version with configurable sort order and detail mode, use `GetCoWorkers1`.

---

## Related APIs

- [GetCoWorkers1](GetCoWorkers1.md) - Co-workers with configurable sort and detail level
- [GetLocalUsers](GetLocalUsers.md) - Users of a specific domain/library
- [GetAllUsers](GetAllUsers.md) - All users in the system (admin only)

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/GetCoWorkers*
