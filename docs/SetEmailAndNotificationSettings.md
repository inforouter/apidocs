# SetEmailAndNotificationSettings API

Updates the email and notification settings for the infoRouter system. Requires system administrator privileges.

## Endpoint

```
/srv.asmx/SetEmailAndNotificationSettings
```

## Methods

- **GET** `/srv.asmx/SetEmailAndNotificationSettings?authenticationTicket=...&settingsXml=...`
- **POST** `/srv.asmx/SetEmailAndNotificationSettings` (form data)
- **SOAP** Action: `http://tempuri.org/SetEmailAndNotificationSettings`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from AuthenticateUser |
| `settingsXml` | string | Yes | XML-serialized `EmailAndNotificationSettings` object |

## settingsXml Structure

Use `GetEmailAndNotificationSettings` to retrieve the current settings and use that XML as the input template. All fields must be present.

```xml
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
```

## Response

### Success Response
```xml
<root success="true" />
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
| `AttachmentSizeLimit` | long | Maximum attachment size in **bytes** (e.g., 5242880 = 5 MB) |
| `AllowPartialEmailUploads` | bool | Allow email documents to be uploaded even if some parts are missing |
| `TruncateLongEmailFields` | bool | Truncate oversized email header fields on import |

### Send To (outbound email)
| Field | Type | Description |
|-------|------|-------------|
| `SendToSendEmail` | bool | Enable the Send To Email feature |
| `SendToAllowSendEmailAttachments` | bool | Allow document attachments in Send To emails |
| `SendToDisplayUserList` | bool | Show a user list picker in the Send To Email dialog |
| `SendToSendEmailsFromUsersEmail` | bool | Use the logged-in user's email address as the From address |
| `SendToLogCcAddress` | string | CC address for all outbound Send To emails (audit/log copy) |

## Required Permissions

Caller must be a **system administrator** with `UpdateApplicationSettingsAndPolicies` permission.

## Example

### Request (POST)
```
POST /srv.asmx/SetEmailAndNotificationSettings HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&settingsXml=<EmailAndNotificationSettings>...</EmailAndNotificationSettings>
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

Takes what `GetEmailAndNotificationSettings` returns, as it stands - the reader already answers under
`<EmailAndNotificationSettings>`, which is what this deserializes against. Read, change what you mean to change, send
the whole document back: anything left out goes back to its default rather than staying as it was.

```javascript
const current = await call('GetEmailAndNotificationSettings', { authenticationTicket: ticket });
const settings = current.querySelector('EmailAndNotificationSettings');

// ... change what you mean to change ...

await call('SetEmailAndNotificationSettings', {
  authenticationTicket: ticket,
  settingsXml: new XMLSerializer().serializeToString(settings)
});
```

## Notes

- The recommended workflow is: call `GetEmailAndNotificationSettings`, modify the returned XML, then pass it to `SetEmailAndNotificationSettings`.
- SMTP server connection settings (server, port, username, password) are managed in `appsettings.json` and cannot be changed through this API.
- `AttachmentSizeLimit` must be provided in bytes; the UI displays this value in KB.
- `FaxQue` is accepted in the XML but only persisted if it differs from the default value (`c:\faxque`).
- Settings take effect immediately; the in-memory cache is invalidated on a successful update.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4030` | the caller may not change the application settings - including a caller with no ticket |
| `4000` | `settingsXml` is not well formed, or does not deserialize into the settings document |

