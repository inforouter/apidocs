# DeleteUser API

Deletes the specified infoRouter user account. If the system is configured to require password confirmation for user deletion, this method will fail and `DeleteUser1` must be used instead.

## Endpoint

```
/srv.asmx/DeleteUser
```

## Methods

- **GET** `/srv.asmx/DeleteUser?authenticationTicket=...&UserName=...`
- **POST** `/srv.asmx/DeleteUser` (form data)
- **SOAP** Action: `http://tempuri.org/DeleteUser`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `UserName` | string | Yes | The username to delete, or a short ID reference in the format `ID:userid` (e.g., `ID:123`). |

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

### GET Request (by username)

```
GET /srv.asmx/DeleteUser
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &UserName=jdoe
HTTP/1.1
```

### GET Request (by user ID)

```
GET /srv.asmx/DeleteUser
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &UserName=ID:123
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/DeleteUser HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&UserName=jdoe
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:DeleteUser>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:UserName>jdoe</tns:UserName>
    </tns:DeleteUser>
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

Deletes a user.

```javascript
await call('DeleteUser', { authenticationTicket: ticket, UserName: 'jsmith' });
```

What the user owned does not go with them. Move it first with the `TransferUser...` family -
[TransferUserDocumentOwnerships](TransferUserDocumentOwnerships.md) and its neighbours - or it is
left pointing at an account that is gone.

## Notes

- The `UserName` parameter accepts either a plain username string (e.g., `jdoe`) or a short ID reference in the format `ID:userid` (e.g., `ID:123`).
- If the system is configured to require administrator password confirmation for user deletion (`PasswordRePromptActions.UserDelete = true`) and Windows Authentication is not enabled, this method returns error `[2767]` and requires `DeleteUser1` instead.
- Deleting a user is permanent and cannot be undone.
- Before deleting a user, consider using the `TransferUser*` APIs to transfer the user's data (documents, tasks, subscriptions) to another user.

---

## Related APIs

- [DeleteUser1](DeleteUser1.md) - Delete a user with administrator password confirmation
- [UserExists](UserExists.md) - Check if a user exists before attempting deletion
- [TransferUserDocumentOwnerships](TransferUserDocumentOwnerships.md) - Transfer document ownerships before deletion
- [TransferUserTasks](TransferUserTasks.md) - Transfer workflow tasks before deletion
- [ChangeUserStatus](ChangeUserStatus.md) - Disable a user account without deleting it

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4030` | there is no ticket at all, or the caller is not allowed to delete users |
| `4000` | no user by that name - including a user already deleted, so a second delete is refused rather than accepted |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

---
