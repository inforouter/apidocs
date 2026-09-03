# GetNextSearchPage API



Retrieves the next page of results from a previously prepared search. This API must be called after a successful `Search` call, which stores the result set in the user's session. Each subsequent call to `GetNextSearchPage` advances the page cursor forward by one page. When the last page has been reached, the `LastPage` attribute in the response is set to `true`.



## Endpoint



```

/srv.asmx/GetNextSearchPage

```



## Methods



- **GET** `/srv.asmx/GetNextSearchPage?authenticationTicket=...&withrules=...&withPropertySets=...&withSecurity=...&withOwner=...&withVersions=...`

- **POST** `/srv.asmx/GetNextSearchPage` (form data)

- **SOAP** Action: `http://tempuri.org/GetNextSearchPage`



## Parameters



| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. Must belong to the same session that executed the `Search` call. |
| `withrules` | bool | Yes | `true` to include folder rules (`<Rules>` child element) in each folder result. `false` to omit. |
| `withPropertySets` | bool | Yes | `true` to include applied custom property set data (`<PropertySets>` child element) in each result. `false` to omit. |
| `withSecurity` | bool | Yes | `true` to include the access control list (`<AccessList>` child element) in each result. `false` to omit. |
| `withOwner` | bool | Yes | `true` to include owner user information as a child element in each result. `false` to omit. |
| `withVersions` | bool | Yes | `true` to include document version history (`<Versions>` child element) in each document result. `false` to omit. |



> **Note:** Setting `withrules`, `withPropertySets`, `withSecurity`, `withOwner`, and `withVersions` to `false` produces the most compact and fastest response. Only request additional data when your application needs it.



---



## Response



### Success Response -" Results Found



The root element carries pagination metadata as attributes, with one child element per result item (documents and folders interleaved as returned by the search engine).



> **The root element is `<response>`, not `<root>`.** The `<folder>` and `<document>` elements are
> the same ones [GetFolder](GetFolder.md) and [GetDocument](GetDocument.md) return, with the same
> attribute names - `Name` rather than `DocumentName`, `Size` rather than `DocumentSize`, `Type`
> rather than `MimeTypeDescription`, `VersionNumber` rather than `LastVersionNumber`. The example
> below shows a representative subset; [GetDocument](GetDocument.md) has the full attribute table.

