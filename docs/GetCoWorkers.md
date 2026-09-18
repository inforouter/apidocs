# GetCoWorkers API

Returns the co-workers of the currently authenticated user. Co-workers are all users who share at least one domain/library membership with the current user.

## Endpoint

```
/srv.asmx/GetCoWorkers
```

## Methods

- **GET** `/srv.asmx/GetCoWorkers?authenticationTicket=...`
- **POST** `/srv.asmx/GetCoWorkers` (form data)
- **SOAP** Action: `http://tempuri.org/GetCoWorkers`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |

---

## Response

### Success Response

Returns a `<users>` collection with one `<User>` element per co-worker, sorted by first name and last name ascending with full user detail.

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

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

---

## Required Permissions

Any **authenticated user** can call this API.

---

## Example

### GET Request

```
GET /srv.asmx/GetCoWorkers
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetCoWorkers HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetCoWorkers>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
    </tns:GetCoWorkers>
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

The people the caller shares a library with.

```javascript
const root = await call('GetCoWorkers', { authenticationTicket: ticket });
```

Unlike the `GetAllUsers` family this is not an administrator's call: it answers from the caller's
own library memberships.

## Notes

- Returns users from all domains/libraries where the calling user is a member.
- Results are sorted by first name then last name, ascending.
- Each `<User>` element includes a child `<Preferences>` element with notification and display settings.
- For a version with configurable sort order and detail mode, use `GetCoWorkers1`.

---

## Related APIs

- [GetCoWorkers1](GetCoWorkers1.md) - Co-workers with configurable sort and detail level
- [GetLocalUsers](GetLocalUsers.md) - Users of a specific domain/library
- [GetAllUsers](GetAllUsers.md) - All users in the system (admin only)

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |

---
