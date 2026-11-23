---
search:
  exclude: true
---

# GetEmailAndNotificationSettings API

**Available in:** infoRouter 9.0 and later

!!! warning "Internal API"
    Made for infoRouter's own user interface. It is not part of the public web API: there is no SOAP
    form and no promise of backward compatibility, and it may change or be removed in any release
    without notice. Do not use it in an integration.

Returns all email and notification settings for the infoRouter system. Requires an administrator or a Policy Manager.

## Endpoint

```
/api/UIInternals/GetEmailAndNotificationSettings
```

## Methods

- **GET** `/api/UIInternals/GetEmailAndNotificationSettings?authenticationTicket=...`
- **POST** `/api/UIInternals/GetEmailAndNotificationSettings` (form data)

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from AuthenticateUser |

## Response

### Success Response
```xml
<root success="true">
  <EmailAndNotificationSettings>
    <FaxQue>c:\faxque</FaxQue>
    <TruncateLongEmailFields>false</TruncateLongEmailFields>
    <AllowEmailAttachments>true</AllowEmailAttachments>
    <AttachmentSizeLimit>5242880</AttachmentSizeLimit>
    <SubscriptionNotifications>true</SubscriptionNotifications>
    <AllowPartialEmailUploads>false</AllowPartialEmailUploads>
    <SendToSendEmail>true</SendToSendEmail>
    <SendToAllowSendEmailAttachments>true</SendToAllowSendEmailAttachments>
    <SendToDisplayUserList>true</SendToDisplayUserList>
    <SendToSendEmailsFromUsersEmail>false</SendToSendEmailsFromUsersEmail>
    <SendToLogCcAddress></SendToLogCcAddress>
    <SendNotificationsOnDragDrop>false</SendNotificationsOnDragDrop>
    <TimeZoneSettingsNotifications>UseGMT</TimeZoneSettingsNotifications>
  </EmailAndNotificationSettings>
</root>
```

### Error Response
```xml
<root success="false" error="[ErrorCode] Error message" />
```

## Fields

### Subscription Notifications
| Field | Type | Description |
|-------|------|-------------|
| `SubscriptionNotifications` | bool | Enable email notifications for document/folder subscriptions |
| `SendNotificationsOnDragDrop` | bool | Send notifications when documents are moved via drag-and-drop |
| `TimeZoneSettingsNotifications` | string | Timezone for notification timestamps: `UseGMT` or `UseServerLocal` |

### Email Attachments (inbound)
| Field | Type | Description |
|-------|------|-------------|
| `AllowEmailAttachments` | bool | Allow documents to be attached to outgoing emails |
| `AttachmentSizeLimit` | long | Maximum attachment size in bytes |
| `AllowPartialEmailUploads` | bool | Allow email documents to be uploaded even if some parts are missing |
| `TruncateLongEmailFields` | bool | Truncate oversized email header fields (Subject, From, To, CC) on import |

### Send To (outbound email)
| Field | Type | Description |
|-------|------|-------------|
| `SendToSendEmail` | bool | Enable the Send To Email feature |
| `SendToAllowSendEmailAttachments` | bool | Allow document attachments in Send To emails |
| `SendToDisplayUserList` | bool | Show a user list picker in the Send To Email dialog |
| `SendToSendEmailsFromUsersEmail` | bool | Use the logged-in user's email address as the From address |
| `SendToLogCcAddress` | string | CC address for all outbound Send To emails (audit/log copy) |

## Required Permissions

Caller must be an **administrator** or a member of **[Policy Managers]**: the same right [SetEmailAndNotificationSettings](SetEmailAndNotificationSettings.md) asks for. Up to 8.7 reading was administrators only.

## Example

### Request (GET)
```
GET /api/UIInternals/GetEmailAndNotificationSettings?authenticationTicket=abc123 HTTP/1.1
```

### Request (POST)
```
POST /api/UIInternals/GetEmailAndNotificationSettings HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123
```

## JavaScript

Every call answers XML with HTTP 200, success or not, so `success` is the thing to branch on and
`errorCode` is the number to report.

```javascript
async function call(action, params) {
  const response = await fetch(`/api/UIInternals/${action}?${new URLSearchParams(params)}`);
  const root = new DOMParser()
    .parseFromString(await response.text(), 'text/xml')
    .documentElement;

  if (root.getAttribute('success') !== 'true') {
    throw new Error(`${root.getAttribute('errorCode')}: ${root.getAttribute('error')}`);
  }
  return root;
}
```

Reads where mail is sent from and what is notified. Everything is under `<EmailAndNotificationSettings>`.

```javascript
const root = await call('GetEmailAndNotificationSettings', { authenticationTicket: ticket });
const settings = root.querySelector('EmailAndNotificationSettings');
```

## Notes

- Use the returned XML as the input template for `SetEmailAndNotificationSettings`.
- SMTP server connection settings (server, port, username, password) are not returned by this API: they are kept in `config\smtp-setting.json`, and [GetSmtpSettings](GetSmtpSettings.md) returns them.
- `AttachmentSizeLimit` is in bytes; the UI displays it in KB.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4030` | a caller with no ticket, or one who is neither an administrator nor a Policy Manager |

