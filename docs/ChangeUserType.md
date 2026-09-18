# ChangeUserType API

Changes the type of the specified infoRouter user account between author and read-only user.

> **The change cannot be read back through the API.** `GetUser` carries no user type attribute
> at all, so there is no way to confirm what a user's type is now, or what it was before this
> call. `GetAllUsers2` can filter on it but does not report it either.
>
> `0` (Unspecified) is refused, so a user whose type has been set once cannot be put back.

## Endpoint

```
/srv.asmx/ChangeUserType
```

## Methods

- **GET** `/srv.asmx/ChangeUserType?authenticationTicket=...&userName=...&userType=...`
- **POST** `/srv.asmx/ChangeUserType` (form data)
- **SOAP** Action: `http://tempuri.org/ChangeUserType`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `userName` | string | Yes | The username of the account whose type will be changed. |
| `userType` | int | Yes | The new user type. Valid values: `1` = author (can upload and modify documents), `2` = read-only user (can only view documents). |

---

## Response

### Success Response

```xml
<response success="true" error="" />
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

---

## Required Permissions

**System administrator.** Only system administrators can change user account types.

---

## Example

### GET Request (change to author)

```
GET /srv.asmx/ChangeUserType
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &userName=jdoe
  &userType=1
HTTP/1.1
```

### GET Request (change to read-only)

```
GET /srv.asmx/ChangeUserType
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &userName=jdoe
  &userType=2
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/ChangeUserType HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&userName=jdoe
&userType=2
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:ChangeUserType>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:UserName>jdoe</tns:UserName>
      <tns:UserType>2</tns:UserType>
    </tns:ChangeUserType>
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

Marks a user as an author or a reader.

```javascript
await call('ChangeUserType', { authenticationTicket: ticket, userName: 'jsmith', userType: 1 }); // author
await call('ChangeUserType', { authenticationTicket: ticket, userName: 'jsmith', userType: 2 }); // reader
```

## Notes

- **Author** users (type `1`) can upload, edit, and manage documents based on their permissions.
- **Read-only** users (type `2`) can only view and download documents; they cannot upload or edit.
- Changing a user to read-only does not remove their existing document ownership or folder memberships.
- The `ReadOnlyUser` attribute in `GetUser` responses reflects the current user type.

---

## Related APIs

- [GetUser](GetUser.md) - Get current user properties including user type
- [ChangeUserStatus](ChangeUserStatus.md) - Enable or disable a user account
- [CreateUser](CreateUser.md) - Create a new user with a specified type

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4030` | the caller is not a system administrator |
| `4041` | no user by that name |
| `4000` | `userType` is anything but 1 or 2 - including 0, and the refusal does not say which values are allowed |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

---
