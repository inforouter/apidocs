# CreateFolder1 API

Creates a new subfolder with an optional description inside the specified parent folder. The parent folder must already exist. Use this variant when you need to specify both the parent path and the new folder name separately, and optionally provide a description.

## Endpoint

```
/srv.asmx/CreateFolder1
```

## Methods

- **GET** `/srv.asmx/CreateFolder1?authenticationTicket=...&ParentFolderPath=...&NewFolderName=...&Description=...`
- **POST** `/srv.asmx/CreateFolder1` (form data)
- **SOAP** Action: `http://tempuri.org/CreateFolder1`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `ParentFolderPath` | string | Yes | Full infoRouter path to the existing parent folder (e.g. `/Finance/Reports`). This folder must already exist. |
| `NewFolderName` | string | Yes | Name of the new subfolder to create. Invalid characters are sanitized automatically. |
| `Description` | string | No | Optional description for the new folder. |

---

## Response

### Success Response

```xml
<response success="true" FolderId="789" FolderName="2024" />
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
GET /srv.asmx/CreateFolder1
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &ParentFolderPath=/Finance/Reports
  &NewFolderName=2024
  &Description=Annual reports for fiscal year 2024
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/CreateFolder1 HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&ParentFolderPath=/Finance/Reports
&NewFolderName=2024
&Description=Annual reports for fiscal year 2024
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:CreateFolder1>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:ParentFolderPath>/Finance/Reports</tns:ParentFolderPath>
      <tns:NewFolderName>2024</tns:NewFolderName>
      <tns:Description>Annual reports for fiscal year 2024</tns:Description>
    </tns:CreateFolder1>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Root-level folders (domains/libraries) cannot be created using this API. Use `CreateDomain` instead.
- Unlike `CreateFolder`, this variant takes the parent path and new folder name as separate parameters, making it more suitable when the folder name is dynamic.
- Folder names are sanitized (invalid characters are removed or replaced) before creation.
- If `Description` is omitted or null, the folder is created without a description.

---

## Related APIs

- [CreateFolder](CreateFolder.md) - Create a folder using a single full path
- [CreateDomain](CreateDomain.md) - Create a top-level domain/library
- [DeleteFolder](DeleteFolder.md) - Delete a folder
- [UpdateFolderProperties](UpdateFolderProperties.md) - Update folder name and description

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Folder not found | The parent folder path does not exist. |
| Access denied | The user does not have permission to create subfolders. |
| Root level folders cannot be created | The parent path points to the system root. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/CreateFolder1*
