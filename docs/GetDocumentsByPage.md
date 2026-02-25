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

The root element is `<response>` and carries metadata about the queried folder and paging state as attributes. Each document on the requested page is returned as a `<d>` child element. Sub-folder items are never included.

```xml
<response success="true"
          error=""
          folderid="10"
          parentid="3"
          name="Reports"
          path="/Finance/Reports"
          documentfilter=""
          itemcount="47"
          page="2"
          pageSize="20">

  <d id="1071"
     n="Budget-2024.xlsx"
     mdate="2024-05-20"
     cdate="2024-01-10"
     size="98304"
     dformat="Microsoft Excel Spreadsheet"
     chkoutbyusername=""
     chkoutbyfullname=""
     version="2"
     publishedversion="0"
     regdate="2024-01-10"
     dtype="0" />

  <d id="1072"
     n="Forecast-Q3.pdf"
     mdate="2024-07-01"
     cdate="2024-07-01"
     size="51200"
     dformat="PDF Document"
     chkoutbyusername="jsmith"
     chkoutbyfullname="John Smith"
     version="1"
     publishedversion="1"
     regdate="2024-07-01"
     dtype="5" />

</response>
```

### Root Element (`<response>`) Attributes

| Attribute | Description |
|-----------|-------------|
| `success` | `true` if the request succeeded. |
| `error` | Error message if `success` is `false`; otherwise empty. |
| `folderid` | Integer ID of the queried folder. |
| `parentid` | Integer ID of the queried folder's parent. |
| `name` | Name of the queried folder. |
| `path` | Full infoRouter path of the queried folder. |
| `documentfilter` | The document name filter that was applied (empty string if no filter). |
| `itemcount` | **Total** number of documents matching the filter across all pages, not just the current page. Use this together with `pageSize` to calculate total page count. |
| `page` | The page number that was returned (present only when `PageNumber` is not `-1`). |
| `pageSize` | The number of documents per page as configured in system settings (present only when `PageNumber` is not `-1`). |

### Document Element (`<d>`) Attributes

| Attribute | Description |
|-----------|-------------|
| `id` | Unique integer ID of the document. |
| `n` | Document file name (including extension). |
| `mdate` | Last modification date (`yyyy-MM-dd` format). |
| `cdate` | Creation date (`yyyy-MM-dd` format). |
| `size` | File size in bytes. |
| `dformat` | MIME type description (e.g. `PDF Document`, `Microsoft Excel Spreadsheet`). |
| `chkoutbyusername` | Login name of the user who has the document checked out, or empty if not checked out. |
| `chkoutbyfullname` | Full name of the user who has the document checked out, or empty if not checked out. |
| `version` | Latest version number. |
| `publishedversion` | Published version number (`0` if no version is published). |
| `regdate` | Date the document was registered/uploaded (`yyyy-MM-dd` format). |
| `dtype` | Document type integer ID (`0` if no type assigned). |

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
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
totalDocuments = response/@itemcount
pageSize       = response/@pageSize
totalPages     = ceil(totalDocuments / pageSize)

for page = 1 to totalPages:
    GET /srv.asmx/GetDocumentsByPage?...&PageNumber={page}
```

---

## Notes

- `PageNumber` is **1-based** -" the first page is `1`, not `0`.
- The page size is controlled by the **Search Page Size** system setting; it is returned in the `pageSize` attribute of the response so clients can calculate total pages without additional calls.
- `itemcount` reflects the **total** number of documents matching `DocumentFilter` across all pages, not the count of items returned on the current page.
- `DocumentFilter` accepts a semicolon-separated list of partial name patterns. For example, `Report;Budget` returns documents whose names contain "Report" or "Budget".
- Sub-folder items are never returned. To retrieve sub-folders alongside documents, use `GetFoldersAndDocumentsByPage`.
- The listing is **not recursive** -" only the immediate documents in the specified `Path` are considered.
- Passing `PageNumber=-1` disables paging and returns all matching documents in a single response (equivalent to `GetDocuments1` with a filter). The `page` and `pageSize` attributes are absent in this case.
- The `Path` parameter is case-insensitive and leading/trailing slashes are normalized automatically.
- Date fields use `yyyy-MM-dd` format.

---

## Related APIs

- [GetDocuments1](GetDocuments1.md) - Get all documents in a folder in short form without paging
- [GetDocuments](GetDocuments.md) - Get full properties of every document in a folder path
- [GetFoldersAndDocumentsByPage](GetFoldersAndDocumentsByPage.md) - Get a paged listing of both sub-folders and documents
- [GetFoldersByPage](GetFoldersByPage.md) - Get a paged listing of sub-folders only
- [GetDocument](GetDocument.md) - Get the full properties of a single document by path

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Folder not found` | The specified `Path` does not exist or is not accessible to the calling user. |
| `SystemError:...` | An unexpected server-side error occurred. |

---
