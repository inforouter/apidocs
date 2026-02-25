# GetOwner API

Returns the owner of the document or folder at the specified path.

## Endpoint

```
/srv.asmx/GetOwner
```

## Methods

- **GET** `/srv.asmx/GetOwner?authenticationTicket=...&Path=...`
- **POST** `/srv.asmx/GetOwner` (form data)
- **SOAP** Action: `http://tempuri.org/GetOwner`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full path to the document or folder. |

---

## Response

### Success Response

```xml
<response success="true">
  <User UserID="42"
        FirstName="John"
        LastName="Smith"
        Email="jsmith@example.com"
        Enabled="TRUE"
        UserName="jsmith" />
</response>
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

### User Attributes

| Attribute | Description |
|-----------|-------------|
| `UserID` | The internal numeric ID of the user. |
| `FirstName` | The user's first name. |
| `LastName` | The user's last name. |
| `Email` | The user's email address. |
| `Enabled` | `TRUE` if the user account is active; `FALSE` if disabled. |
| `UserName` | The user's login name. |

---

## Required Permissions

Any authenticated user with at least **List** access to the target document or folder.

---

## Example

### GET Request

```
GET /srv.asmx/GetOwner
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports/Q4Report.pdf
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetOwner HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance/Reports/Q4Report.pdf
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetOwner>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:Path>/Finance/Reports/Q4Report.pdf</tns:Path>
    </tns:GetOwner>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Works for both documents and folders.
- Returns basic user information only (not the extended profile). To get full user details, call `GetUser` with the returned `UserName`.
- To change the owner, use `SetOwner`.

---

## Related APIs

- [SetOwner](SetOwner.md) - Change the owner of a document or folder
- [GetUser](GetUser.md) - Retrieve full profile details for a user
- [GetAccessList](GetAccessList.md) - Retrieve the access list for a document or folder

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Path not found | The specified document or folder does not exist. |
| Owner not found | The owner record could not be retrieved. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/GetOwner*
