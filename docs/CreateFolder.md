# CreateFolder API

Creates a folder at the specified path. Multiple sub-folders can be created in a single call by providing a full path. The top-level folder (domain/library) must already exist -" this API cannot create root-level libraries.

## Endpoint

```
/srv.asmx/CreateFolder
```

## Methods

- **GET** `/srv.asmx/CreateFolder?authenticationTicket=...&Path=...`
- **POST** `/srv.asmx/CreateFolder` (form data)
- **SOAP** Action: `http://tempuri.org/CreateFolder`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the folder to create (e.g. `/Finance/Reports/2024`). Every missing folder along the way is created too; only the library at the start of the path must already exist. The last segment is sanitised - see below. |

---

## Response

### Success Response

```xml
<response success="true" FolderId="456" FolderName="2024" />
```

### Error Response

```xml
<response error="Folder not found." />
```

| Attribute | Description |
|-----------|-------------|
| `success` | `"true"` if the folder was created successfully. |
| `FolderId` | The internal ID of the newly created folder. |
| `FolderName` | The sanitized name of the created folder. |

---

## Required Permissions

The calling user must have **create subfolder** permission on the parent folder.

---

## Example

### GET Request

```
GET /srv.asmx/CreateFolder
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports/2024
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/CreateFolder HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance/Reports/2024
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:CreateFolder>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:Path>/Finance/Reports/2024</tns:Path>
    </tns:CreateFolder>
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

Creates one folder, named by its full path.

**It creates the folders above it as well.** The parent is resolved with path creation switched on,
so a path whose parent does not exist is not refused - the whole chain is created and the response
reports the leaf. If a caller needs "fail when the parent is missing", it has to check with
[FolderExists](FolderExists.md) first.

### The name is cleaned before it is used

The folder that appears may not be the one that was asked for, which is why the response reports
`FolderName` rather than echoing the request. Read it back rather than assuming.

| In the name | What happens |
|---|---|
| `/` `\` `:` `*` `?` `"` `<` `>` `|` `#` tab `%` `&` `+` | each becomes one `_` |
| `..` | collapses to `.`, repeatedly |
| two spaces | collapse to one, repeatedly |
| leading or trailing `.` | removed |
| leading or trailing whitespace | removed |
| more than 128 characters | truncated, with a hash added before the extension |

So `..Q3 report  <final>..` is created as `Q3 report _final_`.

```javascript
const root = await call('CreateFolder', {
  authenticationTicket: ticket,
  Path: '/Finance/Reports/2026'
});

console.log(root.getAttribute('FolderId'), root.getAttribute('FolderName'));
```

A trailing `/` or `\` is ignored, and either separator may be used throughout. Libraries are not
created this way: a one-segment path such as `/NewLibrary` is answered `4041`.

## Notes

- Root-level folders (domains/libraries) cannot be created using this API. Use `CreateDomain` instead.
- If the full path contains multiple levels that do not exist, all intermediate folders are created automatically.
- Folder names are sanitized (invalid characters are removed or replaced) before creation.
- For creating a folder with a description, use `CreateFolder1`.

---

## Related APIs

- [CreateFolder1](CreateFolder1.md) - Create a folder with a description
- [CreateDomain](CreateDomain.md) - Create a top-level domain/library
- [DeleteFolder](DeleteFolder.md) - Delete a folder
- [FolderExists](FolderExists.md) - Check whether a folder exists

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all - the anonymous user is told "Anonymous users cannot perform this action" |
| `4090` | a folder of that name is already in the parent |
| `4041` | the path names a library that does not exist - including a one-segment path, since libraries are not created here |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |


| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Folder not found | The parent folder in the path does not exist. |
| Access denied | The user does not have permission to create subfolders. |
| Root level folders cannot be created | The path points to a root-level domain/library. |
| `SystemError:...` | An unexpected server-side error occurred. |

---