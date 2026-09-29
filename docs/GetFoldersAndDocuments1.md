# GetFoldersAndDocuments1 API

Returns the immediate sub-folders and documents in the specified infoRouter path in **short form**. This is a lightweight, high-performance variant of `GetFoldersAndDocuments` that uses abbreviated element names and a minimal attribute set. Folder items contain only their ID and name; document items contain a small set of essential fields. No optional enrichment flags are available -" use `GetFoldersAndDocuments` when full document or folder metadata is required.

## Endpoint

```

/srv.asmx/GetFoldersAndDocuments1

```

## Methods

- **GET** `/srv.asmx/GetFoldersAndDocuments1?authenticationTicket=...&Path=...`

- **POST** `/srv.asmx/GetFoldersAndDocuments1` (form data)

- **SOAP** Action: `http://tempuri.org/GetFoldersAndDocuments1`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the parent folder whose contents to list (e.g. `/Finance/Reports`). Must point to an existing folder the user can access. |

---

## Response

### Success Response

The root is `<response>` and describes the folder that was read. Subfolders come first as `<f>` elements, then documents as `<d>` elements.

```xml
<response success="true" error="" folderid="1170" parentid="1132" name="Reports"
          path="\Finance\Reports" folderfilter="" documentfilter="" itemcount="4">
  <f id="1171" n="2024" />
  <f id="1172" n="2023" />
  <d id="1051" n="Q1-Report.pdf" mdate="2024-06-15T14:30:00.000Z" cdate="2024-03-01T09:00:00.000Z"
     size="204800" dformat="PDF Document" chkoutbyusername="" chkoutbyfullname=""
     version="3000000" publishedversion="3000000" regdate="2024-03-01T09:00:00.000Z" dtype="0" />
  <d id="1052" n="Budget.docx" mdate="2024-05-20T08:15:00.000Z" cdate="2024-01-10T10:00:00.000Z"
     size="98304" dformat="Office Document" chkoutbyusername="jsmith" chkoutbyfullname="John Smith"
     version="2000000" publishedversion="1000000" regdate="2024-01-10T10:00:00.000Z" dtype="5" />
</response>
```

A folder with nothing to list is a success with `itemcount="0"` and no children.

### `<response>` attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `folderid` | integer | The id of the folder named by `Path`. |
| `parentid` | integer | That folder's parent id; `0` when `Path` names a library. |
| `name` | string | That folder's name. |
| `path` | string | That folder's full path, with backslashes (`\Library\Folder`). |
| `folderfilter` | string | The folder name filter applied - always empty, this call takes none. |
| `documentfilter` | string | The document name filter applied - always empty, this call takes none. |
| `itemcount` | integer | The number of `<f>` and `<d>` elements in this response. |

### `<f>` attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | integer | The subfolder's id. |
| `n` | string | The subfolder's name. |

### `<d>` attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | integer | The document's id. |
| `n` | string | The document's name, with its extension. |
| `mdate` | datetime (UTC) | When the document was last modified. |
| `cdate` | datetime (UTC) | When the document was created. |
| `size` | integer | The document's size in bytes. |
| `dformat` | string | The description of its file format, looked up from the extension (e.g. `PDF Document`, `Internet Document`) - the value [GetDocument](GetDocument.md) reports as `Type`. |
| `chkoutbyusername` | string | Login name of the user who has the document checked out; empty if it is not checked out. `~U` and the user id if that user can no longer be read. |
| `chkoutbyfullname` | string | That user's full name; empty if it is not checked out. |
| `version` | integer | The latest version, in the large-integer scheme where version 1 is `1000000` (`VersionNumber` in GetDocument). |
| `publishedversion` | integer | The published version, in the same scheme; `0` if no version is published (`PublishedVersionNumber`). |
| `regdate` | datetime (UTC) | When the document was registered - first added to infoRouter (`RegisterDate`). |
| `dtype` | integer | The id of the document type assigned to it; `0` if none (`DocTypeID`). |

Dates are written in universal format, `yyyy-MM-ddTHH:mm:ss.fffZ`.

### Error Response

No folder at `Path`, including one the caller may not see:

```xml
<response success="false" error="Target folder cannot be found." errorCode="4041" />
```

A refusal raised while the folder's contents are being read - the caller not being allowed to list it -
carries no `errorCode`:

```xml
<response success="false" error="..." />
```

---

## Required Permissions

The calling user must have at least **List** permission on the specified folder. Documents and sub-folders to which the user has no access are automatically excluded from the response. Read-only users may call this API.

---

## Example

### GET Request

