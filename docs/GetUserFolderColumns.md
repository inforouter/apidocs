# GetUserFolderColumns API

Returns the effective column layout and custom property set preference saved for the authenticated user on the specified folder. Falls back to the user's global preference, then to the system default, when no folder-specific setting exists.

## Endpoint

```
/srv.asmx/GetUserFolderColumns
```

## Methods

- **GET** `/srv.asmx/GetUserFolderColumns?authenticationTicket=...&folderPath=...`
- **POST** `/srv.asmx/GetUserFolderColumns` (form data)
- **SOAP** Action: `http://tempuri.org/GetUserFolderColumns`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `folderPath` | string | Yes | Full infoRouter path of the folder (e.g. `/Domain/Folder`) |

## Response

### Success

```xml
<root success="true">
  <propertySetId>5</propertySetId>
  <sortBy>ItemName</sortBy>
  <sortVector>asc</sortVector>
  <sortByPropertySetId>0</sortByPropertySetId>
  <sortByPropertySetColumnName></sortByPropertySetColumnName>
  <columns>
    <column>ItemName</column>
    <column>DocumentSize</column>
    <column>DocumentFormat</column>
    <column>ModificationDate</column>
    <column>OwnerName</column>
  </columns>
</root>
```

| Field | Description |
|-------|-------------|
| `<propertySetId>` | ID of the custom property set associated with this folder view. `0` means no custom property set |
| `<sortBy>` | Column name used for sorting (e.g. `ItemName`, `ModificationDate`) |
| `<sortVector>` | Sort direction: `asc`, `desc`, or empty string (system default) |
| `<sortByPropertySetId>` | Property set ID used for sorting when sorting by a custom property field. `0` when not applicable |
| `<sortByPropertySetColumnName>` | Custom property field name used for sorting. Empty when not applicable |
| `<column>` | Internal column name (language-independent). See the column name table below |

### Error

```xml
<root success="false" error="[901]Session expired or Invalid ticket" />
```

## Column Names

| Name | Description |
|------|-------------|
| `ItemName` | Document or folder name |
| `ItemId` | Internal item ID |
| `DocumentSize` | File size |
| `DocumentFormat` | File format / extension |
| `ApprovalStatus` | Approval/publishing status |
| `ParentFolderName` | Name of the containing folder |
| `LastVersionNumber` | Most recent version number |
| `PercentComplete` | Completion percentage |
| `CreationDate` | Date the item was created |
| `ModifiedByName` | Name of the last modifier |
| `OwnerName` | Document owner name |
| `FlowName` | Active workflow name |
| `CheckedOutByName` | Name of the user who checked out the document |
| `StepNumber` | Current workflow step number |
| `StepName` | Current workflow step name |
| `CompletionDate` | Workflow or task completion date |
| `Importance` | Document importance level |
| `RetentionDefId` | Retention schedule ID |
| `ClassificationLevel` | Security classification level |
| `DeclassifyOn` | Declassification date |
| `DowngradeOn` | Downgrade date |
| `DispositionDate` | Retention disposition date |
| `LastIsoReview` | Date of the last ISO review |
| `NextIsoReview` | Date of the next scheduled ISO review |
| `DocumentTypeName` | Document type name |
| `DocumentSource` | Document source |
| `DocumentLanguage` | Document language |
| `DocumentAuthor` | Document author |
| `ExpirationDate` | Document expiration date |
| `ReleasedVersion` | Published (released) version number |
| `RegisterDate` | Date the document was registered |
| `CutOffDate` | Records cut-off date |
| `RetainUntil` | Retain-until date |
| `ModificationDate` | Date the item was last modified |

## Required Permissions

- User must be authenticated.

## Example Requests

### Request (GET)

```
GET /srv.asmx/GetUserFolderColumns?authenticationTicket=abc123&folderPath=/MyDomain/Reports HTTP/1.1
```

### Request (POST)

```
POST /srv.asmx/GetUserFolderColumns HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&folderPath=/MyDomain/Reports
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetUserFolderColumns"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetUserFolderColumns xmlns="http://tempuri.org/">
      <authenticationTicket>abc123</authenticationTicket>
      <folderPath>/MyDomain/Reports</folderPath>
    </GetUserFolderColumns>
  </soap:Body>
</soap:Envelope>
```

## Error Codes

| Error | Description |
|-------|-------------|
| `[901] Session expired or Invalid ticket` | Invalid or expired authentication ticket |
| Folder not found | The specified `folderPath` does not exist |

## Notes

- The returned column list reflects the effective preference: folder-specific user setting → user global setting → system default, in that priority order.
- When no setting has been saved for the user and folder, the system default columns are returned (`ItemName`, `DocumentSize`, `DocumentFormat`, `ModificationDate`, `OwnerName`).
- `propertySetId="0"` means no custom property set is associated.

## Related APIs

- `SetUserFolderColumns` — Save the column layout and property set preference for a folder
- `GetFoldersAndDocuments` — Browse folder contents
