# RemoveDocumentCutoffDate API

Removes the cutoff date from the specified document, returning it to an unconstrained state. Once the cutoff date is cleared the document can again be checked out and modified. If the document has a Retention & Disposition schedule assigned, removing the cutoff date may also recalculate the associated retention and disposition dates.

> **Note:** If the document's parent folder itself has a cutoff date applied, the document's individual cutoff state cannot be removed until the folder-level cutoff is cleared first (using `RemoveFolderCutoffDate`).

## Endpoint

```
/srv.asmx/RemoveDocumentCutoffDate
```

## Methods

- **GET** `/srv.asmx/RemoveDocumentCutoffDate?authenticationTicket=...&path=...`
- **POST** `/srv.asmx/RemoveDocumentCutoffDate` (form data)
- **SOAP** Action: `http://tempuri.org/RemoveDocumentCutoffDate`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1-Report.pdf`), or a short document ID path (`~D{id}` or `~D{id}.ext`). |

---

## Response

### Success Response

```xml
<response success="true" error="" />
```

### Error Response

```xml
<response success="false" error="Cutoff state of this document cannot be removed. Parent folder is cut-off. Please remove the parent folder's cutoff state first." />
```

---

## Required Permissions

The calling user must have **Retention Period Change** permission on the document or its containing folder.

---

## Example

### GET Request

```
GET /srv.asmx/RemoveDocumentCutoffDate
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &path=/Finance/Reports/Q1-2024-Report.pdf
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/RemoveDocumentCutoffDate HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&path=/Finance/Reports/Q1-2024-Report.pdf
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:RemoveDocumentCutoffDate>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:path>/Finance/Reports/Q1-2024-Report.pdf</tns:path>
    </tns:RemoveDocumentCutoffDate>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Shortcut documents (`.LNK`) cannot have their cutoff date modified; this call will return an error for shortcuts.
- If the document's **parent folder** has a cutoff date applied, the document's cutoff state cannot be individually removed. The folder-level cutoff must be cleared first using `RemoveFolderCutoffDate`.
- If the document has a **Retention & Disposition (R&D) schedule** assigned, clearing the cutoff date triggers a recalculation of the retention and disposition dates based on the schedule definition.
- Document subscribers are notified of the update when the cutoff date is successfully removed.
- Use `SetDocumentCutoffDate` to apply a cutoff date to a document.
- Use `GetDocument` to check the current `CutOffDate` attribute of a document before calling this API.

---

## Related APIs

- [SetDocumentCutoffDate](SetDocumentCutoffDate.md) - Apply a cutoff date to a document
- [RemoveFolderCutoffDate](RemoveFolderCutoffDate.md) - Remove the cutoff date from a folder (required first if the parent folder is cut off)
- [GetDocument](GetDocument.md) - Get document properties including the current `CutOffDate`
- [GetDomainPolicies](GetDomainPolicies.md) - Get retention and disposition policies for a domain/library

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Document not found | The specified path does not resolve to an existing document. |
| Shortcut document | Cutoff dates cannot be modified on shortcut (`.LNK`) documents. |
| Parent folder is cut-off | The parent folder has a cutoff date; remove the folder cutoff first. |
| Access denied | The user does not have Retention Period Change permission. |
| `SystemError:...` | An unexpected server-side error occurred. |

---
