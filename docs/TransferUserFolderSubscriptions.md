# TransferUserFolderSubscriptions API

Transfers folder subscriptions from one user to another. The target user is subscribed to all folders that the source user currently subscribes to.

## Endpoint

```
/srv.asmx/TransferUserFolderSubscriptions
```

## Methods

- **GET** `/srv.asmx/TransferUserFolderSubscriptions?authenticationTicket=...&fromUserName=...&toUserName=...`
- **POST** `/srv.asmx/TransferUserFolderSubscriptions` (form data)
- **SOAP** Action: `http://tempuri.org/TransferUserFolderSubscriptions`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `fromUserName` | string | Yes | The username whose folder subscriptions will be transferred. |
| `toUserName` | string | Yes | The username who will receive the folder subscriptions. |

---

## Response

### Success Response

```xml
<root success="true" />
```

### Success Response (with warnings)

```xml
<root success="true" warnings="Some folder subscriptions could not be transferred." />
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
GET /srv.asmx/TransferUserFolderSubscriptions
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &fromUserName=jdoe
  &toUserName=jsmith
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/TransferUserFolderSubscriptions HTTP/1.1
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
    <tns:TransferUserFolderSubscriptions>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:FromUserName>jdoe</tns:FromUserName>
      <tns:ToUserName>jsmith</tns:ToUserName>
    </tns:TransferUserFolderSubscriptions>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- The `toUserName` is subscribed to all folders that `fromUserName` is currently subscribed to.
- Folders where `toUserName` is already subscribed are skipped without error.
- The response root element is `<root>`, not `<response>`.
- Typically used as part of a user offboarding process before deleting the source user.

---

## Related APIs

- [TransferUserDocumentSubscriptions](TransferUserDocumentSubscriptions.md) - Transfer document subscriptions
- [TransferUserFolderOwnerships](TransferUserFolderOwnerships.md) - Transfer folder ownerships
- [DeleteUser](DeleteUser.md) - Delete a user after transferring their data

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| User not found | The specified `fromUserName` or `toUserName` does not exist. |
| Access denied | The calling user is not a system administrator. |
| `SystemError:...` | An unexpected server-side error occurred. |

---