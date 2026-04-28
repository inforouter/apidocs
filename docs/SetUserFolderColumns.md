# SetUserFolderColumns API

Saves the column layout and custom property set preference for the authenticated user on the specified folder. The setting applies only to the calling user and does not affect other users.

## Endpoint

```
/srv.asmx/SetUserFolderColumns
```

## Methods

- **GET** `/srv.asmx/SetUserFolderColumns?authenticationTicket=...&folderPath=...&columnIds=...&propertySetId=...`
- **POST** `/srv.asmx/SetUserFolderColumns` (form data)
- **SOAP** Action: `http://tempuri.org/SetUserFolderColumns`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `folderPath` | string | Yes | Full infoRouter path of the folder (e.g. `/Domain/Folder`) |
| `columnNames` | string | Yes | Comma-separated list of column names to display (e.g. `"ItemName,DocumentSize,ModificationDate"`). Pass an empty string to revert to the system/user global default |
| `propertySetId` | int | Yes | ID of the custom property set to display alongside the standard columns. Pass `0` for none |
| `sortBy` | string | Yes | Column name to sort by (e.g. `"ModificationDate"`). Pass an empty string for the default sort |
| `sortVector` | string | Yes | Sort direction: `"asc"`, `"desc"`, or empty string for the system default |
| `sortByPropertySetId` | int | Yes | Property set ID when sorting by a custom property field. Pass `0` when not sorting by a custom property |
| `sortByPropertySetColumnName` | string | Yes | Custom property field name when sorting by a custom property. Pass an empty string otherwise |

## Response

### Success

```xml
<root success="true" />
```

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

### Request (POST)

```
POST /srv.asmx/SetUserFolderColumns HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&folderPath=/MyDomain/Reports&columnNames=ItemName,DocumentSize,ModificationDate,OwnerName&propertySetId=5&sortBy=ModificationDate&sortVector=desc&sortByPropertySetId=0&sortByPropertySetColumnName=
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/SetUserFolderColumns"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <SetUserFolderColumns xmlns="http://tempuri.org/">
      <authenticationTicket>abc123</authenticationTicket>
      <folderPath>/MyDomain/Reports</folderPath>
      <columnNames>ItemName,DocumentSize,ModificationDate,OwnerName</columnNames>
      <propertySetId>5</propertySetId>
      <sortBy>ModificationDate</sortBy>
      <sortVector>desc</sortVector>
      <sortByPropertySetId>0</sortByPropertySetId>
      <sortByPropertySetColumnName></sortByPropertySetColumnName>
    </SetUserFolderColumns>
  </soap:Body>
</soap:Envelope>
```

## Error Codes

| Error | Description |
|-------|-------------|
| `[901] Session expired or Invalid ticket` | Invalid or expired authentication ticket |
| Folder not found | The specified `folderPath` does not exist |

## Notes

- The setting is saved per-user per-folder. Other users viewing the same folder are not affected.
- Unrecognised column names are silently ignored. Column name matching is case-insensitive.
- The column order in the response of `GetUserFolderColumns` reflects the order of names supplied here.
- Pass `propertySetId=0` to remove any previously saved property set association.
- When `sortByPropertySetId` is non-zero it takes precedence over `sortBy`; the sort column is treated as a custom property field.
- Pass `sortVector` as an empty string to use the system default sort direction.

## Related APIs

- `GetUserFolderColumns` — Read the current column layout preference for a folder
- `GetFoldersAndDocuments` — Browse folder contents
