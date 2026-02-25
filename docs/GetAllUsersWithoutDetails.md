# GetAllUsersWithoutDetails API

Returns a paged and filtered list of infoRouter users without preference detail (lighter response), supporting the same filters and sorting as `GetAllUsers2`.

## Endpoint

```
/srv.asmx/GetAllUsersWithoutDetails
```

## Methods

- **GET** `/srv.asmx/GetAllUsersWithoutDetails?authenticationTicket=...&startingRowNumber=...&numberOfRow=...&...`
- **POST** `/srv.asmx/GetAllUsersWithoutDetails` (form data)
- **SOAP** Action: `http://tempuri.org/GetAllUsersWithoutDetails`

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

Returns a `<users>` collection. Each `<User>` element contains only the basic identity attributes — no `<Preferences>` child element is included.

```xml
<response success="true" error="" totalusercount="150">
  <users>
    <User exists="true"
          UserID="123"
          FirstName="Jane"
          LastName="Doe"
          Email="jane.doe@example.com"
          Enabled="TRUE"
          UserName="janedoe" />
    <User exists="true"
          UserID="456"
          FirstName="John"
          LastName="Smith"
          Email="john.smith@example.com"
          Enabled="TRUE"
          UserName="jsmith" />
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

### GET Request (first page, all users)

```
GET /srv.asmx/GetAllUsersWithoutDetails
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &startingRowNumber=0
  &numberOfRow=50
  &userStatusFilter=-1
  &userTypeFilter=-1
  &sortBy=2
  &sortAscending=true
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetAllUsersWithoutDetails HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&startingRowNumber=0
&numberOfRow=50
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
    <tns:GetAllUsersWithoutDetails>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:StartingRowNumber>0</tns:StartingRowNumber>
      <tns:NumberOfRow>50</tns:NumberOfRow>
      <tns:UserStatusFilter>-1</tns:UserStatusFilter>
      <tns:UserTypeFilter>-1</tns:UserTypeFilter>
      <tns:SortBy>2</tns:SortBy>
      <tns:SortAscending>true</tns:SortAscending>
    </tns:GetAllUsersWithoutDetails>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Returns user identity attributes only (UserID, FirstName, LastName, Email, Enabled, UserName). The `<Preferences>` child element, Domain, LastLogonDate, LastPasswordChangeDate, AuthenticationAuthority, and ReadOnlyUser are **not** included.
- Use this API when you only need user identity data and want a lighter-weight response for large user sets.
- The `totalusercount` attribute reflects the total matching users across all pages.
- Use `GetAllUsers2` for the same filtering but with full user details.

---

## Related APIs

- [GetAllUsers2](GetAllUsers2.md) - Same filters with full user detail
- [GetAllUsers1](GetAllUsers1.md) - Paged list without user type filter
- [GetAllUsers](GetAllUsers.md) - All users without pagination
- [GetUser](GetUser.md) - Full properties of a specific user

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Access denied | The calling user is not a system administrator. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/GetAllUsersWithoutDetails*