```

GET /srv.asmx/GetFoldersAndDocuments1?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

  &Path=/Finance/Reports

HTTP/1.1

```

### POST Request

```

POST /srv.asmx/GetFoldersAndDocuments1 HTTP/1.1

Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301&Path=/Finance/Reports

```

### SOAP Request

```xml

<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"

               xmlns:tns="http://tempuri.org/">

  <soap:Body>

    <tns:GetFoldersAndDocuments1>

      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>

      <tns:Path>/Finance/Reports</tns:Path>

    </tns:GetFoldersAndDocuments1>

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

Lists the folders and documents directly inside one folder in the short shape: `<f>` for each
subfolder and `<d>` for each document, with a handful of attributes each. The root says which folder
was read and how many items are below it.

`Path` is a non-nullable string on the REST action, so an empty one is refused by model binding with
HTTP 400 before the operation runs - there is no error document to read in that case.

```javascript
const root = await call('GetFoldersAndDocuments1', {
  authenticationTicket: ticket,
  Path: '/Public/ApiTests'
});

console.log(root.getAttribute('name'), root.getAttribute('itemcount'));

for (const f of root.querySelectorAll(':scope > f')) console.log('[dir]', f.getAttribute('n'));
for (const d of root.querySelectorAll(':scope > d')) console.log('     ', d.getAttribute('n'), d.getAttribute('size'));
```

This is `GetFoldersAndDocumentsByPage` with no filters and no paging - the whole folder in one
answer. The root still carries the empty `folderfilter` and `documentfilter` it applied, but no
`page` or `pageSize`.

## Notes

- The listing is **not recursive** -" only the immediate children (sub-folders and documents) of the specified `Path` are returned.

- The root element is `<response>`, not `<root>`, which differs from most other infoRouter APIs. Parse the response accordingly.

- Folder items use the abbreviated element name `<f>` and carry only `id` and `n` (name). To retrieve full folder metadata, use `GetFolder` or `GetFoldersAndDocuments`.

- This API returns the short-form `<f>` / `<d>` elements. Extended attributes - property sets, security, rules, `UserViewStatus`, `AIEnhanced` - are not included. Use [GetFoldersAndDocuments](GetFoldersAndDocuments.md) for the full `<document>` element.

- Document items use the abbreviated element name `<d>` and carry a minimal attribute set. To retrieve full document metadata, use `GetDocument` or `GetFoldersAndDocuments`.

- All items are returned in a single response with no paging. For large folders with hundreds of items, consider `GetFoldersAndDocumentsByPage` or `GetFoldersAndDocumentsByPage2` to page through results.

- Folders appear before documents in the response.

- The `Path` parameter is case-insensitive and leading/trailing slashes are normalized automatically.

- If the path does not exist or the user has no access to it, an error response is returned (the `error` attribute is set on the `<response>` element and `success="false"`).

- Dates are in universal format (UTC), e.g. `2024-06-15T14:30:00.000Z`.

- This API is significantly faster than `GetFoldersAndDocuments` for large folders because it avoids loading full document and folder objects. Use it when only identity, name, size, date, or checkout information is needed.

---

## Related APIs

- [GetFoldersAndDocuments](GetFoldersAndDocuments.md) - Full-detail listing with optional property sets, security, owner, and version history

- [GetFoldersAndDocumentsByPage](GetFoldersAndDocumentsByPage.md) - Paged listing (first page, up to 20 items) of folder contents

- [GetFoldersAndDocumentsByPage2](GetFoldersAndDocumentsByPage2.md) - Paged listing in enhanced form

- [GetFolders](GetFolders.md) - Returns only the sub-folders of the specified path

- [GetDocuments](GetDocuments.md) - Returns only the documents in the specified path

- [GetDocument](GetDocument.md) - Returns full metadata for a single document by path

- [Search](Search.md) - Find documents and folders across the system using search criteria

---

A missing folder answers `4041`, as `GetFoldersAndDocuments`, `GetFoldersAndDocuments2` and
`GetFoldersAndDocumentsByPage2` do.

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4041` | no folder at that path, including one the caller may not see |
| none | a refusal raised while the folder's contents are read, such as the caller not being allowed to list it; the error document has no `errorCode` attribute |
| `HTTP 400` | `Path` was empty; refused by model binding, so there is no error document |

A call with no ticket at all is not automatically refused: it signs in as the anonymous user, so a
library flagged as anonymous can be listed without authenticating. Everything else answers `4041`,
because a folder the anonymous user cannot see is not told apart from one that does not exist.

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Folder not found` | The specified `Path` does not exist or is not accessible to the calling user. |

---

