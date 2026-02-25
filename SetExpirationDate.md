# SetExpirationDate API

Sets the expiration date of the specified document. When a document reaches its expiration date, infoRouter can optionally notify a designated user a configurable number of days before expiration. Expiration is informational metadata — it does not automatically archive or delete the document.

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

## Notes

- To disable expiration notifications, pass `0` for both `notificationAgentId` and `notifyBeforeDays`.
- The `notificationAgentId` must be the numeric user ID of a valid infoRouter user. Use `GetAllUsers` to look up user IDs.
- UTC date values are automatically converted to the server's local time zone before storing.
- To remove the expiration date entirely, use `RemoveExpirationDate`.
- Expiration does not automatically lock, archive, or delete the document. It is metadata used to drive notification workflows.
- Use `GetDocument` to read the current `ExpirationDate` attribute before calling this API.

---

## Related APIs

- [RemoveExpirationDate](RemoveExpirationDate) - Remove the expiration date from a document
- [GetDocument](GetDocument) - Get document properties including the current `ExpirationDate`
- [GetAllUsers](GetAllUsers) - Look up numeric user IDs for the `notificationAgentId` parameter

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Document not found | The specified path does not resolve to an existing document. |
| Access denied | The user does not have write permission on the document. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/SetExpirationDate*
