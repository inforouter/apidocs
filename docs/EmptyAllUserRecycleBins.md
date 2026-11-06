# EmptyAllUserRecycleBins API

Empties every user's Recycle Bin into the system recycle bin, one user at a time. It is
[EmptyRecycleBin](EmptyRecycleBin.md) for every user at once. **Nothing is purged.** The users can no longer see
([GetRecycleBinContent](GetRecycleBinContent.md)) or restore the items themselves, but a system administrator can still find them
([SearchRecycledItems1](SearchRecycledItems1.md)), restore them ([RestoreRecycleBinItem](RestoreRecycleBinItem.md))
or purge them for good ([PurgeRecycleBinItem](PurgeRecycleBinItem.md)) in the system recycle bin. The system
recycle bin's automatic purge, if it is configured, applies to them from then on.

## Endpoint

```
/srv.asmx/EmptyAllUserRecycleBins
```

## Methods

- **GET** `/srv.asmx/EmptyAllUserRecycleBins?authenticationTicket=...`
- **POST** `/srv.asmx/EmptyAllUserRecycleBins` (form data)
- **SOAP** Action: `http://tempuri.org/EmptyAllUserRecycleBins`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket of a system administrator, obtained from `AuthenticateUser`. |

---

## Response

### Success Response

```xml
<response success="true" error="" recycleBinCount="2" folderCount="1" documentCount="2" />
```

| Attribute | Description |
|-----------|-------------|
| `recycleBinCount` | How many users' recycle bins this call emptied (bins it found already empty are not counted). |
| `folderCount` | How many recycled folders this call moved. A folder counts once, with everything in it. |
| `documentCount` | How many recycled documents this call moved. |

All three are `0` when every user's Recycle Bin was already empty.

### Error Response

```xml
<response success="false" error="Only the system administrator can perform this operation" errorCode="4030" />
```

---

## Required Permissions

**System administrators only.** Everyone else, User Managers included, gets `4030`.

---

## Example

### GET Request

```
GET /srv.asmx/EmptyAllUserRecycleBins?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301 HTTP/1.1
```

### POST Request

```
POST /srv.asmx/EmptyAllUserRecycleBins HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:EmptyAllUserRecycleBins>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
    </tns:EmptyAllUserRecycleBins>
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

Empties every user's recycle bin. Then, if the items are to go for good, the system recycle bin is purged one item
at a time.

```javascript
const result = await call('EmptyAllUserRecycleBins', { authenticationTicket: ticket });
console.log(`${result.getAttribute('recycleBinCount')} recycle bins emptied`);

// If the request was dropped before an answer came back, calling it again carries on.
// The items are now in the system recycle bin: SearchRecycledItems1 with searchIn=1 finds them, and
// PurgeRecycleBinItem removes them for good, one by one.
```

## Notes

- **Long running, and safe to cut off.** The call works through the users' Recycle Bins one after another. Each
  item moves to the system recycle bin in a transaction of its own, together with its delete-log entries. A call
  that is cut off (a timeout, a dropped connection, a server restart) leaves every item either moved and logged
  or untouched. **Calling it again carries on** with what the users' Recycle Bins still hold, so a client that
  got no answer simply calls it again. The counts of a repeated call cover only what that call moved.
- **Nothing is destroyed.** To remove the items for good, purge them from the system recycle bin with
  [PurgeRecycleBinItem](PurgeRecycleBinItem.md).
- **Logged.** Every moved item is written to the delete log as a recycle-bin empty by the calling administrator,
  with each document and subfolder inside a moved folder logged as well, exactly as `EmptyRecycleBin` logs a
  user's own empty.
- **Items already in the system recycle bin are not touched**, nor are items a user deletes while the call runs
  in a recycle bin the call has already passed. The next call picks those up.

---

## Related APIs

- [EmptyRecycleBin](EmptyRecycleBin.md) - Empty the current user's own Recycle Bin into the system recycle bin
- [SearchRecycledItems1](SearchRecycledItems1.md) - Search the Recycle Bins a page at a time; `searchIn=1` for the system recycle bin only (admin only)
- [RestoreRecycleBinItem](RestoreRecycleBinItem.md) - Restore a recycled item
- [PurgeRecycleBinItem](PurgeRecycleBinItem.md) - Permanently delete a single recycled item (admin only)

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4030` | the caller is not a system administrator |
