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
| `AUTOPROMPTPROPERTYSETNAME` | Property set name string, or empty string to clear | Auto-prompts users to fill the named property set when uploading. Pass an empty string to remove the prompt. |

> **Note:** Rule names are case-insensitive. Only rules present in `xmlRules` are updated; omitted rules retain their current values.

---

## Response

### Success Response

```xml
<root success="true" />
```

### Error Response

```xml
<root success="false" error="Folder not found." />
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

## Notes

- Rule names are case-insensitive.
- Only the rules present in `xmlRules` are updated; rules not mentioned retain their current values.
- Setting `ApplyToTree=true` recursively applies the specified rules to all subfolders.
- Use `GetFolderRules` to retrieve the current rules for a folder before modifying them.

---

## Related APIs

- [GetFolderRules](GetFolderRules.md) - Retrieve the current rules for a folder
- [GetFolder](GetFolder.md) - Get folder properties including rules (when WithRules=true)

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Folder not found | The specified path does not resolve to an existing folder. |
| Access denied | The user does not have the required permissions. |
| Invalid xmlRules | The `xmlRules` parameter is not a valid XML string. |
| `SystemError:...` | An unexpected server-side error occurred. |
