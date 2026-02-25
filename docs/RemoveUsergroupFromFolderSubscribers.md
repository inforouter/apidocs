# RemoveUsergroupFromFolderSubscribers API

Removes the specified user group from the subscription list of a folder. After removal, members of that group will no longer receive email notifications via the group subscription for any events on that folder. Optionally removes the group from all sub-folders and documents within the folder as well.

## Endpoint

```
/srv.asmx/RemoveUsergroupFromFolderSubscribers
```

## Methods

- **GET** `/srv.asmx/RemoveUsergroupFromFolderSubscribers?AuthenticationTicket=...&FolderPath=...&groupName=...&IncludeSubObjects=...`
- **POST** `/srv.asmx/RemoveUsergroupFromFolderSubscribers` (form data)
- **SOAP** Action: `http://tempuri.org/RemoveUsergroupFromFolderSubscribers`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `FolderPath` | string | Yes | Full infoRouter path to the folder (e.g. `/Finance/Reports`). The folder must already exist. |
| `groupName` | string | Yes | Name of the user group to remove from the folder's subscription list. Can be a local or global group. |
| `IncludeSubObjects` | bool | Yes | When `true`, also removes the group subscription from all sub-folders and documents nested within the specified folder. When `false`, only the subscription on the specified folder itself is removed. |

---

## Response

### Success Response

```xml
<response success="true" error="" />
```

### Error Response

```xml
<response success="false" error="User group not found." />
```

---

## Required Permissions

The calling user must be authenticated. To remove a user group from a folder's subscription list, the calling user must have **write access** or **manage access** to the folder.

---

## Example

### GET Request

```
GET /srv.asmx/RemoveUsergroupFromFolderSubscribers
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &FolderPath=/Finance/Reports
  &groupName=Finance-Managers
  &IncludeSubObjects=true
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/RemoveUsergroupFromFolderSubscribers HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&FolderPath=/Finance/Reports
&groupName=Finance-Managers
&IncludeSubObjects=true
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:RemoveUsergroupFromFolderSubscribers>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:FolderPath>/Finance/Reports</tns:FolderPath>
      <tns:groupName>Finance-Managers</tns:groupName>
      <tns:IncludeSubObjects>true</tns:IncludeSubObjects>
    </tns:RemoveUsergroupFromFolderSubscribers>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- **Not Subscribed**: If the specified group is not currently subscribed to the folder, the API returns `success="true"` -" it does not treat this as an error.
- **Group Must Exist**: The `groupName` must match an existing infoRouter user group (local or global). If the group is not found, an error is returned.
- **IncludeSubObjects**: When `true`, the removal is applied recursively to all sub-folders and documents existing at the time of the call. Items created after this call will not be affected retroactively.
- **Individual User Subscriptions Unaffected**: This API only removes the group-level subscription. Individual users who are members of the group and have their own personal subscriptions will continue to receive notifications. Use `RemoveUserFromFolderSubscribers` to remove individual user subscriptions.
- **Local vs Global Groups**: Both local groups (defined within a library) and global groups (system-wide) can be removed. The `groupName` must match the group's name exactly.
- **Document Group Subscriptions**: This API operates on folder subscriptions only. To remove a group from a document subscription, use `RemoveUsergroupFromDocumentSubscribers`.

---

## Related APIs

- [AddUsergroupToFolderSubscribers](AddUsergroupToFolderSubscribers.md) - Add a user group to a folder's subscription list
- [RemoveUserFromFolderSubscribers](RemoveUserFromFolderSubscribers.md) - Remove an individual user from a folder's subscription list
- [RemoveUsergroupFromDocumentSubscribers](RemoveUsergroupFromDocumentSubscribers.md) - Remove a user group from a document's subscription list
- [GetSubscribers](GetSubscribers.md) - Get the full subscriber list of a document or folder
- [GetSubscriptions](GetSubscriptions.md) - Get all subscriptions for the current user

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Folder not found | The specified `FolderPath` does not resolve to an existing folder. |
| User group not found | The specified `groupName` does not match an existing user group. |
| Insufficient rights | The calling user does not have permission to manage subscriptions for this folder. |
| `SystemError:...` | An unexpected server-side error occurred. |

---
