# GetDocumentTypes API

Returns the list of all document type definitions configured in the system. Document types allow documents to be classified and associated with a required custom property set.

## Endpoint

```
/srv.asmx/GetDocumentTypes
```

## Methods

- **GET** `/srv.asmx/GetDocumentTypes?AuthenticationTicket=...`
- **POST** `/srv.asmx/GetDocumentTypes` (form data)
- **SOAP** Action: `http://tempuri.org/GetDocumentTypes`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |

---

## Response

### Success Response

Returns a `<response>` root element containing a `<DocumentTypes>` child with one `<DocumentType>` element per defined document type. If no document types are configured, `<DocumentTypes>` is present but empty.

```xml
<response success="true" error="">
  <DocumentTypes>
    <DocumentType TypeID="1"
                  TypeName="Contract"
                  PropertySetID="5"
                  PropertySetName="Contract Details" />
    <DocumentType TypeID="2"
                  TypeName="Invoice"
                  PropertySetID="8"
                  PropertySetName="Invoice Metadata" />
    <DocumentType TypeID="3"
                  TypeName="General"
                  PropertySetID="0"
                  PropertySetName="" />
  </DocumentTypes>
</response>
```

### DocumentType Element Attributes

| Attribute | Description |
|-----------|-------------|
| `TypeID` | Unique integer ID of the document type. |
| `TypeName` | Display name of the document type. |
| `PropertySetID` | Integer ID of the custom property set associated with this document type. `0` if no property set is linked. |
| `PropertySetName` | Name of the associated property set. Empty string if no property set is linked. |

### No Document Types Response

When no document types are configured in the system:

```xml
<response success="true" error="">
  <DocumentTypes />
</response>
```

### Error Response

```xml
<response success="false" error="[900] Authentication failed" />
```

---

## Required Permissions

Any authenticated user may call this API.

---

## Example

### GET Request

```
GET /srv.asmx/GetDocumentTypes
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetDocumentTypes HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetDocumentTypes>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
    </tns:GetDocumentTypes>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- All document types defined in the system are returned; there is no filtering or pagination.
- `PropertySetID="0"` and `PropertySetName=""` indicate the document type has no associated property set requirement.
- To create, update, or delete document type definitions, use `CreateDocumentTypeDef`, `UpdateDocumentTypeDef`, or `DeleteDocumentTypeDef`.

---

## Related APIs

- [CreateDocumentTypeDef](CreateDocumentTypeDef.md) - Create a new document type definition
- [DeleteDocumentTypeDef](DeleteDocumentTypeDef.md) - Delete a document type definition
- [GetDocument](GetDocument.md) - Get document properties (includes `DocTypeID` and `DocTypeName`)

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `SystemError:...` | An unexpected server-side error occurred. |

---
