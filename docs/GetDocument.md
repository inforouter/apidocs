# GetDocument API



Returns the full metadata and properties of a single document identified by its infoRouter path. Optional parameters control whether additional detail (custom property sets, access control list, owner, version history) is included in the response.



## Endpoint



```

/srv.asmx/GetDocument

```



## Methods



- **GET** `/srv.asmx/GetDocument?AuthenticationTicket=...&Path=...&withPropertySets=...&withSecurity=...&withOwner=...&withVersions=...`

- **POST** `/srv.asmx/GetDocument` (form data)

- **SOAP** Action: `http://tempuri.org/GetDocument`



## Parameters



| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1-Report.pdf`), or a short document ID path (`~D{id}` or `~D{id}.ext`, e.g. `~D1051` or `~D1051.pdf`). |
| `withPropertySets` | bool | Yes | `true` to include applied custom property set data (`<PropertySets>` child element). `false` to omit. |
| `withSecurity` | bool | Yes | `true` to include the access control list (`<AccessList>` child element). `false` to omit. |
| `withOwner` | bool | Yes | `true` to include owner user information as a child element. `false` to omit. |
| `withVersions` | bool | Yes | `true` to include document version history (`<Versions>` child element). `false` to omit. |



### Path Formats



Both full paths and short ID paths are accepted:



```

/Finance/Reports/Q1-2024-Report.pdf

~D1051

~D1051.pdf

```



> **Performance tip:** Set all boolean flags to `false` for the fastest, most compact response. Only enable the flags your application actually needs.



---



## Response



### Success Response



Returns a `<response>` root element with a single `<document>` child element containing the document's properties.



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

            CutoffDate=""

            RDDefId="0"

            ExpirationDate=""

            RegisterDate="2024-03-01"

            RegisteredBy="jsmith"

            DocTypeID="0"

            DocTypeName=""

            AIEnhanced="17"

            AIEnhancedAttributes="Summary, DocumentType"

            AIExtractConfidence="65"

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

            VersionCount="3"

            UserViewStatus="2">



    <!-- Included only when withPropertySets=true -->

    <PropertySets> ... </PropertySets>



    <!-- Included only when the description has a recorded author -->

    <DescriptionLog AppliedById="4" AppliedBy="System Administrator" DateApplied="2024-03-01T09:14:22.000Z" />



    <!-- Included only when withSecurity=true -->

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
| `Description` | Document description text. Who wrote it is in the `<DescriptionLog>` child element. |
| `UpdateInstructions` | Instructions for the next person checking in an update. |
| `CreationDate` | Date the document was created (`yyyy-MM-dd` format). |
| `ModificationDate` | Date the document was last modified. |
| `CheckoutDate` | Date the document was checked out, or empty if not checked out. |
| `CheckoutBy` | Display name of the user who has the document checked out, or empty. |
| `CheckoutByUserName` | Login name of the user who has the document checked out, or empty. |
| `Size` | File size in bytes. |
| `Type` | Human-readable document type / MIME description. |
| `PercentComplete` | Completion percentage (0-"100). |
| `CompletionDate` | Scheduled completion date, or empty if not set. |
| `Importance` | Importance level (integer). |
| `RetentionDate` | Calculated retain-until date, or empty if not set. |
| `DispositionDate` | Scheduled disposition date, or empty if not set. |
| `CutoffDate` | The date the retention clock is measured from, or empty if not set. `RetentionDate` and `DispositionDate` are calculated from it. Set with [SetDocumentCutoffDate](SetDocumentCutoffDate.md) and cleared with [RemoveDocumentCutoffDate](RemoveDocumentCutoffDate.md). |
| `RDDefId` | The retention and disposition schedule applied to this document, or `0` when none is. Pass it to [GetRandDScheduleInfo](GetRandDScheduleInfo.md) for the schedule itself. |
| `ExpirationDate` | Document expiration date, or empty if not set. |
| `RegisterDate` | Date the document was registered / first uploaded. |
| `RegisteredBy` | Login name of the user who registered the document. |
| `DocTypeID` | Document type definition ID (`0` if none assigned). |
| `DocTypeName` | Document type name, or empty if none assigned. |
| `AIEnhanced` | Which of the document's attributes infoRouter Connect produced, as a set of bits. `0` when none did. See [AIEnhanced](GetDocument.md#aienhanced) for the bit values. |
| `AIEnhancedAttributes` | The same thing named, e.g. `Summary, DocumentType`. Empty when `AIEnhanced` is `0`. Convenience only - test the bits, not the text. |
| `AIExtractConfidence` | How sure infoRouter Connect was about the weakest value it extracted into the document's property sets, as a percentage `0` - `100`. `0` means nothing needs reviewing. See [AIExtractConfidence](GetDocument.md#aiextractconfidence). |
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
| `UserViewStatus` | Integer indicating whether the current user has viewed the document. `0` = `NoView` (never viewed), `1` = `Changed` (viewed but the published version has since changed), `2` = `Viewed` (viewed the current published version). |



### Optional Child Elements



| Element | Enabled by | Description |
|---------|------------|-------------|
| `<DescriptionLog>` | always, where there is an author | Who last wrote the `Description`, and when. See below. |
| `<PropertySets>` | `withPropertySets=true` | Custom property set fields and values applied to the document. |
| `<AccessList>` | `withSecurity=true` | Access control list (users, groups, rights) for the document. |
| `<User>` | `withOwner=true` | Owner user details. |
| `<Versions>` | `withVersions=true` | Full version history list for the document. |



### `<DescriptionLog>`

A description can be typed by a person or produced by infoRouter Connect, and this is how a client
tells them apart - a Connect-written description is attributed to the system account. The same three
attributes [GetPropertySets](GetPropertySets.md), [GetDocumentSummary](GetDocumentSummary.md) and
[GetDocumentAbstract](GetDocumentAbstract.md) use.

| Attribute | Meaning |
|-----------|---------|
| `AppliedById` | ID of the user who last wrote the description. Use this to identify them - a username is a label, not a key. |
| `AppliedBy` | Their display name. |
| `DateApplied` | When the description was written, in universal format. |

The element is **absent** where there is no author to report: a document with no description, one
whose description was written before the author was recorded, and a document old enough that its
description is still kept in the warehouse rather than the database. Saying nothing is deliberate -
it beats reporting user `0`.

It sits beside the description rather than on it because `Description` is an attribute, and an XML
attribute cannot carry attributes of its own.

### Error Response



```xml

