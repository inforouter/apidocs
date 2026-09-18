# AddUsergroupToDocumentSubscribers API

Adds a user group to the subscription list of a document. All members of the group receive email notifications for the selected events.

## Endpoint

```
/srv.asmx/AddUsergroupToDocumentSubscribers
```

## Methods

- **GET** `/srv.asmx/AddUsergroupToDocumentSubscribers?authenticationTicket=...&DocumentPath=...&groupName=...&ON_READ=...&...`
- **POST** `/srv.asmx/AddUsergroupToDocumentSubscribers` (form data)
- **SOAP** Action: `http://tempuri.org/AddUsergroupToDocumentSubscribers`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DocumentPath` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1.pdf`). |
| `groupName` | string | Yes | Name of the user group. A group belonging to the library the item is in is looked for first, then the global groups, so either kind can be named. |
| `ON_READ` | boolean | Yes | `true` to notify when the document is read/viewed. |
| `ON_CHANGE` | boolean | Yes | `true` to notify when document metadata changes. |
| `ON_UPDATE` | boolean | Yes | `true` to notify when a new version is uploaded. |
| `ON_CHECKOUT` | boolean | Yes | `true` to notify when the document is checked out. |
| `ON_APPROVE` | boolean | Yes | `true` to notify when the document or workflow step is approved. |
| `ON_REJECT` | boolean | Yes | `true` to notify when the document or workflow step is rejected. |
| `ON_COMMENT` | boolean | Yes | `true` to notify when a comment is added to the document. |
| `ON_MOVE` | boolean | Yes | `true` to notify when the document is moved to another folder. |
| `ON_DELETE` | boolean | Yes | `true` to notify when the document is deleted. |
| `ON_CHECKIN` | boolean | Yes | `true` to notify when the document is checked in. |

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

Any authenticated user may call this API. The specified group and document must both exist.

## Example

### GET Request

```
GET /srv.asmx/AddUsergroupToDocumentSubscribers
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &DocumentPath=/Finance/Reports/Q1.pdf
    &groupName=Finance Team
    &ON_READ=true
    &ON_CHANGE=true
    &ON_UPDATE=true
    &ON_CHECKOUT=false
    &ON_APPROVE=true
    &ON_REJECT=true
    &ON_COMMENT=false
    &ON_MOVE=false
    &ON_DELETE=false
    &ON_CHECKIN=false
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/AddUsergroupToDocumentSubscribers HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&DocumentPath=/Finance/Reports/Q1.pdf&groupName=Finance Team&ON_READ=true&ON_CHANGE=true&ON_UPDATE=true&ON_CHECKOUT=false&ON_APPROVE=true&ON_REJECT=true&ON_COMMENT=false&ON_MOVE=false&ON_DELETE=false&ON_CHECKIN=false
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

Subscribes a user group to one document.

```javascript
await call('AddUsergroupToDocumentSubscribers', {
  authenticationTicket: ticket,
  DocumentPath: '/Public/Reports/q3.pdf',
  groupName: 'Auditors',          // the document's own library first, then the global groups
  ON_READ: true, ON_CHANGE: true, ON_UPDATE: false, ON_CHECKOUT: false, ON_APPROVE: false,
  ON_REJECT: false, ON_COMMENT: false, ON_MOVE: false, ON_DELETE: true, ON_CHECKIN: false,
});
```

## Notes

- All members of the group will receive notifications for the selected events.
- Document subscriptions do not include `ON_NEWDOC` -" that flag is only available for folder subscriptions.
- If the group is already subscribed to the document, the existing subscription is replaced with the new event flags.
- At least one event flag should be set to `true`.
- To subscribe a single user instead of a group, use [AddUserToDocumentSubscribers](AddUserToDocumentSubscribers.md).
- To subscribe a group to a folder, use [AddUsergroupToFolderSubscribers](AddUsergroupToFolderSubscribers.md).

## Related APIs

- [AddUserToDocumentSubscribers](AddUserToDocumentSubscribers.md) -" Subscribe a single user to a document.
- [AddUsergroupToFolderSubscribers](AddUsergroupToFolderSubscribers.md) -" Subscribe a user group to a folder.
- [RemoveUsergroupFromDocumentSubscribers](RemoveUsergroupFromDocumentSubscribers.md) -" Remove a group subscription from a document.
- [GetSubscribers](GetSubscribers.md) -" List all subscribers of a document or folder.
- [GetSubscriptions](GetSubscriptions.md) -" List all subscriptions of the current user.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | no document at that path, including one the caller may not see |
| `4041` | no user group by that name, in the document's library or among the global groups |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

The ten event flags are the same on every add operation, and all ten have to be sent: they are
declared as plain booleans, so a missing one is a model binding failure rather than a default.
`ON_NEWDOC` is the eleventh, and belongs to the folder forms only.
