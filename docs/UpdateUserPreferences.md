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

Rewrites one user's preferences block, whole.

```javascript
const xmlPreferences = `<Preferences>
  <Language>en</Language>
  <DefaultPortal />
  <ShowArchives>FALSE</ShowArchives>
  <ShowHiddens>TRUE</ShowHiddens>
  <NotificationType>DAILY</NotificationType>
  <EmailType>TEXT</EmailType>
  <AttachDocumentToEmail>TRUE</AttachDocumentToEmail>
</Preferences>`;

await call('UpdateUserPreferences', { authenticationTicket: ticket, UserName: 'jsmith', xmlPreferences });
```

This replaces the block rather than merging into it, and the values are written in capitals -
`TRUE`, `FALSE`, `DAILY`, `TEXT`. Read the current block from
[GetUser](GetUser.md)'s `<Preferences>` element, change what you mean to change, and send the whole
thing back.

## Notes

- Only the attributes present in the `<Preferences>` XML are updated; omitted attributes retain their current values.
- The `NotificationType` values are: `NONE` (no notifications), `INSTANT` (email on each change), `DAILY REPORT` (digest email once per day).
- Use `GetUser` to retrieve the current preferences before updating.

---

## Related APIs

- [GetUser](GetUser.md) - Get current user preferences
- [UpdateUserProfile](UpdateUserProfile.md) - Update the user's name and username
- [UpdateUserEmail](UpdateUserEmail.md) - Update the user's email address

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4030` | there is no ticket at all |
| `4010` | the ticket is expired or unknown |
| `4041` | no user by that name |
| `4000` | `xmlPreferences` is not well-formed XML; the message quotes the parser, in English, and gives the line and position |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

---
