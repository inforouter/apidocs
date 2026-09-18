# GetRecycleBinContent API

Returns the list of all documents and folders currently in the Recycle Bin of the authenticated user. Each item includes its original path, deletion date, size, the user who deleted it, and a handler value that can be used with `PurgeRecycleBinItem` or `RestoreRecycleBinItem`. Use this API to inspect the contents of a user's Recycle Bin before deciding whether to restore or permanently delete items.

> This reads **the caller's own** recycled items.
> [SearchRecycledItems](SearchRecycledItems.md) with no filters reads everything recycled on the
> instance, which is a very much larger list. The two are not different views of the same set.

## Endpoint

```

/srv.asmx/GetRecycleBinContent

```

## Methods

- **GET** `/srv.asmx/GetRecycleBinContent?AuthenticationTicket=...`

- **POST** `/srv.asmx/GetRecycleBinContent` (form data)

- **SOAP** Action: `http://tempuri.org/GetRecycleBinContent`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. The recycle bin returned is always that of the user who owns this ticket. |

---

## Response

### Success Response

Returns a `<response>` element with `success="true"` containing zero or more `<document>` and `<folder>` child elements, one per recycled item.

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

    DeletedById="12"

    DeletedByName="jsmith"

    RecycledItemStatusId="0"

    RecycledItemStatus="In User Recycle Bin"

    Handler="F4312" />

</response>

```

### Response Attribute Reference

| Attribute | Description |
|-----------|-------------|
| `Name` | Original name of the deleted document or folder. |
| `DateDeleted` | UTC date and time the item was deleted, in ISO 8601 format (`yyyy-MM-ddTHH:mm:ss.fffZ`). |
| `TotalSize` | Total size of the item in bytes (rounded to nearest integer). For folders this includes all content. |
| `OriginalFolderId` | Internal ID of the folder the item was deleted from. |
| `DeletePath` | Full infoRouter path the item occupied before it was deleted. |
| `DeletedById` | Internal user ID of the user who deleted the item. |
| `DeletedByName` | Username of the user who deleted the item. |
| `RecycledItemStatusId` | Integer status code: `0` = In User Recycle Bin, `1` = In System Recycle Bin. |
| `RecycledItemStatus` | Localized string label for the status. |
| `Handler` | Item handler used to reference this item in `PurgeRecycleBinItem` and `RestoreRecycleBinItem`. Format: `D{id}` for documents, `F{id}` for folders (e.g. `D9871`, `F4312`). |

### Empty Recycle Bin Response

When the bin is empty, the response contains no child elements:

```xml

<response success="true" error="" />

```

### Error Response

```xml

<response success="false" error="[901] Session expired or Invalid ticket." />

```

---

## Required Permissions

Any authenticated user can retrieve their own Recycle Bin contents. The API always returns items belonging to the user identified by the authentication ticket -" it cannot be used to query another user's Recycle Bin.

---

## Example

### GET Request

```

GET /srv.asmx/GetRecycleBinContent

  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

HTTP/1.1

```

### POST Request

```

POST /srv.asmx/GetRecycleBinContent HTTP/1.1

Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

```

### SOAP Request

```xml

<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"

               xmlns:tns="http://tempuri.org/">

  <soap:Body>

    <tns:GetRecycleBinContent>

      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>

    </tns:GetRecycleBinContent>

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

The caller's own recycled items.

```javascript
const root = await call('GetRecycleBinContent', { authenticationTicket: ticket });

for (const item of root.children) {
  console.log(item.tagName,                          // document or folder
              item.getAttribute('Name'),
              item.getAttribute('DeletePath'),        // where it was, in backslashes
              item.getAttribute('DateDeleted'),
              item.getAttribute('Handler'));          // what the writers take
}
```

Each item is a `<document>` or a `<folder>` element directly under the root, carrying `Name`,
`DeletePath`, `DeletedByName`, `DateDeleted`, `TotalSize`, `OriginalFolderId`,
`RecycledItemStatusId`, `RecycledItemStatus` and `Handler`. `DeletePath` is the folder the item was
deleted from, written with backslashes.

## Notes

- **Current User Only**: Returns only the items belonging to the authenticated user. There is no filter parameter; all of the user's recycled items are always returned.

- **Element Type**: Each returned child element is named `<document>` or `<folder>` based on the type of the recycled object.

- **Handler for Further Actions**: The `Handler` attribute value must be passed to `PurgeRecycleBinItem` or `RestoreRecycleBinItem` to operate on individual items.

- **RecycledItemStatusId `1` (System Recycle Bin)**: Items with status `1` have been moved to the system-level recycle bin (typically by an administrator action). They appear in the listing but may require admin action to purge or restore.

- **Date Format**: `DateDeleted` is always in UTC ISO 8601 format (`yyyy-MM-ddTHH:mm:ss.fffZ`).

- **TotalSize**: Expressed in bytes as a floating-point number rounded to the nearest integer. For folders, this represents the total size of all contents at the time of deletion.

---

## Related APIs

- [EmptyRecycleBin](EmptyRecycleBin.md) - Permanently delete all items in the current user's Recycle Bin

- [PurgeRecycleBinItem](PurgeRecycleBinItem.md) - Permanently delete a single item from the Recycle Bin by Handler

- [RestoreRecycleBinItem](RestoreRecycleBinItem.md) - Restore a Recycle Bin item to its original or a specified location

- [SearchRecycledItems](SearchRecycledItems.md) - Search for documents and folders in the Recycle Bin with filter criteria

- [DeleteDocument](DeleteDocument.md) - Delete a document (moves it to the Recycle Bin)

- [DeleteFolder](DeleteFolder.md) - Delete a folder (moves it to the Recycle Bin)

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4000` | the ticket is a well-formed GUID that no session has - an unknown ticket is reported as a bad request here, where the neighbouring operations report 4010 |

An item in the bin is named by its **handler**: the letter `D` and a document id, or the letter
`F` and a folder id - `D4512`, `F183`. It is read off the `Handler` attribute of an item returned
by [GetRecycleBinContent](GetRecycleBinContent.md) or
[SearchRecycledItems](SearchRecycledItems.md); there is no other way to build one, because the ids
are not the ones a caller sees anywhere else.

---
