# GetFolder API

Returns the properties of the folder at the specified path, with optional detail levels for rules, property sets, security (ACL), and owner information.

## Endpoint

```
/srv.asmx/GetFolder
```

## Methods

- **GET** `/srv.asmx/GetFolder?authenticationTicket=...&Path=...&WithRules=...&withPropertySets=...&withSecurity=...&withOwner=...`
- **POST** `/srv.asmx/GetFolder` (form data)
- **SOAP** Action: `http://tempuri.org/GetFolder`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the folder (e.g. `/Finance/Reports`). |
| `WithRules` | bool | Yes | If `true`, includes folder rules (file type restrictions, checkout/checkin policies, etc.) in the response. |
| `withPropertySets` | bool | Yes | If `true`, includes applied property set values in the response. |
| `withSecurity` | bool | Yes | If `true`, includes the folder's access control list (ACL) in the response. |
| `withOwner` | bool | Yes | If `true`, includes the owner user information in the response. |

---

## Response

### Success Response

```xml
<response success="true">
  <folder id="456" name="Reports" description="Quarterly Reports" parentid="100"
          createdate="2023-01-15T09:00:00" modifydate="2024-03-20T14:30:00"
          owner="jsmith" classificationlevel="0">
    <!-- Included only when WithRules=true -->
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
    <!-- Included only when withPropertySets=true -->
    <propertysets>...</propertysets>
    <!-- Included only when withSecurity=true -->
    <security>...</security>
    <!-- Included only when withOwner=true -->
    <owner>...</owner>
  </folder>
</response>
```

### Error Response

```xml
<response error="Folder not found." />
```

---

## Required Permissions

The calling user must have **read** permission on the folder.

---

## Example

### GET Request

```
GET /srv.asmx/GetFolder
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports
  &WithRules=true
  &withPropertySets=false
  &withSecurity=false
  &withOwner=false
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetFolder HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance/Reports
&WithRules=true
&withPropertySets=false
&withSecurity=false
&withOwner=false
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetFolder>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:Path>/Finance/Reports</tns:Path>
      <tns:WithRules>true</tns:WithRules>
      <tns:withPropertySets>false</tns:withPropertySets>
      <tns:withSecurity>false</tns:withSecurity>
      <tns:withOwner>false</tns:withOwner>
    </tns:GetFolder>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Set all boolean flags to `false` for the fastest response (metadata only, no sub-elements).
- Set `WithRules=true` to retrieve folder restrictions (allowed file types, checkout/checkin policies).
- Set `withSecurity=true` to retrieve the full ACL of the folder.
- To get a list of subfolders, use `GetFolders` instead.
- To get folder rules only (without other properties), use `GetFolderRules`.

---

## Related APIs

- [GetFolders](GetFolders.md) - Get list of subfolders with full properties
- [GetFolderRules](GetFolderRules.md) - Get only the rules for a folder
- [UpdateFolderProperties](UpdateFolderProperties.md) - Update folder name and description
- [SetFolderRules](SetFolderRules.md) - Set folder rules

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

*For detailed documentation visit: https://support.inforouter.com/api-docs/GetFolder*
