# CreateDocumentTypeDef1 API

Creates a new document type definition with an optional required property set and an optional default retention and disposition schedule. When a document is assigned this type, the configured schedule is automatically applied.

## Endpoint

```
/srv.asmx/CreateDocumentTypeDef1
```

## Methods

- **GET** `/srv.asmx/CreateDocumentTypeDef1?authenticationTicket=...&DocumentTypeName=...&RequiredPropertySetName=...&RandDScheduleName=...`
- **POST** `/srv.asmx/CreateDocumentTypeDef1` (form data)
- **SOAP** Action: `http://tempuri.org/CreateDocumentTypeDef1`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DocumentTypeName` | string | Yes | Name for the new document type. Maximum 30 characters. May contain only letters, digits, spaces, and underscores. The name `GENERIC` is reserved and cannot be used. |
| `RequiredPropertySetName` | string | No | Name of an existing global property set to associate with this document type. The property set must be global and applicable to documents. Pass an empty string or omit for no required property set. |
| `RandDScheduleName` | string | No | Name of an existing retention and disposition schedule to automatically assign when this document type is applied to a document. Pass an empty string or omit for no default schedule. |

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

Only **system administrators** may call this API.

---

## Example

### GET Request — with schedule

```
GET /srv.asmx/CreateDocumentTypeDef1
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DocumentTypeName=Financial+Record
  &RequiredPropertySetName=FinanceMetadata
  &RandDScheduleName=Finance+Records+-+7+Years
HTTP/1.1
```

### GET Request — without schedule

```
GET /srv.asmx/CreateDocumentTypeDef1
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DocumentTypeName=Contract
  &RequiredPropertySetName=
  &RandDScheduleName=
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/CreateDocumentTypeDef1 HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&DocumentTypeName=Financial+Record
&RequiredPropertySetName=FinanceMetadata
&RandDScheduleName=Finance+Records+-+7+Years
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:CreateDocumentTypeDef1>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:DocumentTypeName>Financial Record</tns:DocumentTypeName>
      <tns:RequiredPropertySetName>FinanceMetadata</tns:RequiredPropertySetName>
      <tns:RandDScheduleName>Finance Records - 7 Years</tns:RandDScheduleName>
    </tns:CreateDocumentTypeDef1>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Document type names are case-insensitive for uniqueness checks — `Contract` and `CONTRACT` are treated as the same name.
- The name `GENERIC` (any casing) is reserved and cannot be used.
- If `RequiredPropertySetName` is provided, the property set must already exist, be global (system-wide), and be configured to apply to documents.
- If `RandDScheduleName` is provided, the schedule must already exist. The name is looked up by exact match (case-insensitive).
- The retention schedule is applied automatically when the document type is later assigned to a document via `UpdateDocumentType`. It does not affect documents that were assigned the type before this definition was created.
- The returned `DocumentTypeId` can be used with `UpdateDocumentTypeDef1` and `DeleteDocumentTypeDef`.

---

## Related APIs

- [CreateDocumentTypeDef](CreateDocumentTypeDef.md) - Create a document type without a retention schedule
- [UpdateDocumentTypeDef1](UpdateDocumentTypeDef1.md) - Update a document type definition including its retention schedule
- [GetDocumentTypes](GetDocumentTypes.md) - Retrieve all defined document types
- [DeleteDocumentTypeDef](DeleteDocumentTypeDef.md) - Delete a document type definition

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
| `Specified custom propertyset is not a public property set.` | The named property set is not a global property set. |
| `Property set not found` | The value in `RequiredPropertySetName` does not match any existing property set. |
| `The selected retention and disposition schedule cannot be found.` | The value in `RandDScheduleName` does not match any existing schedule. |
