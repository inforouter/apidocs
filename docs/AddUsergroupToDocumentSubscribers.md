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
| `groupName` | string | Yes | Name of the user group to subscribe. |
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

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed -" invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Group not found | No user group with the specified `groupName` exists. |
| Document not found | No document was found at the specified `DocumentPath`. |
