# GetFoldersAndDocuments API

Returns the complete list of immediate sub-folders and documents in the specified infoRouter path. Both folders and documents are returned in a single response -" folders first, followed by documents sorted by name ascending. Optional parameters control how much detail is included for each item, allowing callers to request property sets, security lists, owner information, and version history as needed.

## Endpoint

```
/srv.asmx/GetFoldersAndDocuments
```

## Methods

- **GET** `/srv.asmx/GetFoldersAndDocuments?authenticationTicket=...&Path=...&withrules=...&withpropertysets=...&withsecurity=...&withOwner=...&withVersions=...`
- **POST** `/srv.asmx/GetFoldersAndDocuments` (form data)
- **SOAP** Action: `http://tempuri.org/GetFoldersAndDocuments`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the parent folder whose contents to list (e.g. `/Finance/Reports`). The path must point to an existing folder the user can access. |
| `withrules` | bool | Yes | `true` to include folder rules (`<Rules>` child element) in each folder result. `false` to omit. Has no effect on document items. |
| `withpropertysets` | bool | Yes | `true` to include applied custom property set data (`<PropertySets>` child element) in each result. `false` to omit. |
| `withsecurity` | bool | Yes | `true` to include the access control list (`<AccessList>` child element) in each result. `false` to omit. |
| `withOwner` | bool | Yes | `true` to include owner user information as a child element in each result. `false` to omit. |
| `withVersions` | bool | Yes | `true` to include document version history (`<Versions>` child element) in each document result. `false` to omit. Has no effect on folder items. |

> **Performance tip:** Set all boolean flags to `false` for the fastest, most compact response. Only enable the flags your application actually consumes.

---

## Response

### Success Response

Folders appear first, followed by documents. All items are immediate children of the specified path -" the listing is **not** recursive.

