# GetDocuments1 API

Returns the documents in the specified infoRouter folder path in **short form**. This is a lightweight, high-performance variant of `GetDocuments` that uses abbreviated element names and a minimal attribute set. No optional enrichment flags are available — use `GetDocuments` when full document metadata (property sets, security, owner, versions) is required.

## Endpoint

```
/srv.asmx/GetDocuments1
```

## Methods

- **GET** `/srv.asmx/GetDocuments1?AuthenticationTicket=...&Path=...`
- **POST** `/srv.asmx/GetDocuments1` (form data)
- **SOAP** Action: `http://tempuri.org/GetDocuments1`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the folder whose documents should be returned (e.g. `/Finance/Reports`). Must point to an existing folder the user can access. |

---

## Response

### Success Response

The root element is `<response>` and carries metadata about the queried folder as attributes. Each document in the folder is returned as a `<d>` child element using short, abbreviated attribute names. Sub-folder items are not included. If the folder exists but contains no documents, only the root element with folder metadata is returned.

```xml
<response success="true"
          error=""
          folderid="10"
          parentid="3"
          name="Reports"
          path="/Finance/Reports"
          folderfilter=""
          documentfilter=""
          itemcount="2">

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
| `folderid` | Integer ID of the queried folder. |
| `parentid` | Integer ID of the queried folder's parent. |
| `name` | Name of the queried folder. |
| `path` | Full infoRouter path of the queried folder. |
| `folderfilter` | The folder name filter applied (always empty — no filter for this API). |
| `documentfilter` | The document name filter applied (always empty — no filter for this API). |
| `itemcount` | Total count of document items returned. |

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

The calling user must have at least **List** permission on the specified folder. Documents to which the user has no access are automatically excluded from the response. Read-only users may call this API.

---

## Example

### GET Request

```
GET /srv.asmx/GetDocuments1
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetDocuments1 HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301&Path=/Finance/Reports
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetDocuments1>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:Path>/Finance/Reports</tns:Path>
    </tns:GetDocuments1>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- The listing is **not recursive** — only the immediate documents in the specified `Path` are returned. Sub-folder contents are not traversed.
- Sub-folder items are never included in the response. To retrieve both folders and documents in short form, use `GetFoldersAndDocuments1`.
- The root element is `<response>`, not `<root>`, which differs from most other infoRouter APIs. Parse the response accordingly.
- Document items use the abbreviated element name `<d>` and carry a minimal attribute set. To retrieve full document metadata, use `GetDocument` or `GetDocuments`.
- All documents are returned in a single response with no paging. For large folders, consider `GetDocumentsByPage` to page through results.
- The `Path` parameter is case-insensitive and leading/trailing slashes are normalized automatically.
- If the path does not exist or the user has no access to it, an error response is returned with `success="false"`.
- Date fields use `yyyy-MM-dd` format.
- This API is significantly faster than `GetDocuments` for large folders because it avoids loading full document objects. Use it when only identity, name, size, date, or checkout status is needed.

---

## Related APIs

- [GetDocuments](GetDocuments.md) - Get full properties of every document in a folder path
- [GetFoldersAndDocuments1](GetFoldersAndDocuments1.md) - Return both sub-folders and documents in short form
- [GetDocumentsByPage](GetDocumentsByPage.md) - Get a paginated list of documents in a folder in short form
- [GetDocument](GetDocument.md) - Get the full properties of a single document by path
- [GetFoldersAndDocuments](GetFoldersAndDocuments.md) - Full-detail listing with optional property sets, security, owner, and version history

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Folder not found` | The specified `Path` does not exist or is not accessible to the calling user. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/GetDocuments1*
