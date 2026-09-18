# UserExists API

Determines whether the given user name refers to an existing infoRouter user.

> **"No" is reported as a failure.** A user who exists answers `success="true"`; a user who does
> not answers `success="false"` with `4000` and "user not found". A client has to treat that
> refusal as the answer rather than as an error.

## Endpoint

```
/srv.asmx/UserExists
```

## Methods

- **GET** `/srv.asmx/UserExists?authenticationTicket=...&UserName=...`
- **POST** `/srv.asmx/UserExists` (form data)
- **SOAP** Action: `http://tempuri.org/UserExists`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `UserName` | string | Yes | The username to check for existence. |

---

## Response

### Success Response (user exists)

```xml
<response success="true" error="" />
```

### Error Response (user not found or access denied)

```xml
<response success="false" error="[ErrorCode] Error message" />
```

---

## Required Permissions

Any **authenticated user** can call this API. Anonymous (unauthenticated) users are rejected.

---

## Example

### GET Request

```
GET /srv.asmx/UserExists
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &UserName=jdoe
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/UserExists HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&UserName=jdoe
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:UserExists>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:UserName>jdoe</tns:UserName>
    </tns:UserExists>
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

Asks whether a user exists. It is not a boolean: yes is `success="true"` and no is
`success="false"` with `errorCode="4041"`. The code is what tells "there is no such user", which
is the answer, from a real error on the same call, which is not - until 9.0 both were `4000`.

```javascript
// Not a boolean: the answer is a success or a failure, so catch rather than read.
async function userExists(userName) {
  const response = await fetch(
    `/srv.asmx/UserExists?${new URLSearchParams({ authenticationTicket: ticket, UserName: userName })}`);
  const root = new DOMParser().parseFromString(await response.text(), 'text/xml').documentElement;
  return root.getAttribute('success') === 'true';
}
```

## Notes

- Returns `success="true"` if the user exists; returns an error response if the user is not found.
- Anonymous (unauthenticated) callers receive error `[2730]`.
- The check is case-insensitive for the username.

---

## Related APIs

- [GetUser](GetUser.md) - Get full properties of an existing user
- [CreateUser](CreateUser.md) - Create a new user
- [DeleteUser](DeleteUser.md) - Delete an existing user

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4000` | no user by that name - this is the "no" answer, not an error |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

---
