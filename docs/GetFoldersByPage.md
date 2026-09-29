# GetFoldersByPage API

Returns a page of direct subfolders from the specified parent folder, with optional name filtering. Each page contains up to 20 folders. Use `PageNumber` to navigate through large folder lists.

## Endpoint

```
/srv.asmx/GetFoldersByPage
```

## Methods

- **GET** `/srv.asmx/GetFoldersByPage?authenticationTicket=...&Path=...&FolderFilter=...&PageNumber=...`
- **POST** `/srv.asmx/GetFoldersByPage` (form data)
- **SOAP** Action: `http://tempuri.org/GetFoldersByPage`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the parent folder (e.g. `/Finance`). |
| `FolderFilter` | string | No | Optional filter string to search for folder names containing the specified text. Pass empty string or null for no filtering. |
| `PageNumber` | int | Yes | Page number to retrieve (1-based). Pass `1` for the first page. Each page contains up to 20 folders. |

---

## Response

### Success Response

One `<f>` element per subfolder on the requested page. The root describes the folder that was read and the page.

```xml
<response success="true" error="" folderid="1170" parentid="1132" name="Reports"
          path="\Finance\Reports" folderfilter="" page="1" pageSize="20" itemcount="2">
  <f id="1171" n="2024" />
  <f id="1172" n="2023" />
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
| `page` | integer | The `PageNumber` requested. Not written when `PageNumber` is `-1`. |
| `pageSize` | integer | Items per page: the server's search page size setting (20 by default). Not written when `PageNumber` is `-1`. |
| `itemcount` | integer | The number of `<f>` elements in this response - **this page**, not the folder's total. |

### `<f>` attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | integer | The subfolder's id. |
| `n` | string | The subfolder's name. |

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

The calling user must have **read** permission on the parent folder. Only accessible subfolders are returned.

---

## Example

### GET Request (page 1, no filter)

```
GET /srv.asmx/GetFoldersByPage
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance
  &FolderFilter=
  &PageNumber=1
HTTP/1.1
```

### GET Request (page 2, with filter)

```
GET /srv.asmx/GetFoldersByPage
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance
  &FolderFilter=Report
  &PageNumber=2
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetFoldersByPage HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance
&FolderFilter=
&PageNumber=1
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetFoldersByPage>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:Path>/Finance</tns:Path>
      <tns:FolderFilter></tns:FolderFilter>
      <tns:PageNumber>1</tns:PageNumber>
    </tns:GetFoldersByPage>
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

Lists the direct subfolders of one folder as `<f>` elements, a page at a time, with an optional name
filter. `itemcount` counts **this page**.

`*` is the only wildcard the filter understands, and without one it matches the **whole name**:
`report` does not find `report2026`, while `report*` does. A `%`, `_` or `?` in the filter is ordinary
text. Wrapping the value in double quotes forces a whole-name match even if it contains a `*`. Unlike
the document filter on [GetFoldersAndDocumentsByPage](GetFoldersAndDocumentsByPage.md), this one takes
a single value: a `;` in it is part of the name being looked for, not a separator.

```javascript
let page = 1;

for (;;) {
  const root = await call('GetFoldersByPage', {
    authenticationTicket: ticket,
    Path: '/Finance',
    FolderFilter: '',
    PageNumber: page
  });

  for (const f of root.querySelectorAll(':scope > f')) console.log(f.getAttribute('n'));

  if (Number(root.getAttribute('itemcount')) < Number(root.getAttribute('pageSize'))) break;
  page++;
}
```

Pass `PageNumber=-1` for everything in one answer, which also drops `page` and `pageSize` from the
root. A page past the end is a success with nothing in it rather than an error.

## Notes

- Each page returns up to the server's search page size (20 by default), reported back as `pageSize`.
- `FolderFilter` performs a substring match on folder names (case-insensitive on most configurations).
- To get the first page, pass `PageNumber=1`.
- A response with no `<f>` elements means there are no more folders on this or later pages.
- For a combined paged listing of folders and documents, use `GetFoldersAndDocumentsByPage`.

---

## Related APIs

- [GetFolders](GetFolders.md) - Get all subfolders with full properties (no paging)
- [GetFolders1](GetFolders1.md) - Get all subfolders in short form (no paging)
- [GetFoldersAndDocumentsByPage](GetFoldersAndDocumentsByPage.md) - Paged listing of both folders and documents

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4041` | no folder at that path, including one the caller may not see |
| none | a refusal raised while the folder's contents are read, such as the caller not being allowed to list it; the error document has no `errorCode` attribute |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

A call with no ticket is not automatically refused: it signs in as the anonymous user, so a folder in
a library flagged as anonymous can be read without authenticating. The writes in this group refuse it
with `4010`.

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Folder not found | The specified path does not resolve to an existing folder. |
| Access denied | The user does not have read permission on the folder. |
| `SystemError:...` | An unexpected server-side error occurred. |

---