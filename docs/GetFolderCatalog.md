# GetFolderCatalog API

Returns the catalog information for the specified folder. The catalog provides a structured XML description of the folder's contents, metadata, and configuration as used by the infoRouter portal and UI components.

## Endpoint

```
/srv.asmx/GetFolderCatalog
```

## Methods

- **GET** `/srv.asmx/GetFolderCatalog?authenticationTicket=...&folderPath=...`
- **POST** `/srv.asmx/GetFolderCatalog` (form data)
- **SOAP** Action: `http://tempuri.org/GetFolderCatalog`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `folderPath` | string | Yes | Full infoRouter path to the folder (e.g. `/Finance/Reports`). |

---

## Response

### Success Response

```xml
<response success="true">
  <!-- Catalog XML content from the folder's catalog definition -->
  <catalog>...</catalog>
</response>
```

### Error Response

```xml
<response error="Folder not found." />
```

---

## Required Permissions

The calling user must have **read** permission on the folder.

---

## Example

### GET Request

```
GET /srv.asmx/GetFolderCatalog
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &folderPath=/Finance/Reports
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetFolderCatalog HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&folderPath=/Finance/Reports
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetFolderCatalog>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:folderPath>/Finance/Reports</tns:folderPath>
    </tns:GetFolderCatalog>
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

Reports the whole tree below a folder in one answer: `<folder>` elements nested inside each other,
each holding the `<document>` elements directly in it. A document carries only what is needed to tell
a changed file from an unchanged one - `chksum` and `chksumLastVersion` alongside `Size` and `mdate`
- which is what this call is for.

```javascript
const root = await call('GetFolderCatalog', {
  authenticationTicket: ticket,
  folderPath: '/Finance/Reports'
});

(function walk(folder, prefix) {
  for (const document of folder.querySelectorAll(':scope > document')) {
    console.log(prefix + document.getAttribute('name'), document.getAttribute('chksum'));
  }
  for (const child of folder.querySelectorAll(':scope > folder')) {
    walk(child, prefix + child.getAttribute('name') + '/');
  }
})(root.querySelector('folder'), '');
```

There is no depth limit and no paging, so this reads an entire tree in one response. On a large
library prefer [GetFoldersAndDocuments1](GetFoldersAndDocuments1.md) a folder at a time.

## Notes

- The catalog XML content varies depending on the folder's configuration in infoRouter.
- This API is primarily used by the infoRouter portal and UI to render folder views.

---

## Related APIs

- [GetFolder](GetFolder.md) - Get folder metadata and properties
- [GetFolderRules](GetFolderRules.md) - Get folder rules
- [GetFolderStatistics](GetFolderStatistics.md) - Get folder statistics

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4041` | the path does not name a folder - including a path that names a document, and one the caller may not see |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

A call with no ticket is not automatically refused: it signs in as the anonymous user, so a folder in
a library flagged as anonymous can be read without authenticating. The writes in this group -
`CreateFolder`, `CreateFolder1`, `CreateHtmlDocument` - refuse it with `4010`.

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Folder not found | The specified path does not resolve to an existing folder. |
| Access denied | The user does not have read permission on the folder. |
| `SystemError:...` | An unexpected server-side error occurred. |

---