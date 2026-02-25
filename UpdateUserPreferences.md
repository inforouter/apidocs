# UpdateUserPreferences API

Updates the display and notification preferences of the specified infoRouter user.

## Endpoint

```
/srv.asmx/UpdateUserPreferences
```

## Methods

- **GET** `/srv.asmx/UpdateUserPreferences?authenticationTicket=...&UserName=...&xmlPreferences=...`
- **POST** `/srv.asmx/UpdateUserPreferences` (form data)
- **SOAP** Action: `http://tempuri.org/UpdateUserPreferences`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `UserName` | string | Yes | The username whose preferences will be updated. |
| `xmlPreferences` | string | Yes | An XML string containing the `<Preferences>` element with preference attributes to update (see format below). |

### xmlPreferences Format

The `xmlPreferences` parameter must be a valid XML string with a `<Preferences>` element. Supported attributes:

| Attribute | Values | Description |
|-----------|--------|-------------|
| `EmailType` | `HTML`, `TEXT` | Preferred email format for notifications. |
| `Language` | Language name string (e.g., `English`) | Preferred display language. |
| `AttachDocumentToEmail` | `true`, `false` | Whether to attach documents to notification emails. |
| `DefaultPortal` | Portal name string | The user's default portal. Leave empty for none. |
| `ShowHiddens` | `true`, `false` | Whether to show hidden domains/libraries in listings. |
| `ShowArchives` | `true`, `false` | Whether to show archived domains/libraries in listings. |
| `NotificationType` | `NONE`, `INSTANT`, `DAILY REPORT` | How and when document change notifications are delivered. |

**Example xmlPreferences value:**
```xml
<Preferences EmailType="HTML" Language="English" AttachDocumentToEmail="false" DefaultPortal="" ShowHiddens="false" ShowArchives="false" NotificationType="INSTANT" />
```

---

## Response

### Success Response

```xml
<response success="true" error="" />
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

---

## Required Permissions

**System administrator** or the **user themselves.** A user can update their own preferences; a system administrator can update any user's preferences.

---

## Example

### GET Request

```
GET /srv.asmx/UpdateUserPreferences
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &UserName=jdoe
  &xmlPreferences=%3CPreferences+EmailType%3D%22HTML%22+Language%3D%22English%22+AttachDocumentToEmail%3D%22false%22+ShowHiddens%3D%22false%22+ShowArchives%3D%22false%22+NotificationType%3D%22INSTANT%22+%2F%3E
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/UpdateUserPreferences HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&UserName=jdoe
&xmlPreferences=<Preferences EmailType="HTML" Language="English" AttachDocumentToEmail="false" DefaultPortal="" ShowHiddens="false" ShowArchives="false" NotificationType="INSTANT" />
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:UpdateUserPreferences>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:UserName>jdoe</tns:UserName>
      <tns:XmlPreferences>&lt;Preferences EmailType="HTML" Language="English" AttachDocumentToEmail="false" DefaultPortal="" ShowHiddens="false" ShowArchives="false" NotificationType="INSTANT" /&gt;</tns:XmlPreferences>
    </tns:UpdateUserPreferences>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Only the attributes present in the `<Preferences>` XML are updated; omitted attributes retain their current values.
- The `NotificationType` values are: `NONE` (no notifications), `INSTANT` (email on each change), `DAILY REPORT` (digest email once per day).
- Use `GetUser` to retrieve the current preferences before updating.

---

## Related APIs

- [GetUser](GetUser) - Get current user preferences
- [UpdateUserProfile](UpdateUserProfile) - Update the user's name and username
- [UpdateUserEmail](UpdateUserEmail) - Update the user's email address

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| User not found | The specified username does not exist. |
| Access denied | The calling user lacks permission to update these preferences. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/UpdateUserPreferences*
