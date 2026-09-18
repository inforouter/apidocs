# TransferUserExpirationNotices API

Transfers document expiration notices from one user to another. The target user takes over responsibility for receiving and acting on document expiration alerts that were assigned to the source user.

> **A transfer to the same user is accepted... no longer.** `fromUserName` and `toUserName` may
> not name one account: the call is refused with `4000`, because moving everything away from an
> account and handing it to nobody is not a transfer. It used to be accepted and reported as a
> success.

## Endpoint

```
/srv.asmx/TransferUserExpirationNotices
```

## Methods

- **GET** `/srv.asmx/TransferUserExpirationNotices?authenticationTicket=...&fromUserName=...&toUserName=...`
- **POST** `/srv.asmx/TransferUserExpirationNotices` (form data)
- **SOAP** Action: `http://tempuri.org/TransferUserExpirationNotices`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `fromUserName` | string | Yes | The username whose document expiration notices will be transferred. |
| `toUserName` | string | Yes | The username who will receive the document expiration notices. |

---

## Response

### Success Response

```xml
<root success="true" />
```

### Success Response (with warnings)

```xml
<root success="true" warnings="Some expiration notices could not be transferred." />
```

### Error Response

```xml
<root success="false" error="[ErrorCode] Error message" />
```

---

## Required Permissions

**System administrator.** Only system administrators can transfer user data between accounts.

---

## Example

### GET Request

```
GET /srv.asmx/TransferUserExpirationNotices
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &fromUserName=jdoe
  &toUserName=jsmith
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/TransferUserExpirationNotices HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&fromUserName=jdoe
&toUserName=jsmith
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:TransferUserExpirationNotices>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:FromUserName>jdoe</tns:FromUserName>
      <tns:ToUserName>jsmith</tns:ToUserName>
    </tns:TransferUserExpirationNotices>
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

Moves the expiration notices addressed to one user to another user.

```javascript
const root = await call('TransferUserExpirationNotices', {
  authenticationTicket: ticket,
  fromUserName: 'jsmith',
  toUserName: 'agarcia',
});

// There is no errorCode here - branch on success, and read the optional warnings attribute.
const warnings = root.getAttribute('warnings');
```

An answer may carry a `warnings` attribute when some of the expiration notices could not be moved - a conflict at
the destination, most often. It is absent when everything moved.

This is one of the calls to make before [DeleteUser](DeleteUser.md): what the account holds does
not go with it.

## Notes

- Transfers the notification target for document expiration dates from `fromUserName` to `toUserName`.
- The response root element is `<root>`, not `<response>`.
- Typically used as part of a user offboarding process before deleting the source user.

---

## Related APIs

- [TransferUserDocumentOwnerships](TransferUserDocumentOwnerships.md) - Transfer document ownerships
- [TransferUserDocumentSubscriptions](TransferUserDocumentSubscriptions.md) - Transfer document subscriptions
- [DeleteUser](DeleteUser.md) - Delete a user after transferring their data

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4030` | there is no ticket at all |
| `4041` | no user by either name |
| `4000` | `fromUserName` and `toUserName` name the same account |
| `HTTP 400` | `fromUserName` or `toUserName` was empty; refused by model binding, so there is no error document |

Every answer carries an `errorCode` now, including a `0` on success. The family used to write
none at all, so `success` was the only thing a client could branch on.

---
