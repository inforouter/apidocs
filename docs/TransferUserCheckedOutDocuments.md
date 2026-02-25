# TransferUserCheckedOutDocuments API

Transfers checked-out documents from one user to another. The check-out ownership is reassigned so the target user can check in or cancel the check-out.

## Endpoint

```
/srv.asmx/TransferUserCheckedOutDocuments
```

## Methods

- **GET** `/srv.asmx/TransferUserCheckedOutDocuments?authenticationTicket=...&fromUserName=...&toUserName=...`
- **POST** `/srv.asmx/TransferUserCheckedOutDocuments` (form data)
- **SOAP** Action: `http://tempuri.org/TransferUserCheckedOutDocuments`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `fromUserName` | string | Yes | The username whose checked-out documents will be transferred. |
| `toUserName` | string | Yes | The username who will take ownership of the checked-out documents. |

---

## Response

### Success Response

```xml
<root success="true" />
```

### Success Response (with warnings)

```xml
<root success="true" warnings="Some checked-out documents could not be transferred." />
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
GET /srv.asmx/TransferUserCheckedOutDocuments
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &fromUserName=jdoe
  &toUserName=jsmith
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/TransferUserCheckedOutDocuments HTTP/1.1
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
    <tns:TransferUserCheckedOutDocuments>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:FromUserName>jdoe</tns:FromUserName>
      <tns:ToUserName>jsmith</tns:ToUserName>
    </tns:TransferUserCheckedOutDocuments>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Reassigns the check-out lock ownership from `fromUserName` to `toUserName`.
- Documents remain checked out; only the ownership of the check-out changes.
- The response root element is `<root>`, not `<response>`.
- Typically used as part of a user offboarding process before deleting the source user.

---

## Related APIs

- [TransferUserDocumentOwnerships](TransferUserDocumentOwnerships.md) - Transfer document ownerships
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

*For detailed documentation visit: https://support.inforouter.com/api-docs/TransferUserCheckedOutDocuments*