```xml
<response success="true" error="" FirstPage="true" from="1" to="20" LastPage="false">

  <!-- Folder result -->
  <folder FolderID="1329"
          ParentID="1001"
          Name="ApiTests"
          Path="\Public\ApiTests"
          Description=""
          CreationDate="2026-08-19T15:34:41.250Z"
          OwnerName="System Administrator"
          DomainId="1001"
          ClassificationLevel="NoMarkings"
          ClassificationLevelId="0"
          DeclassifyOn=""
          DowngradeOn=""
          RDDefId="0"
          RetentionDate=""
          DispositionDate=""
          CutoffDate="">

    <!-- Included only when withOwner=true -->
    <User exists="true" UserID="4" FirstName="System" LastName="Administrator"
          Email="admin@example.com" MobileNumber="" Enabled="TRUE" UserName="sysadmin" />

    <!-- Included only when withrules=true -->
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
    <Propertysets />

    <!-- Included only when withSecurity=true -->
    <AccessList DateApplied="" AppliedBy="" InheritedSecurity="true">
      <Anonymous Right="2" Description="(Read)" />
    </AccessList>

  </folder>

  <!-- Document result. The full <document> element - see GetDocument for every attribute. -->
  <document DocumentID="1494"
            Name="Q1-2024-Report.pdf"
            Path="\Finance\Annual Reports"
            Description=""
            Size="204800"
            Type="PDF Document"
            CreationDate="2026-08-19T15:34:41.527Z"
            ModificationDate="2026-08-19T15:34:41.527Z"
            VersionNumber="3000000"
            PublishedVersionNumber="3000000"
            DocTypeID="0"
            DocTypeName=""
            AIEnhanced="17"
            AIEnhancedAttributes="Summary, DocumentType"
            OwnerId="4"
            OwnerName="System Administrator"
            FolderId="1329"
            Foldername="Annual Reports"
            DomainId="1001"
            DomainName="Finance"
            UserViewStatus="2">

    <!-- Present whenever the description carries an author stamp -->
    <DescriptionLog AppliedById="4" AppliedBy="System Administrator"
                    DateApplied="2026-09-02T13:02:48.250Z" />

    <!-- Included only when a full-text KEYWORDS search ranked this result -->
    <RankInfo Rank="95"
              FoundInPropertiesOrComments="FALSE"
              FoundInAttachments="FALSE"
              FoundInWorkflowHistory="FALSE"
              FoundInVersionNumber="3000000"
              FoundInPublishedVersion="TRUE" />

    <!-- Included only when withOwner=true -->
    <User exists="true" UserID="4" FirstName="System" LastName="Administrator"
          Email="admin@example.com" MobileNumber="" Enabled="TRUE" UserName="sysadmin" />

    <!-- Included only when withPropertySets=true -->
    <Propertysets />

    <!-- Included only when withSecurity=true -->
    <AccessList DateApplied="" AppliedBy="" InheritedSecurity="true"> ... </AccessList>

    <!-- Included only when withVersions=true. Child elements, not attributes. -->
    <Versions>
      <Version Number="3000000">
        <VersionAuthor>System Administrator</VersionAuthor>
        <VersionAuthorId>4</VersionAuthorId>
        <VersionSize>204800</VersionSize>
        <CheckSum>BFDB77A6</CheckSum>
        <DateCreated>2026-08-19T15:34:41.527Z</DateCreated>
        <DatePublished>2026-08-19T15:34:41.773Z</DatePublished>
        <Comment />
        <ApprovalStatus>NoResult</ApprovalStatus>
        <ApprovalDate />
      </Version>
    </Versions>

  </document>

  <!-- ... additional result items ... -->

</response>
```

### Root Element Attributes



| Attribute | Type | Description |
|-----------|------|-------------|
| `success` | string | `true` if the page was retrieved successfully. |
| `error` | string | Error message when `success` is `false`; otherwise empty. |
| `FirstPage` | string | `true` if this is the first page of results. |
| `LastPage` | string | `true` if this is the last page of results (no more items). |
| `from` | string | 1-based index of the first item on this page (e.g. `1`, `21`, `41`). |
| `to` | string | 1-based index of the last item on this page (e.g. `20`, `40`). |



### Success Response -" No Results Found



When the search produced zero matches, the response still has `success="true"` with all pagination positions set to zero:



```xml

<response success="true" error="" FirstPage="true" LastPage="true" from="0" to="0" />

```



### Document Element Attributes



Each `<document>` element in the response contains the standard document attributes (see `GetDocument` for the full attribute reference), plus a `UserViewStatus` attribute:

| Attribute | Type | Description |
|-----------|------|-------------|
| `UserViewStatus` | integer | Integer indicating whether the current user has viewed the document. `0` = `NoView` (never viewed), `1` = `Changed` (viewed but the published version has since changed), `2` = `Viewed` (viewed the current published version). |



### RankInfo Element (Full-Text Search Results)



When results include documents found via a `KEYWORDS` full-text search, each document element may contain a `<RankInfo>` child element:



| Attribute | Type | Description |
|-----------|------|-------------|
| `Rank` | integer | Relevance score assigned by the content search engine. Higher values indicate closer matches. |
| `FoundInPropertiesOrComments` | TRUE/FALSE | The match was found in the document's metadata properties or comments. |
| `FoundInAttachments` | TRUE/FALSE | The match was found in an attachment file. |
| `FoundInWorkflowHistory` | TRUE/FALSE | The match was found in the workflow history of the document. |
| `FoundInVersionNumber` | integer | The version number in which the match was found. `0` means the match is not version-specific. |
| `FoundInPublishedVersion` | TRUE/FALSE | The matching version is the published version of the document. |



