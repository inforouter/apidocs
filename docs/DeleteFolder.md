# DeleteFolder API

Deletes the folder at the specified path, including all its contents (subfolders and documents). This operation is permanent and cannot be undone unless items are in the recycle bin.

## Endpoint

```
/srv.asmx/DeleteFolder
```

## Methods

- **GET** `/srv.asmx/DeleteFolder?authenticationTicket=...&Path=...`
- **POST** `/srv.asmx/DeleteFolder` (form data)
- **SOAP** Action: `http://tempuri.org/DeleteFolder`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the folder to delete (e.g. `/Finance/Reports/2024`). |

---

## Response

### Success Response

```xml
<response success="true" />
```

### Error Response

```xml
<response error="Access denied." />
```

---

## Required Permissions

The calling user must have **delete** permission on the folder. The user must also have permission to delete all documents within the folder.

---

## Example

### GET Request

```
GET /srv.asmx/DeleteFolder
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports/2024
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/DeleteFolder HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance/Reports/2024
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:DeleteFolder>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:Path>/Finance/Reports/2024</tns:Path>
    </tns:DeleteFolder>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Top-level folders (domains/libraries) **cannot** be deleted using this API. Use `DeleteDomain` instead.
- Deleting a folder removes all subfolders and documents within it.
- Depending on server configuration, deleted items may be moved to the recycle bin rather than being permanently deleted.
- Checked-out documents within the folder may prevent deletion unless the user has administrator rights.
- Folder rules (`DisallowFolderDelete`) may restrict this operation.

---

## Related APIs

- [CreateFolder](CreateFolder.md) - Create a folder
- [FolderExists](FolderExists.md) - Check whether a folder exists
- [DeleteDomain](DeleteDomain.md) - Delete a top-level domain/library
- [DeleteDocument](DeleteDocument.md) - Delete a single document

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Folder not found | The specified path does not resolve to an existing folder. |
| Access denied | The user does not have delete permission on the folder. |
| Top-level domain cannot be deleted | The path points to a root-level domain/library. |
| `SystemError:...` | An unexpected server-side error occurred. |

---