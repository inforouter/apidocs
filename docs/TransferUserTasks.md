# TransferUserTasks API

Transfers all open workflow tasks from one user to another. Used when a user is leaving or is temporarily unavailable.

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

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| User not found | The specified `fromUserName` or `toUserName` does not exist. |
| Access denied | The calling user is not a system administrator. |
| `SystemError:...` | An unexpected server-side error occurred. |

---