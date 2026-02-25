# FolderExists API

Determines whether a folder exists at the specified path. Returns success if the path resolves to an existing folder, or an error if the folder is not found or cannot be accessed.

## Endpoint

```
/srv.asmx/FolderExists
```

## Methods

- **GET** `/srv.asmx/FolderExists?authenticationTicket=...&Path=...`
- **POST** `/srv.asmx/FolderExists` (form data)
- **SOAP** Action: `http://tempuri.org/FolderExists`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to check (e.g. `/Finance/Reports/2024`). |

---

## Response

### Success Response — Folder Exists

```xml
<response success="true" />
```

### Error Response — Folder Does Not Exist

```xml
<response error="Folder not found." />
```

The API returns `success="true"` if and only if the path resolves to an existing folder. If the folder does not exist, an error response is returned.

---

## Required Permissions

The calling user must be authenticated. The path must be accessible to the user.

---

## Example

### GET Request

```
GET /srv.asmx/FolderExists
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports/2024
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/FolderExists HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance/Reports/2024
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:FolderExists>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:Path>/Finance/Reports/2024</tns:Path>
    </tns:FolderExists>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- This API only checks for folders. To check for a document, use `DocumentExists`.
- The response does not include a `folderExists` attribute — existence is indicated by whether `success="true"` or an error is returned.
- Use `FolderExists1` to check for a subfolder by parent path and folder name as separate parameters.

---

## Related APIs

- [FolderExists1](FolderExists1.md) - Check folder existence by parent path and name
- [DocumentExists](DocumentExists.md) - Check whether a document exists
- [GetFolder](GetFolder.md) - Retrieve folder properties
- [CreateFolder](CreateFolder.md) - Create a folder

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Folder not found | The specified path does not resolve to an existing folder. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/FolderExists*
