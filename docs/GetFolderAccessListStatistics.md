# GetFolderAccessListStatistics API

Counts the subfolders and documents under a folder whose access list is not the folder's own. These are the items that [SetAccessList](SetAccessList.md) with `ApplyToTree=true` overwrites, so a client can warn the user before applying a folder's security to its whole tree.

## Endpoint

```
/srv.asmx/GetFolderAccessListStatistics
```

## Methods

- **GET** `/srv.asmx/GetFolderAccessListStatistics?authenticationTicket=...&folderPath=...`
- **POST** `/srv.asmx/GetFolderAccessListStatistics` (form data)
- **SOAP** Action: `http://tempuri.org/GetFolderAccessListStatistics`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `folderPath` | string | Yes | Full infoRouter path of the folder whose tree is counted (e.g. `/Finance/Contracts`). |

---

## Response

### Success Response

```xml
<response success="true" error="">
  <statistics FolderID="2417" Name="Contracts"
              SubFolderCount="58" SubFoldersNotInherited="12"
              DocumentCount="1930" DocumentsNotInherited="340" />
</response>
```

### Error Response

```xml
<response success="false" error="Path not found." errorCode="4041" />
```

### Statistics Attributes

| Attribute | Description |
|-----------|-------------|
| `FolderID` | Internal ID of the folder. |
| `Name` | Name of the folder. |
| `SubFolderCount` | Number of subfolders at every depth below the folder. |
| `SubFoldersNotInherited` | Of those, the subfolders whose access list is not this folder's. |
| `DocumentCount` | Number of documents in the folder and all subfolders. |
| `DocumentsNotInherited` | Of those, the documents whose access list is not this folder's. |

---

## What "not inherited" means

An item is counted as not inherited when the access list it carries is a different one from the given folder's. That covers two cases:

- the item was given an access list of its own;
- the item inherits from a subfolder that was given one. A subfolder with its own list takes everything below it out of the given folder's list.

So the numbers are measured against the folder that was asked about, not against each item's direct parent. In [GetAccessList](GetAccessList.md), `InheritedSecurity` compares an item with its direct parent; a document that reports `InheritedSecurity="true"` there is still counted here when its folder has a list of its own.

Items in the recycle bin are not part of the tree and are not counted.

---

## Required Permissions

The calling user must be allowed to **change the security** of the folder, the same right [SetAccessList](SetAccessList.md) asks for. The counts include subfolders and documents the caller may not be able to see.

---

## Example

### GET Request

```
GET /srv.asmx/GetFolderAccessListStatistics
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &folderPath=/Finance/Contracts
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetFolderAccessListStatistics HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&folderPath=/Finance/Contracts
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetFolderAccessListStatistics>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:folderPath>/Finance/Contracts</tns:folderPath>
    </tns:GetFolderAccessListStatistics>
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

Ask before applying a folder's access list to its tree.

```javascript
const root = await call('GetFolderAccessListStatistics', {
  authenticationTicket: ticket,
  folderPath: '/Finance/Contracts'
});

const statistics = root.querySelector('statistics');
const folders = Number(statistics.getAttribute('SubFoldersNotInherited'));
const documents = Number(statistics.getAttribute('DocumentsNotInherited'));

let applyToTree = true;
if (folders > 0 || documents > 0) {
  applyToTree = confirm(
    `${folders} folders and ${documents} documents below this folder have different security. ` +
    'Replace it with this folder\'s?'
  );
}
```

## Notes

- Every count covers the whole tree below the folder, not just its direct children.
- When both not-inherited numbers are `0`, `ApplyToTree=true` and `ApplyToTree=false` change the same items.
- The numbers are a snapshot: another user can change an access list between this call and `SetAccessList`.
- A document path is answered `4041`; a document has no tree.

---

## Related APIs

- [SetAccessList](SetAccessList.md) - Set the access list, optionally on the whole tree
- [GetAccessList](GetAccessList.md) - Get the access list of one document or folder
- [ApplyInheritedAccessList](ApplyInheritedAccessList.md) - Put an item back to inheriting from its parent
- [GetFolderStatistics](GetFolderStatistics.md) - Count the subfolders and documents of a folder

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is missing, expired or unknown |
| `4041` | no folder at that path, or the path is a document |
| `HTTP 400` | `folderPath` was empty; refused by model binding, so there is no error document |

A signed-in user who may not change the folder's security is refused as well.

---
