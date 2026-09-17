# GetFolderAIPreferences API

Returns the infoRouter Connect (AI) preferences in effect for the specified folder. These preferences control which operations — summarization, description, abstract, classification, keyword extraction, data extraction, OCR — are performed automatically on the documents of the folder, and whether PII is scrubbed before document text is handed to the AI provider. There is one switch per answer: each asks for that answer and nothing else.

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
    <Preference Name="AutoDescribe" Value="on" />
    <Preference Name="AutoAbstract" Value="off" />
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
| `AutoSummarize` | `"on"` / `"off"` | Summarize new document versions. |
| `AutoDescribe` | `"on"` / `"off"` | Write the one line description of new document versions. |
| `AutoAbstract` | `"on"` / `"off"` | Write the longer abstract of new document versions. |
| `AutoExtractKeywords` | `"on"` / `"off"` | Produce keywords for new document versions. |
| `AutoOCR` | `"on"` / `"off"` | Read the text out of scanned documents so they become searchable. |
| `AutoClassify` | `"on"` / `"off"` | Stored but **not yet performed by the server**. |
| `AutoExtractData` | `"on"` / `"off"` | Stored but **not yet performed by the server**. |
| `ScrubPII` | `"on"` / `"off"` | Scrub PII before document text is handed to the AI provider. |
| `ApplyToSubfolders` | `"on"` / `"off"` | The preferences also govern the subfolder tree, including subfolders created later. |

### What actually runs when a document arrives

Switching a preference on does not queue work by itself. Work is queued when a document is **uploaded, checked in as a new version, or imported** into the folder, and only for the operations this server can carry out.

**Each switch asks for its own answer, and however many are on it is still one job and one call.** One call answers all of them, and it answers only what was asked for - so a folder that switches on `AutoDescribe` alone is written a description, and does not quietly acquire a summary, keywords and a document type with it.

| Preferences switched on | Queued for a PDF |
|-------------------------|------------------|
| `AutoDescribe` only | one job, answering the description |
| `AutoSummarize` + `AutoExtractKeywords` + `AutoOCR` | one job, answering the summary, the keywords and the OCR text |
| `AutoSummarize` + `AutoDescribe` + `AutoExtractKeywords` + `AutoClassify` | one job, answering all four |

Some documents are skipped entirely:

- **Shortcuts and URL documents** have no content to read, so nothing is queued for them.
- **File types infoRouter Connect cannot read** are skipped, except for OCR - OCR is what produces the text in the first place, and the scans that need it most are exactly the types the readable list leaves out.
- **`AutoClassify` and `AutoExtractData` are never queued**, because the server has no implementation for them yet. Switching them on is recorded and has no other effect.

Automatic work is queued behind anything a user is waiting for. If somebody asks for a document's summary through [GetDocumentSummary](GetDocumentSummary.md) while it is still queued, that job moves to the front.

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

## JavaScript

Every call answers XML with HTTP 200, success or not, so `success` is the thing to branch on and
`errorCode` is the number to report.

```javascript
async function call(action, params) {
  const response = await fetch(`/srv.asmx/${action}?${new URLSearchParams(params)}`);
  const root = new DOMParser()
    .parseFromString(await response.text(), 'text/xml')
    .documentElement;

  if (root.getAttribute('success') !== 'true') {
    throw new Error(`${root.getAttribute('errorCode')}: ${root.getAttribute('error')}`);
  }
  return root;
}
```

Reports the AI switches on one folder, each as a `<Preference>` with a `Value` of `on` or `off`.

```javascript
const root = await call('GetFolderAIPreferences', {
  authenticationTicket: ticket,
  Path: '/Finance/Reports'
});

const preferences = Object.fromEntries(
  [...root.querySelectorAll('Preference')]
    .map(p => [p.getAttribute('Name'), p.getAttribute('Value') === 'on'])
);

if (preferences.AutoSummarize) console.log('new versions here are summarised');
```

A folder that has never been configured still answers, with every switch `off`, `UpdatedByUserID` of
`0` and `UpdatedOn` of `1900-01-01T00:00:00`. Note that `UpdatedOn` is written in local time without
a zone, unlike the `...Z` timestamps most of the API uses.

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

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4041` | no folder at that path - including one the caller may not see |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

A call with no ticket is not automatically refused: it signs in as the anonymous user, so a folder in
a library flagged as anonymous can be read without authenticating. The writes in this group -
`CreateFolder`, `CreateFolder1`, `CreateHtmlDocument` - refuse it with `4010`.

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `[903]Required parameter.'Path'` | The `Path` parameter was empty. |
| Folder not found | The specified path does not resolve to an existing folder. |
| Access denied | The user does not have read permission on the folder. |
| `SystemError:...` | An unexpected server-side error occurred. |

---
