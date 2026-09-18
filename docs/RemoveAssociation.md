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
<response success="true" error="" errorCode="0" />
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

Removes a link. There is one link, seen from two sides, so removing it from either end removes it
from both.

```javascript
// From the item the link was made on:
await call('RemoveAssociation', {
  authenticationTicket: ticket,
  ItemPath: '/Finance/Invoices/inv-1001.pdf',
  AssociationWith_ItemPath: '/Finance/Purchase orders/po-1001.pdf',
  IsReverseAssociation: false
});

// From the item it points at - same link, the flag turned round:
await call('RemoveAssociation', {
  authenticationTicket: ticket,
  ItemPath: '/Finance/Purchase orders/po-1001.pdf',
  AssociationWith_ItemPath: '/Finance/Invoices/inv-1001.pdf',
  IsReverseAssociation: true
});
```

`IsReverseAssociation` says which end `ItemPath` is - it is the value the readers put on the link.

Removing a link that was never made is a **success**, so the answer says nothing about whether
anything was there.

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

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | nothing at `ItemPath` |
| `4030` | the caller may not change it |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
