# UpdateDocumentProperties1 API

Updates the core properties of the specified document: display name, description, update instructions, source, language, and author. All fields are optional — only the fields provided are updated. This is an extended version of `UpdateDocumentProperties` that adds source, language, and author fields. To also update importance, use `UpdateDocumentProperties2`.

## Endpoint

```
/srv.asmx/UpdateDocumentProperties1
```

## Methods

- **GET** `/srv.asmx/UpdateDocumentProperties1?authenticationTicket=...&path=...&newDocumentName=...&newDescription=...&newUpdateInstructions=...&newDocumentSource=...&newDocumentLanguage=...&newDocumentAuthor=...`
- **POST** `/srv.asmx/UpdateDocumentProperties1` (form data)
- **SOAP** Action: `http://tempuri.org/UpdateDocumentProperties1`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1-Report.pdf`), or a short document ID path (`~D{id}`). |
| `newDocumentName` | string | No | New display name for the document. Pass `null` or omit to leave unchanged. |
| `newDescription` | string | No | New description for the document. Line endings are normalized automatically. |
| `newUpdateInstructions` | string | No | New update instructions for contributors. Line endings are normalized automatically. |
| `newDocumentSource` | string | No | New source value (e.g. originating organization, system, or URL). Line endings are normalized automatically. |
| `newDocumentLanguage` | string | No | New language tag for the document (e.g. `en`, `en-US`, `fr`). Line endings are normalized automatically. |
| `newDocumentAuthor` | string | No | New author name for the document. Line endings are normalized automatically. |

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
GET /srv.asmx/UpdateDocumentProperties1
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &path=/Finance/Reports/Q1-2024-Report.pdf
  &newDocumentName=Q1+2024+Financial+Report
  &newDescription=Quarterly+financial+summary
  &newUpdateInstructions=Update+quarterly
  &newDocumentSource=Finance+Department
  &newDocumentLanguage=en-US
  &newDocumentAuthor=Jane+Smith
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/UpdateDocumentProperties1 HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&path=/Finance/Reports/Q1-2024-Report.pdf
&newDocumentName=Q1 2024 Financial Report
&newDescription=Quarterly financial summary
&newUpdateInstructions=Update quarterly
&newDocumentSource=Finance Department
&newDocumentLanguage=en-US
&newDocumentAuthor=Jane Smith
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:UpdateDocumentProperties1>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:path>/Finance/Reports/Q1-2024-Report.pdf</tns:path>
      <tns:newDocumentName>Q1 2024 Financial Report</tns:newDocumentName>
      <tns:newDescription>Quarterly financial summary</tns:newDescription>
      <tns:newUpdateInstructions>Update quarterly</tns:newUpdateInstructions>
      <tns:newDocumentSource>Finance Department</tns:newDocumentSource>
      <tns:newDocumentLanguage>en-US</tns:newDocumentLanguage>
      <tns:newDocumentAuthor>Jane Smith</tns:newDocumentAuthor>
    </tns:UpdateDocumentProperties1>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Passing `null` for any optional parameter leaves that field unchanged on the document.
- Line endings in text fields are normalized to the server format.
- To also update the document **importance level**, use `UpdateDocumentProperties2`.
- The base version `UpdateDocumentProperties` only updates name, description, and update instructions.

---

## Related APIs

- [UpdateDocumentProperties](UpdateDocumentProperties) - Update name, description, and update instructions only
- [UpdateDocumentProperties2](UpdateDocumentProperties2) - Update all properties including importance
- [GetDocument](GetDocument) - Get all current document properties

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

*For detailed documentation visit: https://support.inforouter.com/api-docs/UpdateDocumentProperties1*
