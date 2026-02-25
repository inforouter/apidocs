# AssociateDocument API

Creates an association between the specified source document and a target item (document or folder). Associations let you link related content together so that users can navigate between items that are conceptually connected. The association type controls the semantic relationship -" for example, marking one document as a rendition or a copy of another. Use this API to build cross-references between documents, or to link documents to folders.

## Endpoint

```
/srv.asmx/AssociateDocument
```

## Methods

- **GET** `/srv.asmx/AssociateDocument?AuthenticationTicket=...&DocumentPath=...&AssociateWith_ItemPath=...&AssociationTypeID=...`
- **POST** `/srv.asmx/AssociateDocument` (form data)
- **SOAP** Action: `http://tempuri.org/AssociateDocument`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DocumentPath` | string | Yes | Full infoRouter path to the source document (e.g. `/Finance/Reports/Q1-Report.pdf`). |
| `AssociateWith_ItemPath` | string | Yes | Full infoRouter path to the target document or folder to associate with. The API first attempts to resolve this as a document; if not found, it attempts to resolve it as a folder. |
| `AssociationTypeID` | int | Yes | Numeric code representing the type of association to create. See valid values below. **Note:** If the target item (`AssociateWith_ItemPath`) resolves to a folder, this parameter is ignored and `Related` (0) is always used. |

### AssociationTypeID Values

| Value | Name | Description |
|-------|------|-------------|
| `0` | Related | General relationship between two items. |
| `1` | Rendition | The target is a rendition (alternate format) of the source document. |
| `2` | Copy | The target is a copy of the source document. |
| `3` | ParentChild | The source is a parent of the target document. |
| `4` | Derivation | The target is derived from the source document. |

---

## Response

### Success Response

```xml
<response success="true" />
```

### Error Response

```xml
<response success="false" error="Insufficient rights." />
```

---

## Required Permissions

The calling user must have the **`DocumentPropertyChange`** permission on the **source document** (`DocumentPath`). This is typically granted to document owners, domain managers, and users with Edit access. Read-only users cannot create associations.

No specific permission check is performed on the target item (`AssociateWith_ItemPath`) -" only read access is needed to resolve the target path.

---

## Example

### GET Request

```
GET /srv.asmx/AssociateDocument
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DocumentPath=/Finance/Reports/Q1-2024-Report.pdf
  &AssociateWith_ItemPath=/Finance/Reports/Q1-2024-Report-Final.pdf
  &AssociationTypeID=1
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/AssociateDocument HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&DocumentPath=/Finance/Reports/Q1-2024-Report.pdf
&AssociateWith_ItemPath=/Finance/Reports/Q1-2024-Report-Final.pdf
&AssociationTypeID=1
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:AssociateDocument>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:DocumentPath>/Finance/Reports/Q1-2024-Report.pdf</tns:DocumentPath>
      <tns:AssociateWith_ItemPath>/Finance/Reports/Q1-2024-Report-Final.pdf</tns:AssociateWith_ItemPath>
      <tns:AssociationTypeID>1</tns:AssociationTypeID>
    </tns:AssociateDocument>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- **Document-to-document associations**: When `AssociateWith_ItemPath` resolves to a document, the `AssociationTypeID` is applied as specified. The association is stored bidirectionally in the database.
- **Document-to-folder associations**: When `AssociateWith_ItemPath` resolves to a folder (i.e., is not found as a document), `AssociationTypeID` is ignored and the `Related` (0) type is always used for folder associations.
- **Duplicate handling for Related type**: If an association of type `Related` between the same two items already exists, the call returns `success="true"` without creating a duplicate record.
- **Overwrite behaviour for other types**: For association types other than `Related`, any existing association between the same two items is deleted and then re-created with the new type. This means calling `AssociateDocument` is effectively an upsert operation.
- **Self-association not allowed**: A document cannot be associated with itself. Passing the same path for both `DocumentPath` and `AssociateWith_ItemPath` returns an error.
- **Target path resolution order**: The API first tries to resolve `AssociateWith_ItemPath` as a document. Only if no document is found does it try to resolve it as a folder. If neither is found, the call fails.
- **Subscribers are notified**: When a document-to-document association is created, document subscribers are notified of the property change.
- **Association types for folders**: Folder associations only support `Related` (0). If you need typed associations, both sides must be documents.

---

## Related APIs

- [AssociateFolder](AssociateFolder.md) - Create an association from a folder to a document or folder
- [AssociatedDocuments](AssociatedDocuments.md) - Get the list of documents associated with a document or folder
- [AssociatedFolders](AssociatedFolders.md) - Get the list of folders associated with a document or folder
- [AssociatedFoldersAndDocuments](AssociatedFoldersAndDocuments.md) - Get all associated items of a document or folder
- [AssociationTypes](AssociationTypes.md) - Get the list of configured association types
- [RemoveAssociation](RemoveAssociation.md) - Remove an existing association between two items

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Document not found.` | `DocumentPath` does not resolve to an existing document. |
| `[error from path resolution]` | `AssociateWith_ItemPath` does not resolve to any existing document or folder. |
| `Insufficient rights.` | The calling user does not have the `DocumentPropertyChange` permission on the source document. |
| `Objects cannot be associated with themselves.` | `DocumentPath` and `AssociateWith_ItemPath` resolve to the same object. |
| `SystemError:...` | An unexpected server-side error occurred. |
