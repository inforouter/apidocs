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

```xml
<response success="true">
  <folder id="456" name="Reports" />
  <folder id="457" name="Invoices" />
  <folder id="458" name="Contracts" />
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

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Folder not found | The specified path does not resolve to an existing folder. |
| Access denied | The user does not have read permission on the folder. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/GetFolders1*
