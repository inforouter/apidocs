# AssociatedFoldersAndDocuments API

Returns the combined list of all items -" both documents and folders -" that are associated with the specified document or folder. Both forward associations (where the specified item is the source) and reverse associations (where the specified item is the target) are included in each group. Use this API as a single call to discover all associations of an item without making separate calls to [AssociatedDocuments](AssociatedDocuments.md) and [AssociatedFolders](AssociatedFolders.md).

## Endpoint

```
/srv.asmx/AssociatedFoldersAndDocuments
```

## Methods

- **GET** `/srv.asmx/AssociatedFoldersAndDocuments?AuthenticationTicket=...&ItemPath=...`
- **POST** `/srv.asmx/AssociatedFoldersAndDocuments` (form data)
- **SOAP** Action: `http://tempuri.org/AssociatedFoldersAndDocuments`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `ItemPath` | string | Yes | Full infoRouter path to the source document or folder whose associations are to be retrieved (e.g. `/Finance/Reports/Q1-Report.pdf` or `/Finance/Reports`). |

---

## Response

### Success Response

The response contains a `<response success="true">` root element with two child sections: `<AssociatedDocuments>` and `<AssociatedFolders>`. Each section contains the relevant associated items.

```xml
<response success="true">
  <AssociatedDocuments>
    <AssociatedDocument
        IsReverseAssociation="FALSE"
        AssociationTypeID="1"
        AssociationTypeName="Rendition"
        DocumentID="1234"
        Path="/Finance/Reports/Q1-2024-Report-Final.pdf"
        Size="204800"
        DateModified="2024-06-15T14:30:00">
      <!-- full document properties -->
    </AssociatedDocument>
    <AssociatedDocument
        IsReverseAssociation="TRUE"
        AssociationTypeID="0"
        AssociationTypeName="Related"
        DocumentID="5678"
        Path="/Finance/Archive/Q1-2023-Report.pdf"
        Size="102400"
        DateModified="2023-06-10T09:00:00">
      <!-- full document properties -->
    </AssociatedDocument>
  </AssociatedDocuments>
  <AssociatedFolders>
    <AssociatedFolder
        IsReverseAssociation="FALSE"
        AssociationTypeID="0"
        AssociationTypeName="Related"
        FolderID="42"
        Path="/Finance/Archive/2023-Reports">
      <!-- full folder properties -->
    </AssociatedFolder>
  </AssociatedFolders>
</response>
```

### AssociatedDocument Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `IsReverseAssociation` | string | `TRUE` if the specified item is the association target; `FALSE` if it is the source. |
| `AssociationTypeID` | int | Numeric association type: 0=Related, 1=Rendition, 2=Copy, 3=ParentChild, 4=Derivation. |
| `AssociationTypeName` | string | Localised display name of the association type. |
| `DocumentID` | int | Internal numeric ID of the associated document. |
| `Path` | string | Full infoRouter path of the associated document. Empty if unresolvable. |
| `Size` | int | File size of the associated document in bytes. Empty if unresolvable. |
| `DateModified` | string | Last modification date of the associated document. Empty if unresolvable. |

### AssociatedFolder Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `IsReverseAssociation` | string | `TRUE` if the specified item is the association target; `FALSE` if it is the source. |
| `AssociationTypeID` | int | Always `0` (Related) -" folder associations only support the Related type. |
| `AssociationTypeName` | string | Always `Related` for folder associations. |
| `FolderID` | int | Internal numeric ID of the associated folder. |
| `Path` | string | Full infoRouter path of the associated folder. Empty if unresolvable. |

### Empty Result

When there are no associated items, both child elements are empty:

```xml
<response success="true">
  <AssociatedDocuments />
  <AssociatedFolders />
</response>
```

### Error Response

```xml
<response success="false" error="Document not found." />
```

---

## Required Permissions

Any authenticated user with read access to the item at `ItemPath` can call this API. No elevated permissions are required to retrieve the association list.

---

## Example

### GET Request

```
GET /srv.asmx/AssociatedFoldersAndDocuments
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &ItemPath=/Finance/Reports/Q1-2024-Report.pdf
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/AssociatedFoldersAndDocuments HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&ItemPath=/Finance/Reports/Q1-2024-Report.pdf
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:AssociatedFoldersAndDocuments>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:ItemPath>/Finance/Reports/Q1-2024-Report.pdf</tns:ItemPath>
    </tns:AssociatedFoldersAndDocuments>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- **Source can be a document or folder**: `ItemPath` is first resolved as a document; if not found, it is resolved as a folder. Associations for whichever is found are returned.
- **Both directions are returned**: Each section includes forward associations (`IsReverseAssociation="FALSE"`, where the item is the source) and reverse associations (`IsReverseAssociation="TRUE"`, where the item is the target).
- **Combined response**: This API is equivalent to calling [AssociatedDocuments](AssociatedDocuments.md) and [AssociatedFolders](AssociatedFolders.md) in sequence and merging the results. Both `<AssociatedDocuments>` and `<AssociatedFolders>` elements are always present in the response, even when empty.
- **Folder associations are always Related**: The `AssociationTypeID` for every `<AssociatedFolder>` element will always be `0` (Related). Document associations may have any type (0-"4).
- **Unresolvable items**: If an associated document or folder has been deleted or is inaccessible, its `Path`, and for documents `Size` and `DateModified`, are returned as empty strings. The ID is still present.

---

## Related APIs

- [AssociateDocument](AssociateDocument.md) - Create an association from a document to another document or folder
- [AssociateFolder](AssociateFolder.md) - Create an association from a folder to another document or folder
- [AssociatedDocuments](AssociatedDocuments.md) - Get only the associated documents of a document or folder
- [AssociatedFolders](AssociatedFolders.md) - Get only the associated folders of a document or folder
- [AssociationTypes](AssociationTypes.md) - Get the list of configured association types
- [RemoveAssociation](RemoveAssociation.md) - Remove an existing association between two items

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Document not found.` | `ItemPath` does not resolve to an existing document or folder. |
| `SystemError:...` | An unexpected server-side error occurred. |
