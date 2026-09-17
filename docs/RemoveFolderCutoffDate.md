# RemoveFolderCutoffDate API

Removes the cutoff date from the specified folder and, optionally, from its subfolders and documents. Once its cutoff date is removed, the folder accepts new documents and subfolders again. Removal works from the top down: a folder's cutoff date cannot be removed while its parent folder has one.

This call is not all-or-nothing. Items that fail are listed in the response; items that succeeded keep their cutoff date removed.

## Endpoint

```
/srv.asmx/RemoveFolderCutoffDate
```

## Methods

- **GET** `/srv.asmx/RemoveFolderCutoffDate?authenticationTicket=...&path=...&includeSubFolders=...&includeDocuments=...`
- **POST** `/srv.asmx/RemoveFolderCutoffDate` (form data)
- **SOAP** Action: `http://tempuri.org/RemoveFolderCutoffDate`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full infoRouter path to the folder (e.g. `/Finance/Reports`). |
| `includeSubFolders` | bool | Yes | If `true`, the cutoff date is also removed from all subfolders, recursively. |
| `includeDocuments` | bool | Yes | If `true`, the cutoff date is also removed from the documents in the folder, and in its subfolders when `includeSubFolders=true`. |

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
    <item>\Finance\Reports</item>
    <error>The parent folder has been cut off. The cut-off state cannot be removed from child folders.</error>
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
GET /srv.asmx/RemoveFolderCutoffDate
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &path=/Finance/Reports
  &includeSubFolders=true
  &includeDocuments=true
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/RemoveFolderCutoffDate HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&path=/Finance/Reports
&includeSubFolders=true
&includeDocuments=true
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:RemoveFolderCutoffDate>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:path>/Finance/Reports</tns:path>
      <tns:includeSubFolders>true</tns:includeSubFolders>
      <tns:includeDocuments>true</tns:includeDocuments>
    </tns:RemoveFolderCutoffDate>
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

Clears the cutoff date on a folder, and optionally on what is inside it. Removing a cutoff date that
was never set is a success, so this is safe to call blindly.

```javascript
await call('RemoveFolderCutoffDate', {
  authenticationTicket: ticket,
  path: '/Finance/Reports',
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

## Notes

- **Parent folder rule.** If the folder's parent has a cutoff date, the folder is listed with `The parent folder has been cut off. The cut-off state cannot be removed from child folders.` Nothing inside it is changed. Start from the top of the cut-off tree.
- **Order of work.** The folder's own date is removed first, then its subfolders and documents when requested. This is why one call with `includeSubFolders=true` can clear a whole tree.
- If `includeSubFolders=false` and `includeDocuments=false`, only the folder's own date is removed, and everything inside keeps its date. Use this to reopen a single document: remove the folder's date this way, then call `RemoveDocumentCutoffDate` on the document.
- Once anything inside has no cutoff date, the folder cannot be cut off again until that item has one.
- **Shortcuts** (`.LNK`) are skipped.
- The call succeeds for a folder that has no cutoff date; its contents are still processed as requested.
- If clearing a date changes a folder's or document's disposition date, its open retention and disposition tasks are removed.
- Subscribers are **not** notified when cutoff dates are removed.

---

## Related APIs

- [SetFolderCutoffDate](SetFolderCutoffDate.md) - Set the cutoff date on a folder
- [RemoveDocumentCutoffDate](RemoveDocumentCutoffDate.md) - Remove cutoff date from a single document
- [SetDocumentCutoffDate](SetDocumentCutoffDate.md) - Set cutoff date on a single document

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all - the anonymous user is told "Anonymous users cannot perform this action" |
| `4041` | no folder at that path - including one the caller may not see |
| `4030` | the caller may not change cutoff dates here |
| `none` | some items could not be done: `success="false" error="MultiStatus"` with no `errorCode` |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Folder not found | The specified path does not resolve to an existing folder. |
| `MultiStatus` | One or more items failed. See the `log` elements. |
| `The parent folder has been cut off. The cut-off state cannot be removed from child folders.` | Logged for a folder whose parent folder has a cutoff date. |
| Access denied | Logged for a folder or document the caller is not allowed to change under the Retention Period Change policy. |
| `SystemError:...` | An unexpected server-side error occurred. |

---
