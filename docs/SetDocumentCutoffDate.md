# SetDocumentCutoffDate API

Applies a cutoff date to the specified document. Once cut off, the document is frozen: it can no longer be checked out or modified. If the document has a Retention & Disposition (R&D) schedule assigned, applying the cutoff date triggers a recalculation of the associated retention and disposition dates. Document subscribers are notified when the cutoff date is successfully applied.

> **Note:** If the document already has a cutoff date, this call returns success without updating the date. To change an existing cutoff date, first call `RemoveDocumentCutoffDate` to clear it, then call `SetDocumentCutoffDate` with the new date.

## Endpoint

```
/srv.asmx/SetDocumentCutoffDate
```

## Methods

- **GET** `/srv.asmx/SetDocumentCutoffDate?authenticationTicket=...&path=...&cutoffDate=...`
- **POST** `/srv.asmx/SetDocumentCutoffDate` (form data)
- **SOAP** Action: `http://tempuri.org/SetDocumentCutoffDate`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1-Report.pdf`), or a short document ID path (`~D{id}` or `~D{id}.ext`). |
| `cutoffDate` | DateTime | Yes | The cutoff date to apply to the document (e.g. `2024-12-31`). UTC values are automatically converted to server local time. |

---

## Response

### Success Response

```xml
<response success="true" error="" />
```

### Error Response

```xml
<response success="false" error="This document is checked out. Cutoff date cannot be applied to the checked out documents." />
```

---

## Required Permissions

The calling user must have **Retention Period Change** permission on the document or its containing folder.

---

## Example

### GET Request

```
GET /srv.asmx/SetDocumentCutoffDate
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &path=/Finance/Reports/Q1-2024-Report.pdf
  &cutoffDate=2024-12-31
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/SetDocumentCutoffDate HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&path=/Finance/Reports/Q1-2024-Report.pdf
&cutoffDate=2024-12-31
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:SetDocumentCutoffDate>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:path>/Finance/Reports/Q1-2024-Report.pdf</tns:path>
      <tns:cutoffDate>2024-12-31</tns:cutoffDate>
    </tns:SetDocumentCutoffDate>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- **Shortcut documents** (`.LNK`) cannot have a cutoff date applied; this call returns an error for shortcuts.
- **Checked-out documents** cannot be cut off. The document must be checked in first.
- If the document **already has a cutoff date**, this call returns success without making any changes. To update an existing cutoff date, call `RemoveDocumentCutoffDate` first to clear the existing date, then call `SetDocumentCutoffDate` with the new date.
- If the document has a **Retention & Disposition (R&D) schedule** assigned, applying the cutoff date triggers recalculation of the retention and disposition dates based on the schedule definition.
- Document subscribers are notified of the update when the cutoff date is successfully applied.
- Use `RemoveDocumentCutoffDate` to clear the cutoff date and return the document to an unconstrained state.
- Use `GetDocument` to check the current `CutOffDate` attribute of a document before calling this API.

---

## Related APIs

- [RemoveDocumentCutoffDate](RemoveDocumentCutoffDate.md) - Remove the cutoff date from a document (required before changing an existing cutoff date)
- [GetDocument](GetDocument.md) - Get document properties including the current `CutOffDate`
- [GetDomainPolicies](GetDomainPolicies.md) - Get retention and disposition policies for a domain/library

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Document not found | The specified path does not resolve to an existing document. |
| Shortcut document | Cutoff dates cannot be applied to shortcut (`.LNK`) documents. |
| Document is checked out | The document must be checked in before a cutoff date can be applied. |
| Access denied | The user does not have Retention Period Change permission. |
| `SystemError:...` | An unexpected server-side error occurred. |

---
