# UpdateDocumentProperties2 API

Updates the core properties of the specified document: display name, description, update instructions, source, language, author, and importance level. All fields are optional -" only the fields provided are updated. This is the most complete version of the UpdateDocumentProperties family.

## Endpoint

```
/srv.asmx/UpdateDocumentProperties2
```

## Methods

- **GET** `/srv.asmx/UpdateDocumentProperties2?authenticationTicket=...&path=...&newDocumentName=...&newDescription=...&newUpdateInstructions=...&newDocumentSource=...&newDocumentLanguage=...&newDocumentAuthor=...&importance=...`
- **POST** `/srv.asmx/UpdateDocumentProperties2` (form data)
- **SOAP** Action: `http://tempuri.org/UpdateDocumentProperties2`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1-Report.pdf`), or a short document ID path (`~D{id}`). |
| `newDocumentName` | string | No | New display name for the document. Pass `null` or omit to leave unchanged. |
| `newDescription` | string | No | New description for the document. Line endings are normalized automatically. |
| `newUpdateInstructions` | string | No | New update instructions for contributors. Line endings are normalized automatically. |
| `newDocumentSource` | string | No | New source value (e.g. originating organization or URL). Line endings are normalized automatically. |
| `newDocumentLanguage` | string | No | New language tag (e.g. `en`, `en-US`, `fr`). Line endings are normalized automatically. |
| `newDocumentAuthor` | string | No | New author name. Line endings are normalized automatically. |
| `importance` | short (int16) | No | Importance level: `-1` = NoMarkings, `0` = Low, `1` = Normal, `2` = High, `3` = Vital. Pass `null` or omit to leave unchanged. |

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
GET /srv.asmx/UpdateDocumentProperties2
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &path=/Finance/Reports/Q1-2024-Report.pdf
  &newDocumentName=Q1+2024+Financial+Report
  &newDescription=Quarterly+financial+summary
  &newDocumentAuthor=Jane+Smith
  &importance=2
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/UpdateDocumentProperties2 HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&path=/Finance/Reports/Q1-2024-Report.pdf
&newDocumentName=Q1 2024 Financial Report
&newDescription=Quarterly financial summary
&newDocumentAuthor=Jane Smith
&importance=2
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:UpdateDocumentProperties2>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:path>/Finance/Reports/Q1-2024-Report.pdf</tns:path>
      <tns:newDocumentName>Q1 2024 Financial Report</tns:newDocumentName>
      <tns:newDescription>Quarterly financial summary</tns:newDescription>
      <tns:newDocumentAuthor>Jane Smith</tns:newDocumentAuthor>
      <tns:importance>2</tns:importance>
    </tns:UpdateDocumentProperties2>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Passing `null` for any optional parameter leaves that field unchanged on the document.
- The `importance` field maps to: `-1` = NoMarkings, `0` = Low, `1` = Normal, `2` = High, `3` = Vital. To set importance independently, you can also use `SetDocumentImportance`.
- Line endings in all text fields are normalized to the server format.
- This is the most complete variant. Use `UpdateDocumentProperties` or `UpdateDocumentProperties1` if you don't need the importance field.

---

## Related APIs

- [UpdateDocumentProperties](UpdateDocumentProperties.md) - Update name, description, and update instructions only
- [UpdateDocumentProperties1](UpdateDocumentProperties1.md) - Update properties including source, language, and author
- [SetDocumentImportance](SetDocumentImportance.md) - Set the importance level independently
- [GetDocument](GetDocument.md) - Get all current document properties

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