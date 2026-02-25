# AssociateFolder API

Creates an association between the specified source folder and a target item (document or folder). This lets you link a folder to related content so that users can navigate between conceptually connected items. Use this API to cross-reference a folder with documents or other folders it is related to.

> **Note:** Because the source is always a folder, the association type is always `Related` regardless of the `AssociationTypeID` value supplied. To create typed associations (Rendition, Copy, ParentChild, Derivation), both sides must be documents -" use [AssociateDocument](AssociateDocument.md) instead.

## Endpoint

```
/srv.asmx/AssociateFolder
```

## Methods

- **GET** `/srv.asmx/AssociateFolder?AuthenticationTicket=...&FolderPath=...&AssociateWith_ItemPath=...&AssociationTypeID=...`
- **POST** `/srv.asmx/AssociateFolder` (form data)
- **SOAP** Action: `http://tempuri.org/AssociateFolder`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `FolderPath` | string | Yes | Full infoRouter path to the source folder (e.g. `/Finance/Reports`). |
| `AssociateWith_ItemPath` | string | Yes | Full infoRouter path to the target document or folder to associate with. The API first attempts to resolve this as a document; if not found, it attempts to resolve it as a folder. |
| `AssociationTypeID` | int | Yes | Ignored. Because the source is a folder, the association type is always forced to `Related` (0). The parameter must be supplied but its value has no effect. |

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

The calling user must have the **`FolderPropertyChange`** permission on the **source folder** (`FolderPath`). This is typically granted to folder owners, domain managers, and users with Edit access on the folder. Read-only users cannot create associations.

No specific permission check is performed on the target item (`AssociateWith_ItemPath`) -" only read access is needed to resolve the target path.

---

## Example

### GET Request

```
GET /srv.asmx/AssociateFolder
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &FolderPath=/Finance/Reports
  &AssociateWith_ItemPath=/Finance/Archive/2023-Reports
  &AssociationTypeID=0
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/AssociateFolder HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&FolderPath=/Finance/Reports
&AssociateWith_ItemPath=/Finance/Archive/2023-Reports
&AssociationTypeID=0
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:AssociateFolder>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:FolderPath>/Finance/Reports</tns:FolderPath>
      <tns:AssociateWith_ItemPath>/Finance/Archive/2023-Reports</tns:AssociateWith_ItemPath>
      <tns:AssociationTypeID>0</tns:AssociationTypeID>
    </tns:AssociateFolder>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- **Association type is always Related**: Because the source is a folder, the system always overrides `AssociationTypeID` and stores the association as `Related` (0). This applies even when the target is a document. Typed associations (Rendition, Copy, ParentChild, Derivation) are only available when both objects are documents -" use [AssociateDocument](AssociateDocument.md) for those cases.
- **Target path resolution order**: The API first attempts to resolve `AssociateWith_ItemPath` as a document. Only if no document is found does it attempt to resolve it as a folder. If neither is found, the call fails with an error.
- **Folder-to-document association**: When `AssociateWith_ItemPath` resolves to a document, the association is stored between the source folder and that document (type always `Related`).
- **Folder-to-folder association**: When `AssociateWith_ItemPath` resolves to a folder, the association is stored between the two folders (type always `Related`).
- **Duplicate handling**: If a `Related` association between the same two items already exists, the call returns `success="true"` without creating a duplicate record.
- **Self-association not allowed**: A folder cannot be associated with itself. Passing the same path for both `FolderPath` and `AssociateWith_ItemPath` returns an error.
- **No subscriber notification**: Unlike document-to-document associations, folder associations do not trigger subscriber notifications.

---

## Related APIs

- [AssociateDocument](AssociateDocument.md) - Create an association from a document to another document or folder (supports typed associations)
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
| `Folder not found.` | `FolderPath` does not resolve to an existing folder. |
| `[error from path resolution]` | `AssociateWith_ItemPath` does not resolve to any existing document or folder. |
| `Insufficient rights.` | The calling user does not have the `FolderPropertyChange` permission on the source folder. |
| `Objects cannot be associated with themselves.` | `FolderPath` and `AssociateWith_ItemPath` resolve to the same object. |
| `SystemError:...` | An unexpected server-side error occurred. |
