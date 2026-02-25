# TransferUserFolderOwnerships API

Transfers folder ownerships from one user to another. All folders owned by the source user are reassigned to the target user.

## Endpoint

```
/srv.asmx/TransferUserFolderOwnerships
```

## Methods

- **GET** `/srv.asmx/TransferUserFolderOwnerships?authenticationTicket=...&fromUserName=...&toUserName=...`
- **POST** `/srv.asmx/TransferUserFolderOwnerships` (form data)
- **SOAP** Action: `http://tempuri.org/TransferUserFolderOwnerships`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `fromUserName` | string | Yes | The username whose folder ownerships will be transferred. |
| `toUserName` | string | Yes | The username who will become the new owner of the folders. |

---

## Response

### Success Response

```xml
<root success="true" />
```

### Success Response (with warnings)

```xml
<root success="true" warnings="Some folder ownerships could not be transferred." />
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
GET /srv.asmx/TransferUserFolderOwnerships
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &fromUserName=jdoe
  &toUserName=jsmith
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/TransferUserFolderOwnerships HTTP/1.1
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
    <tns:TransferUserFolderOwnerships>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:FromUserName>jdoe</tns:FromUserName>
      <tns:ToUserName>jsmith</tns:ToUserName>
    </tns:TransferUserFolderOwnerships>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Reassigns the ownership of all folders where `fromUserName` is currently the owner.
- The response root element is `<root>`, not `<response>`.
- Typically used as part of a user offboarding process before deleting the source user.

---

## Related APIs

- [TransferUserDocumentOwnerships](TransferUserDocumentOwnerships.md) - Transfer document ownerships
- [TransferUserFolderSubscriptions](TransferUserFolderSubscriptions.md) - Transfer folder subscriptions
- [SetOwner](SetOwner.md) - Manually set owner of a folder or document
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

*For detailed documentation visit: https://support.inforouter.com/api-docs/TransferUserFolderOwnerships*
