# GetFoldersAndDocuments1 API

Returns the immediate sub-folders and documents in the specified infoRouter path in **short form**. This is a lightweight, high-performance variant of `GetFoldersAndDocuments` that uses abbreviated element names and a minimal attribute set. Folder items contain only their ID and name; document items contain a small set of essential fields. No optional enrichment flags are available — use `GetFoldersAndDocuments` when full document or folder metadata is required.

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

  <!-- Folder items — id and name only -->
  <f id="42" n="Q1 Reports" />
  <f id="43" n="Q2 Reports" />
  <f id="44" n="Q3 Reports" />

  <!-- Document items — abbreviated attribute set -->
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
| `folderfilter` | The folder name filter applied (empty string — no filter for this API). |
| `documentfilter` | The document name filter applied (empty string — no filter for this API). |
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

## Notes

- The listing is **not recursive** — only the immediate children (sub-folders and documents) of the specified `Path` are returned.
- The root element is `<response>`, not `<root>`, which differs from most other infoRouter APIs. Parse the response accordingly.
- Folder items use the abbreviated element name `<f>` and carry only `id` and `n` (name). To retrieve full folder metadata, use `GetFolder` or `GetFoldersAndDocuments`.
- Document items use the abbreviated element name `<d>` and carry a minimal attribute set. To retrieve full document metadata, use `GetDocument` or `GetFoldersAndDocuments`.
- All items are returned in a single response with no paging. For large folders with hundreds of items, consider `GetFoldersAndDocumentsByPage` or `GetFoldersAndDocumentsByPage2` to page through results.
- Folders appear before documents in the response.
- The `Path` parameter is case-insensitive and leading/trailing slashes are normalized automatically.
- If the path does not exist or the user has no access to it, an error response is returned (the `error` attribute is set on the `<response>` element and `success="false"`).
- Date fields use `yyyy-MM-dd` format.
- This API is significantly faster than `GetFoldersAndDocuments` for large folders because it avoids loading full document and folder objects. Use it when only identity, name, size, date, or checkout information is needed.

---

## Related APIs

- [GetFoldersAndDocuments](GetFoldersAndDocuments) - Full-detail listing with optional property sets, security, owner, and version history
- [GetFoldersAndDocumentsByPage](GetFoldersAndDocumentsByPage) - Paged listing (first page, up to 20 items) of folder contents
- [GetFoldersAndDocumentsByPage2](GetFoldersAndDocumentsByPage2) - Paged listing in enhanced form
- [GetFolders](GetFolders) - Returns only the sub-folders of the specified path
- [GetDocuments](GetDocuments) - Returns only the documents in the specified path
- [GetDocument](GetDocument) - Returns full metadata for a single document by path
- [Search](Search) - Find documents and folders across the system using search criteria

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Folder not found` | The specified `Path` does not exist or is not accessible to the calling user. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/GetFoldersAndDocuments1*
