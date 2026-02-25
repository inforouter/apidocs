# UpdateDocumentProperties API

Updates the core properties of the specified document: display name, description, and update instructions. All three fields are optional — only the fields provided are updated. This is the base version of the API; use `UpdateDocumentProperties1` or `UpdateDocumentProperties2` to also update source, language, author, and importance.

## Endpoint

```
/srv.asmx/UpdateDocumentProperties
```

## Methods

- **GET** `/srv.asmx/UpdateDocumentProperties?authenticationTicket=...&path=...&newDocumentName=...&newDescription=...&newUpdateInstructions=...`
- **POST** `/srv.asmx/UpdateDocumentProperties` (form data)
- **SOAP** Action: `http://tempuri.org/UpdateDocumentProperties`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1-Report.pdf`), or a short document ID path (`~D{id}`). |
| `newDocumentName` | string | No | New display name for the document (without extension). Pass `null` or omit to leave unchanged. |
| `newDescription` | string | No | New description for the document. Pass `null` or omit to leave unchanged. Line endings are normalized automatically. |
| `newUpdateInstructions` | string | No | New update instructions for contributors. Pass `null` or omit to leave unchanged. Line endings are normalized automatically. |

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
GET /srv.asmx/UpdateDocumentProperties
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &path=/Finance/Reports/Q1-2024-Report.pdf
  &newDocumentName=Q1+2024+Financial+Report
  &newDescription=Quarterly+financial+summary+for+Q1+2024
  &newUpdateInstructions=Update+by+end+of+following+quarter
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/UpdateDocumentProperties HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&path=/Finance/Reports/Q1-2024-Report.pdf
&newDocumentName=Q1 2024 Financial Report
&newDescription=Quarterly financial summary for Q1 2024
&newUpdateInstructions=Update by end of following quarter
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:UpdateDocumentProperties>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:path>/Finance/Reports/Q1-2024-Report.pdf</tns:path>
      <tns:newDocumentName>Q1 2024 Financial Report</tns:newDocumentName>
      <tns:newDescription>Quarterly financial summary for Q1 2024</tns:newDescription>
      <tns:newUpdateInstructions>Update by end of following quarter</tns:newUpdateInstructions>
    </tns:UpdateDocumentProperties>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Passing `null` for any optional parameter leaves that field unchanged.
- Line endings in `newDescription` and `newUpdateInstructions` are normalized to the server format.
- To also update `source`, `language`, and `author`, use `UpdateDocumentProperties1`.
- To also update `importance`, use `UpdateDocumentProperties2`.
- Renaming a document via `newDocumentName` does not change its URL path — the path uses the file name including extension.

---

## Related APIs

- [UpdateDocumentProperties1](UpdateDocumentProperties1) - Update properties including source, language, and author
- [UpdateDocumentProperties2](UpdateDocumentProperties2) - Update properties including source, language, author, and importance
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

*For detailed documentation visit: https://support.inforouter.com/api-docs/UpdateDocumentProperties*
