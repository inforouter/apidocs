# SearchRecycledItems1 API

Searches documents and folders across all users' Recycle Bins, one page at a time, with a sort order and the total number of matches. It takes the filters of [SearchRecycledItems](SearchRecycledItems.md), which returns every match at once, and returns the same item elements.

## Endpoint

```
/srv.asmx/SearchRecycledItems1
```

## Methods

- **GET** `/srv.asmx/SearchRecycledItems1?authenticationTicket=...&objectName=...&startingRowNumber=...&numberOfRows=...&sortBy=...&sortAscending=...`
- **POST** `/srv.asmx/SearchRecycledItems1` (form data)
- **SOAP** Action: `http://tempuri.org/SearchRecycledItems1`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. The user must be a system administrator. |
| `objectName` | string | No | Name of the recycled item. Matched exactly, unless it contains `*`, which stands for any run of characters (`*report*`, `*.pdf`). Empty matches any name. |
| `dateDeletedMinDate` | DateTime | No | Items deleted on or after this date. UTC values are converted to server local time. Empty for no lower bound. |
| `dateDeletedMaxDate` | DateTime | No | Items deleted on or before this date (the whole day is included). Empty for no upper bound. |
| `minSize` | long | No | Minimum total size in bytes. `0` or empty for no minimum. |
| `maxSize` | long | No | Maximum total size in bytes. `0` or empty for no maximum. |
| `deletedByUsername` | string | No | Items deleted by this user. Empty for all users. The user must exist. |
| `startingRowNumber` | int | Yes | Zero-based index of the first item to return. `0` starts from the beginning. |
| `numberOfRows` | int | Yes | Number of items per page. `0` or less returns every match, and `startingRowNumber` is then not used. |
| `sortBy` | string | No | `DateDeleted` (default), `Name`, `Size`, `OriginalLocation`, `DeletedBy`, `RecycleStatus` or `DateEmptied`. Not case-sensitive. |
| `sortAscending` | bool | Yes | `true` for ascending order, `false` for descending. |

## Response

### Success Response

`totalCount` is the number of items the whole search matches, not the number on the page. The child elements are the `<document>` and `<folder>` elements of [SearchRecycledItems](SearchRecycledItems.md).

```xml
<response success="true" error="" totalCount="801">
  <document Handler="..." Name="q3.pdf" DeletePath="\Finance\Reports" DeletedByName="Jane Doe" DateDeleted="2026-09-18T10:22:31.000Z" TotalSize="71994" ... />
  <folder Handler="..." Name="Old drafts" ... />
</response>
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

## Required Permissions

System administrators only.

## Example

### Request (POST)

```
POST /srv.asmx/SearchRecycledItems1 HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&objectName=*.pdf&startingRowNumber=0&numberOfRows=25&sortBy=DateDeleted&sortAscending=false
```

## Notes

- A `startingRowNumber` past the last match returns no items and the same `totalCount`.
- Items that tie on the sort column keep one order from page to page, so no item is repeated or skipped while the bin does not change. An item deleted or purged between two calls shifts the pages after it.
- Only items still in a recycle bin are searched; items already queued for purging are not.

## Related APIs

- [SearchRecycledItems](SearchRecycledItems.md) - The same search, returning every match at once
- [GetRecycleBinContent](GetRecycleBinContent.md) - List the current user's own Recycle Bin
- [RestoreRecycleBinItem](RestoreRecycleBinItem.md) - Restore an item by its handler
- [PurgeRecycleBinItem](PurgeRecycleBinItem.md) - Permanently delete an item by its handler

## Error Codes

| `errorCode` | When |
|---:|---|
| `4000` | `sortBy` is not one of the listed values |
| `4010` | `[901]` the ticket is expired or unknown |
| `4030` | The caller is not a system administrator |
| `4041` | `deletedByUsername` is not a user |
