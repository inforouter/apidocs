# Lock API

Locks (checks out) the document or all documents within the folder at the specified path. Locking prevents other users from creating new versions of a document until the lock is released. Use `UnLock` to release the lock when done editing.

> **Terminology note:** "Lock" and "Check Out" are synonymous in infoRouter. The terms are used interchangeably throughout the system.

## Endpoint

```
/srv.asmx/Lock
```

## Methods

- **GET** `/srv.asmx/Lock?AuthenticationTicket=...&Path=...`
- **POST** `/srv.asmx/Lock` (form data)
- **SOAP** Action: `http://tempuri.org/Lock`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to a document or folder (e.g. `/Finance/Reports/Q1-Report.pdf` or `/Finance/Reports`). When a folder path is given, all documents inside the folder are locked in bulk. |

---

## Response

### Document path — Success

```xml
<response success="true" error="" />
```

### Document path — Failure

```xml
<response success="false" error="Document is checked out by John Smith." />
```

### Folder path — All documents locked successfully

```xml
<response success="true" error="" />
```

### Folder path — One or more documents could not be locked

When a folder path is given and at least one document fails, the response contains a `<log>` entry per failed document with its name and the reason:

```xml
<response success="false" error="[log]">
  <log>
    <item>Q1-2024-Report.pdf</item>
    <error>Document is checked out by John Smith.</error>
  </log>
  <log>
    <item>Budget-2024.xlsx</item>
    <error>Completed documents cannot be checked out.</error>
  </log>
</response>
```

| Field | Description |
|-------|-------------|
| `success` | `"true"` if the operation succeeded (document locked, or all folder documents locked). `"false"` on any failure. |
| `error` | Empty on success. Error description on single failure. `"[log]"` when multiple failures occurred (see `<log>` child elements). |
| `<log>/<item>` | Document name that could not be locked (folder bulk operation only). |
| `<log>/<error>` | Reason the specific document could not be locked. |

---

## Required Permissions

The calling user must have **checkout (lock) permission** on the document or its containing folder. Domain managers and document owners typically have this right by default.

For folder bulk operations, each individual document is checked independently. Documents the user cannot lock are reported in the log; documents the user can lock are locked regardless.

---

## Example

### GET Request — single document

```
GET /srv.asmx/Lock
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports/Q1-2024-Report.pdf
HTTP/1.1
```

### GET Request — all documents in a folder

```
GET /srv.asmx/Lock
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/Lock HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance/Reports/Q1-2024-Report.pdf
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:Lock>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:Path>/Finance/Reports/Q1-2024-Report.pdf</tns:Path>
    </tns:Lock>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- **Document path**: Locks the single document. Returns `success="true"` or `success="false"` with an error message.
- **Folder path**: Attempts to lock every document directly inside the folder. Returns `success="true"` if all succeeded, or a `<log>`-based response listing every document that failed and why.
- Shortcut documents (`.LNK`) are automatically resolved to their target document before locking.
- The same permission and state conditions enforced by `IsLockPossible` apply here. Use `IsLockPossible` first if you want to surface errors without attempting the operation.
- Locking does not create a new version — it marks the document as checked out by the current user, preventing others from uploading new versions until the lock is released.
- After locking, upload a new version with `UploadDocument` or `UploadDocumentWithHandler`, then release the lock with `UnLock`. To cancel without creating a new version, call `UnLock` with no upload.

---

## Related APIs

- [UnLock](UnLock.md) - Release a lock (check in) on a document or all documents in a folder
- [IsLockPossible](IsLockPossible.md) - Check whether the current user can lock a document before attempting
- [GetCheckedoutDocuments](GetCheckedoutDocuments.md) - Get the list of documents currently locked by the current user
- [GetDocument](GetDocument.md) - Get document properties including `CheckoutBy` and `CheckoutDate`
- [UploadDocument](UploadDocument.md) - Upload a new version of a locked document

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Document not found | The specified path does not resolve to an existing document or folder. |
| Already checked out by you | The document is already locked by the calling user. |
| Already checked out by [name] | The document is locked by another user. |
| Archived domain | The document is in an archived (offline) library. |
| Completed document | The document is marked as 100% complete and cannot be locked. |
| Cutoff date applied | The document has a cutoff date and cannot be locked. |
| Checkout not allowed in folder | The folder has the Disallow Document Checkout rule applied. |
| Access denied | The user does not have checkout permission. |
| In workflow | The document is under workflow review and only the assigned task holder can lock it. |
| `[log]` | Folder bulk operation: one or more documents failed. See `<log>` child elements for details. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/Lock*
