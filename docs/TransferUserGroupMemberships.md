# TransferUserGroupMemberships API

Transfers user group memberships from one user to another. The target user is added to all user groups where the source user is currently a member.

> **The thirteen `TransferUser...` operations carry no `errorCode`.** They answer
> `<root success="true"/>` or `<root success="false" error="..."/>` and no code attribute at all,
> and an expired ticket comes back as the legacy text `[901]Session expired or Invalid ticket`
> rather than `4010`. `success` is the only thing a client can branch on here.
>
> **A transfer to the same user is accepted.** `fromUserName` and `toUserName` may name one
> account, and the call reports success - having moved everything away from that account and
> handed it to nobody. This is not reversible and there is no report of what went. Check the two
> names are different before calling.

## Endpoint

```
/srv.asmx/TransferUserGroupMemberships
```

## Methods

- **GET** `/srv.asmx/TransferUserGroupMemberships?authenticationTicket=...&fromUserName=...&toUserName=...`
- **POST** `/srv.asmx/TransferUserGroupMemberships` (form data)
- **SOAP** Action: `http://tempuri.org/TransferUserGroupMemberships`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `fromUserName` | string | Yes | The username whose group memberships will be transferred. |
| `toUserName` | string | Yes | The username who will receive the group memberships. |

---

## Response

### Success Response

```xml
<root success="true" />
```

### Success Response (with warnings)

```xml
<root success="true" warnings="Some group memberships could not be transferred." />
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
GET /srv.asmx/TransferUserGroupMemberships
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &fromUserName=jdoe
  &toUserName=jsmith
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/TransferUserGroupMemberships HTTP/1.1
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
    <tns:TransferUserGroupMemberships>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:FromUserName>jdoe</tns:FromUserName>
      <tns:ToUserName>jsmith</tns:ToUserName>
    </tns:TransferUserGroupMemberships>
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

Moves one user's user group memberships to another user.

```javascript
const root = await call('TransferUserGroupMemberships', {
  authenticationTicket: ticket,
  fromUserName: 'jsmith',
  toUserName: 'agarcia',
});

// There is no errorCode here - branch on success, and read the optional warnings attribute.
const warnings = root.getAttribute('warnings');
```

An answer may carry a `warnings` attribute when some of the group memberships could not be moved - a conflict at
the destination, most often. It is absent when everything moved.

This is one of the calls to make before [DeleteUser](DeleteUser.md): what the account holds does
not go with it.

## Notes

- The `toUserName` is added as a member of each user group where `fromUserName` is a member.
- Groups where `toUserName` is already a member are skipped without error.
- The response root element is `<root>`, not `<response>`.
- Typically used as part of a user offboarding process before deleting the source user.

---

## Related APIs

- [TransferUserDomainMemberships](TransferUserDomainMemberships.md) - Transfer domain memberships
- [TransferUserDomainManagerRoles](TransferUserDomainManagerRoles.md) - Transfer domain manager roles
- [DeleteUser](DeleteUser.md) - Delete a user after transferring their data

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `*none*` | this family answers no `errorCode` at all - see the warning at the top of the page |
| `HTTP 400` | `fromUserName` or `toUserName` was empty; refused by model binding, so there is no error document |

The failures this operation reports, all of them with `success="false"` and no code:

| Message | When |
|---|---|
| user not found | `fromUserName` or `toUserName` names no user |
| access denied, coworker/administrator/library manager/user manager required | there is no ticket at all |
| `[901]Session expired or Invalid ticket` | the ticket is expired or unknown |

---
