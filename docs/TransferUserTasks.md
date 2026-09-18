# TransferUserTasks API

Transfers all open workflow tasks from one user to another. Used when a user is leaving or is temporarily unavailable.

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
/srv.asmx/TransferUserTasks
```

## Methods

- **GET** `/srv.asmx/TransferUserTasks?authenticationTicket=...&fromUserName=...&toUserName=...`
- **POST** `/srv.asmx/TransferUserTasks` (form data)
- **SOAP** Action: `http://tempuri.org/TransferUserTasks`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `fromUserName` | string | Yes | The username whose tasks will be transferred away. |
| `toUserName` | string | Yes | The username who will receive the transferred tasks. |

---

## Response

### Success Response

```xml
<root success="true" />
```

### Success Response (with warnings)

```xml
<root success="true" warnings="Some tasks could not be transferred." />
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
GET /srv.asmx/TransferUserTasks
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &fromUserName=jdoe
  &toUserName=jsmith
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/TransferUserTasks HTTP/1.1
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
    <tns:TransferUserTasks>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:FromUserName>jdoe</tns:FromUserName>
      <tns:ToUserName>jsmith</tns:ToUserName>
    </tns:TransferUserTasks>
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

Moves the workflow tasks queued against one user to another user.

```javascript
const root = await call('TransferUserTasks', {
  authenticationTicket: ticket,
  fromUserName: 'jsmith',
  toUserName: 'agarcia',
});

// There is no errorCode here - branch on success, and read the optional warnings attribute.
const warnings = root.getAttribute('warnings');
```

An answer may carry a `warnings` attribute when some of the tasks could not be moved - a conflict at
the destination, most often. It is absent when everything moved.

This is one of the calls to make before [DeleteUser](DeleteUser.md): what the account holds does
not go with it.

## Notes

- Transfers all **open** (not yet completed) workflow tasks assigned to `fromUserName`.
- If some tasks cannot be transferred (e.g., due to workflow rules), a `warnings` attribute is included in the success response describing the issue.
- The response root element is `<root>`, not `<response>`.
- Typically used as part of a user offboarding process. Run all relevant `TransferUser*` APIs before deleting a user.

---

## Related APIs

- [TransferUserDomainMemberships](TransferUserDomainMemberships.md) - Transfer domain memberships
- [TransferUserDocumentOwnerships](TransferUserDocumentOwnerships.md) - Transfer document ownerships
- [TransferUserWorkflowDefinitions](TransferUserWorkflowDefinitions.md) - Transfer workflow definition roles
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
