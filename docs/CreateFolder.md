# CreateFolder API

Creates a folder at the specified path. Multiple sub-folders can be created in a single call by providing a full path. The top-level folder (domain/library) must already exist — this API cannot create root-level libraries.

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
| `Path` | string | Yes | Full infoRouter path to the folder to create (e.g. `/Finance/Reports/2024`). All intermediate folders in the path will be created if they do not exist. The top-level domain/library must already exist. |

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

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Folder not found | The parent folder in the path does not exist. |
| Access denied | The user does not have permission to create subfolders. |
| Root level folders cannot be created | The path points to a root-level domain/library. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/CreateFolder*
