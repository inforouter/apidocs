# GetRecycleBinStatistics API

Answers what the recycle bins of the whole instance hold, by where it is: the **system recycle bin**, the
**users' recycle bins** and the **purge queue**, each with how many folders and documents it holds and their total
size in bytes. With `withDetails=true`, the users' recycle bins are listed one by one as well. It only reads.
See [What happens to a deleted document or folder](rules/recycle-bin.md) for what the three places are.

## Endpoint

```
/srv.asmx/GetRecycleBinStatistics
```

## Methods

- **GET** `/srv.asmx/GetRecycleBinStatistics?authenticationTicket=...&withDetails=...`
- **POST** `/srv.asmx/GetRecycleBinStatistics` (form data)
- **SOAP** Action: `http://tempuri.org/GetRecycleBinStatistics`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket of a system administrator, obtained from `AuthenticateUser`. |
| `withDetails` | bool | No | Default `false`. `true` adds one `<recyclebin>` per user's recycle bin that holds anything, sorted by user name. Over SOAP the parameter is required; pass `false` for the default. |

---

## Response

### Success Response

```xml
<response success="true" error="">
  <systemRecycleBin folderCount="26" documentCount="9078" totalSize="9816823965" />
  <userRecycleBins recycleBinCount="2" folderCount="1244" documentCount="232" totalSize="410046">
    <!-- only with withDetails=true, sorted by username -->
    <recyclebin username="jane"  folderCount="1222" documentCount="12"  totalSize="210023" />
    <recyclebin username="utkuc" folderCount="22"   documentCount="220" totalSize="200023" />
  </userRecycleBins>
  <purgeQueue folderCount="3" documentCount="41" totalSize="1048576" />
</response>
```

| Element | What it counts |
|---------|----------------|
| `<systemRecycleBin>` | What has been emptied out of the users' recycle bins. Only a system administrator can find, restore or purge it ([SearchRecycledItems1](SearchRecycledItems1.md) with `searchIn=1`). |
| `<userRecycleBins>` | What is still in the users' own recycle bins, where each user can restore it. `recycleBinCount` is how many users' recycle bins hold anything. |
| `<recyclebin>` | Only with `withDetails=true`: one user's recycle bin. `username` is empty for a recycle bin nobody owns any more. The numbers of all `<recyclebin>` elements add up to those of `<userRecycleBins>`. |
| `<purgeQueue>` | What is queued for the purge job, which removes it for good within minutes. Nothing in it can be restored or found by a search. |

Each element carries:

| Attribute | Description |
|-----------|-------------|
| `folderCount` | How many deleted folders. A folder counts once, with everything in it. |
| `documentCount` | How many deleted documents, not counting the documents inside the deleted folders. |
| `totalSize` | Their total size, in bytes, as a plain integer (no separators). A folder's size is that of its contents when it was deleted. |

There are **no totals on the root**. Add the parts up on the client if a total is wanted; the purge queue is
usually left out of it, since it is about to be gone.

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
GET /srv.asmx/GetRecycleBinStatistics?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301&withDetails=true HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetRecycleBinStatistics HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301&withDetails=true
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetRecycleBinStatistics>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:withDetails>true</tns:withDetails>
    </tns:GetRecycleBinStatistics>
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

const stats = await call('GetRecycleBinStatistics', { authenticationTicket: ticket, withDetails: true });
const counts = el => ({
  folders: Number(el.getAttribute('folderCount')),
  documents: Number(el.getAttribute('documentCount')),
  bytes: Number(el.getAttribute('totalSize')),
});

const system = counts(stats.querySelector('systemRecycleBin'));
const users = counts(stats.querySelector('userRecycleBins'));
// Restorable in total: the users' recycle bins and the system recycle bin, not the purge queue.
console.log(`${(system.bytes + users.bytes).toLocaleString()} bytes can still be restored`);

for (const bin of stats.querySelectorAll('userRecycleBins > recyclebin')) {
  const c = counts(bin);
  console.log(`${bin.getAttribute('username')}: ${c.documents} documents, ${c.folders} folders`);
}
```

## Notes

- **The whole instance.** The numbers cover every user's recycle bin, not the caller's. A user's own recycle bin is
  listed by [GetRecycleBinContent](GetRecycleBinContent.md).
- **Counted the way the empties count.** The three numbers are the ones [EmptyRecycleBin](EmptyRecycleBin.md),
  [EmptyUserRecycleBin](EmptyUserRecycleBin.md) and [EmptyAllUserRecycleBins](EmptyAllUserRecycleBins.md) answer
  for what they moved: emptying a user's recycle bin moves its numbers from that `<recyclebin>` to
  `<systemRecycleBin>`.
- **A snapshot.** The numbers are read in one pass at the moment of the call; deletes, empties and the purge job
  change them from then on. The purge job takes up to 1,000 items from the purge queue every 5 minutes.
- **Reads only.** Nothing is changed.

---

## Related APIs

- [SearchRecycledItems1](SearchRecycledItems1.md) - The items themselves, a page at a time; `searchIn` for one recycle bin, `path` for one library or folder (admin only)
- [EmptyUserRecycleBin](EmptyUserRecycleBin.md) - Empty one user's Recycle Bin into the system recycle bin (admin only)
- [EmptyAllUserRecycleBins](EmptyAllUserRecycleBins.md) - Empty every user's Recycle Bin into the system recycle bin (admin only)
- [PurgeRecycleBinItem](PurgeRecycleBinItem.md) - Permanently delete a single recycled item (admin only)

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4030` | the caller is not a system administrator |

## Since

- **9.0 (2026-11-06):** the call.
