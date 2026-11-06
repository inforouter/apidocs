# SearchRecycledItems1 API

Searches the deleted documents and folders of the whole instance, one page at a time, sorted, with the total number of matches. `searchIn` says where to look: the users' recycle bins, the system recycle bin, or both (the default); `path` narrows it to the items deleted from one library or folder. It takes the filters of [SearchRecycledItems](SearchRecycledItems.md), which always searches both bins and returns every match at once, and returns the same item elements. See [What happens to a deleted document or folder](rules/recycle-bin.md#the-system-recycle-bin-and-searching-it).

## Endpoint

```
/srv.asmx/SearchRecycledItems1
```

## Methods

- **GET** `/srv.asmx/SearchRecycledItems1?authenticationTicket=...&objectName=...&startingRowNumber=...&numberOfRows=...&sortBy=...&sortAscending=...&searchIn=...&path=...`
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
| `searchIn` | int | No | Where to search. `0` or empty: everywhere, the users' recycle bins and the system recycle bin. `1`: the system recycle bin only, the items that have been emptied there. `2`: the users' recycle bins only, the items no one has emptied yet. Any other value is refused with `4000`. SOAP callers that leave it out get `0`. |
| `path` | string | No | A library or folder path, such as `/Accounting/` or `/Accounting/Invoices`: only the items deleted from there or from any folder below it. Empty or `/` for anywhere. `/` and `\` are both separators; a trailing one makes no difference. A path that matches nothing is not an error: the answer is empty. |

## Response

### Success Response

`totalCount` is the number of items the whole search matches, not the number on the page. The child elements are the `<document>` and `<folder>` elements of [SearchRecycledItems](SearchRecycledItems.md). `RecycledItemStatusId` on each one says where it is: `0` in a user's recycle bin, `1` in the system recycle bin.

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

### Request (GET): what has been emptied into the system recycle bin, oldest first

```
GET /srv.asmx/SearchRecycledItems1?authenticationTicket=abc123&startingRowNumber=0&numberOfRows=100&sortBy=DateEmptied&sortAscending=true&searchIn=1
```

Each item's `Handler` then goes to [PurgeRecycleBinItem](PurgeRecycleBinItem.md) to purge it, or to
[RestoreRecycleBinItem](RestoreRecycleBinItem.md) to bring it back.

### Request (GET): what was deleted from the Accounting library, in either recycle bin

`path=/Accounting/Invoices/` would keep what was deleted from the Invoices folder and its subfolders.

```
GET /srv.asmx/SearchRecycledItems1?authenticationTicket=abc123&startingRowNumber=0&numberOfRows=25&sortBy=DateDeleted&sortAscending=false&path=/Accounting/
```

## Notes

- A `startingRowNumber` past the last match returns no items and the same `totalCount`.
- Items that tie on the sort column keep one order from page to page, so no item is repeated or skipped while the bin does not change. An item deleted or purged between two calls shifts the pages after it.
- Only items still in a recycle bin are searched; items already queued for purging are not, whatever `searchIn` says.
- `searchIn=1` is how an administrator works through the system recycle bin alone, for instance to purge what [EmptyAllUserRecycleBins](EmptyAllUserRecycleBins.md) moved there, item by item, without touching what users can still restore themselves. [SearchRecycledItems](SearchRecycledItems.md) has no such filter. (8.7 did this in its user interface, by opening the system recycle bin as a library.)
- The numbers of `searchIn` are its own, not the `RecycledItemStatusId` values: `searchIn=1` finds the items with `RecycledItemStatusId="1"`, but `searchIn=2` finds those with `RecycledItemStatusId="0"`, and `0` is everywhere.
- `searchIn` and `path` are checked after the caller is found to be a system administrator, so anyone else is refused with `4030` whatever they say.
- `path` matches where each item was **deleted from**, which is recorded with the item when it is deleted: its library, and `DeletePath`, the folder it was in. It is not where the item is now: a deleted item sits in a recycle bin.
  - **A library alone** (`/Accounting/`) is matched on the library, so a library renamed after the delete is found by its current name.
  - **A folder** (`/Accounting/Invoices`) is matched on `DeletePath` as it was at the delete: that folder and every folder below it, on whole folder names (`/Accounting/Inv` does not match `/Accounting/Invoices`). When the library still exists, the search is kept to it as well.
  - **A library that no longer exists** is matched on `DeletePath` too, so what was deleted from a library that was deleted afterwards can still be found.
  - The item **at** the path is not included, only what was in it: a deleted folder `/Accounting/Invoices` is found with `path=/Accounting/`, since its `DeletePath` is `\Accounting`.
  - Whether letter case must match depends on the database collation: on the usual SQL Server and MySQL setups it does not; on Oracle it does. `DeletePath` is cut at 255 characters, so a path longer than that matches nothing.

## Related APIs

- [SearchRecycledItems](SearchRecycledItems.md) - The same search in both bins, returning every match at once
- [EmptyAllUserRecycleBins](EmptyAllUserRecycleBins.md) - Empty every user's Recycle Bin into the system recycle bin
- [GetRecycleBinContent](GetRecycleBinContent.md) - List the current user's own Recycle Bin
- [RestoreRecycleBinItem](RestoreRecycleBinItem.md) - Restore an item by its handler
- [PurgeRecycleBinItem](PurgeRecycleBinItem.md) - Permanently delete an item by its handler

## Error Codes

| `errorCode` | When |
|---:|---|
| `4000` | `sortBy` is not one of the listed values, or `searchIn` is not `0`, `1` or `2` |
| `4010` | `[901]` the ticket is expired or unknown |
| `4030` | The caller is not a system administrator |
| `4041` | `deletedByUsername` is not a user |

## Since

- **9.0 (2026-10-09):** the call.
- **9.0 (2026-11-06):** `searchIn`, to search one recycle bin only. Before, it always searched both.
- **9.0 (2026-11-06):** `path`, to search the items deleted from one library or folder.
