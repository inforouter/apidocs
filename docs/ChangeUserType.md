# ChangeUserType API

Changes the type of the specified infoRouter user account between author and read-only user.

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

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| User not found | The specified username does not exist. |
| Access denied | The calling user is not a system administrator. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/ChangeUserType*
