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
<response success="true" error="" errorCode="0" />
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

Links a document to another document or to a folder.

```javascript
await call('AssociateDocument', {
  authenticationTicket: ticket,
  DocumentPath: '/Finance/Invoices/inv-1001.pdf',
  AssociateWith_ItemPath: '/Finance/Purchase orders/po-1001.pdf',
  AssociationTypeID: 3            // this one is the parent of that one
});
```

Making the same link twice does not create a second one. A document cannot be associated with
itself - that is refused `4000`.

**`AssociationTypeID` is checked against the five** and anything else is refused `4000`. Until 9.0
any number was accepted and stored, and the readers then gave it the name belonging to type 0 - so an
association came back labelled "Related" while carrying a type id that means nothing.

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

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | no document at `DocumentPath`, or nothing at `AssociateWith_ItemPath` |
| `4000` | the two paths are the same |
| `4030` | the caller may not change that document |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
