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

The root element is `<response>` (not `<root>`). It carries metadata about the queried folder as attributes. Folder items are returned as `<f>` child elements; document items as `<d>` child elements. Both item types use short, abbreviated attribute names. Folders appear before documents.

```xml

<response success="true"

          error=""

          folderid="10"

          parentid="3"

          name="Reports"

          path="/Finance/Reports"

          folderfilter=""

          documentfilter=""

          itemcount="5">

  <!-- Folder items -" id and name only -->

  <f id="42" n="Q1 Reports" />

  <f id="43" n="Q2 Reports" />

  <f id="44" n="Q3 Reports" />

  <!-- Document items -" abbreviated attribute set -->

  <d id="1051"

     n="Annual-Summary-2024.pdf"

     mdate="2024-06-15"

     cdate="2024-03-01"

     size="204800"

     dformat="PDF Document"

     chkoutbyusername=""

     chkoutbyfullname=""

     version="3"

     publishedversion="3"

     regdate="2024-03-01"

     dtype="0" />

  <d id="1052"

     n="Budget-2024.xlsx"

     mdate="2024-05-20"

     cdate="2024-01-10"

     size="98304"

     dformat="Microsoft Excel Spreadsheet"

     chkoutbyusername="jsmith"

     chkoutbyfullname="John Smith"

     version="2"

     publishedversion="0"

     regdate="2024-01-10"

     dtype="0" />

</response>

```

### Root Element (`<response>`) Attributes

| Attribute | Description |
|-----------|-------------|
| `success` | `true` if the request succeeded. |
| `error` | Error message if `success` is `false`; otherwise empty. |
| `folderid` | Integer ID of the queried folder (the folder at `Path`). |
| `parentid` | Integer ID of the queried folder's parent. |
| `name` | Name of the queried folder. |
| `path` | Full infoRouter path of the queried folder. |
| `folderfilter` | The folder name filter applied (empty string -" no filter for this API). |
| `documentfilter` | The document name filter applied (empty string -" no filter for this API). |
| `itemcount` | Total count of folders and documents returned. |

### Folder Element (`<f>`) Attributes

| Attribute | Description |
|-----------|-------------|
| `id` | Unique integer ID of the sub-folder. |
| `n` | Name of the sub-folder. |

### Document Element (`<d>`) Attributes

| Attribute | Description |
|-----------|-------------|
| `id` | Unique integer ID of the document. |
| `n` | Document file name (including extension). |
| `mdate` | Last modification date, universal format (`2026-08-19T15:34:41.527Z`). |
| `cdate` | Creation date, universal format. |
| `size` | File size in bytes. |
| `dformat` | MIME type description (e.g. `PDF Document`, `Microsoft Excel Spreadsheet`). |
| `chkoutbyusername` | Login name of the user who has the document checked out, or empty if not checked out. |
| `chkoutbyfullname` | Full name of the user who has the document checked out, or empty if not checked out. |
| `version` | Latest version number. |
| `publishedversion` | Published version number (`0` if no version is published). |
| `regdate` | Date the document was registered/uploaded, universal format. |
| `dtype` | Document type integer ID (`0` if no type assigned). |

### Error Response

```xml

<response success="false" error="[ErrorCode] Error message" />

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

- Date fields use `yyyy-MM-dd` format.

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

**The code for a missing folder is not the same across the family.** `GetFoldersAndDocuments`,
`GetFoldersAndDocuments2` and `GetFoldersAndDocumentsByPage2` answer `4041`; this one and
`GetFoldersAndDocumentsByPage` answer `4000`. The message is the same in all five. A client that has to work
with more than one of them should treat both numbers as "no such folder".

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4000` | no folder at that path - including one the caller may not see. Its three siblings answer `4041` for the same condition; see the note below |
| `HTTP 400` | `Path` was empty; refused by model binding, so there is no error document |

A call with no ticket at all is not automatically refused: it signs in as the anonymous user, so a
library flagged as anonymous can be listed without authenticating. Everything else answers `4000`,
because a folder the anonymous user cannot see is not told apart from one that does not exist.

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Folder not found` | The specified `Path` does not exist or is not accessible to the calling user. |

---

