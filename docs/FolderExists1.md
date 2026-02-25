# FolderExists1 API

Determines whether a subfolder with the given name exists inside the specified parent folder. Returns success if the subfolder is found, or an error if it does not exist. Use this variant when you have the parent path and the subfolder name as separate values.

## Endpoint

```
/srv.asmx/FolderExists1
```

## Methods

- **GET** `/srv.asmx/FolderExists1?authenticationTicket=...&FolderPath=...&FolderName=...`
- **POST** `/srv.asmx/FolderExists1` (form data)
- **SOAP** Action: `http://tempuri.org/FolderExists1`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `FolderPath` | string | Yes | Full infoRouter path to the parent folder (e.g. `/Finance/Reports`). |
| `FolderName` | string | Yes | Name of the subfolder to look for within the parent folder (e.g. `2024`). |

---

## Response

### Success Response — Subfolder Exists

```xml
<response success="true" />
```

### Error Response — Subfolder Does Not Exist

```xml
<response error="Folder not found." />
```

The API returns `success="true"` if the named subfolder exists inside the parent folder. Otherwise an error is returned.

---

## Required Permissions

The calling user must be authenticated and have at least read access to the parent folder.

---

## Example

### GET Request

```
GET /srv.asmx/FolderExists1
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &FolderPath=/Finance/Reports
  &FolderName=2024
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/FolderExists1 HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&FolderPath=/Finance/Reports
&FolderName=2024
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:FolderExists1>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:FolderPath>/Finance/Reports</tns:FolderPath>
      <tns:FolderName>2024</tns:FolderName>
    </tns:FolderExists1>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- This variant accepts the parent path and folder name as separate parameters, which is useful when building folder paths programmatically.
- Use `FolderExists` instead if you already have the full path to the folder.
- The check is case-insensitive for folder names on most configurations.

---

## Related APIs

- [FolderExists](FolderExists.md) - Check folder existence using a full path
- [GetFolder](GetFolder.md) - Retrieve folder properties
- [CreateFolder1](CreateFolder1.md) - Create a subfolder with parent path and name as separate parameters

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Folder not found | The parent path does not exist or the named subfolder is not found within it. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/FolderExists1*
