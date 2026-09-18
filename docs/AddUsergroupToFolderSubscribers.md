# AddUsergroupToFolderSubscribers API

Adds a specified user group to the subscription list of a folder, configuring which events trigger email notifications to all members of that group. Optionally cascades the subscription to all existing sub-folders. This is the user group equivalent of `AddUserToFolderSubscribers` -" it subscribes all members of a group at once rather than individual users.

> **Only a global user group can be subscribed.** The group is looked up with no library name, so
> a group that belongs to a library is never found and the call is refused with `4041` - reading as
> though the group does not exist, when it plainly does. Create the group with an empty
> `DomainName` if it has to be subscribed to anything.

## Endpoint

```

/srv.asmx/AddUsergroupToFolderSubscribers

```

## Methods

- **GET** `/srv.asmx/AddUsergroupToFolderSubscribers?authenticationTicket=...&folderPath=...&groupName=...&ON_READ=...&...`

- **POST** `/srv.asmx/AddUsergroupToFolderSubscribers` (form data)

- **SOAP** Action: `http://tempuri.org/AddUsergroupToFolderSubscribers`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `folderPath` | string | Yes | Full infoRouter path to the folder (e.g. `/Finance/Reports`). |
| `groupName` | string | Yes | Name of the user group to add as a subscriber. Must be a **global** group. A group that belongs to a library is never found - the lookup is done with no library name - and the call is refused as though no such group existed. |
| `ON_READ` | bool | Yes | If `true`, notify the group when a document in the folder is read or downloaded. |
| `ON_CHANGE` | bool | Yes | If `true`, notify the group when a document's properties or metadata are changed. |
| `ON_UPDATE` | bool | Yes | If `true`, notify the group when a new version of a document is uploaded. |
| `ON_CHECKOUT` | bool | Yes | If `true`, notify the group when a document is checked out. |
| `ON_APPROVE` | bool | Yes | If `true`, notify the group when a document version is approved. |
| `ON_REJECT` | bool | Yes | If `true`, notify the group when a document version is rejected. |
| `ON_COMMENT` | bool | Yes | If `true`, notify the group when a comment is added to a document. |
| `ON_MOVE` | bool | Yes | If `true`, notify the group when a document or sub-folder is moved. |
| `ON_DELETE` | bool | Yes | If `true`, notify the group when a document or sub-folder is deleted. |
| `ON_CHECKIN` | bool | Yes | If `true`, notify the group when a document is checked in. |
| `ON_NEWDOC` | bool | Yes | If `true`, notify the group when a new document is added to the folder. |
| `IncludeSubObjects` | bool | Yes | If `true`, the subscription is cascaded recursively to all existing sub-folders. |

### Boolean Parameter Format

All boolean parameters accept:

- `true` or `True` or `1` -" enable

- `false` or `False` or `0` -" disable

---

## Response

### Success Response

```xml

<response success="true" error="" />

```

### Error Response

```xml

<response success="false" error="Folder not found." />

```

---

## Required Permissions

The calling user must be authenticated. To add a user group as a subscriber, the calling user must have **write access** or **manage access** to the folder.

---

## Example

### GET Request

```

GET /srv.asmx/AddUsergroupToFolderSubscribers

  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

  &folderPath=/Finance/Reports

  &groupName=Finance-Managers

  &ON_READ=false

  &ON_CHANGE=true

  &ON_UPDATE=true

  &ON_CHECKOUT=false

  &ON_APPROVE=true

  &ON_REJECT=true

  &ON_COMMENT=true

  &ON_MOVE=true

  &ON_DELETE=true

  &ON_CHECKIN=false

  &ON_NEWDOC=true

  &IncludeSubObjects=true

HTTP/1.1

```

### POST Request

```

POST /srv.asmx/AddUsergroupToFolderSubscribers HTTP/1.1

Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

&folderPath=/Finance/Reports

&groupName=Finance-Managers

&ON_READ=false

&ON_CHANGE=true

&ON_UPDATE=true

&ON_CHECKOUT=false

&ON_APPROVE=true

&ON_REJECT=true

&ON_COMMENT=true

&ON_MOVE=true

&ON_DELETE=true

&ON_CHECKIN=false

&ON_NEWDOC=true

&IncludeSubObjects=true

```

### SOAP Request

