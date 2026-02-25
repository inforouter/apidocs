# DeleteUser1 API

Deletes the specified infoRouter user account with administrator password confirmation. Use this API instead of `DeleteUser` when the system requires password re-prompting for user deletion.

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

## Notes

- This method performs administrator password verification before proceeding with deletion. The `UserPassword` is the password of the **calling administrator**, not the user being deleted.
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

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `[900] Authentication failed` | The provided `UserPassword` is incorrect. |
| User not found | The specified username does not exist. |
| Access denied | The calling user is not a system administrator. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/DeleteUser1*
