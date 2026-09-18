# SetUserFolderColumns API

Saves the column layout and custom property set preference for the authenticated user on the specified folder. The setting applies only to the calling user and does not affect other users.

> **Wrong values are refused.** A column name that is not a column, a `sortBy` that is not one
> either, a `sortVector` that is neither `asc` nor `desc`, and a property set id nothing matches are
> each refused and the stored layout is left alone. Until 9.0 all four were dropped without a word
> while the call answered `success="true"` - and if every column name was wrong the saved list was
> empty, which reads back as the three default columns, so the caller was shown a list it never
> asked for.
>

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
| `columnNames` | string | Yes | Comma-separated list of column names to display (e.g. `"ItemName,DocumentSize,ModificationDate"`). Required: an empty string is refused with HTTP 400 before the operation is reached. A name that is not a column is refused `4000`, and the refusal names every column there is. |
| `propertySetId` | int | Yes | ID of the custom property set to display alongside the standard columns. Pass `0` for none. An id no property set has is refused `4041`. The id is the `Id` attribute [GetPropertySetDefinition](GetPropertySetDefinition.md) reports. |
| `sortBy` | string | Yes | Column name to sort by (e.g. `"ModificationDate"`). Required: an empty string is refused with HTTP 400. A name that is not in `enum_IR.ColumnList` is refused `4000`. Not looked at at all when `sortByPropertySetId` is non-zero. |
| `sortVector` | string | Yes | Sort direction: `"asc"` or `"desc"`, read without regard to case. Required: an empty string is refused with HTTP 400. Anything else is refused `4000`. Until 9.0 the comparison was case-sensitive, so `"ASC"` was quietly stored as no sort direction at all. |
| `sortByPropertySetId` | int | Yes | Property set ID when sorting by a custom property field. Pass `0` when not sorting by a custom property. An id no property set has is refused `4041`. |
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

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | no folder at that path, including one the caller may not see |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

### Column names

`columnNames` is a comma separated list of these, matched without regard to case and trimmed of
spaces:

```
ItemName            ItemId              DocumentSize        DocumentFormat
ModificationDate    ApprovalStatus      ParentFolderName    LastVersionNumber
PercentComplete     CreationDate        ModifiedByName      OwnerName
FlowName            CheckedOutByName    StepNumber          StepName
CompletionDate      Importance          RetentionDefId      ClassificationLevel
DeclassifyOn        DowngradeOn         DispositionDate     LastIsoReview
NextIsoReview       DocumentTypeName    DocumentSource      DocumentLanguage
DocumentAuthor      ExpirationDate      ReleasedVersion     RegisterDate
CutOffDate          RetainUntil
```

Nothing else is a column, including several names that are in the `ColumnList` enum but have no
column definition behind them: `Description`, `CheckOutBy`, `Thumbnail`, `FolderID`, `TemplateID`,
`ViewDate`, `AssociatedDocumentCount`, `CustomPropertySet` and `Rank`. A name that is not on the
list above is refused `4000`, and the refusal carries the whole list.

`sortBy` takes any name from `enum_IR.ColumnList`, including the nine above - it is the sort key
rather than a column to show. `sortVector` is `asc` or `desc`, read without regard to case.

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

Saves the caller's own column and sort settings for one folder.

```javascript
await call('SetUserFolderColumns', {
  authenticationTicket: ticket,
  folderPath: '/Public/Reports',
  columnNames: 'ItemName,DocumentSize,ModificationDate',
  propertySetId: 0,
  sortBy: 'DocumentSize',
  sortVector: 'desc',                 // lower case only
  sortByPropertySetId: 0,
  sortByPropertySetColumnName: '-',   // required even when unused; any non-empty value
});
```

All five string parameters are declared without a question mark, so every one has to carry
something - including `sortByPropertySetColumnName` when there is no property set sort. The list
replaces what was saved rather than adding to it, and the column order is kept as given.

To sort by a property set column, set `sortByPropertySetId` to the property set and
`sortByPropertySetColumnName` to the field. That takes precedence: `sortBy` is not looked at, and
the answer from [GetUserFolderColumns](GetUserFolderColumns.md) reports `sortBy` as
`CustomPropertySet`.

## Notes

- The setting is saved per-user per-folder. Other users viewing the same folder are not affected.
- An unrecognised column name is refused `4000` and nothing is saved. Column name matching is case-insensitive.
- The column order in the response of `GetUserFolderColumns` reflects the order of names supplied here.
- Pass `propertySetId=0` to remove any previously saved property set association.
- When `sortByPropertySetId` is non-zero it takes precedence over `sortBy`; the sort column is treated as a custom property field.
- `sortVector` cannot be empty: the parameter is declared without a question mark. There is no way to store "no direction" through this operation - send `asc` or `desc`.

## Related APIs

- `GetUserFolderColumns` — Read the current column layout preference for a folder
- `GetFoldersAndDocuments` — Browse folder contents
