# GetFolderRules API

Returns the rules of a folder: which file types it accepts, which actions it allows, and which property set it prompts for. Every rule it returns can be written back with [SetFolderRules](SetFolderRules.md).

## Endpoint

```
/srv.asmx/GetFolderRules
```

## Methods

- **GET** `/srv.asmx/GetFolderRules?AuthenticationTicket=...&Path=...`
- **POST** `/srv.asmx/GetFolderRules` (form data)
- **SOAP** Action: `http://tempuri.org/GetFolderRules`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `Path` | string | Yes | Full infoRouter path of the folder, e.g. `/Finance/Reports`. A library's root folder is `/Finance` |

## Response

### Success

```xml
<response success="true" error="">
  <Rules>
    <Rule Name="AllowableFileTypes" Value="DOCX,PDF" />
    <Rule Name="Checkins" Value="allows" />
    <Rule Name="Checkouts" Value="disallows" />
    <Rule Name="DocumentDeletes" Value="allows" />
    <Rule Name="FolderDeletes" Value="allows" />
    <Rule Name="NewDocuments" Value="allows" />
    <Rule Name="NewFolders" Value="disallows" />
    <Rule Name="ClassifiedDocuments" Value="disallows" />
    <Rule Name="AutoPromptPropertsetName" Value="INVOICE" warning="mispelled attribute name. Use 'AutoPromptPropertysetName' instead." />
    <Rule Name="AutoPromptPropertysetName" Value="INVOICE" />
  </Rules>
</response>
```

### Error

```xml
<response success="false" error="Target folder cannot be found" errorcode="4041" />
```

## The Rules

| Rule | Value | Meaning |
|------|-------|---------|
| `AllowableFileTypes` | `*`, or extensions separated by commas | Which file types may be uploaded. `*` = any. Extensions come back upper case, without dots, in alphabetical order (`DOCX,PDF`) |
| `Checkins` | `allows` / `disallows` | Whether documents may be checked in |
| `Checkouts` | `allows` / `disallows` | Whether documents may be checked out |
| `DocumentDeletes` | `allows` / `disallows` | Whether documents may be deleted |
| `FolderDeletes` | `allows` / `disallows` | Whether subfolders may be deleted |
| `NewDocuments` | `allows` / `disallows` | Whether documents may be added |
| `NewFolders` | `allows` / `disallows` | Whether subfolders may be created |
| `ClassifiedDocuments` | `allows` / `disallows` | Whether classified documents may be stored here |
| `AutoPromptPropertysetName` | A property set name, or empty | The property set the user is prompted to fill in when uploading. Empty = no prompt |
| `AutoPromptPropertsetName` | Same value | The same rule under the name it first shipped with, missing the `y`. Kept so older callers keep working, and carries a `warning` attribute saying so. Read `AutoPromptPropertysetName` instead |

A newly created library allows everything, accepts every file type, prompts for no property set, and disallows classified documents.

## Required Permissions

- Read permission on the folder.

## Examples

### GET

```
GET /srv.asmx/GetFolderRules?AuthenticationTicket=abc123&Path=%2FFinance%2FReports HTTP/1.1
```

### POST

```
POST /srv.asmx/GetFolderRules HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=abc123&Path=%2FFinance%2FReports
```

### SOAP 1.1

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetFolderRules"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetFolderRules xmlns="http://tempuri.org/">
      <AuthenticationTicket>abc123</AuthenticationTicket>
      <Path>/Finance/Reports</Path>
    </GetFolderRules>
  </soap:Body>
</soap:Envelope>
```

### JavaScript: Read the Rules, Change One, Write It Back

`GetFolderRules` returns the rules in the form `SetFolderRules` takes, so a UI can round-trip them. Leave the misspelled rule out of what you send.

```js
async function disallowNewFolders(ticket, path) {
  const post = async (action, params) => {
    const response = await fetch(`/srv.asmx/${action}`, {
      method: 'POST',
      body: new URLSearchParams({ AuthenticationTicket: ticket, ...params }),
    });
    const root = new DOMParser().parseFromString(await response.text(), 'text/xml').documentElement;
    if (root.getAttribute('success') !== 'true') throw new Error(root.getAttribute('error'));
    return root;
  };

  // Read.
  const rules = Array.from((await post('GetFolderRules', { Path: path })).getElementsByTagName('Rule'))
    .map((rule) => ({ name: rule.getAttribute('Name'), value: rule.getAttribute('Value') }))
    .filter((rule) => rule.name !== 'AutoPromptPropertsetName');   // the misspelled duplicate

  // Change one.
  rules.find((rule) => rule.name === 'NewFolders').value = 'disallows';

  // Write back. The values are already in the form SetFolderRules expects.
  const xml = `<Rules>${rules.map((r) => `<Rule Name="${r.name}" Value="${r.value}" />`).join('')}</Rules>`;
  await post('SetFolderRules', { Path: path, xmlRules: xml, ApplyToTree: 'false' });
}
```

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

| `errorcode` | Error (English) | Cause |
|-------------|-----------------|-------|
| `4010` | `[901]Session expired or Invalid ticket` | Missing, invalid or expired ticket |
| `4041` | `Target folder cannot be found` | No folder at `Path`, or the caller may not see it |
| `4000` | `Required argument: Path` | `Path` was empty |

## Notes

- The rules are the folder's own. They are not merged with a parent's: `SetFolderRules` with `ApplyToTree` writes a parent's rules onto its subfolders.
- `AutoPromptPropertysetName` names a property set. If that property set is later deleted, the rule comes back empty.
- Both spellings always carry the same value; they are one rule, returned twice.

## Related APIs

- [SetFolderRules](SetFolderRules.md) — Write the rules of a folder
- [GetFolder](GetFolder.md) — Folder properties, optionally including its rules
- [GetFolderAIPreferences](GetFolderAIPreferences.md) — The infoRouter Connect preferences of a folder
- [GetPropertySetDefinitions](GetPropertySetDefinitions.md) — The property sets a folder can prompt for
