# GetAllUsers1 API

Returns a paged and filtered list of infoRouter users with full detail, supporting sorting, status filtering, and text-based field filters.

## Endpoint

```
/srv.asmx/GetAllUsers1
```

## Methods

- **GET** `/srv.asmx/GetAllUsers1?authenticationTicket=...&StartingRowNumber=...&NumbeOfRow=...&...`
- **POST** `/srv.asmx/GetAllUsers1` (form data)
- **SOAP** Action: `http://tempuri.org/GetAllUsers1`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `StartingRowNumber` | int | Yes | Zero-based index of the first row to return. Use `0` to start from the beginning. |
| `NumbeOfRow` | int | Yes | Number of rows per page. |
| `firstNameFilter` | string | No | Filter by first name (partial match). Pass empty or null for no filter. |
| `lastNameFilter` | string | No | Filter by last name (partial match). Pass empty or null for no filter. |
| `userNameFilter` | string | No | Filter by username (partial match). Pass empty or null for no filter. |
| `emailFilter` | string | No | Filter by email address (partial match). Pass empty or null for no filter. |
| `authenticationSourceFilter` | string | No | Filter by authentication source (partial match). Pass empty or null for no filter. |
| `domainNameFilter` | string | No | Filter by domain/library membership (partial match). Pass empty or null for no filter. |
| `StatusFilter` | int | Yes | Filter by account status. Valid values: `-1` = no filter (all users), `0` = disabled only, `1` = enabled only. |
| `SortBy` | int | Yes | Sort field. Valid values: `0` = default (first name + last name ascending), `1` = username, `2` = first name + last name, `3` = last name + first name, `4` = email, `5` = status, `6` = authentication source, `7` = domain/library, `8` = user type. |
| `SortAscending` | bool | Yes | If `true`, sort in ascending order; if `false`, sort in descending order. |

---

## Response

### Success Response

Returns a `<users>` collection with a `totalusercount` attribute on the root `<response>` element indicating the total number of matching users (across all pages).

```xml
<response success="true" error="" totalusercount="150">
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

**System administrator.** Only system administrators can list all users.

---

## Example

### GET Request (first page, enabled users only, sorted by username)

```
GET /srv.asmx/GetAllUsers1
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &StartingRowNumber=0
  &NumbeOfRow=25
  &firstNameFilter=
  &lastNameFilter=
  &userNameFilter=
  &emailFilter=
  &authenticationSourceFilter=
  &domainNameFilter=Finance
  &StatusFilter=1
  &SortBy=1
  &SortAscending=true
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetAllUsers1 HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&StartingRowNumber=0
&NumbeOfRow=25
&StatusFilter=-1
&SortBy=2
&SortAscending=true
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetAllUsers1>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:StartingRowNumber>0</tns:StartingRowNumber>
      <tns:NumbeOfRow>25</tns:NumbeOfRow>
      <tns:StatusFilter>1</tns:StatusFilter>
      <tns:SortBy>2</tns:SortBy>
      <tns:SortAscending>true</tns:SortAscending>
    </tns:GetAllUsers1>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- The `totalusercount` attribute on the `<response>` element shows the total count of matching users across all pages, not just the current page.
- Use `StartingRowNumber` and `NumbeOfRow` to implement pagination. For example, to get page 3 with 25 rows per page, set `StartingRowNumber=50` and `NumbeOfRow=25`.
- Text filters perform partial (contains) matching.
- Each `<User>` element includes a child `<Preferences>` element with notification and display settings.
- To filter by user type (author vs read-only), use `GetAllUsers2`.

---

## Related APIs

- [GetAllUsers](GetAllUsers) - Get all users without pagination
- [GetAllUsers2](GetAllUsers2) - Paged list with additional user type filter
- [GetAllUsersWithoutDetails](GetAllUsersWithoutDetails) - Paged list without preference details
- [GetUser](GetUser) - Get full properties of a specific user

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Access denied | The calling user is not a system administrator. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/GetAllUsers1*
