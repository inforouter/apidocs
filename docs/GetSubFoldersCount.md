# GetSubFoldersCount API

Returns the count of direct subfolders within the specified folder. This is a lightweight alternative to `GetFolderStatistics` when only the subfolder count is needed.

## Endpoint

```
/srv.asmx/GetSubFoldersCount
```

## Methods

- **GET** `/srv.asmx/GetSubFoldersCount?authenticationTicket=...&Path=...`
- **POST** `/srv.asmx/GetSubFoldersCount` (form data)
- **SOAP** Action: `http://tempuri.org/GetSubFoldersCount`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the folder (e.g. `/Finance/Reports`). |

---

## Response

### Success Response

```xml
<response success="true" SubFolderCount="5" />
```

### Error Response

```xml
<response error="Folder not found." />
```

| Attribute | Description |
|-----------|-------------|
| `success` | `"true"` if the count was retrieved successfully. |
| `SubFolderCount` | Number of direct subfolders in the specified folder. |

---

## Required Permissions

The calling user must have **read** permission on the folder.

---

## Example

### GET Request

```
GET /srv.asmx/GetSubFoldersCount
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetSubFoldersCount HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance/Reports
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetSubFoldersCount>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:Path>/Finance/Reports</tns:Path>
    </tns:GetSubFoldersCount>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Returns only the count of direct subfolders, not recursive subfolder counts.
- For full statistics including total document count and storage size, use `GetFolderStatistics`.

---

## Related APIs

- [GetFolderStatistics](GetFolderStatistics.md) - Get comprehensive folder statistics
- [GetFolders](GetFolders.md) - Get the list of subfolders

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