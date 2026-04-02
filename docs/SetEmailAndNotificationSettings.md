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

## Notes

- The recommended workflow is: call `GetEmailAndNotificationSettings`, modify the returned XML, then pass it to `SetEmailAndNotificationSettings`.
- SMTP server connection settings (server, port, username, password) are managed in `appsettings.json` and cannot be changed through this API.
- `AttachmentSizeLimit` must be provided in bytes; the UI displays this value in KB.
- `FaxQue` is accepted in the XML but only persisted if it differs from the default value (`c:\faxque`).
- Settings take effect immediately; the in-memory cache is invalidated on a successful update.
