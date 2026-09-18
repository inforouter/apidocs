# GetCoWorkers1 API

Returns the co-workers of the currently authenticated user with configurable sort order and detail level. Co-workers are all users who share at least one domain/library membership with the current user.

## Endpoint

```
/srv.asmx/GetCoWorkers1
```

## Methods

- **GET** `/srv.asmx/GetCoWorkers1?authenticationTicket=...&sortBy=...&sortAscending=...&detailMode=...`
- **POST** `/srv.asmx/GetCoWorkers1` (form data)
- **SOAP** Action: `http://tempuri.org/GetCoWorkers1`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `sortBy` | int | Yes | Sort field. Valid values: `1` = username, `2` = first name + last name, `3` = last name + first name, `4` = email, `5` = status, `6` = authentication source, `7` = domain/library, `8` = user type. |
| `sortAscending` | bool | Yes | If `true`, sort in ascending order; if `false`, sort in descending order. |
| `detailMode` | bool | Yes | If `true`, returns full user details including the `<Preferences>` child element and extended attributes. If `false`, returns basic identity attributes only. |

---

## Response

### Success Response (detailMode=true)

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

### Success Response (detailMode=false)

```xml
<response success="true" error="">
  <users>
    <User exists="true"
          UserID="456"
          FirstName="Jane"
          LastName="Smith"
          Email="jane.smith@example.com"
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

Any **authenticated user** can call this API.

---

## Example

### GET Request (full detail, sorted by last name)

```
GET /srv.asmx/GetCoWorkers1
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &sortBy=3
  &sortAscending=true
  &detailMode=true
HTTP/1.1
```

### GET Request (basic info only, sorted by username)

```
GET /srv.asmx/GetCoWorkers1
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &sortBy=1
  &sortAscending=true
  &detailMode=false
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetCoWorkers1 HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&sortBy=2
&sortAscending=true
&detailMode=false
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetCoWorkers1>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:SortBy>2</tns:SortBy>
      <tns:SortAscending>true</tns:SortAscending>
      <tns:DetailMode>false</tns:DetailMode>
    </tns:GetCoWorkers1>
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

The people the caller shares a library with, sorted, optionally in brief.

```javascript
const root = await call('GetCoWorkers1', {
  authenticationTicket: ticket,
  sortBy: 1,
  sortAscending: true,
  detailMode: false,     // true also returns property sets and the rest of each record
});
```

## Notes

- Returns users from all domains/libraries where the calling user is a member.
- When `detailMode=false`, the response excludes Domain, LastLogonDate, LastPasswordChangeDate, AuthenticationAuthority, ReadOnlyUser, and the `<Preferences>` child element.
- For the simple version with no configuration, use `GetCoWorkers` (which always returns full detail sorted by first name + last name ascending).

---

## Related APIs

- [GetCoWorkers](GetCoWorkers.md) - Co-workers with fixed sort and full detail
- [GetLocalUsers](GetLocalUsers.md) - Users of a specific domain/library
- [GetAllUsers](GetAllUsers.md) - All users in the system (admin only)

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4000` | `sortBy` is not one of the sort columns - this operation checks it where GetAllUsers2 does not |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

---
