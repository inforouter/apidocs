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

Removes a document type.

```javascript
await call('DeleteDocumentTypeDef', {
  authenticationTicket: ticket,
  documentTypeId: 1081
});
```

**An id that does not exist is still a success.** There is no `4041` and no count of what was removed,
so a caller cannot tell a delete that removed a type from one that found nothing - unlike
[DeleteDocument](DeleteDocument.md) and [DeleteDocumentThumbnail](DeleteDocumentThumbnail.md) next to
it, which both answer `4041`. Check with [GetDocumentTypes](GetDocumentTypes.md) if it matters.

## Notes

- This operation permanently deletes the document type definition
- Documents that are currently using this document type will lose their type association
- It's recommended to verify no documents are using this type before deletion
- Related APIs:
  - `GetDocumentTypes` - List all document types
  - `CreateDocumentTypeDef` - Create a new document type
  - `UpdateDocumentTypeDef` - Update an existing document type

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all - the anonymous user is refused |
| `4030` | the caller is not a system administrator |
| `none` | an id that matches no document type is a success, not an error |

Common error responses:

- `[901]Session expired or Invalid ticket` - Invalid authentication ticket
- `[2730]Insufficient rights. Anonymous users cannot perform this action` - User is not authenticated
- `Document type not found` - The specified documentTypeId does not exist
- `Document type is in use` - Cannot delete because documents are using this type
