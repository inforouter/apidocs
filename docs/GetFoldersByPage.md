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

```xml
<response success="true">
  <folder id="456" name="Reports" />
  <folder id="457" name="Invoices" />
</response>
```

### Error Response

```xml
<response error="Folder not found." />
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

- Each page returns up to 20 folders.
- `FolderFilter` performs a substring match on folder names (case-insensitive on most configurations).
- To get the first page, pass `PageNumber=1`.
- An empty response (no `folder` elements) indicates no more folders are available on subsequent pages.
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
| `4000` | no folder at that path - including one the caller may not see. The setters in this group answer `4041` for the same condition; see the note below |
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