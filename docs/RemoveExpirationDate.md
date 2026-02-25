# RemoveExpirationDate API

Removes the expiration date from the specified document, returning it to an unconstrained (non-expiring) state. When the expiration date is cleared, any associated notification schedule is also removed. If the document did not have an expiration date, the call succeeds without making any changes.

## Endpoint

```
/srv.asmx/RemoveExpirationDate
```

## Methods

- **GET** `/srv.asmx/RemoveExpirationDate?authenticationTicket=...&documentPath=...`
- **POST** `/srv.asmx/RemoveExpirationDate` (form data)
- **SOAP** Action: `http://tempuri.org/RemoveExpirationDate`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `documentPath` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1-Report.pdf`), or a short document ID path (`~D{id}` or `~D{id}.ext`). |

---

## Response

### Success Response

```xml
<response success="true" error="" />
```

### Error Response

```xml
<response success="false" error="Access denied." />
```

---

## Required Permissions

The calling user must have **Document Property Change** permission on the document.

---

## Example

### GET Request

```
GET /srv.asmx/RemoveExpirationDate
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &documentPath=/Finance/Reports/Q1-2024-Report.pdf
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/RemoveExpirationDate HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&documentPath=/Finance/Reports/Q1-2024-Report.pdf
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:RemoveExpirationDate>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:documentPath>/Finance/Reports/Q1-2024-Report.pdf</tns:documentPath>
    </tns:RemoveExpirationDate>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Removing the expiration date also clears any associated **notification schedule** (the notify-before-days value and notification agent are both reset).
- If the document does not currently have an expiration date, the call completes successfully with no changes made.
- **Shortcut documents** (`.LNK`) that have an expiration date set cannot have it removed via this API; the call returns an error. Shortcut expiration dates must be managed through the parent document.
- Document subscribers are **not notified** when an expiration date is removed (notifications are only sent when a new expiration date is applied).
- Use `SetExpirationDate` to apply or update an expiration date with optional advance notification.
- Use `GetDocument` to inspect the current `ExpirationDate` attribute of a document before calling this API.

---

## Related APIs

- [SetExpirationDate](SetExpirationDate.md) - Apply an expiration date to a document, optionally with advance notification
- [GetDocument](GetDocument.md) - Get document properties including the current `ExpirationDate`

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Document not found | The specified path does not resolve to an existing document. |
| Shortcut document | A shortcut (`.LNK`) document that has an existing expiration date cannot have it removed through this API. |
| Access denied | The user does not have Document Property Change permission on the document. |
| `SystemError:...` | An unexpected server-side error occurred. |

---
