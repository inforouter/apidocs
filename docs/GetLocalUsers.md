# GetLocalUsers API

Returns the local users of the specified domain/library: user accounts that were created in and belong to that library, as opposed to global users who are given membership of it.

## Endpoint

```
/srv.asmx/GetLocalUsers
```

## Methods

- **GET** `/srv.asmx/GetLocalUsers?authenticationTicket=...&DomainName=...`
- **POST** `/srv.asmx/GetLocalUsers` (form data)
- **SOAP** Action: `http://tempuri.org/GetLocalUsers`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DomainName` | string | Yes | The name of the domain/library whose local users will be returned. |

---

## Response

### Success Response

Returns a `<users>` collection with one `<User>` element per local user.

```xml
<response success="true" error="">
  <users>
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
  </users>
</response>
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

---

## Required Permissions

**Any authenticated user.** The call checks only that the caller is signed in; it does not require management of the library. Anonymous callers are refused.

---

## Example

### GET Request

```
GET /srv.asmx/GetLocalUsers
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DomainName=Finance
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetLocalUsers HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&DomainName=Finance
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetLocalUsers>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:DomainName>Finance</tns:DomainName>
    </tns:GetLocalUsers>
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

The users that belong to one library.

```javascript
const root = await call('GetLocalUsers', { authenticationTicket: ticket, DomainName: 'Finance' });
```

These are the library's **own** users - the ones created with that `DomainName` - not everybody
with access to it. Every `<User>` returned carries that library in its `Domain` attribute.

## Notes

- Returns only accounts whose home library is this one. Global users who are members of the library, whether added directly or through a user group, are not included.
- To get every user with access to the library, use `GetDomainUsers`. For its direct members only, use `GetDomainMembers`.
- A library that owns no user accounts returns an empty list, even when it has many members.
- Each `<User>` element includes a child `<Preferences>` element with notification and display settings.

---

## Related APIs

- [GetDomainUsers](GetDomainUsers.md) - Get all users in a domain including indirect members
- [GetDomainMembers](GetDomainMembers.md) - Get users and user groups that are members of a domain
- [AddUserAsDomainMember](AddUserAsDomainMember.md) - Add a user to a domain as a direct member
- [RemoveUserFromDomainMembership](RemoveUserFromDomainMembership.md) - Remove a user from a domain

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | no library by that name, including one the caller cannot see |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

---
