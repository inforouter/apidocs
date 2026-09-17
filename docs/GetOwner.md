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

Reports the user who owns a folder or a document, as the same `<User>` element the user operations
return.

```javascript
const root = await call('GetOwner', {
  authenticationTicket: ticket,
  Path: '/Finance/Reports/Q1.pdf'
});

const owner = root.querySelector('User');
console.log(owner.getAttribute('UserName'), owner.getAttribute('Email'));
```

Unlike the access list, the owner is not treated as private: a caller with no ticket may read it where
the item itself is readable.

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

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | nothing at that path - including one the caller may not see |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Path not found | The specified document or folder does not exist. |
| Owner not found | The owner record could not be retrieved. |
| `SystemError:...` | An unexpected server-side error occurred. |

---