# GetFolderAIPreferences API

Returns the infoRouter Connect (AI) preferences in effect for the specified folder. These preferences control which operations — summarization, classification, keyword extraction, data extraction, profiling, OCR — are performed automatically on the documents of the folder, and whether PII is scrubbed before document text is handed to the AI provider.

A folder that has no preferences of its own inherits them from the nearest parent folder whose `ApplyToSubfolders` preference is on. When there is no such parent folder, every option is off.

## Endpoint

```
/srv.asmx/GetFolderAIPreferences
```

## Methods

- **GET** `/srv.asmx/GetFolderAIPreferences?authenticationTicket=...&Path=...`
- **POST** `/srv.asmx/GetFolderAIPreferences` (form data)
- **SOAP** Action: `http://tempuri.org/GetFolderAIPreferences`

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
  <AIPreferences FolderID="1042" UpdatedByUserID="3" UpdatedOn="2026-08-03T11:24:07">
    <Preference Name="AutoSummarize" Value="on" />
    <Preference Name="AutoClassify" Value="off" />
    <Preference Name="AutoExtractKeywords" Value="on" />
    <Preference Name="AutoExtractData" Value="off" />
    <Preference Name="AutoProfile" Value="off" />
    <Preference Name="AutoOCR" Value="on" />
    <Preference Name="ScrubPII" Value="on" />
    <Preference Name="ApplyToSubfolders" Value="off" />
  </AIPreferences>
</response>
```

### Error Response

```xml
<response success="false" error="[901]Session expired or Invalid ticket" />
```

### AIPreferences Attributes

| Attribute | Description |
|-----------|-------------|
| `FolderID` | Id of the folder the preferences apply to. |
| `UpdatedByUserID` | Id of the user who last saved the preferences. `0` when the folder has never been configured. |
| `UpdatedOn` | When the preferences were last saved, in `yyyy-MM-ddTHH:mm:ss` form. |

### Preference Descriptions

| Preference Name | Possible Values | Description |
|-----------------|-----------------|-------------|
| `AutoSummarize` | `"on"` / `"off"` | Summarize new document versions automatically. |
| `AutoClassify` | `"on"` / `"off"` | Classify new document versions against the configured taxonomy automatically. |
| `AutoExtractKeywords` | `"on"` / `"off"` | Extract keywords (tags) from new document versions automatically. |
| `AutoExtractData` | `"on"` / `"off"` | Run structured data extraction on new document versions automatically. |
| `AutoProfile` | `"on"` / `"off"` | Fill the applied property sets of new document versions automatically. |
| `AutoOCR` | `"on"` / `"off"` | OCR scanned documents automatically. |
| `ScrubPII` | `"on"` / `"off"` | Scrub PII before document text is handed to the AI provider. |
| `ApplyToSubfolders` | `"on"` / `"off"` | The preferences also govern the subfolder tree, including subfolders created later. |

---

## Required Permissions

The calling user must have **read** permission on the folder.

---

## Example

### GET Request

```
GET /srv.asmx/GetFolderAIPreferences
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetFolderAIPreferences HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance/Reports
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetFolderAIPreferences>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:Path>/Finance/Reports</tns:Path>
    </tns:GetFolderAIPreferences>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Use `SetFolderAIPreferences` to modify the preferences of a folder.
- The call always succeeds for an existing, readable folder: a folder that was never configured (and inherits nothing) reports every preference as `off`.
- `FolderID` in the response is always the id of the folder that was asked for, also when the values were inherited from a parent folder.
- The automatic operations additionally require infoRouter Connect to be configured on the server (`AppSettings:IRConnect`); preferences that are on have no effect while Connect is unconfigured.

---

## Related APIs

- [SetFolderAIPreferences](SetFolderAIPreferences.md) - Set the AI preferences of a folder
- [GetFolderRules](GetFolderRules.md) - Get the rules and policies configured for a folder

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `[903]Required parameter.'Path'` | The `Path` parameter was empty. |
| Folder not found | The specified path does not resolve to an existing folder. |
| Access denied | The user does not have read permission on the folder. |
| `SystemError:...` | An unexpected server-side error occurred. |

---
