# GetUser API

Returns the detailed properties of the specified infoRouter user, including profile information, authentication source, and notification preferences.

> **The booleans on `<User>` do not agree with each other.** `exists` is `"true"` in lower case;
> `Enabled` and `ReadOnlyUser` beside it are `"TRUE"` and `"FALSE"` in capitals. Compare them
> case-insensitively.
>
> **There is no user type here.** `<User>` carries no author/reader attribute, so what
> [ChangeUserType](ChangeUserType.md) sets cannot be read back through this operation.

## Endpoint

```
/srv.asmx/GetUser
```

## Methods

- **GET** `/srv.asmx/GetUser?authenticationTicket=...&UserName=...`
- **POST** `/srv.asmx/GetUser` (form data)
- **SOAP** Action: `http://tempuri.org/GetUser`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `UserName` | string | Yes | The username to look up. If empty or omitted, returns the properties of the currently authenticated user. |

---

## Response

### Success Response

Returns a `<User>` element nested inside the `<response>` element with full user detail attributes and a `<Preferences>` child element.

```xml
<response success="true" error="">
  <User exists="true"
        UserID="123"
        FirstName="John"
        LastName="Doe"
        Email="john.doe@example.com"
        Enabled="TRUE"
        UserName="jdoe"
        Domain="Finance"
        LastLogonDate="2024-01-15"
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
| `exists` | Always `true` when the user is found. |
| `UserID` | Unique numeric ID of the user. |
| `FirstName` | User's first name. |
| `LastName` | User's last name. |
| `Email` | User's email address. |
| `Enabled` | `TRUE` if the account is active; `FALSE` if disabled. |
| `UserName` | The user's login name. |
| `Domain` | The default domain/library associated with the user. |
| `LastLogonDate` | Date of the user's last successful login. |
| `LastPasswordChangeDate` | Date the user's password was last changed. |
| `AuthenticationAuthority` | Authentication source: `native`, a Windows domain name, or a configured LDAP/OAuth authority. |
| `ReadOnlyUser` | `TRUE` if the user is a read-only user; `FALSE` if an author. |

## Preferences Element Attributes

| Attribute | Description |
|-----------|-------------|
| `Language` | The user's preferred display language. |
| `DefaultPortal` | The user's default portal name, if set. |
| `ShowArchives` | `TRUE` if the user sees archived domains in listings. |
| `ShowHiddens` | `TRUE` if the user sees hidden domains in listings. |
| `NotificationType` | Notification delivery mode: `NONE`, `INSTANT`, or `DAILY REPORT`. |
| `NotificationTypeId` | Numeric ID corresponding to `NotificationType`. |
| `EmailType` | Email format preference: `HTML` or `TEXT`. |
| `AttachDocumentToEmail` | `TRUE` if documents are attached to notification emails. |

---

## Required Permissions

Any **authenticated user** can call this API. Non-administrators can only retrieve their own user info or users they have access to view. If `UserName` is omitted or empty, the current user's own properties are returned.

---

## Example

### GET Request (specific user)

```
GET /srv.asmx/GetUser
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &UserName=jdoe
HTTP/1.1
```

### GET Request (current user)

```
GET /srv.asmx/GetUser
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &UserName=
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetUser HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&UserName=jdoe
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetUser>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:UserName>jdoe</tns:UserName>
    </tns:GetUser>
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

Reads one user by name.

```javascript
const root = await call('GetUser', { authenticationTicket: ticket, UserName: 'jsmith' });
const user = root.querySelector('User');

user.getAttribute('exists');        // "true"  - lower case
user.getAttribute('Enabled');       // "TRUE"  - capitals, beside it
user.getAttribute('ReadOnlyUser');  // "TRUE" or "FALSE"
```

The `<User>` element carries the account, a `<Preferences>` block and a `<Propertysets>` block with
one `<propertyrow>` per row applied to the user.

## Notes

- If `UserName` is null or whitespace, the API returns the properties of the currently authenticated user.
- To retrieve only basic user identity (without preferences), use `GetAllUsers1` or `GetCoWorkers1` with appropriate filters.
- To check whether a user exists without retrieving full details, use `UserExists`.

---

## Related APIs

- [UserExists](UserExists.md) - Check if a user exists
- [GetAllUsers](GetAllUsers.md) - Get a list of all users
- [UpdateUserProfile](UpdateUserProfile.md) - Update user profile information
- [UpdateUserEmail](UpdateUserEmail.md) - Update the user's email
- [UpdateUserPreferences](UpdateUserPreferences.md) - Update user preferences

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4000` | no user by that name - reported as a bad request rather than 4041 |

---
