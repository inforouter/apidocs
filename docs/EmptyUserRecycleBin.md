# EmptyUserRecycleBin API

Empties one user's Recycle Bin into the system recycle bin and answers what moved: how many folders and documents,
and their total size in bytes. It is [EmptyRecycleBin](EmptyRecycleBin.md) done by an administrator for someone
else, and [EmptyAllUserRecycleBins](EmptyAllUserRecycleBins.md) for one user. **Nothing is purged.** The user can
no longer see ([GetRecycleBinContent](GetRecycleBinContent.md)) or restore the items themselves, but a system
administrator can still find them ([SearchRecycledItems1](SearchRecycledItems1.md) with `searchIn=1`), restore
them ([RestoreRecycleBinItem](RestoreRecycleBinItem.md)) or purge them for good
([PurgeRecycleBinItem](PurgeRecycleBinItem.md)) in the system recycle bin. The system recycle bin's automatic
purge, if it is configured, applies to them from then on.

## Endpoint

```
/srv.asmx/EmptyUserRecycleBin
```

## Methods

- **GET** `/srv.asmx/EmptyUserRecycleBin?authenticationTicket=...&userName=...`
- **POST** `/srv.asmx/EmptyUserRecycleBin` (form data)
- **SOAP** Action: `http://tempuri.org/EmptyUserRecycleBin`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket of a system administrator, obtained from `AuthenticateUser`. |
| `userName` | string | Yes | The user whose Recycle Bin is emptied. Your own name empties your own, as `EmptyRecycleBin` does. Empty is refused with `4000`; a user that does not exist is `4041`. |

---

## Response

### Success Response

```xml
<response success="true" error="" folderCount="22" documentCount="220" totalSize="200023" />
```

| Attribute | Description |
|-----------|-------------|
| `folderCount` | How many recycled folders this call moved. A folder counts once, with everything in it. |
| `documentCount` | How many recycled documents this call moved, not counting the documents inside the moved folders. |
| `totalSize` | The total size of what this call moved, in bytes, as a plain integer (no separators). A folder's size is that of its contents when it was deleted, as recorded with it. |

All three are `0` when the user's Recycle Bin was already empty, or when the user never had one. They are the
same three attributes [EmptyRecycleBin](EmptyRecycleBin.md) answers for the caller's own recycle bin, and that
each `<recyclebin>` of [EmptyAllUserRecycleBins](EmptyAllUserRecycleBins.md) carries.

### Error Response

```xml
<response success="false" error="Only the system administrator can perform this operation" errorCode="4030" />
```

---

## Required Permissions

**System administrators only.** Everyone else, User Managers included, gets `4030`, even for their own name
(their own Recycle Bin is [EmptyRecycleBin](EmptyRecycleBin.md)). The right is asked before the user is looked
up, so a caller without it learns nothing about which users exist.

---

## Example

### GET Request

```
GET /srv.asmx/EmptyUserRecycleBin?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301&userName=jsmith HTTP/1.1
```

### POST Request

```
POST /srv.asmx/EmptyUserRecycleBin HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301&userName=jsmith
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:EmptyUserRecycleBin>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:userName>jsmith</tns:userName>
    </tns:EmptyUserRecycleBin>
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

const moved = await call('EmptyUserRecycleBin', { authenticationTicket: ticket, userName: 'jsmith' });
const bytes = Number(moved.getAttribute('totalSize'));
console.log(`${moved.getAttribute('documentCount')} documents and ${moved.getAttribute('folderCount')} folders ` +
            `(${bytes.toLocaleString()} bytes) moved to the system recycle bin`);
```

## Notes

- **Safe to cut off.** Each item moves to the system recycle bin in a transaction of its own, together with its
  delete-log entries. A call that is cut off leaves every item either moved and logged or untouched, and
  **calling it again carries on** with what is left. The counts and the size of a repeated call cover only what
  that call moved.
- **Only that user's Recycle Bin** is touched: what they deleted. Items already in the system recycle bin are not
  touched, nor are items the user deletes after the call has read their Recycle Bin; the next call picks those up.
- **Logged.** Every moved item is written to the delete log as a recycle-bin empty by the calling administrator,
  with each document and subfolder inside a moved folder logged as well, as `EmptyRecycleBin` logs a user's own
  empty.
- **Display the size yourself.** `totalSize` is bytes; format it (`200023` as "195 KB" or "200,023 bytes") on the
  client, in the reader's language.

---

## Related APIs

- [EmptyRecycleBin](EmptyRecycleBin.md) - Empty the current user's own Recycle Bin into the system recycle bin
- [EmptyAllUserRecycleBins](EmptyAllUserRecycleBins.md) - Empty every user's Recycle Bin, one user at a time (admin only)
- [SearchRecycledItems1](SearchRecycledItems1.md) - Search the Recycle Bins a page at a time; `searchIn=1` for the system recycle bin only (admin only)
- [RestoreRecycleBinItem](RestoreRecycleBinItem.md) - Restore a recycled item
- [PurgeRecycleBinItem](PurgeRecycleBinItem.md) - Permanently delete a single recycled item (admin only)

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4000` | `userName` is empty |
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4030` | the caller is not a system administrator |
| `4041` | no user by that name |

## Since

- **9.0 (2026-11-06):** the call.
