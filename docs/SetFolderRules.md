# SetFolderRules API

Sets the rules (policies) for the specified folder using an XML rules definition. Rules control allowed file types, checkout/checkin policies, document and folder deletion permissions, and other folder behaviors. Optionally applies the rules to the entire subfolder tree.

## Endpoint

```
/srv.asmx/SetFolderRules
```

## Methods

- **GET** `/srv.asmx/SetFolderRules?authenticationTicket=...&Path=...&xmlRules=...&ApplyToTree=...`
- **POST** `/srv.asmx/SetFolderRules` (form data)
- **SOAP** Action: `http://tempuri.org/SetFolderRules`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the folder (e.g. `/Finance/Reports`). |
| `xmlRules` | string | Yes | XML string defining the rules to apply. See format below. |
| `ApplyToTree` | bool | Yes | If `true`, the rules are applied recursively to all subfolders as well as the specified folder. If `false`, only the specified folder is updated. |

### xmlRules Format

The `xmlRules` parameter must be a valid XML string with `<Rules>` as the root element and `<Rule>` child elements, each with `Name` and `Value` attributes.

```xml
<Rules>
  <Rule Name="ALLOWABLEFILETYPES" Value="*" />
  <Rule Name="NEWFOLDERS" Value="allows" />
  <Rule Name="FOLDERDELETES" Value="allows" />
  <Rule Name="CHECKOUTS" Value="allows" />
  <Rule Name="CHECKINS" Value="allows" />
  <Rule Name="DOCUMENTDELETES" Value="allows" />
  <Rule Name="NEWDOCUMENTS" Value="allows" />
  <Rule Name="CLASSIFIEDDOCUMENTS" Value="allows" />
  <Rule Name="AUTOPROMPTPROPERTYSETNAME" Value="" />
</Rules>
```

### Available Rule Names and Values

| Rule Name | Values | Description |
|-----------|--------|-------------|
| `ALLOWABLEFILETYPES` | `*` or comma-separated extensions (e.g. `.pdf,.docx,.xlsx`) | Restricts uploadable file types. `*` allows all types. |
| `NEWFOLDERS` | `"allows"` or `"disallows"` | Controls creation of new subfolders. |
| `FOLDERDELETES` | `"allows"` or `"disallows"` | Controls deletion of subfolders. |
| `CHECKOUTS` | `"allows"` or `"disallows"` | Controls document check-outs. |
| `CHECKINS` | `"allows"` or `"disallows"` | Controls document check-ins. |
| `DOCUMENTDELETES` | `"allows"` or `"disallows"` | Controls document deletion. |
| `NEWDOCUMENTS` | `"allows"` or `"disallows"` | Controls uploading of new documents. |
| `CLASSIFIEDDOCUMENTS` | `"allows"` or `"disallows"` | Controls whether classified (restricted) documents are permitted. |
| `AUTOPROMPTPROPERTYSETNAME` | Property set name string, or empty string to clear | Auto-prompts users to fill the named property set when uploading. Pass an empty string to remove the prompt. Also accepted as `AUTOPROMPTPROPERTSETNAME`, the misspelling it first shipped with. |

> **Note:** Rule **names** are case-insensitive, but **values** are not: only the exact lower-case word `disallows` disallows an action. `DISALLOWS` or `Disallows` reads as `allows`. Only rules present in `xmlRules` are updated; omitted rules retain their current values, and a rule name the server does not know is ignored without an error.

---

## Response

### Success Response

```xml
<response success="true" error="" errorCode="0" />
```

### Error Response

```xml
<response success="false" error="Target folder cannot be found" errorcode="4041" />
```

---

## Required Permissions

The calling user must have **folder manager** or **domain manager** rights to modify folder rules.

---

## Example

### POST Request (restrict to PDF only, disallow deletions)

```
POST /srv.asmx/SetFolderRules HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance/Reports
&xmlRules=<Rules><Rule Name="ALLOWABLEFILETYPES" Value=".pdf"/><Rule Name="DOCUMENTDELETES" Value="disallows"/></Rules>
&ApplyToTree=false
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:SetFolderRules>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:Path>/Finance/Reports</tns:Path>
      <tns:xmlRules><![CDATA[<Rules><Rule Name="ALLOWABLEFILETYPES" Value=".pdf"/></Rules>]]></tns:xmlRules>
      <tns:ApplyToTree>false</tns:ApplyToTree>
    </tns:SetFolderRules>
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

Writes folder rules. Only the rules named in `xmlRules` are changed; the rest keep their values, so
this is a partial update and `<Rules />` is a valid no-op.

```javascript
await call('SetFolderRules', {
  authenticationTicket: ticket,
  Path: '/Finance/Reports',
  xmlRules:
    '<Rules>' +
      '<Rule Name="Checkouts" Value="disallows" />' +
      '<Rule Name="AllowableFileTypes" Value="pdf,docx" />' +
    '</Rules>',
  ApplyToTree: false
});
```

`ApplyToTree=true` writes the same rules down the whole subtree, not just the folder named.
`AllowableFileTypes` comes back from [GetFolderRules](GetFolderRules.md) upper case, without dots and
in alphabetical order, so `pdf,docx` reads back as `DOCX,PDF`.

**A value it cannot use is accepted and ignored.** `<Rule Name="Checkins" Value="perhaps" />` is
answered `success="true"` and the rule keeps the value it had. Nothing reports the mistake, so read
the rules back if it matters. A `Name` the operation does not recognise is ignored the same way. This
is unlike [SetFolderAIPreferences](SetFolderAIPreferences.md), which refuses an unusable value with
`4000` and names the ones it takes.

## Notes

- Rule names are case-insensitive; values are not. Only the exact word `disallows` disallows.
- Only the rules present in `xmlRules` are updated; rules not mentioned retain their current values. An unknown rule name is ignored.
- Setting `ApplyToTree=true` recursively applies the specified rules to all subfolders.
- Use [GetFolderRules](GetFolderRules.md) to read the current rules first. It returns every rule in the form this API takes, so a caller can read them, change one and write them all back.
- **A property set name that matches no property set is ignored**, and the call still reports success: the folder keeps the property set it prompted for before. Check the name with `GetPropertySetDefinitions` first.
- `ALLOWABLEFILETYPES` values are tidied up before they are stored: dots and spaces are dropped and the extensions are upper-cased and sorted, so ` .pdf , docx ` comes back from `GetFolderRules` as `DOCX,PDF`.
- Rules are enforced from the moment they are written: with `NEWFOLDERS` set to `disallows`, `CreateFolder` in that folder is refused.

---

## Related APIs

- [GetFolderRules](GetFolderRules.md) - Retrieve the current rules for a folder
- [GetFolder](GetFolder.md) - Get folder properties including rules (when WithRules=true)

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all - the anonymous user is told "Anonymous users cannot perform this action" |
| `4041` | no folder at that path - including one the caller may not see |
| `4000` | `xmlRules` is missing or is not well-formed XML |
| `4030` | the caller may not change this folder's rules |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Folder not found | The specified path does not resolve to an existing folder. |
| Access denied | The user does not have the required permissions. |
| `4000` Required argument: xmlRules | `xmlRules` is empty or not well-formed XML. |
| `SystemError:...` | An unexpected server-side error occurred. |

Sending `xmlRules` that is not well-formed answers with the error above. Older servers answered it with HTTP 500 and a stack trace.
