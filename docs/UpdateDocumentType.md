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

Assigns a document type to one document, or takes it off.

```javascript
await call('UpdateDocumentType', {
  authenticationTicket: ticket,
  Path: '/Finance/Invoices/4471.pdf',
  DocumentTypeID: 1081          // 0 removes the type
});
```

`DocumentTypeID` of `0` is the way to remove a type - it is not an error. An id no type has is
`4041`. [GetDocument](GetDocument.md) reads the result back as `DocTypeID` and `DocTypeName`.

If the type requires a property set, the document has to satisfy it; see
[GetDocumentTypes](GetDocumentTypes.md) for which sets the types need.

## Notes

- Use `GetDocumentTypes` to retrieve all defined document type IDs and names before calling this API.
- Passing `documentTypeID=0` clears the document type assignment.
- The new document type may have a required property set -" if the required properties are not yet filled in, publishing or other operations may be affected.

---

## Related APIs

- [GetDocumentTypes](GetDocumentTypes.md) - Retrieve all defined document type definitions
- [CreateDocumentTypeDef](CreateDocumentTypeDef.md) - Create a new document type definition
- [UpdateDocumentTypeDef](UpdateDocumentTypeDef.md) - Rename an existing document type definition
- [GetDocument](GetDocument.md) - Get document properties including the current document type

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | no document at that path - including a folder path, and one the caller may not see |
| `4041` | no document type with that id |
| `4030` | the caller may not change this document |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Document not found | The specified path does not resolve to an existing document. |
| Document type not found | The specified `documentTypeID` does not exist. |
| Access denied | The user does not have write permission on the document. |
| `SystemError:...` | An unexpected server-side error occurred. |

---