# RemoveAssociation API

Removes an existing association between two infoRouter items (documents or folders). The source item can be a document or a folder; the target item can likewise be a document or a folder. Use this API to clean up stale cross-references or to undo an association created by [AssociateDocument](AssociateDocument.md) or [AssociateFolder](AssociateFolder.md).

## Endpoint

```
/srv.asmx/RemoveAssociation
```

## Methods

- **GET** `/srv.asmx/RemoveAssociation?AuthenticationTicket=...&ItemPath=...&AssociationWith_ItemPath=...&IsReverseAssociation=...`
- **POST** `/srv.asmx/RemoveAssociation` (form data)
- **SOAP** Action: `http://tempuri.org/RemoveAssociation`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `ItemPath` | string | Yes | Full infoRouter path to the first item in the association (e.g. `/Finance/Reports/Q1-Report.pdf`). When `IsReverseAssociation` is `false` this is the **source** item; when `IsReverseAssociation` is `true` this is the **target** item. |
| `AssociationWith_ItemPath` | string | Yes | Full infoRouter path to the second item in the association. When `IsReverseAssociation` is `false` this is the **target** item; when `IsReverseAssociation` is `true` this is the **source** item. |
| `IsReverseAssociation` | bool | Yes | Determines which item is treated as the **source** (the owner of the association record). Pass `false` when `ItemPath` is the source and `AssociationWith_ItemPath` is the target. Pass `true` to swap the roles so that `AssociationWith_ItemPath` is the source and `ItemPath` is the target. This must match the direction used when the association was originally created. |

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

The calling user must have the **`DocumentPropertyChange`** permission on the **source** item (i.e. the item that owns the association record). For documents this is typically the document owner, the domain manager, or a user with Edit access. Read-only users cannot remove associations.

---

## Example

### GET Request

```
GET /srv.asmx/RemoveAssociation
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &ItemPath=/Finance/Reports/Q1-2024-Report.pdf
  &AssociationWith_ItemPath=/Finance/Reports/Q1-2024-Report-Final.pdf
  &IsReverseAssociation=false
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/RemoveAssociation HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&ItemPath=/Finance/Reports/Q1-2024-Report.pdf
&AssociationWith_ItemPath=/Finance/Reports/Q1-2024-Report-Final.pdf
&IsReverseAssociation=false
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:RemoveAssociation>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:ItemPath>/Finance/Reports/Q1-2024-Report.pdf</tns:ItemPath>
      <tns:AssociationWith_ItemPath>/Finance/Reports/Q1-2024-Report-Final.pdf</tns:AssociationWith_ItemPath>
      <tns:IsReverseAssociation>false</tns:IsReverseAssociation>
    </tns:RemoveAssociation>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- **Direction matters**: The `IsReverseAssociation` flag determines which item is the source (the item that owns the association record in the database). You must pass the same direction that was used when the association was created, otherwise the association will not be found and the call will fail.
- **Mixed types supported**: The source can be a document or a folder, and the target can be a document or a folder -" all four combinations are handled.
- **Path resolution order**: For each item the API first tries to resolve the path as a document; if no document is found it then tries to resolve it as a folder. If neither is found the call fails.
- **Idempotent on missing association**: If the two items exist but the specified association between them does not exist, the underlying remove call will return an error message. The API propagates this as `success="false"`.
- **No notification sent**: Removing an association does not trigger subscriber notifications.

---

## Related APIs

- [AssociateDocument](AssociateDocument.md) - Create an association between a document and another document or folder
- [AssociateFolder](AssociateFolder.md) - Create an association between a folder and another document or folder
- [AssociatedDocuments](AssociatedDocuments.md) - Get the list of documents associated with a document or folder
- [AssociatedFolders](AssociatedFolders.md) - Get the list of folders associated with a document or folder
- [AssociatedFoldersAndDocuments](AssociatedFoldersAndDocuments.md) - Get all associated items of a document or folder
- [AssociationTypes](AssociationTypes.md) - Get the list of configured association types

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Insufficient rights.` | The calling user does not have the required permission on the source item. |
| `[error from path resolution]` | One or both of the supplied paths could not be resolved to an existing document or folder. |
| `SystemError:...` | An unexpected server-side error occurred. |
