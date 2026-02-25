# GetRecentDocuments API

Returns the list of documents recently accessed by the current authenticated user. The list is capped by the system-wide **Recent Document Count** setting (default: 20). Only document items are returned — no folders. Optional flags control whether additional detail (property sets, security, owner, version history) is included for each document.

## Endpoint

```
/srv.asmx/GetRecentDocuments
```

## Methods

- **GET** `/srv.asmx/GetRecentDocuments?AuthenticationTicket=...&withpropertysets=...&withsecurity=...&withOwner=...&withVersions=...`
- **POST** `/srv.asmx/GetRecentDocuments` (form data)
- **SOAP** Action: `http://tempuri.org/GetRecentDocuments`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `withpropertysets` | bool | Yes | `true` to include applied custom property set data (`<PropertySets>` child element) for each document. `false` to omit. |
| `withsecurity` | bool | Yes | `true` to include the access control list (`<AccessList>` child element) for each document. `false` to omit. |
| `withOwner` | bool | Yes | `true` to include owner user information as a child element for each document. `false` to omit. |
| `withVersions` | bool | Yes | `true` to include document version history (`<Versions>` child element) for each document. `false` to omit. |

> **Note:** There is no `withrules` parameter — this API returns documents only; folders are never included.

> **Performance tip:** Set all boolean flags to `false` for the fastest, most compact response. Only enable the flags your application actually needs.

---

## Response

### Success Response

Returns a `<root>` element containing `<document>` child elements. Documents are returned in recency order (most recently accessed first), up to the system-configured maximum. If the user has no recent documents, the root element is returned with no children.

```xml
<root success="true">

  <document DocumentID="1051"
            Name="Q1-2024-Report.pdf"
            Path="\Finance\Reports"
            Description="Q1 financial summary"
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

  <document DocumentID="1088" Name="Budget-2024.xlsx" ...>
    ...
  </document>

</root>
```

### Optional Child Elements

| Element | Enabled by | Description |
|---------|------------|-------------|
| `<PropertySets>` | `withpropertysets=true` | Custom property set fields and values applied to the document. |
| `<AccessList>` | `withsecurity=true` | Access control list (users, groups, rights) for the document. |
| `<User>` | `withOwner=true` | Owner user details. |
| `<Versions>` | `withVersions=true` | Full version history list for the document. |

See `GetDocument` for the complete list of `<document>` element attributes and their descriptions.

### Error Response

```xml
<root success="false" error="[901] Session expired or Invalid ticket" />
```

---

## Required Permissions

Any authenticated user may call this API. The response always reflects the recent documents of the **currently authenticated user** — callers cannot query another user's recent documents list.

---

## Example

### GET Request — minimal (no extra detail)

```
GET /srv.asmx/GetRecentDocuments
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &withpropertysets=false
  &withsecurity=false
  &withOwner=false
  &withVersions=false
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetRecentDocuments HTTP/1.1
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
    <tns:GetRecentDocuments>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:withpropertysets>false</tns:withpropertysets>
      <tns:withsecurity>false</tns:withsecurity>
      <tns:withOwner>false</tns:withOwner>
      <tns:withVersions>false</tns:withVersions>
    </tns:GetRecentDocuments>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- The recent documents list belongs to the **currently authenticated user** only. There is no parameter to specify a different user.
- The list is capped at the system-wide **Recent Document Count** setting (default: **20**). This limit is configured by the system administrator and cannot be overridden per call.
- Documents are returned in recency order — the most recently accessed document appears first.
- Only documents are returned; this API never includes folder items. Use `GetFavorites` or `GetDownloadQue` if you need an API that returns both folders and documents.
- If the user has no recent documents, the response is `<root success="true" />` with no child elements.
- Items are returned with their current properties at the time of the call. Documents that have since been deleted or that the user no longer has access to may be absent.

---

## Related APIs

- [GetFavorites](GetFavorites) - Get the current user's favorites list (documents and folders)
- [GetDownloadQue](GetDownloadQue) - Get the current user's download queue (documents and folders)
- [GetDocument](GetDocument) - Get the full properties of a single document by path
- [GetFoldersAndDocuments](GetFoldersAndDocuments) - Get folders and documents within a specific folder path

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| User has been deleted | The authenticated user account no longer exists. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/GetRecentDocuments*
