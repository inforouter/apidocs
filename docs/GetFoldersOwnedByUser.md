# GetFoldersOwnedByUser API

Returns a paged list of folders owned by the specified user. Supports offset-based paging via `startingRow` and `rowCount`.

## Endpoint

```
/srv.asmx/GetFoldersOwnedByUser
```

## Methods

- **GET** `/srv.asmx/GetFoldersOwnedByUser?authenticationTicket=...&userName=...&startingRow=...&rowCount=...`
- **POST** `/srv.asmx/GetFoldersOwnedByUser` (form data)
- **SOAP** Action: `http://tempuri.org/GetFoldersOwnedByUser`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `userName` | string | Yes | The username whose owned folders are to be retrieved. |
| `startingRow` | int | Yes | Zero-based row offset. Pass `0` to start from the first result. Pass `100` to skip the first 100 results. |
| `rowCount` | int | Yes | Number of rows to return (page size). |

---

## Required Permissions

| Scenario | Required permission |
|----------|---------------------|
| Caller queries their own folders | None — authenticated user only |
| Caller queries another user's folders | **ListingAuditLogOfUser** admin permission for the target user |

---

## Response

### Success Response

Returns a `<response>` element with `success="true"` containing zero or more `<folder>` child elements.

```xml
<response success="true" error="" recordCount="46" startingRow="0" rowCount="2">
  <folder FolderID="42" ParentID="1" Name="Reports" Path="\MyLibrary\Reports" Description=""
          CreationDate="2026-08-19T15:34:41.250Z" OwnerName="John Smith" DomainId="1"
          ClassificationLevel="NoMarkings" ClassificationLevelId="0" DeclassifyOn="" DowngradeOn=""
          RDDefId="0" RetentionDate="" DispositionDate="" CutoffDate="" />
  <folder FolderID="43" ParentID="1" Name="Archive" Path="\MyLibrary\Archive" ... />
</response>
```

### Folder Attribute Reference

The root carries the paging:

| Attribute | Type | Description |
|-----------|------|-------------|
| `recordCount` | int | How many folders the user owns in total, ignoring the paging. |
| `startingRow` | int | The offset that was applied. |
| `rowCount` | int | The page size that was applied - rewritten to `recordCount` when `0` was sent. |

Each `<folder>` is the same element [GetFolder](GetFolder.md) returns, so the attribute names are
capitalised:

| Attribute | Type | Description |
|-----------|------|-------------|
| `FolderID` | int | Unique folder identifier. |
| `ParentID` | int | Id of the folder's parent. |
| `Name` | string | Folder name. |
| `Path` | string | Full infoRouter path, with `\` separators. |
| `Description` | string | Folder description. |
| `CreationDate` | string | When the folder was created, UTC. |
| `OwnerName` | string | Display name of the owner - not the login name. |
| `DomainId` | int | Id of the library the folder belongs to. |
| `ClassificationLevel`, `ClassificationLevelId`, `DeclassifyOn`, `DowngradeOn` | | Classification, as on `GetFolder`. |
| `RDDefId`, `RetentionDate`, `DispositionDate`, `CutoffDate` | | Retention and disposition, as on `GetFolder`. |

### Empty Result

```xml
<response success="true" error="" recordCount="0" startingRow="0" rowCount="100" />
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

---

## Paging

Use `startingRow` and `rowCount` to page through large result sets.

| Goal | startingRow | rowCount |
|------|-------------|----------|
| First page of 50 | `0` | `50` |
| Second page of 50 | `50` | `50` |
| Rows 1001–1100 | `1000` | `100` |

`startingRow` is the number of records to **skip**. `rowCount` is the number of records to **return**.

---

## Example Requests

### GET — first page

```
GET /srv.asmx/GetFoldersOwnedByUser?authenticationTicket=abc123-def456&userName=jsmith&startingRow=0&rowCount=50 HTTP/1.1
Host: server.example.com
```

### GET — second page

```
GET /srv.asmx/GetFoldersOwnedByUser?authenticationTicket=abc123-def456&userName=jsmith&startingRow=50&rowCount=50 HTTP/1.1
Host: server.example.com
```

### POST

```
POST /srv.asmx/GetFoldersOwnedByUser HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&userName=jsmith&startingRow=0&rowCount=50
```

### SOAP 1.1

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetFoldersOwnedByUser"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetFoldersOwnedByUser xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
      <userName>jsmith</userName>
      <startingRow>0</startingRow>
      <rowCount>50</rowCount>
    </GetFoldersOwnedByUser>
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

Lists the folders one user owns, a page at a time. Folders come back in the full `<folder>` shape
[GetFolder](GetFolder.md) uses, and the root carries `recordCount`, the total, alongside the
`startingRow` and `rowCount` that were applied.

```javascript
let startingRow = 0;
const rowCount = 100;

for (;;) {
  const root = await call('GetFoldersOwnedByUser', {
    authenticationTicket: ticket,
    userName: 'jsmith',
    startingRow,
    rowCount
  });

  for (const folder of root.querySelectorAll(':scope > folder')) {
    console.log(folder.getAttribute('Path'));
  }

  startingRow += rowCount;
  if (startingRow >= Number(root.getAttribute('recordCount'))) break;
}
```

**`rowCount=0` means every row, not none.** The answer then reports `rowCount` as the total rather
than the zero that was asked for, so a loop that trusts the value it sent will not terminate.

## Notes

- `startingRow` is zero-based: `startingRow=0` returns from the first record, `startingRow=50` skips the first 50.
- To retrieve all folders without paging, pass `startingRow=0` and a sufficiently large `rowCount`.
- Ownership is determined by the folder owner field. Library root folders (domains) are not included.

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4000` | no user by that name |
| `4010` | the caller has no ticket. The message is "User has been deleted.", which describes neither the caller nor the user asked about |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Insufficient rights.` | The caller does not have `ListingAuditLogOfUser` permission for the target user. |
| User not found | The specified `userName` does not exist. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

## Related APIs

- [GetDocumentsOwnedByUser](GetDocumentsOwnedByUser.md) - Get a paged list of documents owned by a user
- [GetAuthoredDocuments](GetAuthoredDocuments.md) - Get documents authored (created) by a user
- [GetFoldersByUser](GetFoldersByUser.md) - Get folders accessible to a user