<response success="false" error="Document not found." />

```



---




### AIEnhanced

`AIEnhanced` says which of the document's attributes infoRouter Connect produced, one bit per attribute, so a listing can badge a document and say which parts a model wrote without reading each of them.

| Bit | Value | Attribute |
|-----|-------|-----------|
| 0 | `1` | `Summary` |
| 1 | `2` | `Description` |
| 2 | `4` | `Keywords` |
| 3 | `8` | `OcrText` |
| 4 | `16` | `DocumentType` |
| 5 | `32` | `Abstract` |
| 6 | `64` | `ExtractedData` - property set values read out of the document |
| 7 | `128` | `Markdown` |
| 8 | `256` | `RedactedText` |

`AIEnhanced="17"` is `1 | 16`: the summary and the document type. `AIEnhancedAttributes` names the same set for readability; a client should test the number.

A bit is set when Connect writes that attribute, and it **survives a correction**. The flag says where the attribute came from, not who edited it last: a person who fixes a generated summary keeps the flag, because a reader still wants to know it began as the model's work.

A bit is cleared only when the attribute itself is removed - there is then nothing left for it to describe:

| Bit | Cleared by |
|-----|------------|
| `Summary` | [SetDocumentSummary](SetDocumentSummary.md) with an empty summary |
| `Description` | [UpdateDocumentProperties](UpdateDocumentProperties.md) with an empty description |
| `Keywords` | replacing the generated keyword list with an empty one |
| `DocumentType` | `UpdateDocumentType` with `DocumentTypeID=0`, which removes the type |
| `ExtractedData` | removing the property set from the document. Emptying its fields does **not** clear it - the set is still there, and it is still a set the service filled in. A multi-row set loses the flag when its last row goes. |
| `Abstract`, `OcrText`, `Markdown`, `RedactedText` | nothing - these are produced by the server and there is no user operation that removes them |

Whether the values still need somebody's attention is a **separate** question, answered by [AIExtractConfidence](GetDocument.md#aiextractconfidence), which a review does clear. The two together say more than either alone: `ExtractedData` set with `AIExtractConfidence` of `0` means "extracted, and somebody has been through it", which no single flag could express.

A document that predates the flag reports `0`: nothing was produced for it, which is what `0` means. There is no "unknown" state.


### AIExtractConfidence

`AIExtractConfidence` says how sure infoRouter Connect was about the **weakest** value it extracted into the document's property sets, as a percentage from `0` to `100`. It is there so a listing can highlight a document whose extracted values are worth a person's attention.

The lowest of the fields Connect actually filled, because a property set is only as trustworthy as its worst answer and a listing has room for one number. A field a person had already answered does not count towards it - it carries no confidence of the service's at all.

`0` means **nothing to review**. Saving a document's property set values clears it to `0` - that save is what marks the document reviewed. The `ExtractedData` bit of [AIEnhanced](GetDocument.md#aienhanced) is **not** cleared with it: the values are still the model's work, they have just been checked. To tell a reviewed document from one nothing was ever extracted for, read the two together - `ExtractedData` set with a confidence of `0` is "extracted, and reviewed".

Suggested bands, as half-open intervals so they tile with no gap and nothing in two bands at once:

| Band | Range |
|------|-------|
| Poor | `1` - `69` |
| Low | `70` - `79` |
| Medium | `80` - `89` |
| High | `90` - `100` |

> There is no confidence threshold. Whatever Connect finds is written, however unsure it was, on the reasoning that a value a person is going to review is worth more than the blank it would otherwise leave. So the scale runs the whole way: a value of `12` means Connect wrote something it had very little confidence in, and that document is exactly the one to send somebody to.
>
> A written value never reports `0`, because `0` means "nothing here needs reviewing". The lowest a written value reports is `1`.

> A field Connect found nothing for is still left empty and carries no confidence, so it does not enter this number. A document where two fields were extracted at `95` and eight were found nothing for reports `95`. This value reports how good the answers are, not how many of them there are.

## Required Permissions



The calling user must have at least read access to the document. If the document does not exist or is not accessible to the user, an error response is returned.



---



## Example



### GET Request



```

