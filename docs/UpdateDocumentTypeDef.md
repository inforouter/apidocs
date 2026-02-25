# UpdateDocumentTypeDef API

Updates the definition of an existing document type. Allows renaming the document type and optionally changing its required property set. Document type definitions are system-wide and affect all documents assigned to that type.

## Endpoint

```
/srv.asmx/UpdateDocumentTypeDef
```

## Methods

- **GET** `/srv.asmx/UpdateDocumentTypeDef?authenticationTicket=...&documentTypeId=...&newDocumentTypeName=...&newRequiredPropertySetName=...`
- **POST** `/srv.asmx/UpdateDocumentTypeDef` (form data)
- **SOAP** Action: `http://tempuri.org/UpdateDocumentTypeDef`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `documentTypeId` | int | Yes | The numeric ID of the document type definition to update. Use `GetDocumentTypes` to retrieve IDs. |
| `newDocumentTypeName` | string | Yes | The new name for the document type. Must be unique system-wide. |
| `newRequiredPropertySetName` | string | No | The name of the property set to require for documents of this type. Pass `null` or empty string to remove the required property set. |

---

## Response

### Success Response

```xml
<response success="true" error="" />
```

### Error Response

```xml
<response success="false" error="Document type not found." />
```

---

## Required Permissions

The calling user must be an **authenticated user** (anonymous users are not allowed). Administrator role is recommended as document type definitions are system-wide resources.

---

## Example

### GET Request

```
GET /srv.asmx/UpdateDocumentTypeDef
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &documentTypeId=5
  &newDocumentTypeName=Financial+Report
  &newRequiredPropertySetName=FinanceProperties
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/UpdateDocumentTypeDef HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&documentTypeId=5
&newDocumentTypeName=Financial Report
&newRequiredPropertySetName=FinanceProperties
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:UpdateDocumentTypeDef>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:documentTypeId>5</tns:documentTypeId>
      <tns:newDocumentTypeName>Financial Report</tns:newDocumentTypeName>
      <tns:newRequiredPropertySetName>FinanceProperties</tns:newRequiredPropertySetName>
    </tns:UpdateDocumentTypeDef>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Renaming a document type affects all documents currently assigned to that type — they will appear under the new name.
- Changing the required property set may affect compliance validation for documents already assigned to this type.
- Anonymous users cannot call this API (returns an insufficient rights error).
- Use `GetDocumentTypes` to retrieve all existing document type IDs and names.

---

## Related APIs

- [GetDocumentTypes](GetDocumentTypes.md) - Retrieve all defined document type definitions
- [CreateDocumentTypeDef](CreateDocumentTypeDef.md) - Create a new document type definition
- [UpdateDocumentType](UpdateDocumentType.md) - Assign a document type to a specific document

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Insufficient rights | Anonymous users cannot perform this action. |
| Document type not found | The specified `documentTypeId` does not exist. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/UpdateDocumentTypeDef*
