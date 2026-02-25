# AssociatedDocuments API

Returns the list of documents that are associated with the specified document or folder. Both forward associations (where the specified item is the source) and reverse associations (where the specified item is the target) are returned. Use this API to discover all documents linked to an item, regardless of which side created the association.

## Endpoint

```
/srv.asmx/AssociatedDocuments
```

## Methods

- **GET** `/srv.asmx/AssociatedDocuments?AuthenticationTicket=...&ItemPath=...`
- **POST** `/srv.asmx/AssociatedDocuments` (form data)
- **SOAP** Action: `http://tempuri.org/AssociatedDocuments`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `ItemPath` | string | Yes | Full infoRouter path to the source document or folder whose associated documents are to be retrieved (e.g. `/Finance/Reports/Q1-Report.pdf`). |

---

## Response

### Success Response

The response contains a `<response success="true">` root element with an `<AssociatedDocuments>` child element containing one `<AssociatedDocument>` element per associated document. Both forward and reverse association directions are included.

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
</response>
```

### AssociatedDocument Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `IsReverseAssociation` | string | `TRUE` if the specified item is the target of this association (i.e. another item associated to it); `FALSE` if the specified item is the source. |
| `AssociationTypeID` | int | Numeric association type. See values below. |
| `AssociationTypeName` | string | Localised display name of the association type (e.g. `Related`, `Rendition`). |
| `DocumentID` | int | Internal numeric ID of the associated document. |
| `Path` | string | Full infoRouter path of the associated document. Empty if the document cannot be resolved. |
| `Size` | int | File size of the associated document in bytes. Empty if the document cannot be resolved. |
| `DateModified` | string | Last modification date of the associated document. Empty if the document cannot be resolved. |

### AssociationTypeID Values

| Value | Name | Description |
|-------|------|-------------|
| `0` | Related | General relationship. |
| `1` | Rendition | Target is a rendition (alternate format) of the source. |
| `2` | Copy | Target is a copy of the source. |
| `3` | ParentChild | Source is the parent of the target. |
| `4` | Derivation | Target is derived from the source. |

### Empty Result

When there are no associated documents, the `<AssociatedDocuments>` element is empty:

```xml
<response success="true">
  <AssociatedDocuments />
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
GET /srv.asmx/AssociatedDocuments
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &ItemPath=/Finance/Reports/Q1-2024-Report.pdf
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/AssociatedDocuments HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&ItemPath=/Finance/Reports/Q1-2024-Report.pdf
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:AssociatedDocuments>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:ItemPath>/Finance/Reports/Q1-2024-Report.pdf</tns:ItemPath>
    </tns:AssociatedDocuments>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- **Source can be a document or folder**: `ItemPath` is first resolved as a document; if not found, it is resolved as a folder. The list of associated documents is returned for whichever is found.
- **Both directions are returned**: The result includes associations where the item is the source (`IsReverseAssociation="FALSE"`) and associations where the item is the target (`IsReverseAssociation="TRUE"`). Use the `IsReverseAssociation` attribute to distinguish the direction.
- **Only documents are returned**: This API returns associated documents only. To retrieve associated folders, use [AssociatedFolders](AssociatedFolders.md). To retrieve both together, use [AssociatedFoldersAndDocuments](AssociatedFoldersAndDocuments.md).
- **Unresolvable documents**: If an associated document has been deleted or is inaccessible, its `Path`, `Size`, and `DateModified` attributes are returned as empty strings. The `DocumentID` is still present.
- **No filtering by type**: All association types are returned. Filter on the `AssociationTypeID` or `AssociationTypeName` attribute in the response if you need a specific type.

---

## Related APIs

- [AssociateDocument](AssociateDocument.md) - Create an association from a document to another document or folder
- [AssociateFolder](AssociateFolder.md) - Create an association from a folder to another document or folder
- [AssociatedFolders](AssociatedFolders.md) - Get the list of folders associated with a document or folder
- [AssociatedFoldersAndDocuments](AssociatedFoldersAndDocuments.md) - Get all associated items (documents and folders) of a document or folder
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
