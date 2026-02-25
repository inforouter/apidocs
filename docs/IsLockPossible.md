# IsLockPossible API

Checks whether the current authenticated user is able to lock (check out) the document at the specified path. This is a pre-flight check that performs all the same permission and state validations as `Lock` without actually locking the document. Use it to determine in advance whether a lock attempt will succeed and to surface a meaningful reason if it will not.

> **Terminology note:** "Lock" and "Check Out" are synonymous in infoRouter. Locking a document prevents other users from creating new versions until the lock is released.

## Endpoint

```
/srv.asmx/IsLockPossible
```

## Methods

- **GET** `/srv.asmx/IsLockPossible?AuthenticationTicket=...&Path=...`
- **POST** `/srv.asmx/IsLockPossible` (form data)
- **SOAP** Action: `http://tempuri.org/IsLockPossible`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1-Report.pdf`), or a short document ID path (`~D{id}` or `~D{id}.ext`). |

---

## Response

### Success Response

Returns a `<response>` element with `success="true"` when the document can be locked by the current user.

```xml
<response success="true" error="" />
```

### Error Response

Returns `success="false"` with a descriptive error message when the lock is not possible. The `error` attribute contains the reason.

```xml
<response success="false" error="Document is checked out by John Smith." />
```

---

## Required Permissions

The calling user must have **checkout (lock) permission** on the document or its containing folder. Domain managers and document owners typically have this right by default. If the folder has the *Disallow Document Checkout* rule applied, no user can lock documents within it.

---

## Example

### GET Request

```
GET /srv.asmx/IsLockPossible
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports/Q1-2024-Report.pdf
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/IsLockPossible HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance/Reports/Q1-2024-Report.pdf
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:IsLockPossible>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:Path>/Finance/Reports/Q1-2024-Report.pdf</tns:Path>
    </tns:IsLockPossible>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- This is a **read-only check** -" no state is changed, no lock is acquired.
- Shortcut documents (`.LNK`) are automatically resolved to their target document for the check. If the target no longer exists, the call returns an error.
- The following conditions cause the check to return `success="false"`:
  - The document does not exist at the specified path.
  - The document is already locked (checked out) -" by the current user or by another user.
  - The document is in an **archived domain/library**.
  - The document is marked as **completed** (100% complete).
  - The document has a **cutoff date** applied (past or future).
  - The folder has the **Disallow Document Checkout** folder rule set.
  - The user does not have the **checkout permission** on the document or folder.
  - The document is currently **in a workflow** and the current user is not the assigned workflow task holder with edit permission.
  - The document is an **email document** (`.EMAIL` extension).
  - The document is an incomplete upload (still being transferred).

---

## Related APIs

- [Lock](Lock.md) - Lock (check out) the document at the specified path
- [UnLock](UnLock.md) - Unlock (check in) a locked document
- [GetCheckedoutDocuments](GetCheckedoutDocuments.md) - Get the list of documents currently checked out by the current user
- [GetDocument](GetDocument.md) - Get document properties including `CheckoutBy` and `CheckoutDate`

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Document not found | The specified path does not resolve to an existing document. |
| Already checked out by you | The document is already locked by the calling user. |
| Already checked out by [name] | The document is locked by another user. |
| Archived domain | The document is in an archived (offline) library. |
| Completed document | The document is marked as 100% complete and cannot be checked out. |
| Cutoff date applied | The document has a cutoff date and cannot be checked out. |
| Checkout not allowed in folder | The folder has the Disallow Document Checkout rule applied. |
| Access denied | The user does not have checkout permission. |
| In workflow | The document is under workflow review and only the assigned task holder can check it out. |
| Email document | Email documents (`.EMAIL`) cannot be checked out. |
| `SystemError:...` | An unexpected server-side error occurred. |

---
