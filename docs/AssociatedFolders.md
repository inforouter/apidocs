# AssociatedFolders API

Returns the list of folders that are associated with the specified document or folder. Both forward associations (where the specified item is the source) and reverse associations (where the specified item is the target) are returned. Use this API to discover all folders linked to a document or folder, regardless of which side created the association.

> **Note:** All folder associations are always of type `Related` (0). Typed associations (Rendition, Copy, ParentChild, Derivation) are only possible between two documents. See [AssociateDocument](AssociateDocument.md) for details.

## Endpoint

```
/srv.asmx/AssociatedFolders
```

## Methods

- **GET** `/srv.asmx/AssociatedFolders?AuthenticationTicket=...&ItemPath=...`
- **POST** `/srv.asmx/AssociatedFolders` (form data)
- **SOAP** Action: `http://tempuri.org/AssociatedFolders`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `ItemPath` | string | Yes | Full infoRouter path to the source document or folder whose associated folders are to be retrieved (e.g. `/Finance/Reports` or `/Finance/Reports/Q1-Report.pdf`). |

---

## Response

### Success Response

The response contains a `<response success="true">` root element with an `<AssociatedFolders>` child element containing one `<AssociatedFolder>` element per associated folder. Both forward and reverse association directions are included.

```xml
<response success="true">
  <AssociatedFolders>
    <AssociatedFolder
        IsReverseAssociation="FALSE"
        AssociationTypeID="0"
        AssociationTypeName="Related"
        FolderID="42"
        Path="/Finance/Archive/2023-Reports">
      <!-- full folder properties -->
    </AssociatedFolder>
    <AssociatedFolder
        IsReverseAssociation="TRUE"
        AssociationTypeID="0"
        AssociationTypeName="Related"
        FolderID="87"
        Path="/HR/Shared">
      <!-- full folder properties -->
    </AssociatedFolder>
  </AssociatedFolders>
</response>
```

### AssociatedFolder Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `IsReverseAssociation` | string | `TRUE` if the specified item is the target of this association (i.e. another item associated to it); `FALSE` if the specified item is the source. |
| `AssociationTypeID` | int | Numeric association type. Always `0` (Related) for folder associations. |
| `AssociationTypeName` | string | Localised display name of the association type. Always `Related` for folder associations. |
| `FolderID` | int | Internal numeric ID of the associated folder. |
| `Path` | string | Full infoRouter path of the associated folder. Empty if the folder cannot be resolved. |

### Empty Result

When there are no associated folders, the `<AssociatedFolders>` element is empty:

```xml
<response success="true">
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
GET /srv.asmx/AssociatedFolders
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &ItemPath=/Finance/Reports
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/AssociatedFolders HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&ItemPath=/Finance/Reports
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:AssociatedFolders>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:ItemPath>/Finance/Reports</tns:ItemPath>
    </tns:AssociatedFolders>
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

The folder half of [AssociatedDocuments](AssociatedDocuments.md), with the same shape.

```javascript
const root = await call('AssociatedFolders', {
  authenticationTicket: ticket, ItemPath: '/Finance/Invoices/inv-1001.pdf'
});

for (const link of root.querySelectorAll('AssociatedFolder')) {
  console.log(link.getAttribute('AssociationTypeName'),
              link.querySelector('folder').getAttribute('Path'));
}
```

The link's own `Path` attribute is written with forward slashes here and with doubled separators on
`AssociatedDocument` - a third spelling again from the nested `<folder>` element, which uses
backslashes. Read the nested element.

## Notes

- **Source can be a document or folder**: `ItemPath` is first resolved as a document; if not found, it is resolved as a folder. The list of associated folders is returned for whichever is found.
- **Both directions are returned**: The result includes associations where the item is the source (`IsReverseAssociation="FALSE"`) and associations where the item is the target (`IsReverseAssociation="TRUE"`). Use the `IsReverseAssociation` attribute to distinguish the direction.
- **Association type is always Related**: Folder associations are always stored as `Related` (0). The `AssociationTypeID` attribute will always be `0` and `AssociationTypeName` will always be `Related`.
- **Only folders are returned**: This API returns associated folders only. To retrieve associated documents, use [AssociatedDocuments](AssociatedDocuments.md). To retrieve both together, use [AssociatedFoldersAndDocuments](AssociatedFoldersAndDocuments.md).
- **Unresolvable folders**: If an associated folder has been deleted or is inaccessible, the `Path` attribute is returned as an empty string. The `FolderID` is still present.
- **No filtering**: All associated folders are returned. Use the `FolderID` or `Path` attribute to identify specific folders.

---

## Related APIs

- [AssociateDocument](AssociateDocument.md) - Create an association from a document to another document or folder
- [AssociateFolder](AssociateFolder.md) - Create an association from a folder to another document or folder
- [AssociatedDocuments](AssociatedDocuments.md) - Get the list of documents associated with a document or folder
- [AssociatedFoldersAndDocuments](AssociatedFoldersAndDocuments.md) - Get all associated items (documents and folders) of a document or folder
- [AssociationTypes](AssociationTypes.md) - Get the list of configured association types
- [RemoveAssociation](RemoveAssociation.md) - Remove an existing association between two items

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | nothing at that path |
| `4030` | the caller may not see it |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
