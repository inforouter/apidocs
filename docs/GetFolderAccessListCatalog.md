# GetFolderAccessListCatalog API

Lists the subfolders and documents under a folder that hold an access list of their own, each with counts of what inherits from it. These are the places where [SetAccessList](SetAccessList.md) with `ApplyToTree=true` would overwrite something. [GetFolderAccessListStatistics](GetFolderAccessListStatistics.md) gives the totals for the warning; this call shows the user which items the totals are made of, so they can decide before applying.

Items that merely inherit are not listed. They are counted on the node they inherit from, so on a tree of 10,000 folders and 100,000 documents the answer holds a few hundred nodes at most: nodes exist only where someone set a list.

## Endpoint

```
/srv.asmx/GetFolderAccessListCatalog
```

## Methods

- **GET** `/srv.asmx/GetFolderAccessListCatalog?authenticationTicket=...&folderPath=...&depth=1&includeDocuments=true`
- **POST** `/srv.asmx/GetFolderAccessListCatalog` (form data)
- **SOAP** Action: `http://tempuri.org/GetFolderAccessListCatalog`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `folderPath` | string | Yes | Full infoRouter path of the folder (e.g. `/Finance/Contracts`), or `~F` followed by the folder id (e.g. `~F2417`). |
| `depth` | int | No | Default `1`: only the nearest items below the folder whose list differs; nothing is listed below them. `0`: every level. `2`, `3`, ...: that many list levels down. Over SOAP the parameter is required; pass `1` for the default. |
| `includeDocuments` | bool | No | Default `true`. With `false` no `<document>` nodes are listed; the document counts on folders stay. Over SOAP the parameter is required. |

---

## Response

### Success Response

```xml
<response success="true" error="">
  <catalog id="2417" name="Contracts" path="/Finance/Contracts" parentId="2400" level="0"
           subFolderCount="58" documentCount="1930" inheritedFolderCount="29" inheritedDocumentCount="1510"
           depth="0" includeDocuments="true" nodeCount="4" truncated="false">
    <folder id="2551" name="Legal" path="/Finance/Contracts/Legal" parentId="2417" level="1"
            subFolderCount="12" documentCount="305" inheritedFolderCount="11" inheritedDocumentCount="210" />
    <folder id="2590" name="Archive" path="/Finance/Contracts/Legal/Archive" parentId="2551" level="2"
            subFolderCount="0" documentCount="95" inheritedFolderCount="0" inheritedDocumentCount="95" />
    <document id="88120" name="NDA-template.docx" path="/Finance/Contracts/NDA-template.docx" parentId="2417" level="1" />
    <folder id="2602" name="Vendors" path="/Finance/Contracts/Vendors" parentId="2588" level="1"
            subFolderCount="15" documentCount="110" inheritedFolderCount="15" inheritedDocumentCount="110" />
  </catalog>
</response>
```

`<catalog>` is the folder that was asked about, with the counts of its whole tree. Its children are a **flat** list of the nodes below it, in path order, folders and documents together.

### What is a node

A folder or document whose access list is not its parent's. Only the identity of the list is compared, never its rights: a folder whose list was typed in to equal its parent's is still a node, and shows `InheritedSecurity="false"` in [GetAccessList](GetAccessList.md). [ApplyInheritedAccessList](ApplyInheritedAccessList.md) makes such an item inherit again.

### `<catalog>` and `<folder>` attributes

| Attribute | Description |
|---|---|
| `id`, `name`, `path` | The folder, its name and its full path. |
| `parentId` | The real parent folder. For a node this may be an inheriting folder that is not in the answer; `0` for a library root. |
| `level` | How many lists lie between the asked folder and this one: `0` for the asked folder, `1` for the nearest nodes below it, and so on. |
| `subFolderCount`, `documentCount` | Everything below this folder, at every depth. This is what `ApplyToTree=true` overwrites from here down. |
| `inheritedFolderCount`, `inheritedDocumentCount` | Of those, the items that hold this folder's own list. The rest hold other lists and are nodes beneath it, unless `depth` cut them off. |
| `depth`, `includeDocuments` | `<catalog>` only. The parameters the answer was built with. |
| `nodeCount` | `<catalog>` only. The number of `<folder>` and `<document>` children. |
| `truncated` | `<catalog>` only. `true` when the server stopped at 10,000 nodes. The counts are still complete. |

### `<document>` attributes

`id`, `name`, `path`, `parentId` (its folder) and `level`. A document carries no counts.

### Nesting follows lists, not folders

A node's `level` is one more than the nearest node above it, and the inheriting folders in between are not in the answer. In the example, Vendors has `level="1"` and `parentId="2588"`: its real parent is an inheriting folder two levels below Contracts, and that folder is not listed. The folders a node is counted on can always be found from `path`.