```xml
<root success="true">

  <!-- -"--"- Folder items -"--"- -->
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
    <AccessList DateApplied="2024-01-15" AppliedBy="admin" InheritedSecurity="false">
      <DomainMembers Right="4" Description="(Add &amp; Read)" />
      <UserGroup DomainName="Finance" GroupName="Managers" Right="6" Description="(Full Control)" />
      <User DomainName="Finance" UserName="jsmith" Right="6" Description="(Full Control)" />
    </AccessList>

    <!-- Included only when withOwner=true -->
    <User UserID="7" UserName="jsmith" FullName="John Smith" ... />

  </folder>

  <!-- -"--"- Document items -"--"- -->
  <document DocumentID="1051"
            Name="Q1-2024-Report.pdf"
            Path="\Finance\Reports"
            Description="Q1 financial summary"
            UpdateInstructions=""
            CreationDate="2024-03-01"
            ModificationDate="2024-06-15"
            CheckoutDate=""
            CheckoutBy=""
            CheckoutByUserName=""
            Size="204800"
            Type="PDF Document"
            PercentComplete="100"
            CompletionDate=""
            Importance="1"
            RetentionDate=""
            DispositionDate=""
            ExpirationDate=""
            RegisterDate="2024-03-01"
            RegisteredBy="jsmith"
            DocTypeID="0"
            DocTypeName=""
            VersionNumber="3"
            PublishedVersionNumber="3"
            PublishingRule="PublishingNotRequired"
            OwnerName="jsmith"
            WorkflowId="0"
            WorkflowName=""
            WorkflowStepNumber="0"
            WorkflowStepName=""
            Author=""
            Language=""
            Source=""
            ApprovalStatus="Approved"
            ClassificationLevel="NoMarkings"
            ClassificationLevelId="0"
            DeclassifyOn=""
            DomainId="3"
            DomainName="Finance"
            DowngradeOn=""
            FolderId="10"
            Foldername="Reports"
            IsShortcut="FALSE"
            TargetDocumentId="0"
            LastISOReviewDate=""
            NextISOReviewDate=""
            OwnerId="7"
            RegisterById="7"
            TemplateID="0"
            VersionCount="3">

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

### Folder Element Attributes

| Attribute | Description |
|-----------|-------------|
| `FolderID` | Unique integer ID of the folder. |
| `ParentID` | Integer ID of the parent folder. |
| `Name` | Folder name. |
| `Path` | Full infoRouter path to this folder. |
| `Description` | Folder description text. |
| `CreationDate` | Date the folder was created (`yyyy-MM-dd` format). |
| `OwnerName` | Login name of the folder owner. |
| `DomainId` | Integer ID of the domain/library containing this folder. |
| `ClassificationLevel` | Classification level name (`NoMarkings`, `Declassified`, `Confidential`, `Secret`, `TopSecret`). |
| `ClassificationLevelId` | Integer code for the classification level (0-"4). |
| `DeclassifyOn` | Scheduled declassification date, or empty if not set. |
| `DowngradeOn` | Scheduled downgrade date, or empty if not set. |
| `RDDefId` | Retention & Disposition definition ID (`0` if none assigned). |
| `RetentionDate` | Calculated retain-until date, or empty if not set. |
| `DispositionDate` | Scheduled disposition date, or empty if not set. |
| `CutoffDate` | Cutoff date, or empty if not set. |

### Document Element Attributes

| Attribute | Description |
|-----------|-------------|
| `DocumentID` | Unique integer ID of the document. |
| `Name` | Document file name (including extension). |
| `Path` | Path of the parent folder (backslash-separated). |
| `Description` | Document description text. |
| `UpdateInstructions` | Update instructions stored on the document. |
| `CreationDate` | Date the document was created (`yyyy-MM-dd` format). |
| `ModificationDate` | Date the document was last modified (`yyyy-MM-dd` format). |
| `CheckoutDate` | Date the document was checked out, or empty if not checked out. |
| `CheckoutBy` | Full name of the user who has the document checked out. |
| `CheckoutByUserName` | Login name of the user who has the document checked out, or `SYSTEMLOCK` if locked by the system. |
| `Size` | File size in bytes. |
| `Type` | MIME type description (e.g. `PDF Document`, `Microsoft Word Document`). |
| `PercentComplete` | Completion percentage (0-"100). |
| `CompletionDate` | Date the document was marked complete, or empty if not set. |
| `Importance` | Importance level: `0`=Low, `1`=Normal, `2`=High, `3`=Vital. |
| `RetentionDate` | Calculated retain-until date, or empty if not set. |
| `DispositionDate` | Scheduled disposition date, or empty if not set. |
| `ExpirationDate` | Expiration date, or empty if not set. |
| `RegisterDate` | Date the document was registered/uploaded. |
| `RegisteredBy` | Name of the user who registered the document. |
| `DocTypeID` | Document type integer ID (`0` if no type assigned). |
| `DocTypeName` | Document type name, or empty if none. |
| `VersionNumber` | Latest version number. |
| `PublishedVersionNumber` | Published version number (`0` if no version is published). |
| `PublishingRule` | Publishing rule name (`PublishingNotRequired`, `PublishingRequired`, etc.). |
| `OwnerName` | Login name of the document owner. |
| `WorkflowId` | Active workflow definition ID (`0` if no active workflow). |
| `WorkflowName` | Active workflow name, or empty if none. |
| `WorkflowStepNumber` | Current workflow step number (`0` if no active workflow). |
| `WorkflowStepName` | Current workflow step name, or empty if none. |
| `Author` | Document author metadata field. |
| `Language` | Document language metadata field. |
| `Source` | Document source metadata field. |
| `ApprovalStatus` | Approval status name (`Approved`, `Rejected`, `Pending`, etc.). |
| `ClassificationLevel` | Classification level name. |
| `ClassificationLevelId` | Integer code for the classification level (0-"4). |
| `DeclassifyOn` | Scheduled declassification date, or empty if not set. |
| `DomainId` | Integer ID of the domain/library containing this document. |
| `DomainName` | Name of the domain/library (top-level path component). |
| `DowngradeOn` | Scheduled downgrade date, or empty if not set. |
| `FolderId` | Integer ID of the parent folder. |
| `Foldername` | Name of the immediate parent folder. |
| `IsShortcut` | `TRUE` if this document is a shortcut to another document. |
| `TargetDocumentId` | Integer ID of the target document if `IsShortcut=TRUE`, otherwise `0`. |
| `LastISOReviewDate` | Date of the last ISO review, or empty if not set. |
| `NextISOReviewDate` | Date of the next scheduled ISO review, or empty if not set. |
| `OwnerId` | Integer user ID of the document owner. |
| `RegisterById` | Integer user ID of the user who registered the document. |
| `TemplateID` | Template ID used to create the document (`0` if not template-created). |
| `VersionCount` | Total number of versions for this document. |

### Optional Child Elements

| Element | Applies to | Enabled by | Description |
|---------|-----------|------------|-------------|
| `<Rules>` | Folders only | `withrules=true` | Folder-level rules: AllowableFileTypes, Checkins, Checkouts, DocumentDeletes, FolderDeletes, NewDocuments, NewFolders, ClassifiedDocuments. |
| `<PropertySets>` | Folders and documents | `withpropertysets=true` | Custom property set rows applied to the item. |
| `<AccessList>` | Folders and documents | `withsecurity=true` | Access control list showing group and user rights (0=No Access through 6=Full Control). |
| `<User>` (owner) | Folders and documents | `withOwner=true` | Owner user details (UserID, UserName, FullName, etc.). |
| `<Versions>` | Documents only | `withVersions=true` | Full version history of the document. |

### Error Response

```xml
<root success="false" error="[ErrorCode] Error message" />
```

---

## Required Permissions

The calling user must have at least **List** permission on the specified folder to retrieve its contents. Documents and sub-folders to which the user has no access are automatically excluded from the response. Read-only users may call this API.

---

## Example

### GET Request -" minimal response

```
GET /srv.asmx/GetFoldersAndDocuments?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports
  &withrules=false
  &withpropertysets=false
  &withsecurity=false
  &withOwner=false
  &withVersions=false