GET /srv.asmx/GetDocument

  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

  &Path=/Finance/Reports/Q1-2024-Report.pdf

  &withPropertySets=false

  &withSecurity=false

  &withOwner=false

  &withVersions=false

HTTP/1.1

```



### GET Request (short ID path)



```

GET /srv.asmx/GetDocument

  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

  &Path=~D1051

  &withPropertySets=false

  &withSecurity=false

  &withOwner=false

  &withVersions=false

HTTP/1.1

```



### POST Request



```

POST /srv.asmx/GetDocument HTTP/1.1

Content-Type: application/x-www-form-urlencoded



AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

&Path=/Finance/Reports/Q1-2024-Report.pdf

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

    <tns:GetDocument>

      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>

      <tns:Path>/Finance/Reports/Q1-2024-Report.pdf</tns:Path>

      <tns:withPropertySets>false</tns:withPropertySets>

      <tns:withSecurity>false</tns:withSecurity>

      <tns:withOwner>false</tns:withOwner>

      <tns:withVersions>false</tns:withVersions>

    </tns:GetDocument>

  </soap:Body>

</soap:Envelope>

```



---



## Notes



- Both full infoRouter paths and short document ID paths (`~D{id}` or `~D{id}.ext`) are accepted for the `Path` parameter.

- If the document does not exist or the user does not have access, an error response is returned with `success="false"`.

- The `Path` attribute in the response element uses backslash separators and represents the **containing folder path**, not the full document path.

- Setting all boolean flags to `false` returns only the core document attributes, which is the fastest and most compact response.



---



## Related APIs



- [GetFoldersAndDocuments](GetFoldersAndDocuments.md) - List documents and sub-folders within a folder path

- [DocumentExists](DocumentExists.md) - Check whether a document exists and retrieve its CRC32 checksums

- [DownloadDocument](DownloadDocument.md) - Download the latest version of a document as a raw byte array

- [GetDocumentVersions](GetDocumentVersions.md) - Get the version history list for a document



---



## Error Codes



| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Document not found | The specified path does not resolve to an existing document. |
| `SystemError:...` | An unexpected server-side error occurred. |



---


