# UpdateDocumentType API

Updates the document type assigned to the specified document. Document types are administrator-defined classifications that can have required property sets attached. Changing the document type may enforce or relax property set requirements on the document.

## Endpoint

```
/srv.asmx/UpdateDocumentType
```

## Methods

- **GET** `/srv.asmx/UpdateDocumentType?authenticationTicket=...&path=...&documentTypeID=...`
- **POST** `/srv.asmx/UpdateDocumentType` (form data)
- **SOAP** Action: `http://tempuri.org/UpdateDocumentType`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1-Report.pdf`), or a short document ID path (`~D{id}`). |
| `documentTypeID` | int | Yes | The numeric ID of the document type to assign. Use `GetDocumentTypes` to retrieve the list of defined document types and their IDs. Pass `0` to clear the document type. |

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
GET /srv.asmx/UpdateDocumentType
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &path=/Finance/Reports/Q1-2024-Report.pdf
  &documentTypeID=5
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/UpdateDocumentType HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&path=/Finance/Reports/Q1-2024-Report.pdf
&documentTypeID=5
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:UpdateDocumentType>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:path>/Finance/Reports/Q1-2024-Report.pdf</tns:path>
      <tns:documentTypeID>5</tns:documentTypeID>
    </tns:UpdateDocumentType>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Use `GetDocumentTypes` to retrieve all defined document type IDs and names before calling this API.
- Passing `documentTypeID=0` clears the document type assignment.
- The new document type may have a required property set — if the required properties are not yet filled in, publishing or other operations may be affected.

---

## Related APIs

- [GetDocumentTypes](GetDocumentTypes) - Retrieve all defined document type definitions
- [CreateDocumentTypeDef](CreateDocumentTypeDef) - Create a new document type definition
- [UpdateDocumentTypeDef](UpdateDocumentTypeDef) - Rename an existing document type definition
- [GetDocument](GetDocument) - Get document properties including the current document type

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Document not found | The specified path does not resolve to an existing document. |
| Document type not found | The specified `documentTypeID` does not exist. |
| Access denied | The user does not have write permission on the document. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/UpdateDocumentType*
