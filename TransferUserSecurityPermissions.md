# TransferUserSecurityPermissions API

Transfers security permissions (ACL entries) from one user to another. The target user receives all folder and document access rights that were individually assigned to the source user.

## Endpoint

```
/srv.asmx/TransferUserSecurityPermissions
```

## Methods

- **GET** `/srv.asmx/TransferUserSecurityPermissions?authenticationTicket=...&fromUserName=...&toUserName=...`
- **POST** `/srv.asmx/TransferUserSecurityPermissions` (form data)
- **SOAP** Action: `http://tempuri.org/TransferUserSecurityPermissions`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `fromUserName` | string | Yes | The username whose security permissions will be transferred. |
| `toUserName` | string | Yes | The username who will receive the security permissions. |

---

## Response

### Success Response

```xml
<root success="true" />
```

### Success Response (with warnings)

```xml
<root success="true" warnings="Some permissions could not be transferred." />
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
GET /srv.asmx/TransferUserSecurityPermissions
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &fromUserName=jdoe
  &toUserName=jsmith
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/TransferUserSecurityPermissions HTTP/1.1
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
    <tns:TransferUserSecurityPermissions>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:FromUserName>jdoe</tns:FromUserName>
      <tns:ToUserName>jsmith</tns:ToUserName>
    </tns:TransferUserSecurityPermissions>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Transfers individually assigned ACL entries on folders and documents. Permissions granted through user group membership are not affected.
- If `toUserName` already has an explicit permission entry on a given object, the existing entry may be updated or merged.
- The response root element is `<root>`, not `<response>`.
- Typically used as part of a user offboarding process before deleting the source user.

---

## Related APIs

- [TransferUserDomainMemberships](TransferUserDomainMemberships) - Transfer domain memberships
- [TransferUserFolderOwnerships](TransferUserFolderOwnerships) - Transfer folder ownerships
- [SetAccessList](SetAccessList) - Manually set access lists
- [DeleteUser](DeleteUser) - Delete a user after transferring their data

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

*For detailed documentation visit: https://support.inforouter.com/api-docs/TransferUserSecurityPermissions*
