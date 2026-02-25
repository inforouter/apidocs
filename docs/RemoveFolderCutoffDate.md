# RemoveFolderCutoffDate API

Removes the cutoff date from the specified folder and, optionally, from its subfolders and documents. Returns a log of the operation. If any individual item fails, the overall success flag returns `false` even if other items succeeded.

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
| `includeSubFolders` | bool | Yes | If `true`, the cutoff date is also removed from all subfolders recursively. |
| `includeDocuments` | bool | Yes | If `true`, the cutoff date is also removed from all documents within the folder (and subfolders if `includeSubFolders=true`). |

---

## Response

### Success Response -" No Errors

```xml
<response success="true" error="" />
```

### Partial Success Response -" Some Items Failed

```xml
<response success="false" error="MultiStatus">
  <logitem path="/Finance/Reports/Q1.pdf" status="failed" message="Access denied." />
  <logitem path="/Finance/Reports/Q2.pdf" status="success" />
</response>
```

### Error Response

```xml
<response success="false" error="Folder not found." />
```

| Attribute | Description |
|-----------|-------------|
| `success` | `"true"` only if all operations succeeded without any errors. `"false"` if any individual item failed. |
| `error` | `"MultiStatus"` indicates a partial result with per-item log entries. Otherwise contains a single error message. |

---

## Required Permissions

The calling user must have **write** permission on the folder. For documents, write permission on each document is also required.

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

## Notes

- Use `RemoveDocumentCutoffDate` to remove the cutoff date from a single document.
- When `success="false"` with `error="MultiStatus"`, inspect the `logitem` child elements for per-item results.
- If `includeSubFolders=false` and `includeDocuments=false`, only the cutoff date on the specified folder itself is removed.

---

## Related APIs

- [SetFolderCutoffDate](SetFolderCutoffDate.md) - Set the cutoff date on a folder
- [RemoveDocumentCutoffDate](RemoveDocumentCutoffDate.md) - Remove cutoff date from a single document
- [SetDocumentCutoffDate](SetDocumentCutoffDate.md) - Set cutoff date on a single document

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Folder not found | The specified path does not resolve to an existing folder. |
| Access denied | The user does not have write permission on the folder. |
| `MultiStatus` | Some items succeeded and some failed. See `logitem` elements for details. |
| `SystemError:...` | An unexpected server-side error occurred. |

---