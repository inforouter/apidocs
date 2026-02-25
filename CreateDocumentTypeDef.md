# CreateDocumentTypeDef API

Creates a new document type definition in the system. Document types allow documents to be categorized and optionally associated with a required custom property set, enforcing metadata collection for documents of that type.

## Endpoint

```
/srv.asmx/CreateDocumentTypeDef
```

## Methods

- **GET** `/srv.asmx/CreateDocumentTypeDef?authenticationTicket=...&DocumentTypeName=...&RequiredPropertySetName=...`
- **POST** `/srv.asmx/CreateDocumentTypeDef` (form data)
- **SOAP** Action: `http://tempuri.org/CreateDocumentTypeDef`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DocumentTypeName` | string | Yes | Name for the new document type. Maximum 30 characters. May contain only letters, digits, spaces, and underscores. The name `GENERIC` is reserved and cannot be used. |
| `RequiredPropertySetName` | string | No | Name of an existing global property set to associate with this document type. When specified, documents of this type will require the named property set. The property set must be global (system-wide) and applicable to documents. Pass an empty string or omit to create a document type with no required property set. |

## Response

### Success Response

```xml
<response success="true" error="" DocumentTypeId="42" />
```

| Attribute | Description |
|-----------|-------------|
| `success` | `true` if the document type was created successfully. |
| `DocumentTypeId` | The integer ID assigned to the newly created document type. |

### Error Response

```xml
<response success="false" error="Error message" />
```

---

## Required Permissions

Only **system administrators** may call this API. Non-administrator users receive an error even if they are domain managers.

---

## Example

### GET Request — without a property set

```
GET /srv.asmx/CreateDocumentTypeDef
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DocumentTypeName=Contract
  &RequiredPropertySetName=
HTTP/1.1
```

### GET Request — with a required property set

```
GET /srv.asmx/CreateDocumentTypeDef
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DocumentTypeName=Invoice
  &RequiredPropertySetName=InvoiceMetadata
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/CreateDocumentTypeDef HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&DocumentTypeName=Invoice
&RequiredPropertySetName=InvoiceMetadata
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:CreateDocumentTypeDef>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:DocumentTypeName>Invoice</tns:DocumentTypeName>
      <tns:RequiredPropertySetName>InvoiceMetadata</tns:RequiredPropertySetName>
    </tns:CreateDocumentTypeDef>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Document type names are case-insensitive for uniqueness checks — `Contract` and `CONTRACT` are treated as the same name.
- The name `GENERIC` (any casing) is a built-in reserved type and cannot be used as a new document type name.
- If `RequiredPropertySetName` is provided, the named property set must already exist, must be a **global** (system-wide) property set, and must be configured to apply to documents. Domain-level or folder-level property sets are not accepted.
- The returned `DocumentTypeId` can be used with `UpdateDocumentTypeDef` and `DeleteDocumentTypeDef`.
- To retrieve all defined document types, use `GetDocumentTypes`.

---

## Related APIs

- [GetDocumentTypes](GetDocumentTypes) - Retrieve all defined document types
- [UpdateDocumentTypeDef](UpdateDocumentTypeDef) - Update an existing document type definition
- [DeleteDocumentTypeDef](DeleteDocumentTypeDef) - Delete a document type definition

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Only the system administrator can perform this operation` | The authenticated user is not a system administrator. |
| `A document type with this name already exists.` | A document type with the given name already exists in the system. |
| `Reserved value \| 'GENERIC'` | The name `GENERIC` is reserved and cannot be used. |
| `The document type field must contain only letters, numeric, space or underscore characters.` | The `DocumentTypeName` contains invalid characters. |
| `Specified custom propertyset not applicable to the documents.` | The named property set is not configured to apply to documents. |
| `Specified custom propertyset is not a public property set.` | The named property set is not a global (system-wide) property set. |
| `Property set not found` | The value specified in `RequiredPropertySetName` does not match any existing property set. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/CreateDocumentTypeDef*
