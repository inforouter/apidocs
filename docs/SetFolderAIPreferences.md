# SetFolderAIPreferences API

Sets the infoRouter Connect (AI) preferences of the specified folder from an XML preferences definition. Only the preferences listed in the XML are changed; the ones that are not listed keep their current value.

When the `ApplyToSubfolders` preference is on, the preferences are also written onto the whole existing subfolder tree, and subfolders created later inherit them at creation time.

## Endpoint

```
/srv.asmx/SetFolderAIPreferences
```

## Methods

- **GET** `/srv.asmx/SetFolderAIPreferences?authenticationTicket=...&Path=...&xmlPreferences=...`
- **POST** `/srv.asmx/SetFolderAIPreferences` (form data)
- **SOAP** Action: `http://tempuri.org/SetFolderAIPreferences`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the folder (e.g. `/Finance/Reports`). |
| `xmlPreferences` | string (XML) | Yes | XML document with an `AIPreferences` root element and `Preference` child elements carrying `Name` and `Value` attributes. In SOAP this parameter is an XML element, not a string. |

### Supported Preference Names

Names are case-insensitive.

| Preference Name | Description |
|-----------------|-------------|
| `AutoProfile` | Describe the document in one call: description, abstract, summary and keywords together, plus the OCR text of a scan. Replaces the three below rather than adding to them. |
| `AutoSummarize` | Summarize new document versions. |
| `AutoExtractKeywords` | Produce keywords for new document versions. |
| `AutoOCR` | Read the text out of scanned documents so they become searchable. |
| `AutoClassify` | Stored but **not yet performed by the server**. |
| `AutoExtractData` | Stored but **not yet performed by the server**. |
| `ScrubPII` | Scrub PII before document text is handed to the AI provider. |
| `ApplyToSubfolders` | Apply the preferences to the subfolder tree as well (see Notes). |

> **Switching one on does not process the documents already in the folder.** Preferences take effect for documents uploaded, checked in or imported afterwards. To produce content for a document already there, ask for it directly with [GetConnectProfile](GetConnectProfile.md).

> **`AutoProfile` covers `AutoSummarize`, `AutoExtractKeywords` and `AutoOCR`.** One profile call returns all of it, so switching `AutoProfile` on means the other three are not run alongside it - switching them on as well costs nothing and changes nothing. See [GetFolderAIPreferences](GetFolderAIPreferences.md) for exactly what gets queued.

> **`AutoClassify` and `AutoExtractData` are accepted and stored, but the server does not act on them yet.** They are recorded so a folder's intent survives, and will start working when the operations are implemented.

### Supported Values

`on` and `off`. For convenience `true`/`false`, `yes`/`no` and `1`/`0` are also accepted. Values are case-insensitive; any other value fails the call.

### Example xmlPreferences

```xml
<AIPreferences>
  <Preference Name="AutoSummarize" Value="on" />
  <Preference Name="AutoExtractKeywords" Value="on" />
  <Preference Name="ScrubPII" Value="on" />
  <Preference Name="ApplyToSubfolders" Value="on" />
</AIPreferences>
```

---

## Response

### Success Response

```xml
<response success="true" error="" />
```

### Error Response

```xml
<response success="false" error="Invalid value for the 'AUTOSUMMARIZE' preference. Valid values: on, off" />
```

---

## Required Permissions

The calling user must have the **Set Folder Rules** permission on the folder. When `ApplyToSubfolders` is on, the permission is checked on every subfolder as well; the first subfolder the user may not configure aborts the operation and returns an access error. Subfolders processed before that point keep the new preferences.

---

## Example

### GET Request

```
GET /srv.asmx/SetFolderAIPreferences
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports
  &xmlPreferences=%3CAIPreferences%3E%3CPreference%20Name%3D%22AutoSummarize%22%20Value%3D%22on%22%2F%3E%3C%2FAIPreferences%3E
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/SetFolderAIPreferences HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance/Reports
&xmlPreferences=<AIPreferences><Preference Name="AutoSummarize" Value="on"/></AIPreferences>
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:SetFolderAIPreferences>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:Path>/Finance/Reports</tns:Path>
      <tns:xmlPreferences>
        <AIPreferences>
          <Preference Name="AutoSummarize" Value="on" />
        </AIPreferences>
      </tns:xmlPreferences>
    </tns:SetFolderAIPreferences>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- The preferences are merged onto the values currently in effect for the folder, so a call that lists a single preference leaves the others untouched.
- `ApplyToSubfolders` is itself a stored preference, not a one-off switch: while it is on, the folder's preferences are copied to every subfolder created afterwards. Turning it off stops that inheritance but leaves the values already written onto the subfolders in place.
- Unknown `Preference` names are ignored, so a newer client can send preferences an older server does not know yet.
- The automatic operations additionally require infoRouter Connect to be configured on the server (`AppSettings:IRConnect`); preferences that are on have no effect while Connect is unconfigured.

---

## Related APIs

- [GetFolderAIPreferences](GetFolderAIPreferences.md) - Get the AI preferences in effect for a folder
- [SetFolderRules](SetFolderRules.md) - Set the rules and policies for a folder

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `[903]Required parameter.'Path'` | The `Path` parameter was empty. |
| `[903]Required parameter.'xmlPreferences'` | The `xmlPreferences` parameter was empty or not well-formed XML. |
| Invalid value for the '...' preference. Valid values: on, off | A `Preference` element carried a value that is not a recognized switch. |
| Folder not found | The specified path does not resolve to an existing folder. |
| Access denied | The user may not set the rules of the folder or of one of its subfolders. |
| `SystemError:...` | An unexpected server-side error occurred. |

---
