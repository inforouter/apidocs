# GetDocuments API

Returns the full metadata and properties of every document in the specified folder path. Optional flags control whether additional detail (custom property sets, access control list, owner, version history) is included for each document in the response. Documents are returned sorted by name in ascending order.

## Endpoint

```
/srv.asmx/GetDocuments
```

## Methods

- **GET** `/srv.asmx/GetDocuments?AuthenticationTicket=...&Path=...&withPropertySets=...&withSecurity=...&withOwner=...&withVersions=...`
- **POST** `/srv.asmx/GetDocuments` (form data)
- **SOAP** Action: `http://tempuri.org/GetDocuments`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the folder whose documents should be returned (e.g. `/Finance/Reports`). Must be a folder path, not a document path. |
| `withPropertySets` | bool | Yes | `true` to include applied custom property set data (`<PropertySets>` child element) for each document. `false` to omit. |
| `withSecurity` | bool | Yes | `true` to include the access control list (`<AccessList>` child element) for each document. `false` to omit. |
| `withOwner` | bool | Yes | `true` to include owner user information as a child element for each document. `false` to omit. |
| `withVersions` | bool | Yes | `true` to include full version history (`<Versions>` child element) for each document. `false` to omit. |

> **Performance tip:** Set all boolean flags to `false` for the fastest, most compact response. Only enable the flags your application actually needs. For folders with many documents, enabling `withVersions=true` can significantly increase response time and size.

---

## Response

### Success Response

Returns a `<response>` root element with one `<document>` child element per document found in the folder. Documents are sorted alphabetically by name (ascending). If the folder exists but contains no documents, the root element has no children.

```xml
<response success="true" error="">

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

    <!-- Included only when withPropertySets=true -->
    <PropertySets> ... </PropertySets>

    <!-- Included only when withSecurity=true -->
    <AccessList DateApplied="2024-03-01" AppliedBy="jsmith" InheritedSecurity="true"> ... </AccessList>

    <!-- Included only when withOwner=true -->
    <User UserID="7" UserName="jsmith" FullName="John Smith" ... />

    <!-- Included only when withVersions=true -->
    <Versions> ... </Versions>

  </document>

  <document DocumentID="1052"
            Name="Q2-2024-Report.pdf"
            ...>
    ...
  </document>

</response>
```

### Document Element Attributes

| Attribute | Description |
|-----------|-------------|
| `DocumentID` | Unique integer ID of the document. |
| `Name` | Document file name. |
| `Path` | Backslash-separated infoRouter path to the containing folder. |
| `Description` | Document description text. |
| `UpdateInstructions` | Instructions for the next person checking in an update. |
| `CreationDate` | Date the document was created (`yyyy-MM-dd` format). |
| `ModificationDate` | Date the document was last modified. |
| `CheckoutDate` | Date the document was checked out, or empty if not checked out. |
| `CheckoutBy` | Display name of the user who has the document checked out, or empty. |
| `CheckoutByUserName` | Login name of the user who has the document checked out, or empty. |
| `Size` | File size in bytes. |
| `Type` | Human-readable document type / MIME description. |
| `PercentComplete` | Completion percentage (0–100). |
| `CompletionDate` | Scheduled completion date, or empty if not set. |
| `Importance` | Importance level (integer). |
| `RetentionDate` | Calculated retain-until date, or empty if not set. |
| `DispositionDate` | Scheduled disposition date, or empty if not set. |
| `ExpirationDate` | Document expiration date, or empty if not set. |
| `RegisterDate` | Date the document was registered / first uploaded. |
| `RegisteredBy` | Login name of the user who registered the document. |
| `DocTypeID` | Document type definition ID (`0` if none assigned). |
| `DocTypeName` | Document type name, or empty if none assigned. |
| `VersionNumber` | Latest (working) version number. |
| `PublishedVersionNumber` | Published version number (`0` if no published version exists). |
| `PublishingRule` | Publishing rule name (e.g. `PublishingNotRequired`, `MustBePublished`). |
| `OwnerName` | Login name of the document owner. |
| `WorkflowId` | Active workflow ID (`0` if not in a workflow). |
| `WorkflowName` | Active workflow name, or empty. |
| `WorkflowStepNumber` | Current workflow step number. |
| `WorkflowStepName` | Current workflow step name, or empty. |
| `Author` | Author metadata field. |
| `Language` | Language metadata field. |
| `Source` | Source metadata field. |
| `ApprovalStatus` | Approval status string (e.g. `Approved`, `Pending`). |
| `ClassificationLevel` | Classification level name (`NoMarkings`, `Confidential`, `Secret`, etc.). |
| `ClassificationLevelId` | Integer code for the classification level (0–4). |
| `DeclassifyOn` | Scheduled declassification date, or empty if not set. |
| `DomainId` | Integer ID of the domain/library containing this document. |
| `DomainName` | Name of the domain/library. |
| `DowngradeOn` | Scheduled downgrade date, or empty if not set. |
| `FolderId` | Integer ID of the containing folder. |
| `Foldername` | Name of the containing folder. |
| `IsShortcut` | `TRUE` if this document is a shortcut to another document; otherwise `FALSE`. |
| `TargetDocumentId` | ID of the target document if this is a shortcut; otherwise `0`. |
| `LastISOReviewDate` | Last ISO review date, or empty if not set. |
| `NextISOReviewDate` | Next ISO review date, or empty if not set. |
| `OwnerId` | Integer user ID of the document owner. |
| `RegisterById` | Integer user ID of the user who registered the document. |
| `TemplateID` | Template ID used to create the document (`0` if not template-based). |
| `VersionCount` | Total number of versions for this document. |

