# TransferUserWorkflowDefinitions API

Transfers workflow definition roles (assignees and supervisors) from one user to another. The target user replaces the source user in all workflow definitions where the source user is assigned as an assignee or supervisor.

## Endpoint

```
/srv.asmx/TransferUserWorkflowDefinitions
```

## Methods

- **GET** `/srv.asmx/TransferUserWorkflowDefinitions?authenticationTicket=...&fromUserName=...&toUserName=...`
- **POST** `/srv.asmx/TransferUserWorkflowDefinitions` (form data)
- **SOAP** Action: `http://tempuri.org/TransferUserWorkflowDefinitions`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `fromUserName` | string | Yes | The username whose workflow definition roles will be transferred. |
| `toUserName` | string | Yes | The username who will take over the workflow definition roles. |

---

## Response

### Success Response

```xml
<root success="true" />
```

### Success Response (with warnings)

```xml
<root success="true" warnings="Some workflow roles could not be transferred." />
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
GET /srv.asmx/TransferUserWorkflowDefinitions
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &fromUserName=jdoe
  &toUserName=jsmith
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/TransferUserWorkflowDefinitions HTTP/1.1
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
    <tns:TransferUserWorkflowDefinitions>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:FromUserName>jdoe</tns:FromUserName>
      <tns:ToUserName>jsmith</tns:ToUserName>
    </tns:TransferUserWorkflowDefinitions>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Transfers the source user's roles in workflow **definitions** (templates), not active workflow instances (tasks). To transfer active tasks, use `TransferUserTasks`.
- The response root element is `<root>`, not `<response>`.
- Typically used as part of a user offboarding process before deleting the source user.

---

## Related APIs

- [TransferUserTasks](TransferUserTasks.md) - Transfer active workflow tasks
- [TransferUserISOTasks](TransferUserISOTasks.md) - Transfer ISO review tasks
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