# GetAllUsers2 API

Returns a paged and filtered list of infoRouter users with full detail, supporting all filters from `GetAllUsers1` plus an additional user type filter (author vs read-only).

## Endpoint

```
/srv.asmx/GetAllUsers2
```

## Methods

- **GET** `/srv.asmx/GetAllUsers2?authenticationTicket=...&startingRowNumber=...&numberOfRow=...&...`
- **POST** `/srv.asmx/GetAllUsers2` (form data)
- **SOAP** Action: `http://tempuri.org/GetAllUsers2`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `startingRowNumber` | int | Yes | Zero-based index of the first row to return. Use `0` to start from the beginning. |
| `numberOfRow` | int | Yes | Number of rows per page. |
| `firstNameFilter` | string | No | Filter by first name (partial match). Pass empty or null for no filter. |
| `lastNameFilter` | string | No | Filter by last name (partial match). Pass empty or null for no filter. |
| `userNameFilter` | string | No | Filter by username (partial match). Pass empty or null for no filter. |
| `emailFilter` | string | No | Filter by email address (partial match). Pass empty or null for no filter. |
| `authenticationSourceFilter` | string | No | Filter by authentication source (partial match). Pass empty or null for no filter. |
| `domainNameFilter` | string | No | Filter by domain/library membership (partial match). Pass empty or null for no filter. |
| `userStatusFilter` | int | Yes | Filter by account status. Valid values: `-1` = no filter (all users), `0` = disabled only, `1` = enabled only. |
| `userTypeFilter` | int | Yes | Filter by user type. Valid values: `-1` = no filter (all types), `1` = authors only, `2` = read-only users only. |
| `sortBy` | int | Yes | Sort field. Valid values: `0` = default, `1` = username, `2` = first name + last name, `3` = last name + first name, `4` = email, `5` = status, `6` = authentication source, `7` = domain/library, `8` = user type. |
| `sortAscending` | bool | Yes | If `true`, sort in ascending order; if `false`, sort in descending order. |

---

## Response

### Success Response

Returns a `<users>` collection with a `totalusercount` attribute on the root `<response>` element.

```xml
<response success="true" error="" totalusercount="42">
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

### GET Request (read-only users only, first page)

```
GET /srv.asmx/GetAllUsers2
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &startingRowNumber=0
  &numberOfRow=25
  &userStatusFilter=1
  &userTypeFilter=2
  &sortBy=2
  &sortAscending=true
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetAllUsers2 HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&startingRowNumber=0
&numberOfRow=25
&userStatusFilter=-1
&userTypeFilter=-1
&sortBy=2
&sortAscending=true
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetAllUsers2>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:StartingRowNumber>0</tns:StartingRowNumber>
      <tns:NumberOfRow>25</tns:NumberOfRow>
      <tns:UserStatusFilter>1</tns:UserStatusFilter>
      <tns:UserTypeFilter>2</tns:UserTypeFilter>
      <tns:SortBy>2</tns:SortBy>
      <tns:SortAscending>true</tns:SortAscending>
    </tns:GetAllUsers2>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- The `totalusercount` attribute on the `<response>` element shows the total number of matching users across all pages.
- This API is identical to `GetAllUsers1` but adds the `userTypeFilter` parameter to filter by user type (author vs read-only).
- For a version that excludes user preference details (lighter response), use `GetAllUsersWithoutDetails`.

---

## Related APIs

- [GetAllUsers](GetAllUsers) - Get all users without pagination
- [GetAllUsers1](GetAllUsers1) - Paged list without user type filter
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

*For detailed documentation visit: https://support.inforouter.com/api-docs/GetAllUsers2*
