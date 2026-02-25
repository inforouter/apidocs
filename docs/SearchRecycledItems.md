# SearchRecycledItems API

Searches documents and folders across the entire infoRouter Recycle Bin (all users) using optional filter criteria. Returns matching recycled items with the same attributes as `GetRecycleBinContent`, including the `Handler` value needed to purge or restore individual items. This is an administrator-only API that provides system-wide visibility into all recycled content. Use it to audit deletion activity, identify items to recover, or build administrative cleanup tooling.

## Endpoint

```
/srv.asmx/SearchRecycledItems
```

## Methods

- **GET** `/srv.asmx/SearchRecycledItems?authenticationTicket=...&objectName=...&dateDeletedMinDate=...&dateDeletedMaxDate=...&minSize=...&maxSize=...&deletedByUsername=...`
- **POST** `/srv.asmx/SearchRecycledItems` (form data)
- **SOAP** Action: `http://tempuri.org/SearchRecycledItems`

## Parameters

All filter parameters are optional. When all filters are omitted the API returns all recycled items across all users.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. The authenticated user must be a system administrator. |
| `objectName` | string | No | Filter by the name of the recycled item (document or folder name). Supports partial (substring) matching. Leave empty to return items of any name. |
| `dateDeletedMinDate` | DateTime | No | Filter to items deleted on or after this date/time. Format: `yyyy-MM-dd` or `yyyy-MM-ddTHH:mm:ss`. UTC values are automatically converted to server local time. Leave empty for no lower bound. |
| `dateDeletedMaxDate` | DateTime | No | Filter to items deleted on or before this date/time. Format: `yyyy-MM-dd` or `yyyy-MM-ddTHH:mm:ss`. UTC values are automatically converted to server local time. Leave empty for no upper bound. |
| `minSize` | long | No | Filter to items whose total size is at least this many bytes. `0` or omitted means no minimum size filter. |
| `maxSize` | long | No | Filter to items whose total size is at most this many bytes. `0` or omitted means no maximum size filter. |
| `deletedByUsername` | string | No | Filter to items deleted by the specified username. Leave empty to include items deleted by any user. The username must match an existing infoRouter user. |

---

## Response

### Success Response

Returns a `<response>` element with `success="true"` containing zero or more `<document>` and `<folder>` child elements matching the filter criteria.

```xml
<response success="true" error="">
  <document
    Name="Q1-2024-Report.pdf"
    DateDeleted="2024-06-15T10:23:45.000Z"
    TotalSize="204800"
    OriginalFolderId="4521"
    DeletePath="/Finance/Reports/Q1-2024-Report.pdf"
    DeletedById="12"
    DeletedByName="jsmith"
    RecycledItemStatusId="0"
    RecycledItemStatus="In User Recycle Bin"
    Handler="D9871" />
  <folder
    Name="OldProjects"
    DateDeleted="2024-06-14T08:10:00.000Z"
    TotalSize="2048000"
    OriginalFolderId="3200"
    DeletePath="/Finance/OldProjects"
    DeletedById="15"
    DeletedByName="admin"
    RecycledItemStatusId="1"
    RecycledItemStatus="In System Recycle Bin"
    Handler="F4312" />
</response>
```

### Response Attribute Reference

| Attribute | Description |
|-----------|-------------|
| `Name` | Original name of the deleted document or folder. |
| `DateDeleted` | UTC date and time the item was deleted, in ISO 8601 format (`yyyy-MM-ddTHH:mm:ss.fffZ`). |
| `TotalSize` | Total size in bytes (rounded integer). For folders this includes all content at deletion time. |
| `OriginalFolderId` | Internal ID of the folder the item was deleted from. |
| `DeletePath` | Full infoRouter path the item occupied before deletion. |
| `DeletedById` | Internal user ID of the user who deleted the item. |
| `DeletedByName` | Username of the user who deleted the item. |
| `RecycledItemStatusId` | Integer status: `0` = In User Recycle Bin, `1` = In System Recycle Bin. |
| `RecycledItemStatus` | Localized string label for the status. |
| `Handler` | Item handler for use with `PurgeRecycleBinItem` and `RestoreRecycleBinItem`. Format: `D{id}` for documents, `F{id}` for folders (e.g. `D9871`, `F4312`). |

### No Results Response

When no items match the filter criteria the response contains no child elements:

```xml
<response success="true" error="" />
```

### Error Response

```xml
<response success="false" error="Only the system administrator can perform this operation." />
```

---

## Required Permissions

**System administrators only.** Regular users and domain managers cannot call this API. Attempting to call it as a non-administrator immediately returns a permission error without performing any search.

---

## Example

### GET Request -" all recycled items (no filters)

```
GET /srv.asmx/SearchRecycledItems
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
HTTP/1.1
```

### GET Request -" items deleted by a specific user in a date range

```
GET /srv.asmx/SearchRecycledItems
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &deletedByUsername=jsmith
  &dateDeletedMinDate=2024-06-01
  &dateDeletedMaxDate=2024-06-30
HTTP/1.1
```

### POST Request -" filter by name and size

```
POST /srv.asmx/SearchRecycledItems HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&objectName=Report
&minSize=100000
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:SearchRecycledItems>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:objectName>Report</tns:objectName>
      <tns:dateDeletedMinDate>2024-06-01</tns:dateDeletedMinDate>
      <tns:dateDeletedMaxDate>2024-06-30</tns:dateDeletedMaxDate>
      <tns:minSize>0</tns:minSize>
      <tns:maxSize>0</tns:maxSize>
      <tns:deletedByUsername>jsmith</tns:deletedByUsername>
    </tns:SearchRecycledItems>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- **Admin Only**: The authenticated user must be a system administrator. The check is enforced server-side.
- **System-Wide Search**: Unlike `GetRecycleBinContent` which is scoped to a single user's bin, `SearchRecycledItems` searches across all users' recycle bins and the system recycle bin.
- **All Filters Optional**: Calling with only `authenticationTicket` returns every recycled item in the system. Add filters to narrow results.
- **ObjectName is Substring Match**: The `objectName` filter matches any item whose name contains the given string; it is not a full-name-only match.
- **Date Filters**: Both `dateDeletedMinDate` and `dateDeletedMaxDate` can be sent in UTC -" the server automatically converts them to local time for comparison. Either bound can be omitted independently.
- **Size Filters**: `minSize` and `maxSize` are in bytes. A value of `0` is treated as "no filter" for that bound. For folder items the size represents the total content size at the time of deletion.
- **deletedByUsername Must Exist**: If the username provided does not match any existing user, an error is returned rather than an empty result.
- **Handler for Actions**: The `Handler` attribute in each result can be passed directly to `PurgeRecycleBinItem` or `RestoreRecycleBinItem`.

---

## Related APIs

- [GetRecycleBinContent](GetRecycleBinContent.md) - List all items in the current user's own Recycle Bin (no filters, non-admin)
- [PurgeRecycleBinItem](PurgeRecycleBinItem.md) - Permanently delete a single Recycle Bin item by handler (admin only)
- [RestoreRecycleBinItem](RestoreRecycleBinItem.md) - Restore a Recycle Bin item to its original or a specified folder location
- [EmptyRecycleBin](EmptyRecycleBin.md) - Permanently delete all items in the current user's Recycle Bin

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Only the system administrator can perform this operation` | The authenticated user is not a system administrator. |
| User not found | The `deletedByUsername` value does not match any existing infoRouter user. |
| `SystemError:...` | An unexpected server-side error occurred. |

---
