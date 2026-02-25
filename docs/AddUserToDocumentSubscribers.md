# AddUserToDocumentSubscribers API

Adds a user to the subscription list of a document. The subscriber receives email notifications for the selected events.

## Endpoint

```
/srv.asmx/AddUserToDocumentSubscribers
```

## Methods

- **GET** `/srv.asmx/AddUserToDocumentSubscribers?authenticationTicket=...&DocumentPath=...&UserName=...&ON_READ=...&...`
- **POST** `/srv.asmx/AddUserToDocumentSubscribers` (form data)
- **SOAP** Action: `http://tempuri.org/AddUserToDocumentSubscribers`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DocumentPath` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1.pdf`). |
| `UserName` | string | Yes | Login name of the user to subscribe. |
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

Any authenticated user may call this API. The specified user and document must both exist.

## Example

### GET Request

```
GET /srv.asmx/AddUserToDocumentSubscribers
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &DocumentPath=/Finance/Reports/Q1.pdf
    &UserName=jdoe
    &ON_READ=true
    &ON_CHANGE=true
    &ON_UPDATE=true
    &ON_CHECKOUT=false
    &ON_APPROVE=false
    &ON_REJECT=false
    &ON_COMMENT=true
    &ON_MOVE=false
    &ON_DELETE=false
    &ON_CHECKIN=false
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/AddUserToDocumentSubscribers HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&DocumentPath=/Finance/Reports/Q1.pdf&UserName=jdoe&ON_READ=true&ON_CHANGE=true&ON_UPDATE=true&ON_CHECKOUT=false&ON_APPROVE=false&ON_REJECT=false&ON_COMMENT=true&ON_MOVE=false&ON_DELETE=false&ON_CHECKIN=false
```

## Notes

- At least one event flag should be set to `true`; subscribing with all flags `false` creates a subscription that never generates notifications.
- If the user is already subscribed to the document, the existing subscription is replaced with the new event flags.
- Document subscriptions do not include `ON_NEWDOC` -" that flag is only available for folder subscriptions.
- To subscribe a user group instead of a single user, use [AddUsergroupToDocumentSubscribers](AddUsergroupToDocumentSubscribers.md).
- To subscribe to a folder (and optionally its contents), use [AddUserToFolderSubscribers](AddUserToFolderSubscribers.md).

## Related APIs

- [AddUsergroupToDocumentSubscribers](AddUsergroupToDocumentSubscribers.md) -" Subscribe a user group to a document.
- [AddUserToFolderSubscribers](AddUserToFolderSubscribers.md) -" Subscribe a user to a folder.
- [RemoveUserFromDocumentSubscribers](RemoveUserFromDocumentSubscribers.md) -" Remove a user subscription from a document.
- [GetSubscribers](GetSubscribers.md) -" List all subscribers of a document or folder.
- [GetSubscriptions](GetSubscriptions.md) -" List all subscriptions of the current user.

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed -" invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| User not found | No user with the specified `UserName` exists. |
| Document not found | No document was found at the specified `DocumentPath`. |
