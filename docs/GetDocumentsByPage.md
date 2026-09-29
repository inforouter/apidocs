# GetDocumentsByPage API

Returns a single page of documents in the specified infoRouter folder path in **short form**. Supports optional name filtering and 1-based page number navigation. The response uses the same abbreviated element names as `GetDocuments1` but adds paging attributes (`page`, `pageSize`) to the root element. Use this API when iterating through large folders one page at a time.

## Endpoint

```

/srv.asmx/GetDocumentsByPage

```

## Methods

- **GET** `/srv.asmx/GetDocumentsByPage?AuthenticationTicket=...&Path=...&DocumentFilter=...&PageNumber=...`

- **POST** `/srv.asmx/GetDocumentsByPage` (form data)

- **SOAP** Action: `http://tempuri.org/GetDocumentsByPage`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the folder whose documents should be listed (e.g. `/Finance/Reports`). Must point to an existing folder the user can access. |
| `DocumentFilter` | string | No | Semicolon-separated list of document name patterns to filter results (e.g. `Report;Budget`). Pass an empty string or omit to return all documents. Matching is performed against document file names. |
| `PageNumber` | int | Yes | 1-based page number to retrieve. The first page is `1`. The page size is determined by the system-wide **Search Page Size** setting. Pass `-1` to return all documents without paging. |

---

## Response

### Success Response

One `<d>` element per document on the requested page. Subfolders are not listed, and the root has no `folderfilter`.

```xml
<response success="true" error="" folderid="1170" parentid="1132" name="Reports"
          path="\Finance\Reports" documentfilter="" page="1" pageSize="20" itemcount="2">
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
| `documentfilter` | string | The `DocumentFilter` applied; empty for none. |
| `page` | integer | The `PageNumber` requested. Not written when `PageNumber` is `-1`. |
| `pageSize` | integer | Items per page: the server's search page size setting (20 by default). Not written when `PageNumber` is `-1`. |
| `itemcount` | integer | The number of `<d>` elements in this response - **this page**, not the folder's total. |

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

The calling user must have at least **List** permission on the specified folder. Documents to which the user has no access are automatically excluded from the results and counts. Read-only users may call this API.

---

## Example

### GET Request -" first page, no filter

```

GET /srv.asmx/GetDocumentsByPage

  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

  &Path=/Finance/Reports

  &DocumentFilter=

  &PageNumber=1

HTTP/1.1

```

### GET Request -" second page with filter

```

GET /srv.asmx/GetDocumentsByPage

  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

  &Path=/Finance/Reports

  &DocumentFilter=Budget;Forecast

  &PageNumber=2

HTTP/1.1

```

### POST Request

```

POST /srv.asmx/GetDocumentsByPage HTTP/1.1

Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

&Path=/Finance/Reports

&DocumentFilter=

&PageNumber=1

```

### SOAP Request

```xml

<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"

               xmlns:tns="http://tempuri.org/">

  <soap:Body>

    <tns:GetDocumentsByPage>

      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>

      <tns:Path>/Finance/Reports</tns:Path>

      <tns:DocumentFilter></tns:DocumentFilter>

      <tns:PageNumber>1</tns:PageNumber>

    </tns:GetDocumentsByPage>

  </soap:Body>

</soap:Envelope>

```

### Iterating all pages

```

page = 1

repeat:

    GET /srv.asmx/GetDocumentsByPage?...&PageNumber={page}

    page = page + 1

until response/@itemcount < response/@pageSize

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

Lists the documents in one folder a page at a time, with an optional name filter. `itemcount` counts
**this page**.

```javascript
let page = 1;

for (;;) {
  const root = await call('GetDocumentsByPage', {
    authenticationTicket: ticket,
    Path: '/Finance/Reports',
    DocumentFilter: '',
    PageNumber: page
  });

  for (const d of root.querySelectorAll(':scope > d')) console.log(d.getAttribute('n'));

  if (Number(root.getAttribute('itemcount')) < Number(root.getAttribute('pageSize'))) break;
  page++;
}
```

**`DocumentFilter` matches any part of the name** and needs no wildcard: `port` finds `Q1-report.pdf`.
It is not the folder filter, which wants the whole name unless given a `*`. Several values may be
given separated by `;`, and a value in double quotes must match the whole name. `*` is the only
wildcard.

`PageNumber=-1` returns everything in one answer and drops `page` and `pageSize` from the root. A page
past the end is a success with nothing in it rather than an error.

## Notes

- `PageNumber` is **1-based** -" the first page is `1`, not `0`.

- The page size is controlled by the **Search Page Size** system setting; it is returned in the `pageSize` attribute of the response.

- `itemcount` is the number of `<d>` elements on **this page**, not the total across all pages. A page with fewer than `pageSize` items is the last one.

- `DocumentFilter` accepts a semicolon-separated list of partial name patterns. For example, `Report;Budget` returns documents whose names contain "Report" or "Budget".

- Sub-folder items are never returned. To retrieve sub-folders alongside documents, use `GetFoldersAndDocumentsByPage`.

- The listing is **not recursive** -" only the immediate documents in the specified `Path` are considered.

- Passing `PageNumber=-1` disables paging and returns all matching documents in a single response (equivalent to `GetDocuments1` with a filter). The `page` and `pageSize` attributes are absent in this case.

- The `Path` parameter is case-insensitive and leading/trailing slashes are normalized automatically.

- Dates are in universal format (UTC), e.g. `2024-06-15T14:30:00.000Z`.

---

## Related APIs

- [GetDocuments1](GetDocuments1.md) - Get all documents in a folder in short form without paging

- [GetDocuments](GetDocuments.md) - Get full properties of every document in a folder path

- [GetFoldersAndDocumentsByPage](GetFoldersAndDocumentsByPage.md) - Get a paged listing of both sub-folders and documents

- [GetFoldersByPage](GetFoldersByPage.md) - Get a paged listing of sub-folders only

- [GetDocument](GetDocument.md) - Get the full properties of a single document by path

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | no folder at that path, including one the caller may not see |
| none | a refusal raised while the folder's contents are read, such as the caller not being allowed to list it; the error document has no `errorCode` attribute |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

A missing folder answers `4041`, as [GetDocuments](GetDocuments.md) does.

A call with no ticket signs in as the anonymous user, so a document in a library flagged as anonymous
can be read without authenticating.

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Folder not found` | The specified `Path` does not exist or is not accessible to the calling user. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