```xml

<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"

               xmlns:tns="http://tempuri.org/">

  <soap:Body>

    <tns:AddUsergroupToFolderSubscribers>

      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>

      <tns:folderPath>/Finance/Reports</tns:folderPath>

      <tns:groupName>Finance-Managers</tns:groupName>

      <tns:ON_READ>false</tns:ON_READ>

      <tns:ON_CHANGE>true</tns:ON_CHANGE>

      <tns:ON_UPDATE>true</tns:ON_UPDATE>

      <tns:ON_CHECKOUT>false</tns:ON_CHECKOUT>

      <tns:ON_APPROVE>true</tns:ON_APPROVE>

      <tns:ON_REJECT>true</tns:ON_REJECT>

      <tns:ON_COMMENT>true</tns:ON_COMMENT>

      <tns:ON_MOVE>true</tns:ON_MOVE>

      <tns:ON_DELETE>true</tns:ON_DELETE>

      <tns:ON_CHECKIN>false</tns:ON_CHECKIN>

      <tns:ON_NEWDOC>true</tns:ON_NEWDOC>

      <tns:IncludeSubObjects>true</tns:IncludeSubObjects>

    </tns:AddUsergroupToFolderSubscribers>

  </soap:Body>

</soap:Envelope>

```

---

## JavaScript

Every call answers XML with HTTP 200, success or not, so `success` is the thing to branch on and
`errorCode` is the number to report.

```javascript
async function call(action, params) {
  const response = await fetch(`/srv.asmx/${action}?${new URLSearchParams(params)}`);
  const root = new DOMParser()
    .parseFromString(await response.text(), 'text/xml')
    .documentElement;

  if (root.getAttribute('success') !== 'true') {
    throw new Error(`${root.getAttribute('errorCode')}: ${root.getAttribute('error')}`);
  }
  return root;
}
```

Subscribes a global user group to a folder, and optionally to everything inside it.

```javascript
await call('AddUsergroupToFolderSubscribers', {
  authenticationTicket: ticket,
  folderPath: '/Public/Reports',
  groupName: 'Auditors',
  ON_READ: true, ON_CHANGE: true, ON_UPDATE: false, ON_CHECKOUT: false, ON_APPROVE: false,
  ON_REJECT: false, ON_COMMENT: false, ON_MOVE: false, ON_DELETE: true, ON_CHECKIN: false,
  ON_NEWDOC: true,
  IncludeSubObjects: true,
});
```

## Notes

- **Update vs Add**: If the user group is already a subscriber to the folder, this API **updates** the existing event flags rather than creating a duplicate entry.

- **All Flags Required**: All eleven event flag parameters are required and must be explicitly passed. Omitting a flag may result in a parse error or that flag defaulting to `false`.

- **IncludeSubObjects**: When `true`, the subscription is applied recursively to all sub-folders **existing at the time of the call**. Sub-folders created **after** this call will **not** automatically inherit the group subscription.

- **ON_NEWDOC**: This flag is unique to folder subscriptions. It triggers a notification whenever a new document is created or registered in the folder. This flag does not exist in document-level subscriptions.

- **Group Membership**: All current members of the named group will receive notifications. New group members added after the subscription is created will also automatically receive notifications because notifications are sent to all current group members at the time the event fires.

- **Duplicate Notifications**: If a user is both individually subscribed to the folder and a member of a subscribed group, they may receive duplicate notifications for the same event.

- **Global groups only**: a library's own group cannot be subscribed. The group is looked up with an empty library name, so only a global group is ever found and a library group is refused with `4041`.

- **Notifications by Email**: Subscriptions trigger email notifications when the configured events occur. Email notifications require a properly configured email server in the infoRouter settings.

---

## Event Flags Reference

| Flag | Event Description |
|------|-----------------|
| `ON_READ` | A document in the folder was read or downloaded |
| `ON_CHANGE` | A document's properties or metadata were changed |
| `ON_UPDATE` | A new version of a document was uploaded |
| `ON_CHECKOUT` | A document was checked out for editing |
| `ON_APPROVE` | A document version was approved |
| `ON_REJECT` | A document version was rejected |
| `ON_COMMENT` | A comment was added to a document |
| `ON_MOVE` | A document or sub-folder was moved |
| `ON_DELETE` | A document or sub-folder was deleted |
| `ON_CHECKIN` | A document was checked in after editing |
| `ON_NEWDOC` | A new document was added to the folder *(folder-only flag)* |

---

## Related APIs

- [AddUsergroupToDocumentSubscribers](AddUsergroupToDocumentSubscribers.md) - Add a user group to a specific document's subscription list

- [AddUserToFolderSubscribers](AddUserToFolderSubscribers.md) - Add an individual user to a folder's subscription list

- [RemoveUsergroupFromFolderSubscribers](RemoveUsergroupFromFolderSubscribers.md) - Remove a user group from a folder's subscription list

- [GetSubscribers](GetSubscribers.md) - Get the full subscriber list of a document or folder

- [GetSubscriptions](GetSubscriptions.md) - Get all subscriptions for the current user

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | no folder at that path, including one the caller may not see |
| `4041` | no global user group by that name - including a group that exists but belongs to a library |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

The ten event flags are the same on every add operation, and all ten have to be sent: they are
declared as plain booleans, so a missing one is a model binding failure rather than a default.
`ON_NEWDOC` is the eleventh, and belongs to the folder forms only.

---
