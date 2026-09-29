# GetFoldersAndDocumentsByPage API

Returns a page of documents and folders at the specified path, with optional name filtering for both folders and documents. Each page contains up to 20 items. Use `PageNumber` to navigate through large listings.

## Endpoint

```
/srv.asmx/GetFoldersAndDocumentsByPage
```

## Methods

- **GET** `/srv.asmx/GetFoldersAndDocumentsByPage?authenticationTicket=...&Path=...&FolderFilter=...&DocumentFilter=...&PageNumber=...`
- **POST** `/srv.asmx/GetFoldersAndDocumentsByPage` (form data)
- **SOAP** Action: `http://tempuri.org/GetFoldersAndDocumentsByPage`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the folder (e.g. `/Finance/Reports`). |
| `FolderFilter` | string | No | Name filter for subfolders. Matches the whole name unless it contains a `*`. One value only. Empty for no filtering. |
| `DocumentFilter` | string | No | Name filter for documents. Matches any part of the name unless it contains a `*`. Several may be given, separated by `;`. Empty for no filtering. |
| `PageNumber` | int | Yes | Page number to retrieve (1-based). Pass `-1` for every item in one response, with no `page` or `pageSize` on the root. |

---

## Response

### Success Response

Folders come back as `<f>` and documents as `<d>` - the same short-form elements
[GetFoldersAndDocuments1](GetFoldersAndDocuments1.md) returns, with `page` and `pageSize` added to the
root. They are **not** the `<folder>` / `<document>` elements
[GetFoldersAndDocuments](GetFoldersAndDocuments.md) returns. A page is filled with subfolders first, then documents.

```xml
<response success="true" error="" folderid="1170" parentid="1132" name="Reports"
          path="\Finance\Reports" folderfilter="" documentfilter="" page="1" pageSize="20"
          itemcount="4">
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

A folder with nothing to list is a success with `itemcount="0"` and no children. So is a page past the end.

### `<response>` attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `folderid` | integer | The id of the folder named by `Path`. |
| `parentid` | integer | That folder's parent id; `0` when `Path` names a library. |
| `name` | string | That folder's name. |
| `path` | string | That folder's full path, with backslashes (`\Library\Folder`). |
| `folderfilter` | string | The `FolderFilter` applied; empty for none. |
| `documentfilter` | string | The `DocumentFilter` applied; empty for none. |
| `page` | integer | The `PageNumber` requested. Not written when `PageNumber` is `-1`. |
| `pageSize` | integer | Items per page: the server's search page size setting (20 by default). Not written when `PageNumber` is `-1`. |
| `itemcount` | integer | The number of `<f>` and `<d>` elements in this response - **this page**, not the folder's total. |

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

The calling user must have **read** permission on the folder. Only accessible items are returned.

---

## Example

### GET Request (page 1, no filters)

```
GET /srv.asmx/GetFoldersAndDocumentsByPage
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports
  &FolderFilter=
  &DocumentFilter=
  &PageNumber=1
HTTP/1.1
```

### GET Request (page 2, filter for documents with "Q" in name)

```
GET /srv.asmx/GetFoldersAndDocumentsByPage
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports
  &FolderFilter=
  &DocumentFilter=Q
  &PageNumber=2
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetFoldersAndDocumentsByPage HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance/Reports
&FolderFilter=
&DocumentFilter=
&PageNumber=1
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetFoldersAndDocumentsByPage>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:Path>/Finance/Reports</tns:Path>
      <tns:FolderFilter></tns:FolderFilter>
      <tns:DocumentFilter></tns:DocumentFilter>
      <tns:PageNumber>1</tns:PageNumber>
    </tns:GetFoldersAndDocumentsByPage>
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

The same short `<f>` and `<d>` shape as `GetFoldersAndDocuments1`, with two name filters and a page
number. `itemcount` counts **this page**, not the whole folder.

`Path` is a non-nullable string on the REST action, so an empty one is refused by model binding with
HTTP 400 before the operation runs - there is no error document to read in that case.

### The two filters are not the same kind of filter

This is the thing about these operations most likely to catch a caller out. `*` is the only wildcard
either of them understands: a `%`, `_` or `?` in the value is ordinary text, not a pattern.

| | `FolderFilter` | `DocumentFilter` |
|---|---|---|
| With no `*` | matches the **whole name** - `Api` does not find `ApiTests` | matches **any part** of the name - `Api` finds `ApiTests.txt`, and so does `Tests` |
| With a `*` | `Api*` matches, `*` alone matches everything | `Api*` anchors it to the start, so the `%...%` wrap is not added |
| In `"double quotes"` | whole name, even if it contains a `*` | whole name |
| Several values | not supported - the whole string is one name | separate them with `;`, and a name matching any of them is returned |

Both are case-insensitive. Leave a filter empty to apply none.

```javascript
let page = 1;

for (;;) {
  const root = await call('GetFoldersAndDocumentsByPage', {
    authenticationTicket: ticket,
    Path: '/Public/ApiTests',
    FolderFilter: '',
    DocumentFilter: '*.pdf;*.docx',   // several patterns, any of which may match
    PageNumber: page
  });

  for (const d of root.querySelectorAll(':scope > d')) console.log(d.getAttribute('n'));

  if (Number(root.getAttribute('itemcount')) < Number(root.getAttribute('pageSize'))) break;
  page++;
}
```

A page past the end is a success with nothing in it, not an error, so a loop that stops on a short
page never needs to ask for the total first. Pass `PageNumber=-1` for everything in one answer, which
also drops `page` and `pageSize` from the root.

## Notes

- Returns only **direct** children (one level deep) of the specified path.
- Page size is set on the server and reported back as `pageSize`; it is not a parameter of this call.
- `FolderFilter` and `DocumentFilter` do **not** match the same way: without a `*` the folder filter wants the whole name and the document filter matches any part of it. See the table above.
- An empty response (no child elements) after page 1 means there are no matching items.
- For advanced filtering (by metadata, date ranges, or full-text content) and sorting, use `GetFoldersAndDocumentsByPage2`.
- For full property details per item, use `GetFoldersAndDocuments`.
- This paged API returns the short-form `<f>` / `<d>` elements. Extended attributes - property sets, security, rules, `UserViewStatus`, `AIEnhanced` - are not included. Use [GetFoldersAndDocuments](GetFoldersAndDocuments.md) for the full `<document>` element.

---

## Related APIs

- [GetFoldersAndDocuments2](GetFoldersAndDocuments2.md) - Lightweight listing without paging
- [GetFoldersAndDocumentsByPage2](GetFoldersAndDocumentsByPage2.md) - Advanced paged listing with XML filters and sorting
- [GetFoldersByPage](GetFoldersByPage.md) - Paged listing of folders only

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
| Folder not found | The specified path does not resolve to an existing folder. |
| Access denied | The user does not have read permission on the folder. |
| `SystemError:...` | An unexpected server-side error occurred. |

---