Within the list, nodes are ordered by `path`, ignoring case, so a folder node comes before the nodes beneath it. Items in the recycle bin are not listed or counted, as in the statistics call.

### How it matches GetFolderAccessListStatistics

On the same folder, at the same moment:

```
SubFoldersNotInherited = subFolderCount - inheritedFolderCount    (on <catalog>)   -> 58 - 29     = 29
DocumentsNotInherited  = documentCount  - inheritedDocumentCount  (on <catalog>)   -> 1930 - 1510 = 420
```

With `depth=0`, the nodes account for those numbers exactly: each `<folder>` node counts as itself plus its `inheritedFolderCount`, and each `<folder>` node's `inheritedDocumentCount` plus one per `<document>` node adds up to `DocumentsNotInherited`. On any `<folder>` node, `subFolderCount - inheritedFolderCount` is the number of folders listed or counted beneath it.

### Error Response

```xml
<response success="false" error="Folder path not found." errorCode="4041" />
```

---

## Required Permissions

The calling user must be allowed to **change the security** of the folder, the same right [SetAccessList](SetAccessList.md) and [GetFolderAccessListStatistics](GetFolderAccessListStatistics.md) ask for. Nothing is filtered by read right: the nodes are the items the caller could overwrite, and they are listed whether or not the caller may open them.

---

## Example

### GET Request

```
GET /srv.asmx/GetFolderAccessListCatalog
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &folderPath=/Finance/Contracts
  &depth=0
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetFolderAccessListCatalog HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&folderPath=/Finance/Contracts
&depth=1
&includeDocuments=true
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetFolderAccessListCatalog>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:folderPath>/Finance/Contracts</tns:folderPath>
      <tns:depth>1</tns:depth>
      <tns:includeDocuments>true</tns:includeDocuments>
    </tns:GetFolderAccessListCatalog>
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

Show the user what the warning from GetFolderAccessListStatistics is made of, before applying to the tree.

```javascript
const root = await call('GetFolderAccessListCatalog', {
  authenticationTicket: ticket,
  folderPath: '/Finance/Contracts',
  depth: 1
});

const catalog = root.querySelector('catalog');
const n = (el, name) => Number(el.getAttribute(name));

const lines = [...catalog.children].map(node => {
  if (node.tagName === 'document') {
    return `${node.getAttribute('path')} (document with its own security)`;
  }
  const below = `${n(node, 'subFolderCount')} folders and ${n(node, 'documentCount')} documents below it`;
  const other = n(node, 'subFolderCount') - n(node, 'inheritedFolderCount')
              + n(node, 'documentCount') - n(node, 'inheritedDocumentCount');
  return `${node.getAttribute('path')} (own security; ${below}` +
         (other > 0 ? `, ${other} of them with yet another list)` : ')');
});

if (catalog.getAttribute('truncated') === 'true') {
  lines.push('... and more; narrow the folder');
}

const notInherited = n(catalog, 'subFolderCount') - n(catalog, 'inheritedFolderCount')
                   + n(catalog, 'documentCount') - n(catalog, 'inheritedDocumentCount');
const applyToTree = confirm(
  `Applying to the tree replaces the security of ${notInherited} items:\n\n${lines.join('\n')}\n\nContinue?`
);
```

## Notes

- `depth` and `includeDocuments` change the size of the answer, not the time it takes: the server reads the tree's folders in one query and only the documents with a list of their own in another, whatever the depth, then runs two small counts per folder node it lists.
- No paging. The answer stops at 10,000 nodes with `truncated="true"`; ask with `depth=1`, with `includeDocuments=false`, or on a lower folder. A tree reaches that many nodes only when lists were set on thousands of items.
- The answer is a snapshot: a list set or removed between this call and `SetAccessList` changes the tree. Re-call rather than cache.
- Shortcuts (`.lnk` documents) are documents here, as everywhere else.
- A document path is answered `4041`; a document has no tree.

---

## Related APIs

- [GetFolderAccessListStatistics](GetFolderAccessListStatistics.md) - The totals: how many items below a folder do not carry its access list
- [SetAccessList](SetAccessList.md) - Set the access list, optionally on the whole tree
- [GetAccessList](GetAccessList.md) - Get the access list of one document or folder
- [ApplyInheritedAccessList](ApplyInheritedAccessList.md) - Put an item back to inheriting from its parent
- [GetFolderCatalog](GetFolderCatalog.md) - The whole tree, every folder and document

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4000` | `depth` is negative |
| `4010` | the ticket is missing, expired or unknown |
| `4030` | the caller may not change the folder's security |
| `4041` | no folder at that path, or the path is a document |
| `HTTP 400` | `folderPath` was empty; refused by model binding, so there is no error document |

---
