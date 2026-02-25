# GetFolderStatistics API

Returns usage statistics for the specified folder, including subfolder count, total document count, checked-out document count, and total storage size of all documents in the folder tree.

## Endpoint

```
/srv.asmx/GetFolderStatistics
```

## Methods

- **GET** `/srv.asmx/GetFolderStatistics?authenticationTicket=...&folderPath=...`
- **POST** `/srv.asmx/GetFolderStatistics` (form data)
- **SOAP** Action: `http://tempuri.org/GetFolderStatistics`

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
  <statistics SubFolderCount="5" TotalDocumentCount="123" CheckedOutCount="3"
              TotalSize="10485760" FolderID="456" Name="Reports" />
</response>
```

### Error Response

```xml
<response error="Folder not found." />
```

### Statistics Attributes

| Attribute | Description |
|-----------|-------------|
| `SubFolderCount` | Number of direct subfolders in the folder. |
| `TotalDocumentCount` | Total number of documents in the folder and all subfolders. |
| `CheckedOutCount` | Number of currently checked-out documents in the folder tree. |
| `TotalSize` | Total storage size in bytes of all documents in the folder tree. |
| `FolderID` | Internal ID of the folder. |
| `Name` | Name of the folder. |

---

## Required Permissions

The calling user must have **read** permission on the folder.

---

## Example

### GET Request

```
GET /srv.asmx/GetFolderStatistics
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &folderPath=/Finance/Reports
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetFolderStatistics HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&folderPath=/Finance/Reports
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetFolderStatistics>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:folderPath>/Finance/Reports</tns:folderPath>
    </tns:GetFolderStatistics>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Statistics are computed recursively across the entire folder tree, not just direct children.
- `TotalSize` is reported in bytes.
- This API is useful for storage reporting and compliance dashboards.
- Use `GetSubFoldersCount` for a lightweight count of direct subfolders only.

---

## Related APIs

- [GetSubFoldersCount](GetSubFoldersCount.md) - Get only the direct subfolder count
- [GetFolder](GetFolder.md) - Get full folder metadata
- [GetFolders](GetFolders.md) - List subfolders

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