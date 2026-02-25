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

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Folder not found | The specified path does not resolve to an existing folder. |
| Access denied | The user does not have read permission on the folder. |
| `SystemError:...` | An unexpected server-side error occurred. |

---