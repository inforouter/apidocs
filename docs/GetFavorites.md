# GetFavorites API

Returns the list of documents and folders that the current authenticated user has marked as **favorites**. The favorites list is a personal per-user collection for quick access to frequently used items. The response uses the same full-detail folder and document element format as `GetFoldersAndDocuments`. Optional flags control whether additional detail (folder rules, property sets, security, owner, version history) is included for each item.

To add items to the favorites list use `AddToFavorites`. To remove items use `RemoveFromFavorites`.

## Endpoint

```
/srv.asmx/GetFavorites
```

## Methods

- **GET** `/srv.asmx/GetFavorites?AuthenticationTicket=...&withrules=...&withpropertysets=...&withsecurity=...&withOwner=...&withVersions=...`
- **POST** `/srv.asmx/GetFavorites` (form data)
- **SOAP** Action: `http://tempuri.org/GetFavorites`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `withrules` | bool | Yes | `true` to include folder rules (`<Rules>` child element) for each folder in the list. `false` to omit. Has no effect on document items. |
| `withpropertysets` | bool | Yes | `true` to include applied custom property set data (`<PropertySets>` child element) for each item. `false` to omit. |
| `withsecurity` | bool | Yes | `true` to include the access control list (`<AccessList>` child element) for each item. `false` to omit. |
| `withOwner` | bool | Yes | `true` to include owner user information as a child element for each item. `false` to omit. |
| `withVersions` | bool | Yes | `true` to include document version history (`<Versions>` child element) for each document. `false` to omit. Has no effect on folder items. |

> **Performance tip:** Set all boolean flags to `false` for the fastest, most compact response. Only enable the flags your application actually needs.

---

## Response

### Success Response

Returns a `<root>` element with `<folder>` and `<document>` child elements — folders first, then documents sorted by name ascending. If the favorites list is empty, the root element is returned with no children.

```xml
<root success="true">

  <!-- Folder items in the favorites list -->
  <folder FolderID="42"
          ParentID="10"
          Name="Q1 Reports"
          Path="/Finance/Reports/Q1 Reports"
          Description="First quarter reports"
          CreationDate="2024-01-15"
          OwnerName="jsmith"
          DomainId="3"
          ClassificationLevel="NoMarkings"
          ClassificationLevelId="0"
          DeclassifyOn=""
          DowngradeOn=""
          RDDefId="0"
          RetentionDate=""
          DispositionDate=""
          CutoffDate="">

    <!-- Included only when withrules=true -->
    <Rules>
      <Rule Name="AllowableFileTypes"  Value="*" />
      <Rule Name="Checkins"            Value="allows" />
      <Rule Name="Checkouts"           Value="allows" />
      <Rule Name="DocumentDeletes"     Value="allows" />
      <Rule Name="FolderDeletes"       Value="allows" />
      <Rule Name="NewDocuments"        Value="allows" />
      <Rule Name="NewFolders"          Value="allows" />
      <Rule Name="ClassifiedDocuments" Value="disallows" />
    </Rules>

    <!-- Included only when withpropertysets=true -->
    <PropertySets> ... </PropertySets>

    <!-- Included only when withsecurity=true -->
    <AccessList DateApplied="2024-01-15" AppliedBy="admin" InheritedSecurity="false"> ... </AccessList>

    <!-- Included only when withOwner=true -->
    <User UserID="7" UserName="jsmith" FullName="John Smith" ... />

  </folder>

  <!-- Document items in the favorites list -->
  <document DocumentID="1051"
            Name="Q1-2024-Report.pdf"
            Path="\Finance\Reports"
            Description="Q1 financial summary"
            CreationDate="2024-03-01"
            ModificationDate="2024-06-15"
            Size="204800"
            Type="PDF Document"
            VersionNumber="3"
            PublishedVersionNumber="3"
            OwnerName="jsmith"
            ...>

    <!-- Included only when withpropertysets=true -->
    <PropertySets> ... </PropertySets>

    <!-- Included only when withsecurity=true -->
    <AccessList DateApplied="2024-03-01" AppliedBy="jsmith" InheritedSecurity="true"> ... </AccessList>

    <!-- Included only when withOwner=true -->
    <User UserID="7" UserName="jsmith" FullName="John Smith" ... />

    <!-- Included only when withVersions=true -->
    <Versions> ... </Versions>

  </document>

</root>
```

### Optional Child Elements

| Element | Enabled by | Applies to |
|---------|------------|------------|
| `<Rules>` | `withrules=true` | Folders only |
| `<PropertySets>` | `withpropertysets=true` | Folders and documents |
| `<AccessList>` | `withsecurity=true` | Folders and documents |
| `<User>` | `withOwner=true` | Folders and documents |
| `<Versions>` | `withVersions=true` | Documents only |

See `GetFoldersAndDocuments` for the complete list of `<folder>` and `<document>` element attributes and their descriptions.

### Error Response

```xml
<root success="false" error="[901] Session expired or Invalid ticket" />
```

---

## Required Permissions

Any authenticated user may call this API. The response always reflects the favorites list of the **currently authenticated user** — callers cannot query another user's favorites.

---

## Example

### GET Request — minimal (no extra detail)

```
GET /srv.asmx/GetFavorites
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &withrules=false
  &withpropertysets=false
  &withsecurity=false
  &withOwner=false
  &withVersions=false
HTTP/1.1
```

### GET Request — with full detail

```
GET /srv.asmx/GetFavorites
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &withrules=true
  &withpropertysets=true
  &withsecurity=true
  &withOwner=true
  &withVersions=true
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetFavorites HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&withrules=false
&withpropertysets=false
&withsecurity=false
&withOwner=false
&withVersions=false
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetFavorites>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:withrules>false</tns:withrules>
      <tns:withpropertysets>false</tns:withpropertysets>
      <tns:withsecurity>false</tns:withsecurity>
      <tns:withOwner>false</tns:withOwner>
      <tns:withVersions>false</tns:withVersions>
    </tns:GetFavorites>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- The favorites list belongs to the **currently authenticated user** only. There is no parameter to specify a different user.
- Folders appear before documents in the response. Documents are sorted alphabetically by name in ascending order.
- If the favorites list is empty, the response is `<root success="true" />` with no child elements.
- `withrules` applies only to folder items — it has no effect on document elements.
- `withVersions` applies only to document items — it has no effect on folder elements.
- Items are returned with their current properties at the time of the call. Documents or folders that have since been deleted or that the user no longer has access to may be absent from the response.
- Setting all boolean flags to `false` returns only the core attributes for each item, which is the fastest and most compact response.

---

## Related APIs

- [AddToFavorites](AddToFavorites.md) - Add a document or folder to the current user's favorites list
- [RemoveFromFavorites](RemoveFromFavorites.md) - Remove a document or folder from the current user's favorites list
- [GetDownloadQue](GetDownloadQue.md) - Get the current user's download queue (documents and folders)
- [GetRecentDocuments](GetRecentDocuments.md) - Get recently accessed documents for the current user
- [GetFoldersAndDocuments](GetFoldersAndDocuments.md) - Get folders and documents within a specific folder path

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| User has been deleted | The authenticated user account no longer exists. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/GetFavorites*
