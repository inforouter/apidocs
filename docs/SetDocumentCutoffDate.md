# SetDocumentCutoffDate API

Applies a cutoff date to the specified document. The document is locked from the moment the date is saved, even when the date is in the future: it can no longer be checked out, so no new versions can be added. If the document has a Retention & Disposition (R&D) schedule, its retention and disposition dates are recalculated from the cutoff date. Document subscribers are notified.

> **Note:** If the document already has a cutoff date, this call returns success without changing it. To change the date, call `RemoveDocumentCutoffDate` first, then call `SetDocumentCutoffDate` with the new date.

## Endpoint

```
/srv.asmx/SetDocumentCutoffDate
```

## Methods

- **GET** `/srv.asmx/SetDocumentCutoffDate?authenticationTicket=...&path=...&cutoffDate=...`
- **POST** `/srv.asmx/SetDocumentCutoffDate` (form data)
- **SOAP** Action: `http://tempuri.org/SetDocumentCutoffDate`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1-Report.pdf`), or a short document ID path (`~D{id}` or `~D{id}.ext`). |
| `cutoffDate` | DateTime | Yes | The cutoff date, e.g. `2024-12-31`. Any date is accepted, past or future. UTC values are converted to server local time. If it is omitted, or is `1900-01-01` or earlier, the cutoff date is **removed** instead, exactly as `RemoveDocumentCutoffDate` does. |

---

## Response

### Success Response

```xml
<response success="true" error="" errorCode="0" />
```

### Error Response

```xml
<response success="false" error="This document is checked out. A cut-off date cannot be applied." errorCode="4000" />
```

Error text is returned in the calling user's language.

---

## Required Permissions

The caller must be allowed by the library's **Retention Period Change** policy on the document. By default that is the library manager, the document owner, and users with Change permission on the document.

---

## Example

### GET Request

```
GET /srv.asmx/SetDocumentCutoffDate
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &path=/Finance/Reports/Q1-2024-Report.pdf
  &cutoffDate=2024-12-31
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/SetDocumentCutoffDate HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&path=/Finance/Reports/Q1-2024-Report.pdf
&cutoffDate=2024-12-31
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:SetDocumentCutoffDate>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:path>/Finance/Reports/Q1-2024-Report.pdf</tns:path>
      <tns:cutoffDate>2024-12-31</tns:cutoffDate>
    </tns:SetDocumentCutoffDate>
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

Sets the cutoff date on one document.

```javascript
await call('SetDocumentCutoffDate', {
  authenticationTicket: ticket,
  path: '/Finance/Reports/Q1.pdf',
  cutoffDate: '2026-06-30'
});
```

`cutoffDate` is a **nullable** `DateTime`, so an empty one reaches the operation rather than being
refused by model binding, and clears the date - the same thing
[RemoveDocumentCutoffDate](RemoveDocumentCutoffDate.md) does. The date is read as local midnight and
reported back by [GetDocument](GetDocument.md) in UTC, so the day that reads back may differ from the
day that was sent.

Unlike [SetFolderCutoffDate](SetFolderCutoffDate.md) there is no MultiStatus here: one document, one
answer.

## Notes

- **The lock does not wait for the date.** Once any cutoff date is saved, check-out is refused. That includes uploads that check the document out and in, and saves through WebDAV. For a future date the error is `Document cannot be checked out. A future cut-off date has been applied to this document. If you wish to edit this document, please remove the cut-off date.` Once the date has passed it is `Document cannot be checked out. A cut-off date has been specified for this document.`
- A cutoff date does **not** block property or metadata changes, comments, renaming, deleting, or moving the document to a folder without a cutoff date. A moved document keeps its cutoff date; a copy gets none.
- **Shortcut documents** (`.LNK`) cannot have a cutoff date. Cut off the original document instead.
- **Checked-out documents** cannot be cut off. Check the document in, or undo the check-out, first.
- If the document **already has a cutoff date**, this call returns success without making any change.
- With an **R&D schedule**, a retention or disposition trigger of *On Cutoff* is calculated from this date. A disposition date is never earlier than the retention end date. When the disposition date changes, the document's open retention and disposition tasks are removed.
- Subscribers receive an update notification for the *Cut-off date* section.
- To cut off every document in a folder tree, use `SetFolderCutoffDate` with `includeSubFolders` and `includeDocuments` set to `true`.
- Use `GetDocument` to read the current `CutoffDate` attribute before calling this API.

---

## Related APIs

- [RemoveDocumentCutoffDate](RemoveDocumentCutoffDate.md) - Remove the cutoff date from a document (required before changing an existing cutoff date)
- [SetFolderCutoffDate](SetFolderCutoffDate.md) - Set the cutoff date on a folder and optionally its subfolders and documents
- [IsLockPossible](IsLockPossible.md) - Check whether a document can be checked out
- [GetDocument](GetDocument.md) - Get document properties including the current `CutoffDate`

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | no document at that path - including a folder path, and one the caller may not see |
| `4030` | the caller may not set cutoff dates here |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Document not found | The specified path does not resolve to an existing document. |
| `Cut-off dates cannot be applied to document shortcuts. Please cut-off the original document instead.` | The document is a shortcut (`.LNK`). `errorCode="4000"`. |
| `This document is checked out. A cut-off date cannot be applied.` | The document must be checked in first. `errorCode="4000"`. |
| Access denied | The caller is not allowed by the library's Retention Period Change policy. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

## Reading it back

[GetDocument](GetDocument.md) returns the date as the `CutoffDate` attribute, beside the
`RetentionDate` and `DispositionDate` calculated from it. Clear it with
[RemoveDocumentCutoffDate](RemoveDocumentCutoffDate.md).
