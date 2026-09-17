# SetFolderCutoffDate API

Sets the cutoff date on the specified folder and, optionally, on its subfolders and documents. The folder is cut off only when every document and subfolder in it already has a cutoff date, so to cut off a whole tree pass `includeSubFolders=true` and `includeDocuments=true`. From the moment the date is saved, even when the date is in the future, the folder accepts no new documents or subfolders and its documents cannot be checked out.

This call is not all-or-nothing. Items that fail are listed in the response; items that succeeded keep their new cutoff date.

## Endpoint

```
/srv.asmx/SetFolderCutoffDate
```

## Methods

- **GET** `/srv.asmx/SetFolderCutoffDate?authenticationTicket=...&path=...&cutoffDate=...&includeSubFolders=...&includeDocuments=...`
- **POST** `/srv.asmx/SetFolderCutoffDate` (form data)
- **SOAP** Action: `http://tempuri.org/SetFolderCutoffDate`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full infoRouter path to the folder (e.g. `/Finance/Reports`). |
| `cutoffDate` | DateTime | Yes | The cutoff date. Format: `yyyy-MM-dd` or `yyyy-MM-ddTHH:mm:ss`. Any date is accepted, past or future. UTC values are converted to server local time. `1900-01-01` or earlier removes cutoff dates instead, as `RemoveFolderCutoffDate` does. |
| `includeSubFolders` | bool | Yes | If `true`, the date is also applied to all subfolders, recursively. |
| `includeDocuments` | bool | Yes | If `true`, the date is also applied to the documents in the folder, and in its subfolders when `includeSubFolders=true`. |

---

## Response

### Success Response

Every item was processed without an error.

```xml
<response success="true" error="" />
```

### Partial Result

One `log` element for each item that failed. Items not listed succeeded or were skipped.

```xml
<response success="false" error="MultiStatus">
  <log>
    <item>\Finance\Reports\Q1.pdf</item>
    <error>This document is checked out. A cut-off date cannot be applied.</error>
  </log>
  <log>
    <item>\Finance\Reports</item>
    <error>Cut-off date cannot be applied to this folder. To cut off a folder, all documents and sub-folders within the folder must be in a cut-off state.</error>
  </log>
</response>
```

### Error Response

Errors that stop the call before any item is processed, such as an invalid ticket or a folder that does not exist, return a single message and a numeric `errorcode`.

```xml
<response success="false" error="[error message]" errorcode="[number]" />
```

| Attribute / element | Description |
|---------------------|-------------|
| `success` | `"true"` only if no item failed. |
| `error` | `"MultiStatus"` when items failed; the `log` elements list them. Otherwise a single error message, or empty on success. |
| `log/item` | Path of the folder or document that failed, with `\` separators. |
| `log/error` | Why it failed, in the calling user's language. |

---

## Required Permissions

The caller must be allowed by the library's **Retention Period Change** policy on the folder, and on every subfolder and document the call changes. By default that is the library manager, the owner, and users with Change permission. Items the caller is not allowed to change are listed as failures.

---

## Example

### GET Request

```
GET /srv.asmx/SetFolderCutoffDate
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &path=/Finance/Reports
  &cutoffDate=2025-12-31
  &includeSubFolders=true
  &includeDocuments=true
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/SetFolderCutoffDate HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&path=/Finance/Reports
&cutoffDate=2025-12-31
&includeSubFolders=true
&includeDocuments=true
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:SetFolderCutoffDate>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:path>/Finance/Reports</tns:path>
      <tns:cutoffDate>2025-12-31</tns:cutoffDate>
      <tns:includeSubFolders>true</tns:includeSubFolders>
      <tns:includeDocuments>true</tns:includeDocuments>
    </tns:SetFolderCutoffDate>
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

Sets the cutoff date on a folder, and optionally on what is inside it.

