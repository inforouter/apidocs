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

With all four flags `false`, the `<folder>` element has no children:

```xml
<response success="true" error="">
  <folder FolderID="1170" ParentID="1132" Name="WorkFlowTestOutput" Path="\Accounts Receivable\WorkFlowTestOutput"
          Description="output of workflows will be here." CreationDate="2015-10-01T09:12:07.000Z"
          OwnerName="System Administrator" DomainId="1132"
          ClassificationLevel="NoMarkings" ClassificationLevelId="0" DeclassifyOn="" DowngradeOn=""
          RDDefId="0" RetentionDate="" DispositionDate="" CutoffDate="" />
</response>
```

With all four flags `true`, each adds one child:

```xml
<response success="true" error="">
  <folder FolderID="1170" ParentID="1132" Name="WorkFlowTestOutput" ...same attributes as above...>
    <!-- withOwner=true -->
    <User exists="true" UserID="4" FirstName="System" LastName="Administrator" Email="admin@example.com"
          MobileNumber="" Enabled="TRUE" UserName="sysadmin" />
    <!-- WithRules=true -->
    <Rules>
      <Rule Name="AllowableFileTypes" Value="*" />
      <Rule Name="Checkins" Value="allows" />
      <Rule Name="Checkouts" Value="allows" />
      <Rule Name="DocumentDeletes" Value="allows" />
      <Rule Name="FolderDeletes" Value="allows" />
      <Rule Name="NewDocuments" Value="allows" />
      <Rule Name="NewFolders" Value="allows" />
      <Rule Name="ClassifiedDocuments" Value="disallows" />
      <Rule Name="AutoPromptPropertsetName" Value="" warning="mispelled attribute name. Use 'AutoPromptPropertysetName' instead." />
      <Rule Name="AutoPromptPropertysetName" Value="" />
    </Rules>
    <!-- withPropertySets=true -->
    <Propertysets />
    <!-- withSecurity=true -->
    <AccessList DateApplied="" AppliedBy="" InheritedSecurity="true">
      <Anonymous Right="2" Description="Read" />
    </AccessList>
  </folder>
</response>
```

### `<folder>` attributes

| Attribute | Type | Description |
|---|---|---|
| `FolderID` | integer | The folder's id. |
| `ParentID` | integer | The parent folder's id; for a folder at the top of a library, the library's id. |
| `Name` | string | The folder's name. |
| `Path` | string | The full path, with backslashes (`\Library\Folder`). |
| `Description` | string | The folder's description; empty if none. |
| `CreationDate` | datetime (UTC) | When the folder was created. |
| `OwnerName` | string | The owner's full name. `withOwner=true` adds the owner's `<User>` record. |
| `DomainId` | integer | The id of the library (domain) the folder is in. |
| `ClassificationLevel` | string | `NoMarkings`, `Declassified`, `Confidential`, `Secret` or `TopSecret`. |
| `ClassificationLevelId` | integer | The same level as a number: `0` NoMarkings, `1` Declassified, `2` Confidential, `3` Secret, `4` TopSecret. |
| `DeclassifyOn` | datetime (UTC) | When the classification is removed; empty if not scheduled. |
| `DowngradeOn` | datetime (UTC) | When the classification is lowered; empty if not scheduled. |
| `RDDefId` | integer | The retention and disposition schedule applied to the folder; `0` if none. |
| `RetentionDate` | datetime (UTC) | Retained until; empty if no schedule. |
| `DispositionDate` | datetime (UTC) | When the folder is due for disposition; empty if none. |
| `CutoffDate` | datetime (UTC) | The date the retention period is counted from; empty if none. |

Empty dates are written as an empty string, not as a placeholder date.

### Child elements

| Element | Written when | Content |
|---|---|---|
| `<User>` | `withOwner=true` | The owner: `UserID`, `UserName`, `FirstName`, `LastName`, `Email`, `MobileNumber`, `Enabled`. |
| `<Rules>` | `WithRules=true` | One `<Rule Name Value>` per rule: `allows`/`disallows`, or the allowed file types (`*` = any) for `AllowableFileTypes`, or the property set a new document is prompted for (`AutoPromptPropertysetName`). The misspelled `AutoPromptPropertsetName` rule is kept for older clients; read `AutoPromptPropertysetName`. |
| `<Propertysets>` | `withPropertySets=true` | The property set rows applied to the folder; empty if none. |
| `<AccessList>` | `withSecurity=true` | The folder's access list: `InheritedSecurity`, `DateApplied`, `AppliedBy`, and one child per holder (`<Anonymous>`, `<DomainMembers>`, `<UserGroup>`, `<User>`) with its `Right`. |

### Error Response

```xml
<response success="false" error="Target folder cannot be found." errorCode="4041" />
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

Reports one folder as a `<folder>` element.

The four flags never change which folders come back, only how much is written about each: `withOwner`
adds a `<User>` child, `WithRules` a `<Rules>`, `withPropertySets` a `<Propertysets>` and
`withSecurity` an `<AccessList>`. With all four off the `<folder>` element has no children at all.

```javascript
const root = await call('GetFolder', {
  authenticationTicket: ticket,
  Path: '/Finance/Reports',
  WithRules: false,
  withPropertySets: false,
  withSecurity: false,
  withOwner: false
});

const folder = root.querySelector('folder');
console.log(folder.getAttribute('FolderID'), folder.getAttribute('Name'), folder.getAttribute('OwnerName'));
```

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

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4041` | no folder at that path, including one the caller may not see |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

A missing folder answers `4041`, as `GetFolderRules`, `GetFolderAIPreferences`, `GetFolderCatalog`, `GetFolderStatistics` and `DeleteFolder` do.

A call with no ticket is not automatically refused: it signs in as the anonymous user, so a folder in
a library flagged as anonymous can be read without authenticating. The writes in this group -
`CreateFolder`, `CreateFolder1`, `CreateHtmlDocument` - refuse it with `4010`.

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Folder not found | The specified path does not resolve to an existing folder. |
| Access denied | The user does not have read permission on the folder. |
| `SystemError:...` | An unexpected server-side error occurred. |

---