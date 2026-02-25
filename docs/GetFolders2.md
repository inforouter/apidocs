# GetFolders2 API

Returns the list of direct subfolders of the specified folder in short form, applying the system's configured maximum folder display count limit. This API is used by the infoRouter UI folder panel to avoid overloading the interface with extremely large folder lists.

## Endpoint

```
/srv.asmx/GetFolders2
```

## Methods

- **GET** `/srv.asmx/GetFolders2?authenticationTicket=...&Path=...`
- **POST** `/srv.asmx/GetFolders2` (form data)
- **SOAP** Action: `http://tempuri.org/GetFolders2`

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
GET /srv.asmx/GetFolders2
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetFolders2 HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetFolders2>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:Path>/Finance</tns:Path>
    </tns:GetFolders2>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- The maximum number of returned folders is controlled by the `MaximumDisplayFolderCount` UI setting in infoRouter's system configuration.
- If a folder has more subfolders than the limit allows, only the first N folders (up to the limit) are returned.
- For unlimited folder listing, use `GetFolders1`.
- This API is primarily used by the infoRouter web UI folder tree panel.
- For full property details per folder, use `GetFolders` instead.

---

## Related APIs

- [GetFolders1](GetFolders1.md) - Get subfolders with no count limit
- [GetFolders](GetFolders.md) - Get subfolders with full properties
- [GetFoldersByPage](GetFoldersByPage.md) - Get paged subfolders with filter

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

*For detailed documentation visit: https://support.inforouter.com/api-docs/GetFolders2*
