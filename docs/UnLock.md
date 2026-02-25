# UnLock API

Unlocks (checks in) a document or all documents in a folder at the specified path. When `force` is `true`, the calling user can unlock a document currently locked by another user — this is an administrative action that discards the other user's in-progress changes. When `force` is `false`, only the user who locked the document can unlock it.

## Endpoint

```
/srv.asmx/UnLock
```

## Methods

- **GET** `/srv.asmx/UnLock?authenticationTicket=...&path=...&force=...`
- **POST** `/srv.asmx/UnLock` (form data)
- **SOAP** Action: `http://tempuri.org/UnLock`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full infoRouter path to the document or folder (e.g. `/Finance/Reports/Q1-Report.pdf`). When a folder path is given, all locked documents in that folder are unlocked. |
| `force` | bool | Yes | `true` to force-unlock a document locked by another user (administrator action — discards their in-progress changes). `false` to only unlock documents locked by the calling user. |

---

## Response

### Success Response

```xml
<response success="true" error="" />
```

### Error Response

```xml
<response success="false" error="The document is not locked by you." />
```

---

## Required Permissions

- **Normal unlock** (`force=false`): The calling user must be the same user who locked the document.
- **Force unlock** (`force=true`): The calling user must have **administrator** or **domain manager** rights.

---

## Example

### GET Request

```
GET /srv.asmx/UnLock
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &path=/Finance/Reports/Q1-2024-Report.pdf
  &force=false
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/UnLock HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&path=/Finance/Reports/Q1-2024-Report.pdf
&force=false
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:UnLock>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:path>/Finance/Reports/Q1-2024-Report.pdf</tns:path>
      <tns:force>false</tns:force>
    </tns:UnLock>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- **Force unlock discards changes**: When `force=true`, any in-progress changes the locking user has made to their local copy are permanently lost. Use with caution.
- If the path points to a **folder**, all documents locked within that folder are unlocked in one call (subject to the `force` permission rule).
- Use `Lock` to lock a document and `GetCheckedoutDocuments` to list all currently locked documents.

---

## Related APIs

- [Lock](Lock.md) - Lock (check out) a document or all documents in a folder
- [GetCheckedoutDocuments](GetCheckedoutDocuments.md) - Get the list of documents currently checked out by the authenticated user
- [IsLockPossible](IsLockPossible.md) - Check whether a document can be locked

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Document or folder not found | The specified path does not resolve to an existing document or folder. |
| Not locked by you | `force=false` and the document is locked by a different user. |
| Access denied | `force=true` requires administrator or domain manager rights. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/UnLock*
