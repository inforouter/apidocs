# DeleteUser1 API

Deletes the specified infoRouter user account with administrator password confirmation. Use this API instead of `DeleteUser` when the system requires password re-prompting for user deletion.

> **`UserPassword` is only checked when the instance asks for it.** The re-prompt runs only if
> the password policy has "re-prompt on user delete" switched on. With it off, the parameter is
> not looked at: a wrong password deletes the user and reports success, and nothing in the answer
> says which regime was in force. Do not treat this operation as a confirmation step.

## Endpoint

```
/srv.asmx/DeleteUser1
```

## Methods

- **GET** `/srv.asmx/DeleteUser1?authenticationTicket=...&UserPassword=...&UserName=...`
- **POST** `/srv.asmx/DeleteUser1` (form data)
- **SOAP** Action: `http://tempuri.org/DeleteUser1`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `UserPassword` | string | Yes | The current password of the calling administrator. Required for identity confirmation when the system has password re-prompting enabled for user deletion. |
| `UserName` | string | Yes | The username to delete. |

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

**System administrator.** Only system administrators can delete user accounts.

---

## Example

### GET Request

```
GET /srv.asmx/DeleteUser1
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &UserPassword=AdminP%40ssword
  &UserName=jdoe
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/DeleteUser1 HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&UserPassword=AdminP@ssword
&UserName=jdoe
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:DeleteUser1>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:UserPassword>AdminP@ssword</tns:UserPassword>
      <tns:UserName>jdoe</tns:UserName>
    </tns:DeleteUser1>
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

Deletes a user, re-prompting for the caller's own password first.

```javascript
await call('DeleteUser1', {
  authenticationTicket: ticket,
  UserPassword: callersOwnPassword,
  UserName: 'jsmith',
});
```

## Notes

- The `UserPassword` is the password of the **calling administrator**, not the user being deleted - but it is only verified when the instance has password re-prompting switched on for user deletion. With that policy off the parameter is not read at all, and a wrong password deletes the user and reports success.
- If the system does not require password confirmation (`PasswordRePromptActions.UserDelete = false`), both `DeleteUser` and `DeleteUser1` work; you may use either.
- Deleting a user is permanent and cannot be undone.
- Before deleting a user, consider using the `TransferUser*` APIs to reassign the user's data (documents, tasks, subscriptions, memberships) to another user.

---

## Related APIs

- [DeleteUser](DeleteUser.md) - Delete a user without password confirmation (when allowed)
- [UserExists](UserExists.md) - Check if a user exists before attempting deletion
- [TransferUserDocumentOwnerships](TransferUserDocumentOwnerships.md) - Transfer document ownerships before deletion
- [TransferUserTasks](TransferUserTasks.md) - Transfer workflow tasks before deletion

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4030` | the caller is not a system administrator |
| `4000` | no user by that name |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

---
