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
| `FolderFilter` | string | No | Optional substring filter for folder names. Pass empty string or null for no filtering. |
| `DocumentFilter` | string | No | Optional substring filter for document names. Pass empty string or null for no filtering. |
| `PageNumber` | int | Yes | Page number to retrieve (1-based). Pass `-1` for every item in one response, with no `page` or `pageSize` on the root. |

---

## Response

### Success Response

Folders come back as `<f>` and documents as `<d>` - the same short-form elements
[GetFoldersAndDocuments1](GetFoldersAndDocuments1.md) returns, with `page` and `pageSize` added to the
root. They are **not** the `<folder>` / `<document>` elements
[GetFoldersAndDocuments](GetFoldersAndDocuments.md) returns.

```xml
<response success="true"
          error=""
          folderid="1329"
          parentid="1001"
          name="Reports"
          path="\Finance\Reports"
          folderfilter=""
          documentfilter=""
          page="1"
          pageSize="20"
          itemcount="3">

  <!-- Folder items - id and name only -->
  <f id="42" n="2024" />
  <f id="43" n="2023" />

  <!-- Document items -->
  <d id="1494"
     n="Q1-Report.pdf"
     mdate="2026-08-19T15:34:41.527Z"
     cdate="2026-08-19T15:34:41.527Z"
     size="308"
     dformat="Plain Text"
     chkoutbyusername=""
     chkoutbyfullname=""
     version="1000000"
     publishedversion="1000000"
     regdate="2026-08-19T15:34:41.757Z"
     dtype="0" />

</response>
```

#### Root attributes

| Attribute | Description |
|-----------|-------------|
| `success` | `true` if the request succeeded. |
| `error` | Error message if `success` is `false`; otherwise empty. |
| `folderid` | Integer ID of the queried folder (the folder at `Path`). |
| `parentid` | Integer ID of the queried folder's parent. |
| `name` | Name of the queried folder. |
| `path` | Full infoRouter path of the queried folder. |
| `folderfilter` | The folder name filter that was applied. |
| `documentfilter` | The document name filter that was applied. |
| `page` | The page number that was returned. |
| `pageSize` | Items per page, as configured on the server. |
| `itemcount` | Count of folders plus documents in **this page**, not the total across all pages. |

#### `<f>` - folder items

| Attribute | Description |
|-----------|-------------|
| `id` | Unique integer ID of the sub-folder. |
| `n` | Name of the sub-folder. |

#### `<d>` - document items

| Attribute | Description |
|-----------|-------------|
| `id` | Unique integer ID of the document. |
| `n` | Document file name (including extension). |
| `mdate` | Last modification date, universal format (`2026-08-19T15:34:41.527Z`). |
| `cdate` | Creation date, universal format. |
| `size` | File size in bytes. |
| `dformat` | MIME type description (e.g. `PDF Document`, `Plain Text`). |
| `chkoutbyusername` | Login name of the user who has the document checked out, or empty if not checked out. |
| `chkoutbyfullname` | Full name of that user, or empty if not checked out. |
| `version` | Latest version number, in the large-integer scheme (version 1 is `1000000`). |
| `publishedversion` | Published version number (`0` if no version is published). |
| `regdate` | Date the document was registered/uploaded, universal format. |
| `dtype` | Document type integer ID (`0` if no type assigned). |

### Error Response

```xml
<response success="false" error="Folder not found." />
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

## Notes

- Returns only **direct** children (one level deep) of the specified path.
- Page size is set on the server and reported back as `pageSize`; it is not a parameter of this call.
- `FolderFilter` and `DocumentFilter` perform a case-insensitive substring match on the name.
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

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Folder not found | The specified path does not resolve to an existing folder. |
| Access denied | The user does not have read permission on the folder. |
| `SystemError:...` | An unexpected server-side error occurred. |

---