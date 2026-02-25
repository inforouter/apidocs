# UpdateDocumentKeywords API

Updates the user-defined keywords of the specified document. Keywords are free-text tags that help categorize and search for documents. This API replaces the entire existing keyword string with the new value. To append keywords, first retrieve the current keywords using `GetDocumentKeywords`, then append the new keywords and call this API.

## Endpoint

```
/srv.asmx/UpdateDocumentKeywords
```

## Methods

- **GET** `/srv.asmx/UpdateDocumentKeywords?authenticationTicket=...&path=...&keywords=...`
- **POST** `/srv.asmx/UpdateDocumentKeywords` (form data)
- **SOAP** Action: `http://tempuri.org/UpdateDocumentKeywords`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1-Report.pdf`), or a short document ID path (`~D{id}`). |
| `keywords` | string | Yes | Space-separated or comma-separated keywords to assign to the document. Replaces any previously stored keywords. Pass an empty string to clear all keywords. |

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

The calling user must have **write** (modify) permission on the document or its containing folder.

---

## Example

### GET Request

```
GET /srv.asmx/UpdateDocumentKeywords
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &path=/Finance/Reports/Q1-2024-Report.pdf
  &keywords=finance+quarterly+2024+revenue
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/UpdateDocumentKeywords HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&path=/Finance/Reports/Q1-2024-Report.pdf
&keywords=finance quarterly 2024 revenue
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:UpdateDocumentKeywords>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:path>/Finance/Reports/Q1-2024-Report.pdf</tns:path>
      <tns:keywords>finance quarterly 2024 revenue</tns:keywords>
    </tns:UpdateDocumentKeywords>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- This API **replaces** the entire keyword set. To append, read current keywords with `GetDocumentKeywords` first.
- Passing an empty string clears all keywords from the document.
- Keywords are stored as a single string field and are included in full-text search.

---

## Related APIs

- [GetDocumentKeywords](GetDocumentKeywords.md) - Retrieve the current keywords of a document
- [GetDocument](GetDocument.md) - Get all document properties including keywords
- [UpdateDocumentProperties](UpdateDocumentProperties.md) - Update document name, description, and update instructions

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

*For detailed documentation visit: https://support.inforouter.com/api-docs/UpdateDocumentKeywords*
