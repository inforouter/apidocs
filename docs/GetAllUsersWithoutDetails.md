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

Returns a `<users>` collection. Each `<User>` element contains only the basic identity attributes -" no `<Preferences>` child element is included.

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

The same page as [GetAllUsers2](GetAllUsers2.md), with only the names.

```javascript
const root = await call('GetAllUsersWithoutDetails', {
  authenticationTicket: ticket,
  startingRowNumber: 0,
  numberOfRow: 50,
  firstNameFilter: '',
  lastNameFilter: '',
  userNameFilter: '',
  emailFilter: '',
  authenticationSourceFilter: '',
  domainNameFilter: '',
  userStatusFilter: -1,
  userTypeFilter: -1,
  sortBy: 1,
  sortAscending: true,
});
```

Each `<User>` carries the name and little else: no `Domain`, no dates, no `<Propertysets>`. It is
the form to use for a picker.

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

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4030` | the caller is not a system administrator |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

Every filter has to be present - they are declared as plain strings, so an omitted one is an
HTTP 400 rather than "no filter". Send an empty string for the ones you do not want, `-1` for the
status and type filters.

---
