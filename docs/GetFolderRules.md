# GetFolderRules API

Returns the rules (policies) configured for the specified folder. Rules govern what operations are allowed or disallowed within the folder, such as file type restrictions, checkout/checkin policies, and document/folder deletion permissions.

## Endpoint

```
/srv.asmx/GetFolderRules
```

## Methods

- **GET** `/srv.asmx/GetFolderRules?authenticationTicket=...&Path=...`
- **POST** `/srv.asmx/GetFolderRules` (form data)
- **SOAP** Action: `http://tempuri.org/GetFolderRules`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the folder (e.g. `/Finance/Reports`). |

---

## Response

### Success Response

```xml
<response success="true">
  <Rules>
    <Rule Name="AllowableFileTypes" Value="*" />
    <Rule Name="Checkins" Value="allows" />
    <Rule Name="Checkouts" Value="allows" />
    <Rule Name="DocumentDeletes" Value="allows" />
    <Rule Name="FolderDeletes" Value="allows" />
    <Rule Name="NewDocuments" Value="allows" />
    <Rule Name="NewFolders" Value="allows" />
    <Rule Name="ClassifiedDocuments" Value="disallows" />
  </Rules>
</response>
```

### Error Response

```xml
<response error="Folder not found." />
```

### Rule Descriptions

| Rule Name | Possible Values | Description |
|-----------|----------------|-------------|
| `AllowableFileTypes` | `*` or comma-separated extensions (e.g. `.pdf,.docx`) | File types that may be uploaded to this folder. `*` means all file types are allowed. |
| `Checkins` | `"allows"` / `"disallows"` | Whether document check-ins are permitted. |
| `Checkouts` | `"allows"` / `"disallows"` | Whether document check-outs are permitted. |
| `DocumentDeletes` | `"allows"` / `"disallows"` | Whether documents can be deleted from this folder. |
| `FolderDeletes` | `"allows"` / `"disallows"` | Whether subfolders can be deleted. |
| `NewDocuments` | `"allows"` / `"disallows"` | Whether new documents can be uploaded to this folder. |
| `NewFolders` | `"allows"` / `"disallows"` | Whether new subfolders can be created. |
| `ClassifiedDocuments` | `"allows"` / `"disallows"` | Whether classified (restricted) documents are permitted. |

---

## Required Permissions

The calling user must have **read** permission on the folder.

---

## Example

### GET Request

```
GET /srv.asmx/GetFolderRules
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetFolderRules HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance/Reports
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetFolderRules>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:Path>/Finance/Reports</tns:Path>
    </tns:GetFolderRules>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Use `SetFolderRules` to modify the rules for a folder.
- `GetFolder` with `WithRules=true` also returns the rules as part of the full folder object.
- Rules are stored at the folder level and can optionally be applied to the entire subfolder tree using `SetFolderRules` with `ApplyToTree=true`.

---

## Related APIs

- [SetFolderRules](SetFolderRules.md) - Set folder rules
- [GetFolder](GetFolder.md) - Get full folder properties including optional rules
- [UpdateFolderProperties](UpdateFolderProperties.md) - Update folder name and description

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

*For detailed documentation visit: https://support.inforouter.com/api-docs/GetFolderRules*
