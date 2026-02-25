# UpdateFolderProperties API

Updates the name and/or description of the specified folder. The folder itself must already exist; only its metadata is changed.

## Endpoint

```
/srv.asmx/UpdateFolderProperties
```

## Methods

- **GET** `/srv.asmx/UpdateFolderProperties?authenticationTicket=...&Path=...&NewFolderName=...&NewDescription=...`
- **POST** `/srv.asmx/UpdateFolderProperties` (form data)
- **SOAP** Action: `http://tempuri.org/UpdateFolderProperties`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the existing folder (e.g. `/Finance/Reports`). |
| `NewFolderName` | string | Yes | New name for the folder. The name is sanitized (carriage returns/line feeds removed) before saving. |
| `NewDescription` | string | No | New description for the folder. Pass empty string or null to clear the description. |

---

## Response

### Success Response

```xml
<response success="true" error="" />
```

### Error Response

```xml
<response success="false" error="Folder not found." />
```

---

## Required Permissions

The calling user must have **write** (modify) permission on the folder.

---

## Example

### GET Request

```
GET /srv.asmx/UpdateFolderProperties
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports
  &NewFolderName=Financial Reports
  &NewDescription=All financial reports including quarterly and annual summaries
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/UpdateFolderProperties HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance/Reports
&NewFolderName=Financial Reports
&NewDescription=All financial reports including quarterly and annual summaries
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:UpdateFolderProperties>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:Path>/Finance/Reports</tns:Path>
      <tns:NewFolderName>Financial Reports</tns:NewFolderName>
      <tns:NewDescription>All financial reports including quarterly and annual summaries</tns:NewDescription>
    </tns:UpdateFolderProperties>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Renaming a folder changes the folder's path. Any references to the old path will need to be updated.
- The folder name is sanitized: carriage returns and line feeds are stripped.
- The description supports multi-line text; line ending characters are normalized.
- To change folder rules, use `SetFolderRules`.

---

## Related APIs

- [GetFolder](GetFolder.md) - Retrieve current folder name and description
- [SetFolderRules](SetFolderRules.md) - Update folder behavior rules
- [CreateFolder](CreateFolder.md) - Create a new folder

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Folder not found | The specified path does not resolve to an existing folder. |
| Access denied | The user does not have write permission on the folder. |
| `SystemError:...` | An unexpected server-side error occurred. |

---