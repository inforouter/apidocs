# AddUserToFolderSubscribers API

Adds a user to the subscription list of a folder. The subscriber receives email notifications for the selected events on the folder and, optionally, all subfolders and their documents.

## Endpoint

```
/srv.asmx/AddUserToFolderSubscribers
```

## Methods

- **GET** `/srv.asmx/AddUserToFolderSubscribers?authenticationTicket=...&FolderPath=...&UserName=...&ON_READ=...&...&IncludeSubObjects=...`
- **POST** `/srv.asmx/AddUserToFolderSubscribers` (form data)
- **SOAP** Action: `http://tempuri.org/AddUserToFolderSubscribers`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `FolderPath` | string | Yes | Full infoRouter path to the folder (e.g. `/Finance/Reports`). |
| `UserName` | string | Yes | Login name of the user to subscribe. |
| `ON_READ` | boolean | Yes | `true` to notify when documents in the folder are read/viewed. |
| `ON_CHANGE` | boolean | Yes | `true` to notify when folder or document metadata changes. |
| `ON_UPDATE` | boolean | Yes | `true` to notify when a new document version is uploaded. |
| `ON_CHECKOUT` | boolean | Yes | `true` to notify when a document is checked out. |
| `ON_APPROVE` | boolean | Yes | `true` to notify when a document or workflow step is approved. |
| `ON_REJECT` | boolean | Yes | `true` to notify when a document or workflow step is rejected. |
| `ON_COMMENT` | boolean | Yes | `true` to notify when a comment is added to a document. |
| `ON_MOVE` | boolean | Yes | `true` to notify when a document or subfolder is moved. |
| `ON_DELETE` | boolean | Yes | `true` to notify when a document or subfolder is deleted. |
| `ON_CHECKIN` | boolean | Yes | `true` to notify when a document is checked in. |
| `ON_NEWDOC` | boolean | Yes | `true` to notify when a new document is added to the folder. |
| `IncludeSubObjects` | boolean | Yes | `true` to also apply this subscription to all subfolders and their documents recursively. `false` to subscribe to the specified folder only. |

## Response

### Success Response

```xml
<response success="true"/>
```

### Error Response

```xml
<response success="false" error="[901]Session expired or Invalid ticket"/>
```

## Required Permissions

Any authenticated user may call this API. The specified user and folder must both exist.

## Example

### GET Request -" subscribe to folder and all subfolders

```
GET /srv.asmx/AddUserToFolderSubscribers
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &FolderPath=/Finance/Reports
    &UserName=jdoe
    &ON_READ=false
    &ON_CHANGE=false
    &ON_UPDATE=true
    &ON_CHECKOUT=false
    &ON_APPROVE=false
    &ON_REJECT=false
    &ON_COMMENT=false
    &ON_MOVE=false
    &ON_DELETE=false
    &ON_CHECKIN=false
    &ON_NEWDOC=true
    &IncludeSubObjects=true
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/AddUserToFolderSubscribers HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&FolderPath=/Finance/Reports&UserName=jdoe&ON_READ=false&ON_CHANGE=false&ON_UPDATE=true&ON_CHECKOUT=false&ON_APPROVE=false&ON_REJECT=false&ON_COMMENT=false&ON_MOVE=false&ON_DELETE=false&ON_CHECKIN=false&ON_NEWDOC=true&IncludeSubObjects=true
```

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

Subscribes one user to one folder, and optionally to everything inside it.

```javascript
await call('AddUserToFolderSubscribers', {
  authenticationTicket: ticket,
  FolderPath: '/Public/Reports',
  UserName: 'jsmith',
  ON_READ: true, ON_CHANGE: true, ON_UPDATE: false, ON_CHECKOUT: false, ON_APPROVE: false,
  ON_REJECT: false, ON_COMMENT: false, ON_MOVE: false, ON_DELETE: true, ON_CHECKIN: false,
  ON_NEWDOC: true,              // folders only: a new document arrived
  IncludeSubObjects: true,      // subfolders and their documents as well
});
```

With `IncludeSubObjects=false` only the folder itself is subscribed; the documents already in it
are not. With `true` the whole tree below it is subscribed in the same call.

## Notes

- `ON_NEWDOC` is unique to folder subscriptions and fires when a document is added to the subscribed folder.
- When `IncludeSubObjects = true`, the subscription is applied to all subfolders recursively at the time of the call. New subfolders created later do not automatically inherit the subscription.
- If the user is already subscribed to the folder, the existing subscription is replaced with the new event flags.
- At least one event flag should be set to `true`.
- To subscribe a user group instead of a single user, use [AddUsergroupToFolderSubscribers](AddUsergroupToFolderSubscribers.md).
- To subscribe to a single document, use [AddUserToDocumentSubscribers](AddUserToDocumentSubscribers.md).

## Related APIs

- [AddUsergroupToFolderSubscribers](AddUsergroupToFolderSubscribers.md) -" Subscribe a user group to a folder.
- [AddUserToDocumentSubscribers](AddUserToDocumentSubscribers.md) -" Subscribe a user to a specific document.
- [RemoveUserFromFolderSubscribers](RemoveUserFromFolderSubscribers.md) -" Remove a user subscription from a folder.
- [GetSubscribers](GetSubscribers.md) -" List all subscribers of a document or folder.
- [GetSubscriptions](GetSubscriptions.md) -" List all subscriptions of the current user.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | no folder at that path, including one the caller may not see |
| `4041` | no user by that name |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

The ten event flags are the same on every add operation, and all ten have to be sent: they are
declared as plain booleans, so a missing one is a model binding failure rather than a default.
`ON_NEWDOC` is the eleventh, and belongs to the folder forms only.
