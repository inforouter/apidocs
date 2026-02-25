# GetCheckedoutDocuments API

Returns the list of documents currently checked out by the authenticated user. Only documents belonging to the calling user's active checkouts are included -" no folder items are returned. Results are sorted by document name ascending.

To retrieve checked-out documents for a **different** user (requires elevated permissions), use `GetCheckedoutDocumentsByUser`.

## Endpoint

```
/srv.asmx/GetCheckedoutDocuments
```

## Methods

- **GET** `/srv.asmx/GetCheckedoutDocuments?AuthenticationTicket=...&withpropertysets=...&withsecurity=...&withOwner=...&withVersions=...`
- **POST** `/srv.asmx/GetCheckedoutDocuments` (form data)
- **SOAP** Action: `http://tempuri.org/GetCheckedoutDocuments`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `withpropertysets` | bool | Yes | `true` to include applied custom property set data (`<PropertySets>` child element) in each document result. `false` to omit. |
| `withsecurity` | bool | Yes | `true` to include the access control list (`<AccessList>` child element) in each document result. `false` to omit. |
| `withOwner` | bool | Yes | `true` to include owner user information as a child element in each document result. `false` to omit. |
| `withVersions` | bool | Yes | `true` to include document version history (`<Versions>` child element) in each document result. `false` to omit. |

> **Performance tip:** Set all boolean flags to `false` for the fastest, most compact response. Only enable the flags your application actually needs.

---

## Response

### Success Response

Returns a `<response>` root element with `<document>` child elements -" one per checked-out document -" sorted by document name ascending. If the current user has no checked-out documents, the response contains no child elements.

```xml
<response success="true" error="">

  <document DocumentID="1051"
            Name="Q1-2024-Report.pdf"
            Path="\Finance\Reports"
            Description="Q1 financial summary"
            UpdateInstructions=""
            CreationDate="2024-03-01"
            ModificationDate="2024-06-15"
            CheckoutDate="2026-02-10"
            CheckoutBy="John Smith"
            CheckoutByUserName="jsmith"
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
| `CheckoutDate` | Date the document was checked out. Populated for all results since only checked-out documents are returned. |
| `CheckoutBy` | Display name of the user who checked out the document. |
| `CheckoutByUserName` | Login name of the user who checked out the document. |
| `Size` | File size in bytes. |
| `Type` | Human-readable document type / MIME description. |
| `PercentComplete` | Completion percentage (0-"100). |
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
| `ClassificationLevelId` | Integer code for the classification level (0-"4). |
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

### Optional Child Elements

| Element | Enabled by | Description |
|---------|------------|-------------|
| `<PropertySets>` | `withpropertysets=true` | Custom property set fields and values applied to the document. |
| `<AccessList>` | `withsecurity=true` | Access control list (users, groups, rights) for the document. |
| `<User>` | `withOwner=true` | Owner user details. |
| `<Versions>` | `withVersions=true` | Full version history list for the document. |

### Error Response

```xml
<response success="false" error="[900] Authentication failed" />
```

---

## Required Permissions

Any authenticated user may call this API. The response contains only documents checked out by the **calling user** -" there is no way to query another user's checkouts with this method. Use `GetCheckedoutDocumentsByUser` for that purpose (requires elevated permissions).

---

## Example

### GET Request

```
GET /srv.asmx/GetCheckedoutDocuments
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &withpropertysets=false
  &withsecurity=false
  &withOwner=false
  &withVersions=false
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetCheckedoutDocuments HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
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
    <tns:GetCheckedoutDocuments>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:withpropertysets>false</tns:withpropertysets>
      <tns:withsecurity>false</tns:withsecurity>
      <tns:withOwner>false</tns:withOwner>
      <tns:withVersions>false</tns:withVersions>
    </tns:GetCheckedoutDocuments>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Only documents checked out by the **currently authenticated user** are returned. This API cannot be used to query another user's checkouts.
- No folder items are included in the response, only `<document>` elements.
- Results are sorted by document name ascending.
- If the user has no checked-out documents, the response contains an empty `<response>` element with `success="true"`.
- The `CheckoutDate`, `CheckoutBy`, and `CheckoutByUserName` attributes will always be populated for the returned documents since only checked-out documents are included.

---

## Related APIs

- [GetCheckedoutDocumentsByUser](GetCheckedoutDocumentsByUser.md) - Get checked-out documents for a specified user (requires elevated permissions)
- [GetAuthoredDocuments](GetAuthoredDocuments.md) - Get documents authored by a specified user
- [GetISOReviewAssignments](GetISOReviewAssignments.md) - Get documents assigned to a user for ISO review

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `SystemError:...` | An unexpected server-side error occurred. |

---