```javascript
const root = await call('SetFolderCutoffDate', {
  authenticationTicket: ticket,
  path: '/Finance/Reports',
  cutoffDate: '2026-06-30',
  includeSubFolders: true,
  includeDocuments: true
});
```

**A refusal can arrive as a MultiStatus.** When the operation could not do everything it was asked,
the answer is `success="false"` with `error="MultiStatus"`, the reasons inside `<log>` elements, and
**no `errorCode` at all**. That is also the shape of a partial success, so `success="false"` here does
not mean nothing happened - read the `<log>` to find out what did. A client that branches on
`errorCode` sees nothing to branch on.

The commonest case: a folder may only be cut off once everything inside it already is. Asking for one
that still holds uncut subfolders or documents, without `includeSubFolders` and `includeDocuments`, is
refused this way rather than with a code.

**The date is read as local midnight and reported back in UTC.** Sending `2026-06-30` to a server
three hours ahead of UTC stores the instant that reads back as `2026-06-29T21:00:00.000Z` on the
folder. That is the same moment, but a client comparing the date it sent with the date it reads will
see a different day. `cutoffDate` binds as a `DateTime`, so a value that is not a date is refused with
HTTP 400 before the operation runs.

## Notes

- **Order of work.** Subfolders and documents are processed first, deepest level first, and each gets the same date. The folder itself is cut off last, once its contents qualify.
- **Everything inside must be cut off.** A folder is cut off only when all of its documents (shortcuts excluded) and all of its direct subfolders have a cutoff date. Otherwise it is listed with `Cut-off date cannot be applied to this folder…`, and so is every folder above it in the call.
- **Existing dates.** Subfolders and documents that already have a cutoff date keep it; this API cannot override them. The folder named in `path` always takes the new date when its contents qualify, even if it already had one. To replace dates across a tree, call `RemoveFolderCutoffDate`, then this API.
- **The lock does not wait for the date.** A folder with any cutoff date refuses new documents (upload, create, copy, move, restore from the recycle bin) with `This folder has been cut-off. New documents cannot be created in this folder.` It refuses new subfolders with `This folder has been cut off. New folders cannot be created in this folder.` Its documents cannot be checked out.
- **Checked-out documents** cannot be cut off. They are listed as failures, which also stops their folder from being cut off.
- **Shortcuts** (`.LNK`) are skipped and do not stop the folder from being cut off.
- Each document that is cut off notifies its subscribers.
- With an **R&D schedule**, *On Cutoff* retention and disposition dates are calculated from this date for the folder and for each document.

---

## Related APIs

- [RemoveFolderCutoffDate](RemoveFolderCutoffDate.md) - Remove the cutoff date from a folder and optionally its subfolders and documents
- [SetDocumentCutoffDate](SetDocumentCutoffDate.md) - Set the cutoff date on a single document
- [RemoveDocumentCutoffDate](RemoveDocumentCutoffDate.md) - Remove the cutoff date from a single document

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all - the anonymous user is told "Anonymous users cannot perform this action" |
| `4041` | no folder at that path - including one the caller may not see |
| `4030` | the caller may not set cutoff dates here |
| `none` | the folder still holds uncut items, or some items could not be done: `success="false" error="MultiStatus"` with no `errorCode` |
| `HTTP 400` | `cutoffDate` was not a date, or `path` was empty; refused by model binding |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Folder not found | The specified path does not resolve to an existing folder. |
| `MultiStatus` | One or more items failed. See the `log` elements. |
| `Cut-off date cannot be applied to this folder. To cut off a folder, all documents and sub-folders within the folder must be in a cut-off state.` | Logged for a folder that still contains a document or subfolder without a cutoff date. |
| `This document is checked out. A cut-off date cannot be applied.` | Logged for a checked-out document. |
| Access denied | Logged for a folder or document the caller is not allowed to change under the Retention Period Change policy. |
| `SystemError:...` | An unexpected server-side error occurred. |

---