HTTP/1.1
```

### POST Request -" with property sets and owner

```
POST /srv.asmx/GetFoldersAndDocuments HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance/Reports
&withrules=false
&withpropertysets=true
&withsecurity=false
&withOwner=true
&withVersions=false
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetFoldersAndDocuments>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:Path>/Finance/Reports</tns:Path>
      <tns:withrules>false</tns:withrules>
      <tns:withpropertysets>false</tns:withpropertysets>
      <tns:withsecurity>false</tns:withsecurity>
      <tns:withOwner>false</tns:withOwner>
      <tns:withVersions>false</tns:withVersions>
    </tns:GetFoldersAndDocuments>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- The listing is **not recursive** -" only the immediate children (sub-folders and documents) of the specified `Path` are returned.
- Folders appear before documents in the response, regardless of sort order.
- Documents are sorted by name in ascending order.
- The `Path` parameter is case-insensitive and leading/trailing slashes are normalized automatically.
- If the path does not exist or the user has no access to it, an error response is returned rather than an empty list.
- Items to which the user has no access are silently excluded from the results.
- `withrules` only affects folder items; it has no effect on document elements.
- `withVersions` only affects document items; it has no effect on folder elements.
- For large folders, enabling `withpropertysets`, `withsecurity`, `withOwner`, or `withVersions` can significantly increase response size and latency. Use only what is needed.
- Date fields use `yyyy-MM-dd` format. Empty string indicates the field is not set.
- For paged browsing of large folders, consider using `GetFoldersAndDocumentsByPage` or `GetFoldersAndDocumentsByPage2` instead.

---

## Related APIs

- [GetFoldersAndDocuments1](GetFoldersAndDocuments1.md) - Returns the same contents in short form (name, path, and ID only)
- [GetFoldersAndDocumentsByPage](GetFoldersAndDocumentsByPage.md) - Returns the first page (up to 20 items) of folder contents
- [GetFoldersAndDocumentsByPage2](GetFoldersAndDocumentsByPage2.md) - Returns folder contents page by page in enhanced form
- [GetFolders](GetFolders.md) - Returns only the sub-folders of the specified path
- [GetDocuments](GetDocuments.md) - Returns only the documents in the specified path
- [Search](Search.md) - Find documents and folders across the system using search criteria

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Folder not found` | The specified `Path` does not exist or is not accessible to the calling user. |

---
