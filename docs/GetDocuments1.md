# GetDocuments1 API

Returns the documents in the specified infoRouter folder path in **short form**. This is a lightweight, high-performance variant of `GetDocuments` that uses abbreviated element names and a minimal attribute set. No optional enrichment flags are available -" use `GetDocuments` when full document metadata (property sets, security, owner, versions) is required.

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

One `<d>` element per document directly in the folder, in short form. Subfolders are not listed, and the root has no `folderfilter`.

```xml
<response success="true" error="" folderid="1170" parentid="1132" name="Reports"
          path="\Finance\Reports" documentfilter="" itemcount="2">
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
| `documentfilter` | string | The document name filter applied - always empty, this call takes none. |
| `itemcount` | integer | The number of `<d>` elements in this response. |

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

Lists the documents directly in one folder as compact `<d>` elements - the same shape
[GetFoldersAndDocuments1](GetFoldersAndDocuments1.md) uses, with the folders left out.

```javascript
const root = await call('GetDocuments1', {
  authenticationTicket: ticket,
  Path: '/Finance/Reports'
});

for (const d of root.querySelectorAll(':scope > d')) {
  console.log(d.getAttribute('id'), d.getAttribute('n'), d.getAttribute('size'));
}
```

This is [GetDocumentsByPage](GetDocumentsByPage.md) with no filter and no paging - the whole folder in
one answer. The root still reports the empty `documentfilter` it applied, but no `page` or `pageSize`,
and no `folderfilter` because it never looked at folders.

## Notes

- The listing is **not recursive** -" only the immediate documents in the specified `Path` are returned. Sub-folder contents are not traversed.

- Sub-folder items are never included in the response. To retrieve both folders and documents in short form, use `GetFoldersAndDocuments1`.

- The root element is `<response>`, not `<root>`, which differs from most other infoRouter APIs. Parse the response accordingly.

- Document items use the abbreviated element name `<d>` and carry a minimal attribute set. To retrieve full document metadata, use `GetDocument` or `GetDocuments`.

- All documents are returned in a single response with no paging. For large folders, consider `GetDocumentsByPage` to page through results.

- The `Path` parameter is case-insensitive and leading/trailing slashes are normalized automatically.

- If the path does not exist or the user has no access to it, an error response is returned with `success="false"`.

- Dates are in universal format (UTC), e.g. `2024-06-15T14:30:00.000Z`.

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

---

