# DeleteDocumentTypeDef API

Deletes a document type definition from the system.

## Endpoint

```
/srv.asmx/DeleteDocumentTypeDef
```

## Methods

- **GET** `/srv.asmx/DeleteDocumentTypeDef?authenticationTicket=...&documentTypeId=...`
- **POST** `/srv.asmx/DeleteDocumentTypeDef` (form data)
- **SOAP** Action: `http://tempuri.org/DeleteDocumentTypeDef`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from AuthenticateUser |
| `documentTypeId` | int | Yes | ID of the document type to delete |

## Response

### Success Response
```xml
<root success="true" />
```

### Error Response
```xml
<root success="false" error="[ErrorCode] Error message" />
```

## Required Permissions

- User must be authenticated (anonymous users cannot perform this action)
- User must have administrative rights to manage document type definitions

## Example

### Request (POST)
```
POST /srv.asmx/DeleteDocumentTypeDef HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&documentTypeId=5
```

### Request (SOAP)
```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <DeleteDocumentTypeDef xmlns="http://tempuri.org/">
      <authenticationTicket>abc123</authenticationTicket>
      <documentTypeId>5</documentTypeId>
    </DeleteDocumentTypeDef>
  </soap:Body>
</soap:Envelope>
```

### Response
```xml
<?xml version="1.0" encoding="utf-8"?>
<root success="true" />
```

## Notes

- This operation permanently deletes the document type definition
- Documents that are currently using this document type will lose their type association
- It's recommended to verify no documents are using this type before deletion
- Related APIs:
  - `GetDocumentTypes` - List all document types
  - `CreateDocumentTypeDef` - Create a new document type
  - `UpdateDocumentTypeDef` - Update an existing document type

## Error Codes

Common error responses:

- `[901]Session expired or Invalid ticket` - Invalid authentication ticket
- `[2730]Insufficient rights. Anonymous users cannot perform this action` - User is not authenticated
- `Document type not found` - The specified documentTypeId does not exist
- `Document type is in use` - Cannot delete because documents are using this type