Documents come back as the full `<document>` element. Since 9.0 it also carries `AIEnhanced` and
`AIEnhancedAttributes`, saying which of the document's attributes infoRouter Connect produced -
`0` when none did - and `AIExtractConfidence`, how sure it was about the weakest value it put in
a property set, as a percentage. See [AIEnhanced](GetDocument.md#aienhanced) and
[AIExtractConfidence](GetDocument.md#aiextractconfidence).

### Error Response



```xml

<response success="false" error="[ErrorCode] Error message" errorcode="4000" />

```



---



## Required Permissions



Any authenticated user may call this API. Results are filtered server-side to only include items the user has at least **Read** permission for. Read-only users may also call this API.



---



## Example



### GET Request



```

GET /srv.asmx/GetNextSearchPage?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

  &withrules=false

  &withPropertySets=false

  &withSecurity=false

  &withOwner=false

  &withVersions=false

HTTP/1.1

```



### POST Request



```

POST /srv.asmx/GetNextSearchPage HTTP/1.1

Content-Type: application/x-www-form-urlencoded



authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

&withrules=false

&withPropertySets=true

&withSecurity=false

&withOwner=true

&withVersions=false

```



### SOAP Request



```xml

<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"

               xmlns:tns="http://tempuri.org/">

  <soap:Body>

    <tns:GetNextSearchPage>

      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>

      <tns:withrules>false</tns:withrules>

      <tns:withPropertySets>false</tns:withPropertySets>

      <tns:withSecurity>false</tns:withSecurity>

      <tns:withOwner>false</tns:withOwner>

      <tns:withVersions>false</tns:withVersions>

    </tns:GetNextSearchPage>

  </soap:Body>

</soap:Envelope>

```



### Typical Paging Loop (Pseudo-code)



```

// Step 1: Prepare the search

Search(ticket, xmlcriteria, "MODIFICATIONDATE", false)



// Step 2: Page through all results

loop:

  response = GetNextSearchPage(ticket, false, false, false, false, false)

  process(response.items)

  if response.LastPage == "true": break

```



---



## Notes



- `GetNextSearchPage` must be called **after** a successful `Search` call. If `Search` has not been called in the current session, or the session search state has expired, the API returns an error.

- The page size is configured at the system level via the **Search Page Size** setting (typically 20 items per page). This value cannot be overridden per request.

- Each call to `GetNextSearchPage` advances the internal cursor by one page. To revisit earlier pages, use `GetPreviousSearchPage`.

- The first call after `Search` returns the **first page** (`FirstPage="true"`). Subsequent calls return subsequent pages until `LastPage="true"`.

- Search session state expires with the user session (30-day sliding window). If the session expires between calls, the API returns `"The Query has been expired."`.

- The `<RankInfo>` element is only present on document results when full-text `KEYWORDS` search was used and the content search engine assigned a relevance rank.

- Setting all boolean parameters to `false` produces the most compact response and is recommended when only document/folder identity and path information are needed.

- Both folders and documents can appear in the same result page, interleaved in the order returned by the search engine.



---



## Related APIs



- [Search](Search.md) - Prepare a search result set (must be called before this API)

- [GetPreviousSearchPage](GetPreviousSearchPage.md) - Retrieve the previous page of the prepared search results

- [GetFoldersAndDocuments](GetFoldersAndDocuments.md) - List documents and folders in a specific path without a search query

- [GetDocuments](GetDocuments.md) - Return documents in a specific folder path



---



## Error Codes



| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `The Query has been expired.` | No active search session found -" `Search` was not called, or the session expired. |
| `The Query results not found.` | The search result metadata is missing from the session (internal state inconsistency). |



---


