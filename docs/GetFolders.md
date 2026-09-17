# GetFolders API

Returns the list of direct subfolders of the specified folder with full property details. Optional flags control whether rules, property sets, security (ACL), and owner information are included for each subfolder.

## Endpoint

```
/srv.asmx/GetFolders
```

## Methods

- **GET** `/srv.asmx/GetFolders?authenticationTicket=...&Path=...&WithRules=...&withPropertySets=...&withSecurity=...&withOwner=...`
- **POST** `/srv.asmx/GetFolders` (form data)
- **SOAP** Action: `http://tempuri.org/GetFolders`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the parent folder (e.g. `/Finance`). |
| `WithRules` | bool | Yes | If `true`, includes folder rules for each subfolder. |
| `withPropertySets` | bool | Yes | If `true`, includes applied property set values for each subfolder. |
| `withSecurity` | bool | Yes | If `true`, includes the ACL for each subfolder. |
| `withOwner` | bool | Yes | If `true`, includes the owner user information for each subfolder. |

---

## Response

### Success Response

```xml
<response success="true">
  <folder id="456" name="Reports" description="Quarterly Reports" parentid="100"
          createdate="2023-01-15T09:00:00" modifydate="2024-03-20T14:30:00"
          owner="jsmith" classificationlevel="0">
    <!-- Optional sub-elements based on flags -->
    <Rules>...</Rules>
    <propertysets>...</propertysets>
    <security>...</security>
    <owner>...</owner>
  </folder>
  <folder id="457" name="Invoices" ...>
    ...
  </folder>
</response>
```

### Error Response

```xml
<response error="Folder not found." />
```

---

## Required Permissions

The calling user must have **read** permission on the parent folder. Only subfolders the user has access to are returned.

---

## Example

### GET Request

```
GET /srv.asmx/GetFolders
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance
  &WithRules=false
  &withPropertySets=false
  &withSecurity=false
  &withOwner=false
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetFolders HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance
&WithRules=false
&withPropertySets=false
&withSecurity=false
&withOwner=false
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetFolders>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:Path>/Finance</tns:Path>
      <tns:WithRules>false</tns:WithRules>
      <tns:withPropertySets>false</tns:withPropertySets>
      <tns:withSecurity>false</tns:withSecurity>
      <tns:withOwner>false</tns:withOwner>
    </tns:GetFolders>
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

Lists the direct subfolders of one folder, each as a `<folder>` element in the same shape
[GetFolder](GetFolder.md) uses.

The four flags never change which folders come back, only how much is written about each: `withOwner`
adds a `<User>` child, `WithRules` a `<Rules>`, `withPropertySets` a `<Propertysets>` and
`withSecurity` an `<AccessList>`. With all four off the `<folder>` element has no children at all.

```javascript
const root = await call('GetFolders', {
  authenticationTicket: ticket,
  Path: '/Finance',
  WithRules: false,
  withPropertySets: false,
  withSecurity: false,
  withOwner: false
});

for (const folder of root.querySelectorAll(':scope > folder')) {
  console.log(folder.getAttribute('Name'), folder.getAttribute('Path'));
}
```

A folder with no subfolders is a success with an empty root - `<response success="true" error="" />`
- not an error. Documents are not included; use
[GetFoldersAndDocuments](GetFoldersAndDocuments.md) for both.

## Notes

- Returns only **direct** subfolders (one level deep) of the specified path.
- Setting all flags to `false` gives the best performance for large folder trees.
- For a lightweight list (folder names and IDs only), use `GetFolders1` instead.
- For paged results with filtering, use `GetFoldersByPage`.
- For a combined list of folders and documents, use `GetFoldersAndDocuments`.

---

## Related APIs

- [GetFolders1](GetFolders1.md) - Get subfolders in short form (name and ID only)
- [GetFolders2](GetFolders2.md) - Get subfolders with UI display count limit
- [GetFoldersByPage](GetFoldersByPage.md) - Get paged subfolders with filter
- [GetFolder](GetFolder.md) - Get properties of a single folder
- [GetFoldersAndDocuments](GetFoldersAndDocuments.md) - Get both folders and documents

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4000` | no folder at that path - including one the caller may not see. Most of this group answers `4041` for the same condition; see the note below |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

**The code for a missing folder is not the same across this group.** `GetFolderRules`,
`GetFolderAIPreferences`, `GetFolderCatalog`, `GetFolderStatistics` and `DeleteFolder` answer `4041`;
this one and `GetFolder` answer `4000` for the identical condition and message, because they report
the failure through a helper that does not carry the code. A client that has to work with more than
one of them should treat both numbers as "no such folder".

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