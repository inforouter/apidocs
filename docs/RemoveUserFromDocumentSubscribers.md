# RemoveUserFromDocumentSubscribers API

Removes a specified user from the subscription list of a document. After removal, the user will no longer receive email notifications for any events on that document. Use this API to clean up subscriptions when a user no longer needs to track a document, or as part of a user offboarding workflow.

## Endpoint

```
/srv.asmx/RemoveUserFromDocumentSubscribers
```

## Methods

- **GET** `/srv.asmx/RemoveUserFromDocumentSubscribers?authenticationTicket=...&documentPath=...&userName=...`
- **POST** `/srv.asmx/RemoveUserFromDocumentSubscribers` (form data)
- **SOAP** Action: `http://tempuri.org/RemoveUserFromDocumentSubscribers`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `documentPath` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1-Report.pdf`). Supports short document ID paths (`~D{id}` or `~D{id}.ext`). |
| `userName` | string | Yes | Login name of the user to remove from the subscription list. |

---

## Response

### Success Response

```xml
<response success="true" error="" />
```

### Error Response

```xml
<response success="false" error="Document not found." />
```

---

## Required Permissions

The calling user must be authenticated. To remove another user from the subscription list, the calling user must have **write access** or **manage access** to the document. A user may remove themselves if they have read access.

---

## Example

### GET Request

```
GET /srv.asmx/RemoveUserFromDocumentSubscribers
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &documentPath=/Finance/Reports/Q1-2024-Report.pdf
  &userName=jsmith
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/RemoveUserFromDocumentSubscribers HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&documentPath=/Finance/Reports/Q1-2024-Report.pdf
&userName=jsmith
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:RemoveUserFromDocumentSubscribers>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:DocumentPath>/Finance/Reports/Q1-2024-Report.pdf</tns:DocumentPath>
      <tns:UserName>jsmith</tns:UserName>
    </tns:RemoveUserFromDocumentSubscribers>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- **Not Subscribed**: If the specified user is not currently subscribed to the document, the API returns `success="true"` -" it does not treat this as an error.
- **User Must Exist**: The `userName` must match an existing infoRouter user account. If the user does not exist, an error is returned.
- **Group Subscriptions Not Affected**: This API only removes individual user subscriptions. If the user receives notifications because they are a member of a subscribed group, removing their individual subscription will not stop group-based notifications. Use `RemoveUsergroupFromDocumentSubscribers` to remove a group subscription.
- **Short Path Support**: The `documentPath` parameter supports short document ID notation: `~D123` or `~D123.pdf`.
- **Folder Subscriptions**: This API operates on document subscriptions only. To manage folder subscriptions, use `RemoveUserFromFolderSubscribers` (currently listed separately). Note: the underlying `RemoveSubscriber` implementation also supports folders but this endpoint is intended for documents.

---

## Related APIs

- [AddUserToDocumentSubscribers](AddUserToDocumentSubscribers.md) - Add a user to a document's subscription list
- [RemoveUsergroupFromDocumentSubscribers](RemoveUsergroupFromDocumentSubscribers.md) - Remove a user group from a document's subscription list
- [GetSubscribers](GetSubscribers.md) - Get the full subscriber list of a document or folder
- [GetSubscriptions](GetSubscriptions.md) - Get all subscriptions for the current user

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Document not found | The specified documentPath does not resolve to an existing document. |
| User not found | The specified userName does not match an existing user account. |
| Insufficient rights | The calling user does not have permission to manage subscriptions for this document. |
| `SystemError:...` | An unexpected server-side error occurred. |

---
