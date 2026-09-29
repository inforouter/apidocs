# GetFolders1 API

Returns the list of direct subfolders of the specified folder in short form (folder names and IDs only). This is a lightweight alternative to `GetFolders` when you do not need rules, property sets, security, or owner details.

## Endpoint

```
/srv.asmx/GetFolders1
```

## Methods

- **GET** `/srv.asmx/GetFolders1?authenticationTicket=...&Path=...`
- **POST** `/srv.asmx/GetFolders1` (form data)
- **SOAP** Action: `http://tempuri.org/GetFolders1`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the parent folder (e.g. `/Finance`). |

---

## Response

### Success Response

One `<f>` element per direct subfolder, in short form. The root describes the folder that was read.

```xml
<response success="true" error="" folderid="1170" parentid="1132" name="Reports"
          path="\Finance\Reports" folderfilter="" itemcount="2">
  <f id="1171" n="2024" />
  <f id="1172" n="2023" />
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
| `folderfilter` | string | The folder name filter applied - always empty, this call takes none. |
| `itemcount` | integer | The number of `<f>` elements in this response. |

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

The calling user must have **read** permission on the parent folder. Only subfolders the user has access to are returned.

---

## Example

### GET Request

```
GET /srv.asmx/GetFolders1
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetFolders1 HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetFolders1>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:Path>/Finance</tns:Path>
    </tns:GetFolders1>
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

Lists the direct subfolders of one folder as `<f>` elements, with an `id` and a name. Documents are
not included.

```javascript
const root = await call('GetFolders1', {
  authenticationTicket: ticket,
  Path: '/Finance/Reports'
});

for (const f of root.querySelectorAll(':scope > f')) {
  console.log(f.getAttribute('id'), f.getAttribute('n'));
}
```

This is [GetFoldersByPage](GetFoldersByPage.md) with no filter and no paging - the whole folder in one
answer. The root still carries the empty `folderfilter` it applied, but no `page` or `pageSize`. For
the same list with every folder property on it, use [GetFolders](GetFolders.md).

## Notes

- Returns only direct subfolders (one level deep), not recursive.
- No limit on the number of returned folders. For large folder trees, consider using `GetFolders2` which applies the configured display count limit.
- Use `GetFolders` if you need full properties (rules, property sets, security, owner).

---

## Related APIs

- [GetFolders](GetFolders.md) - Get subfolders with full properties
- [GetFolders2](GetFolders2.md) - Get subfolders with UI display count limit applied
- [GetFoldersByPage](GetFoldersByPage.md) - Get paged subfolders with filter
- [GetFoldersAndDocuments](GetFoldersAndDocuments.md) - Get both folders and documents

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4041` | no folder at that path, including one the caller may not see |
| none | a refusal raised while the folder's contents are read, such as the caller not being allowed to list it; the error document has no `errorCode` attribute |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

A missing folder answers `4041`, as `GetSubFoldersCount`, `UpdateFolderProperties`, `SetFolderRules`,
`SetFolderAIPreferences`, `SetFolderCutoffDate`, `RemoveFolderCutoffDate` and `Move` do.

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