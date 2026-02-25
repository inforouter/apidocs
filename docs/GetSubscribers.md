# GetSubscribers API

Returns the complete subscriber list of a document or folder at the specified path. The response includes both individual user subscribers and user group subscribers, each with their configured event notification flags. Use this API to audit who is subscribed to a document or folder and which events they are watching.

## Endpoint

```
/srv.asmx/GetSubscribers
```

## Methods

- **GET** `/srv.asmx/GetSubscribers?authenticationTicket=...&path=...`
- **POST** `/srv.asmx/GetSubscribers` (form data)
- **SOAP** Action: `http://tempuri.org/GetSubscribers`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full infoRouter path to the document or folder (e.g. `/Finance/Reports/Q1-Report.pdf` or `/Finance/Reports`). Supports short document ID paths (`~D{id}` or `~D{id}.ext`). The API automatically detects whether the path refers to a document or a folder. |

---

## Response

### Success Response

Returns a `<response>` element with `success="TRUE"` containing a `<subscribers>` element. The `<subscribers>` element holds zero or more `<usersubscriber>` elements (for individual users) followed by zero or more `<groupsubscriber>` elements (for user groups).

```xml
<response success="TRUE" error="">
  <subscribers>
    <usersubscriber>
      <userid>7</userid>
      <username>jsmith</username>
      <firstname>John</firstname>
      <lastname>Smith</lastname>
      <email>jsmith@example.com</email>
      <emailtype>HTML</emailtype>
      <language>en</language>
      <attachdocumenttoemail>FALSE</attachdocumenttoemail>
      <userstatus>1</userstatus>
      <on_read>FALSE</on_read>
      <on_change>TRUE</on_change>
      <on_update>TRUE</on_update>
      <on_checkout>FALSE</on_checkout>
      <on_approve>TRUE</on_approve>
      <on_reject>TRUE</on_reject>
      <on_comment>TRUE</on_comment>
      <on_move>TRUE</on_move>
      <on_delete>TRUE</on_delete>
      <on_checkin>FALSE</on_checkin>
      <on_newdoc>FALSE</on_newdoc>
    </usersubscriber>
    <groupsubscriber>
      <groupid>14</groupid>
      <groupname>Finance-Managers</groupname>
      <on_read>FALSE</on_read>
      <on_change>TRUE</on_change>
      <on_update>TRUE</on_update>
      <on_checkout>FALSE</on_checkout>
      <on_approve>TRUE</on_approve>
      <on_reject>TRUE</on_reject>
      <on_comment>FALSE</on_comment>
      <on_move>TRUE</on_move>
      <on_delete>TRUE</on_delete>
      <on_checkin>FALSE</on_checkin>
      <on_newdoc>TRUE</on_newdoc>
    </groupsubscriber>
  </subscribers>
</response>
```

### Empty Result (No Subscribers)

```xml
<response success="TRUE" error="">
  <subscribers />
</response>
```

### Error Response

```xml
<response success="false" error="Document not found." />
```

---

### usersubscriber Element Fields

| Field | Type | Description |
|-------|------|-------------|
| `userid` | int | Unique ID of the subscribed user. |
| `username` | string | Login name of the subscribed user. |
| `firstname` | string | First name of the subscribed user. |
| `lastname` | string | Last name of the subscribed user. |
| `email` | string | Email address of the subscribed user. |
| `emailtype` | string | Email format preference (e.g. `HTML` or `TEXT`). |
| `language` | string | Language code for the user's notification emails. |
| `attachdocumenttoemail` | TRUE/FALSE | Whether the document is attached to notification emails. |
| `userstatus` | int | User account status: `1` = active, `0` = inactive/disabled. |
| `on_read` | TRUE/FALSE | Subscribed to read/download events. |
| `on_change` | TRUE/FALSE | Subscribed to property/metadata change events. |
| `on_update` | TRUE/FALSE | Subscribed to new version upload events. |
| `on_checkout` | TRUE/FALSE | Subscribed to checkout events. |
| `on_approve` | TRUE/FALSE | Subscribed to approval events. |
| `on_reject` | TRUE/FALSE | Subscribed to rejection events. |
| `on_comment` | TRUE/FALSE | Subscribed to comment events. |
| `on_move` | TRUE/FALSE | Subscribed to move events. |
| `on_delete` | TRUE/FALSE | Subscribed to deletion events. |
| `on_checkin` | TRUE/FALSE | Subscribed to check-in events. |
| `on_newdoc` | TRUE/FALSE | Subscribed to new document events (folder subscriptions only; always FALSE for document subscriptions). |

### groupsubscriber Element Fields

| Field | Type | Description |
|-------|------|-------------|
| `groupid` | int | Unique ID of the subscribed user group. |
| `groupname` | string | Name of the subscribed user group. |
| `on_read` -" `on_newdoc` | TRUE/FALSE | Same event flags as for user subscribers (see table above). |

---

## Required Permissions

Any authenticated user with **read access** to the document or folder can call this API.

---

## Example

### GET Request

```
GET /srv.asmx/GetSubscribers
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &path=/Finance/Reports/Q1-2024-Report.pdf
HTTP/1.1
```

### GET Request -" Folder

```
GET /srv.asmx/GetSubscribers
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &path=/Finance/Reports
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetSubscribers HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&path=/Finance/Reports/Q1-2024-Report.pdf
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetSubscribers>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:Path>/Finance/Reports/Q1-2024-Report.pdf</tns:Path>
    </tns:GetSubscribers>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- **Document and Folder**: The same API serves both documents and folders. The path is resolved first as a document; if not found, it is resolved as a folder. If neither is found, an error is returned.
- **User Subscribers Sorted**: User subscribers are returned sorted by first name in ascending order.
- **Group Subscribers Sorted**: Group subscribers are returned sorted by group name in ascending order.
- **on_newdoc for Documents**: The `on_newdoc` field is always `FALSE` for document subscriber entries, since new-document events only apply to folder subscriptions.
- **userstatus Values**: A `userstatus` of `1` indicates an active account; `0` indicates a disabled or inactive account. Disabled users will not receive notifications.
- **Short Path Support**: The `path` parameter supports short document ID notation: `~D123` or `~D123.pdf`.
- **Empty List**: If no subscribers exist, the `<subscribers>` element is returned empty -" this is not an error.
- **Response Case**: The `success` attribute value is `TRUE` (uppercase) on success, unlike most other APIs which use lowercase `true`.

---

## Related APIs

- [AddUserToDocumentSubscribers](AddUserToDocumentSubscribers.md) - Add a user to a document's subscription list
- [AddUserToFolderSubscribers](AddUserToFolderSubscribers.md) - Add a user to a folder's subscription list
- [AddUsergroupToDocumentSubscribers](AddUsergroupToDocumentSubscribers.md) - Add a user group to a document's subscription list
- [AddUsergroupToFolderSubscribers](AddUsergroupToFolderSubscribers.md) - Add a user group to a folder's subscription list
- [RemoveUserFromDocumentSubscribers](RemoveUserFromDocumentSubscribers.md) - Remove a user from a document's subscription list
- [GetSubscriptions](GetSubscriptions.md) - Get all subscriptions for the current user

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Document not found / Folder not found | The specified path does not resolve to an existing document or folder. |
| Insufficient rights | The calling user does not have read access to the document or folder. |
| `SystemError:...` | An unexpected server-side error occurred. |

---
