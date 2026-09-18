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

A page of users, filtered, with a user type filter.

```javascript
const root = await call('GetAllUsers2', {
  authenticationTicket: ticket,
  startingRowNumber: 0,
  numberOfRow: 50,
  firstNameFilter: '',
  lastNameFilter: '',
  userNameFilter: '',
  emailFilter: '',
  authenticationSourceFilter: '',
  domainNameFilter: '',
  userStatusFilter: -1,           // -1 any, 0 disabled, 1 enabled
  userTypeFilter: -1,             // -1 any, 1 author, 2 reader
  sortBy: 1,
  sortAscending: true,
});
```

## Notes

- The `totalusercount` attribute on the `<response>` element shows the total number of matching users across all pages.
- This API is identical to `GetAllUsers1` but adds the `userTypeFilter` parameter to filter by user type (author vs read-only).
- For a version that excludes user preference details (lighter response), use `GetAllUsersWithoutDetails`.

---

## Related APIs

- [GetAllUsers](GetAllUsers.md) - Get all users without pagination
- [GetAllUsers1](GetAllUsers1.md) - Paged list without user type filter
- [GetAllUsersWithoutDetails](GetAllUsersWithoutDetails.md) - Paged list without preference details
- [GetUser](GetUser.md) - Get full properties of a specific user

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

`sortBy` is not checked. A number no sort column has is accepted without a word and the list comes
back in whatever order the default gives, where [GetCoWorkers1](GetCoWorkers1.md) refuses the same
value with `4000`.

---
