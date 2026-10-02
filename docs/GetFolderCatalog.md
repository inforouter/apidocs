# GetFolderCatalog API

Builds a catalog of a folder: every subfolder at every depth, and every document in each of them. Each document carries its size, modification date and the checksums of its published and latest versions, so a client can tell which files have changed since it last looked. This is the call a synchronisation client uses. To show a folder in a UI, use the listings compared under [Compared with GetFolders and GetDocuments](#compared-with-getfolders-and-getdocuments).

> **Warning: large folders. Check the size first.**
>
> The whole catalog is built in one request. The server walks the entire tree, looks up two checksums for every document and holds the complete response in memory before sending any of it. On a large tree the call can run for many minutes, puts a sustained load on the database and the server while it runs, and can fail outright if the request times out or the server runs short of memory.
>
> Before calling it, call [GetFolderStatistics](GetFolderStatistics.md) on the same folder and add `SubFolderCount` and `TotalDocumentCount`; both cover the whole tree.
>
> | Folders + documents | Advice |
> |---|---|
> | up to about 10,000 | Call it when needed. |
> | more than about 10,000 | Call it outside business hours, or catalog the subfolders one at a time instead of the whole tree at once. |
>
> 10,000 is a guideline, not a limit the server enforces: what is safe depends on the server's hardware and on how busy it is. Time a call on a folder of known size on your own server and adjust the threshold from that. The statistics count everything in the tree, including what the caller cannot see, so the total is an upper bound on what the catalog returns.

## Endpoint

```
/srv.asmx/GetFolderCatalog
```

## Methods

- **GET** `/srv.asmx/GetFolderCatalog?authenticationTicket=...&folderPath=...`
- **POST** `/srv.asmx/GetFolderCatalog` (form data)
- **SOAP** Action: `http://tempuri.org/GetFolderCatalog`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | No | Authentication ticket obtained from `AuthenticateUser`. Without one the call runs as the anonymous user. |
| `folderPath` | string | Yes | Full infoRouter path to the folder (e.g. `/Finance/Reports`), or `~F` followed by the folder id (e.g. `~F1170`). |

---

## Response

### Success Response

```xml
<response success="true" error="">
  <folder id="167230" name="Reports">
    <document id="97196" name="page.htm" mdate="2026-10-01T10:31:17.960Z" Size="231" chksum="5E707270" chksumLastVersion="5E707270" />
    <folder id="167231" name="Sub">
      <document id="97197" name="page.htm" mdate="2026-10-01T10:31:18.200Z" Size="231" chksum="5E707270" chksumLastVersion="5E707270" />
      <folder id="167232" name="Deeper" />
    </folder>
  </folder>
</response>
```

`<response>` holds one `<folder>`: the folder named in `folderPath`. Every `<folder>` holds its own documents first, sorted by name, and then its subfolders, each nested the same way. An empty folder is an empty `<folder/>` element. There is no depth limit and no paging.

### `<folder>` attributes

| Attribute | Type | Description |
|---|---|---|
| `id` | integer | The folder's id. |
| `name` | string | The folder's name only, not its path. Build a path by joining the names of the enclosing `<folder>` elements. |

### `<document>` attributes

| Attribute | Type | Description |
|---|---|---|
| `id` | integer | The document's id. |
| `name` | string | The document's name. |
| `mdate` | datetime (UTC) | When the document was last modified. |
| `Size` | integer | The size in bytes. The capital `S` is how the server writes it. |
| `chksum` | string | The checksum of the **published** version, as 8 hex digits. Empty if the document has no published version. |
| `chksumLastVersion` | string | The checksum of the **latest** version, which differs from `chksum` while a newer version is unpublished. |

If a checksum cannot be read, for example because the document is marked offline, the attribute holds `N/A Error:` followed by the reason instead of a checksum. The rest of the tree is still returned.

### Error Response

```xml
<response success="false" error="Folder path not found." errorCode="4041" />
```

---

## Compared with GetFolders and GetDocuments

The catalog is written in its own format, different from both listing formats:

| | GetFolderCatalog | GetFolders, GetFolder, GetMyDocumentsAndFolders | GetFolders1/2, GetFoldersAndDocuments1, GetDocuments1, …ByPage |
|---|---|---|---|
| Depth | The whole tree, nested | One level | One level |
| Folder element | `<folder id name>` | `<folder FolderID ParentID Name Path …>` (16 attributes) | `<f id n>` |
| Document element | `<document id name mdate Size chksum chksumLastVersion>` | — | `<d id n mdate cdate size dformat version …>` |
| Attribute case | lowercase, except `Size` | PascalCase | lowercase |
| Paths | none; built from the nesting | `Path` on each folder | the parent's `path` on `<response>` |
| Checksums | yes | no | no |
| Paging and filters | no | no | yes |

So the catalog cannot be read with code written for the listings: the attribute names differ (`name` not `n` or `Name`, `id` not `FolderID`), and folders are nested rather than flat. It has fewer details per item than the listings (no creation date, format, version numbers, owner or check-out state) and adds the two checksums.

---

## Required Permissions

The caller sees only what they may read. Subfolders they cannot see are left out, and so are the documents of any folder whose contents they may not list. Nothing in the response says that something was left out. The folder named in `folderPath` must be readable, or the call answers `4041`.

---

## Example

### GET Request

```
GET /srv.asmx/GetFolderCatalog
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &folderPath=/Finance/Reports
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetFolderCatalog HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&folderPath=/Finance/Reports
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetFolderCatalog>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:folderPath>/Finance/Reports</tns:folderPath>
    </tns:GetFolderCatalog>
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

Walk the tree, building each document's path from the folder names above it:

```javascript
const root = await call('GetFolderCatalog', {
  authenticationTicket: ticket,
  folderPath: '/Finance/Reports'
});

(function walk(folder, prefix) {
  for (const document of folder.querySelectorAll(':scope > document')) {
    console.log(prefix + document.getAttribute('name'), document.getAttribute('chksum'));
  }
  for (const child of folder.querySelectorAll(':scope > folder')) {
    walk(child, prefix + child.getAttribute('name') + '/');
  }
})(root.querySelector('folder'), '');
```

## Notes

- On a large tree the call is slow and the response is large; see the warning at the top of this page. To browse a folder, use [GetFoldersAndDocumentsByPage](GetFoldersAndDocumentsByPage.md) one folder at a time.
- A checksum that has never been stored is calculated from the file when it is first asked for, which makes the first call over old documents slower still.

---

## Related APIs

- [GetFolder](GetFolder.md) - Get one folder's metadata and properties
- [GetFoldersAndDocumentsByPage](GetFoldersAndDocumentsByPage.md) - List one folder's contents, a page at a time
- [GetFolderStatistics](GetFolderStatistics.md) - Count the folders and documents in a tree

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4041` | the path does not name a folder - including a path that names a document, and one the caller may not see |
| `HTTP 400` | `folderPath` was empty; refused by model binding, so there is no error document |

A call with no ticket is not refused: it runs as the anonymous user, so a folder in a library that
allows anonymous access can be read without signing in.