### Optional Child Elements per Document

| Element | Enabled by | Description |
|---------|------------|-------------|
| `<PropertySets>` | `withPropertySets=true` | Custom property set fields and values applied to the document. |
| `<AccessList>` | `withSecurity=true` | Access control list (users, groups, rights) for the document. |
| `<User>` | `withOwner=true` | Owner user details. |
| `<Versions>` | `withVersions=true` | Full version history list for the document. |

### Error Response

```xml
<response success="false" error="Folder not found." />
```

---

## Required Permissions

The calling user must have at least read access to the folder specified by `Path`. Only documents that the user has permission to view are returned. If the folder does not exist or the user does not have access to it, an error response is returned.

---

## Example

### GET Request

```
GET /srv.asmx/GetDocuments
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports
  &withPropertySets=false
  &withSecurity=false
  &withOwner=false
  &withVersions=false
HTTP/1.1
```

### GET Request (with all details)

```
GET /srv.asmx/GetDocuments
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports
  &withPropertySets=true
  &withSecurity=true
  &withOwner=true
  &withVersions=true
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetDocuments HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance/Reports
&withPropertySets=false
&withSecurity=false
&withOwner=false
&withVersions=false
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetDocuments>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:Path>/Finance/Reports</tns:Path>
      <tns:withPropertySets>false</tns:withPropertySets>
      <tns:withSecurity>false</tns:withSecurity>
      <tns:withOwner>false</tns:withOwner>
      <tns:withVersions>false</tns:withVersions>
    </tns:GetDocuments>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- `Path` must refer to an existing folder. Document paths are not accepted.
- Documents are returned sorted alphabetically by name in ascending order.
- If the folder exists but contains no documents, the response is `<response success="true" error="" />` with no child elements.
- For large folders, enabling `withVersions=true` can significantly increase both response time and response payload size. Use only when version history is required.
- Sub-folder contents are not included — only the immediate documents in the specified folder are returned. Use `GetFoldersAndDocuments` to retrieve both folders and documents in a single call.
- To retrieve documents by page rather than all at once, use `GetDocumentsByPage`.
- To retrieve a compact list (short form) without full document properties, use `GetDocuments1`.

---

## Related APIs

- [GetDocument](GetDocument) - Get the full properties of a single document by path
- [GetFoldersAndDocuments](GetFoldersAndDocuments) - List both sub-folders and documents within a folder path with full detail options
- [GetDocuments1](GetDocuments1) - Get the list of documents in a folder in short form
- [GetDocumentsByPage](GetDocumentsByPage) - Get a paginated list of documents in a folder
- [GetDocumentVersions](GetDocumentVersions) - Get the version history for a specific document

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Folder not found | The specified path does not resolve to an existing folder. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/GetDocuments*
