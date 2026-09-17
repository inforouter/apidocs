# RemoveDocumentCutoffDate API

Removes the cutoff date from the specified document so that it can be checked out and given new versions again. Other rules that block check-out, such as folder rules or a completed status, still apply. If the document has a Retention & Disposition (R&D) schedule, retention and disposition dates that were calculated from the cutoff date are cleared; dates calculated from the creation date are kept.

> **Note:** A document's cutoff date cannot be removed while the folder it is in has a cutoff date. Remove the folder's cutoff date first with `RemoveFolderCutoffDate`.

## Endpoint

```
/srv.asmx/RemoveDocumentCutoffDate
```

## Methods

- **GET** `/srv.asmx/RemoveDocumentCutoffDate?authenticationTicket=...&path=...`
- **POST** `/srv.asmx/RemoveDocumentCutoffDate` (form data)
- **SOAP** Action: `http://tempuri.org/RemoveDocumentCutoffDate`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1-Report.pdf`), or a short document ID path (`~D{id}` or `~D{id}.ext`). |

---

## Response

### Success Response

```xml
<response success="true" error="" errorCode="0" />
```

### Error Response

```xml
<response success="false" error="The parent folder has been cut off. The cut-off state cannot be removed from documents within folders that have been cut off." errorCode="4000" />
```

Error text is returned in the calling user's language.

---

## Required Permissions

The caller must be allowed by the library's **Retention Period Change** policy on the document. By default that is the library manager, the document owner, and users with Change permission on the document.

---

## Example

### GET Request

```
GET /srv.asmx/RemoveDocumentCutoffDate
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &path=/Finance/Reports/Q1-2024-Report.pdf
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/RemoveDocumentCutoffDate HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&path=/Finance/Reports/Q1-2024-Report.pdf
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:RemoveDocumentCutoffDate>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:path>/Finance/Reports/Q1-2024-Report.pdf</tns:path>
    </tns:RemoveDocumentCutoffDate>
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

Clears the cutoff date on one document. Removing one that was never set is a success, so this is safe
to call blindly.

```javascript
await call('RemoveDocumentCutoffDate', {
  authenticationTicket: ticket,
  path: '/Finance/Reports/Q1.pdf'
});
```

[SetDocumentCutoffDate](SetDocumentCutoffDate.md) with an empty `cutoffDate` does the same thing.

## Notes

- If the document's **folder** has a cutoff date, removal is refused. To reopen one document in a cut-off folder, call `RemoveFolderCutoffDate` on its folder with `includeSubFolders=false` and `includeDocuments=false`, then call this API. If that folder's parent is also cut off, clear the folders from the top of the cut-off tree down.
- The call succeeds when the document has no cutoff date.
- Shortcut documents (`.LNK`) return an error; they never have a cutoff date.
- If clearing the date changes the document's disposition date, its open retention and disposition tasks are removed.
- Subscribers are **not** notified when a cutoff date is removed.
- Calling `SetDocumentCutoffDate` without a `cutoffDate` has the same effect as this API.
- Once the date is removed, the folder can't be cut off again until this document has a cutoff date again.

---

## Related APIs

- [SetDocumentCutoffDate](SetDocumentCutoffDate.md) - Apply a cutoff date to a document
- [RemoveFolderCutoffDate](RemoveFolderCutoffDate.md) - Remove the cutoff date from a folder (required first if the document's folder is cut off)
- [GetDocument](GetDocument.md) - Get document properties including the current `CutoffDate`

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | no document at that path - including a folder path, and one the caller may not see |
| `4030` | the caller may not change cutoff dates here |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Document not found | The specified path does not resolve to an existing document. |
| `Cut-off dates cannot be applied to document shortcuts. Please cut-off the original document instead.` | The document is a shortcut (`.LNK`). `errorCode="4000"`. |
| `The parent folder has been cut off. The cut-off state cannot be removed from documents within folders that have been cut off.` | The document's folder has a cutoff date; remove that first. `errorCode="4000"`. |
| Access denied | The caller is not allowed by the library's Retention Period Change policy. |
| `SystemError:...` | An unexpected server-side error occurred. |

---
