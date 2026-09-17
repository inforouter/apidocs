# SetExpirationDate API

Sets the expiration date of the specified document. When a document reaches its expiration date, infoRouter can optionally notify a designated user a configurable number of days before expiration. Expiration is informational metadata -" it does not automatically archive or delete the document.

## Endpoint

```
/srv.asmx/SetExpirationDate
```

## Methods

- **GET** `/srv.asmx/SetExpirationDate?authenticationTicket=...&documentPath=...&expirationDate=...&notificationAgentId=...&notifyBeforeDays=...`
- **POST** `/srv.asmx/SetExpirationDate` (form data)
- **SOAP** Action: `http://tempuri.org/SetExpirationDate`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `documentPath` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1-Report.pdf`), or a short document ID path (`~D{id}`). |
| `expirationDate` | DateTime | Yes | The expiration date to set (e.g. `2030-12-31`). UTC values are automatically converted to server local time. |
| `notificationAgentId` | int | Yes | The numeric user ID of the person to notify before expiration. Pass `0` to disable notifications. Use `GetAllUsers` to look up user IDs. |
| `notifyBeforeDays` | int | Yes | Number of days before expiration to send the notification email. Pass `0` to disable notifications. |

---

## Response

### Success Response

```xml
<response success="true" error="" />
```

### Error Response

```xml
<response success="false" error="Document not found." />
```

---

## Required Permissions

The calling user must have **write** (modify properties) permission on the document or its containing folder.

---

## Example

### GET Request

```
GET /srv.asmx/SetExpirationDate
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &documentPath=/Finance/Reports/Q1-2024-Report.pdf
  &expirationDate=2030-12-31
  &notificationAgentId=42
  &notifyBeforeDays=30
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/SetExpirationDate HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&documentPath=/Finance/Reports/Q1-2024-Report.pdf
&expirationDate=2030-12-31
&notificationAgentId=42
&notifyBeforeDays=30
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:SetExpirationDate>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:documentPath>/Finance/Reports/Q1-2024-Report.pdf</tns:documentPath>
      <tns:expirationDate>2030-12-31</tns:expirationDate>
      <tns:notificationAgentId>42</tns:notificationAgentId>
      <tns:notifyBeforeDays>30</tns:notifyBeforeDays>
    </tns:SetExpirationDate>
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

Sets the date a document expires, and who to tell beforehand.

```javascript
await call('SetExpirationDate', {
  authenticationTicket: ticket,
  documentPath: '/Finance/Reports/Q1.pdf',
  expirationDate: '2027-03-31',
  notificationAgentId: 0,        // a user id; 0 for nobody
  notifyBeforeDays: 7
});
```

`notificationAgentId` is the **user id** of the person to notify - an id nobody has is answered `4041`
"user not found", which is the clearest sign of what the parameter means. Pass `0` for no
notification.

**A date in the past is accepted without complaint**, so a document can be given an expiry that has
already gone by. [RemoveExpirationDate](RemoveExpirationDate.md) clears it, leaving the 1900 base date
that [GetDocumentExpirationDate](GetDocumentExpirationDate.md) reports as "no expiry".

## Notes

- To disable expiration notifications, pass `0` for both `notificationAgentId` and `notifyBeforeDays`.
- The `notificationAgentId` must be the numeric user ID of a valid infoRouter user. Use `GetAllUsers` to look up user IDs.
- UTC date values are automatically converted to the server's local time zone before storing.
- To remove the expiration date entirely, use `RemoveExpirationDate`.
- Expiration does not automatically lock, archive, or delete the document. It is metadata used to drive notification workflows.
- Use `GetDocument` to read the current `ExpirationDate` attribute before calling this API.

---

## Related APIs

- [RemoveExpirationDate](RemoveExpirationDate.md) - Remove the expiration date from a document
- [GetDocument](GetDocument.md) - Get document properties including the current `ExpirationDate`
- [GetAllUsers](GetAllUsers.md) - Look up numeric user IDs for the `notificationAgentId` parameter

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | no document at that path, or no user with that `notificationAgentId` |
| `4030` | the caller may not change this document |
| `none` | an expiration date in the past is accepted silently |
| `HTTP 400` | `expirationDate` was not a date; refused by model binding |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Document not found | The specified path does not resolve to an existing document. |
| Access denied | The user does not have write permission on the document. |
| `SystemError:...` | An unexpected server-side error occurred. |

---