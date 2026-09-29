# GetMyDocumentsAndFolders API

Returns all documents and folders owned by the currently authenticated user, across all locations in the infoRouter system. Optional flags control the level of detail included for each item.

## Endpoint

```
/srv.asmx/GetMyDocumentsAndFolders
```

## Methods

- **GET** `/srv.asmx/GetMyDocumentsAndFolders?authenticationTicket=...&withrules=...&withpropertysets=...&withsecurity=...&withOwner=...&withVersions=...`
- **POST** `/srv.asmx/GetMyDocumentsAndFolders` (form data)
- **SOAP** Action: `http://tempuri.org/GetMyDocumentsAndFolders`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `withrules` | bool | Yes | If `true`, includes folder rules (allowed file types, checkout/checkin policies, etc.) for each returned folder. |
| `withpropertysets` | bool | Yes | If `true`, includes applied custom property set values for each item. |
| `withsecurity` | bool | Yes | If `true`, includes the access control list (ACL) for each item. |
| `withOwner` | bool | Yes | If `true`, includes owner user information for each item. |
| `withVersions` | bool | Yes | If `true`, includes full version history for each returned document. |

---

## Response

### Success Response

The owned folders come first, one `<folder>` element each, then the owned documents, one `<document>`
element each - both children of `<response>`, which has no attributes of its own besides `success` and
`error`. With all five flags `false`:

```xml
<response success="true" error="">
  <folder FolderID="1170" ParentID="1001" Name="My Project" Path="\Projects\My Project"
          Description="" CreationDate="2024-01-15T09:00:00.000Z" OwnerName="John Smith" DomainId="1001"
          ClassificationLevel="NoMarkings" ClassificationLevelId="0" DeclassifyOn="" DowngradeOn=""
          RDDefId="0" RetentionDate="" DispositionDate="" CutoffDate="" />
  <folder FolderID="1171" ...same attributes... />
  <document DocumentID="1051" Name="Proposal.docx" Path="\Projects\My Project" Description="" UpdateInstructions=""
            CreationDate="2024-03-01T09:00:00.000Z" ModificationDate="2024-06-15T14:30:00.000Z"
            CheckoutDate="" CheckoutBy="" CheckoutByUserName="" Size="204800" Type="Office Document"
            PercentComplete="0" CompletionDate="" Importance="Normal" RetentionDate="" DispositionDate=""
            CutoffDate="" RDDefId="0" ExpirationDate="" RegisterDate="2024-03-01T09:00:00.000Z"
            RegisteredBy="John Smith" DocTypeID="0" DocTypeName="" AIEnhanced="0" AIExtractConfidence="0"
            VersionNumber="3000000" PublishedVersionNumber="3000000" PublishingRule="LATEST"
            OwnerName="John Smith" WorkflowId="0" WorkflowName="" WorkflowStepNumber="0" WorkflowStepName=""
            Author="" Language="" Source="" ApprovalStatus="NoResult" ClassificationLevel="NoMarkings"
            ClassificationLevelId="0" DeclassifyOn="" DomainId="1001" DomainName="Projects" DowngradeOn=""
            FolderId="1170" Foldername="My Project" IsShortcut="FALSE" TargetDocumentId="0"
            LastISOReviewDate="" NextISOReviewDate="" OwnerId="7" RegisterById="7" TemplateID="0"
            VersionCount="3" UserViewStatus="2" />
  <document DocumentID="1052" ...same attributes... />
</response>
```

A user who owns nothing gets `<response success="true" error="" />`.

### `<folder>` element

The element [GetFolder](GetFolder.md) returns - see its [attribute table](GetFolder.md#folder-attributes)
and [child elements](GetFolder.md#child-elements). `withOwner` adds a `<User>` child, `withrules` a
`<Rules>`, `withpropertysets` a `<Propertysets>` and `withsecurity` an `<AccessList>`. `withVersions`
does not apply to folders.

### `<document>` element

The element [GetDocument](GetDocument.md) returns - see its
[attribute table](GetDocument.md#document-element-attributes) and
[optional child elements](GetDocument.md#optional-child-elements). `withOwner` adds a `<User>` child,
`withpropertysets` the property sets, `withsecurity` an `<AccessList>` and `withVersions` the version
history; a `<DescriptionLog>` is written whenever the description has a recorded author. `withrules`
does not apply to documents. The element carries `AIEnhanced` and `AIExtractConfidence` - see
[AIEnhanced](GetDocument.md#aienhanced) and [AIExtractConfidence](GetDocument.md#aiextractconfidence).

### Error Response

```xml
<response success="false" error="Session expired or invalid ticket" errorCode="4010" />
```

---

## Required Permissions

The calling user must be authenticated. Only items owned by the current user are returned -" no special permissions are required beyond being logged in.

---

## Example

### GET Request (items only, no extra details)

```
GET /srv.asmx/GetMyDocumentsAndFolders
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &withrules=false
  &withpropertysets=false
  &withsecurity=false
  &withOwner=false
  &withVersions=false
HTTP/1.1
```

### GET Request (with version history and property sets)

```
GET /srv.asmx/GetMyDocumentsAndFolders
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &withrules=false
  &withpropertysets=true
  &withsecurity=false
  &withOwner=false
  &withVersions=true
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetMyDocumentsAndFolders HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
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
    <tns:GetMyDocumentsAndFolders>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:withrules>false</tns:withrules>
      <tns:withpropertysets>false</tns:withpropertysets>
      <tns:withsecurity>false</tns:withsecurity>
      <tns:withOwner>false</tns:withOwner>
      <tns:withVersions>false</tns:withVersions>
    </tns:GetMyDocumentsAndFolders>
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

Lists what the calling user owns, in the same full `<folder>` and `<document>` shape as
`GetFoldersAndDocuments` and with the same five flags. There is no `Path`: the answer is about who
the caller is, not where they are looking.

```javascript
const root = await call('GetMyDocumentsAndFolders', {
  authenticationTicket: ticket,
  withrules: false,
  withpropertysets: false,
  withsecurity: false,
  withOwner: false,
  withVersions: false
});

console.log(root.querySelectorAll(':scope > document').length, 'documents owned');
```

A caller with no ticket at all is the anonymous user, and the anonymous user owns nothing, so this is
one of the operations that refuses an unticketed call outright rather than answering for anonymous.

## Notes

- Returns items across all locations in infoRouter where the authenticated user is the owner.
- "Ownership" is determined by the document/folder owner field, not merely by having access.
- Setting all flags to `false` gives the fastest response (metadata only).
- Setting `withVersions=true` on large document sets may significantly increase response size and processing time.
- For a user's favorite items, use `GetFavorites`. For checked-out documents, use `GetCheckedoutDocuments`.
- Each `<document>` element includes a `UserViewStatus` integer attribute: `0` = never viewed, `1` = viewed but the published version has since changed, `2` = viewed the current published version. See `GetDocument` for the full attribute reference.

---

## Related APIs

- [GetFavorites](GetFavorites.md) - Get the current user's favorite items
- [GetCheckedoutDocuments](GetCheckedoutDocuments.md) - Get documents checked out by the current user
- [GetRecentDocuments](GetRecentDocuments.md) - Get recently accessed documents

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all - unlike the folder listings, this operation does not answer for the anonymous user |


| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `SystemError:...` | An unexpected server-side error occurred. |

---