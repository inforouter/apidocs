# DeleteDocumentVersion API

Permanently deletes a specific version of a document. The deletion is irreversible — the version's file content and metadata are removed from the warehouse.

## Endpoint

```
/srv.asmx/DeleteDocumentVersion
```

## Methods

- **GET** `/srv.asmx/DeleteDocumentVersion?authenticationTicket=...&DocumentPath=...&VersionNumber=...`
- **POST** `/srv.asmx/DeleteDocumentVersion` (form data)
- **SOAP** Action: `http://tempuri.org/DeleteDocumentVersion`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DocumentPath` | string | Yes | Full infoRouter path of the document (e.g. `/MyLibrary/Reports/Report.pdf`). |
| `VersionNumber` | int | Yes | Version number to delete. Must be ≥ 1,000,000 (modernized version number format). Use `GetDocumentVersions` to retrieve valid version numbers for a document. |

## Response

### Success Response

```xml
<root success="true" />
```

### Error Response

```xml
<root success="false" error="Error message" />
```

---

## Required Permissions

The authenticated user must have **VersionDelete** permission on the document.

Additionally:
- If the document is **checked out by another user**, the deletion is blocked. The user who has it checked out may delete versions.
- The specified version must exist (not already deleted).

---

## Example

### GET Request

```
GET /srv.asmx/DeleteDocumentVersion
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DocumentPath=/MyLibrary/Reports/Report.pdf
  &VersionNumber=3000000
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/DeleteDocumentVersion HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&DocumentPath=/MyLibrary/Reports/Report.pdf
&VersionNumber=3000000
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:DeleteDocumentVersion>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:DocumentPath>/MyLibrary/Reports/Report.pdf</tns:DocumentPath>
      <tns:VersionNumber>3000000</tns:VersionNumber>
    </tns:DeleteDocumentVersion>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Version numbers in infoRouter use a modernized format where each version is stored as a multiple of 1,000,000 (e.g. version 1 → `1000000`, version 2 → `2000000`, version 3 → `3000000`). Passing a version number below 1,000,000 returns an error immediately.
- Always retrieve current version numbers using `GetDocumentVersions` before calling this API.
- This deletion is **permanent and irreversible**. The version's content and metadata are removed from the warehouse.
- If the document has legacy version numbers stored in the database (below 1,000,000), the system automatically upgrades them to the new format before performing the deletion.
- If the document is **checked out by another user**, the operation fails. The document owner or a domain manager can unlock the document first using `UnLock`.

---

## Related APIs

- [GetDocumentVersions](GetDocumentVersions.md) - List all versions of a document (use to retrieve valid VersionNumber values)
- [GetDocumentVersion](GetDocumentVersion.md) - Get details of a specific document version
- [UnLock](UnLock.md) - Unlock a checked-out document
- [PublishDocument](PublishDocument.md) - Publish a specific version of a document
- [DeleteDocument](DeleteDocument.md) - Move a document to the recycle bin

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Document not found` | The `DocumentPath` does not refer to an existing document. |
| Invalid version number | `VersionNumber` is below 1,000,000 (not in the modernized format). |
| `Version not found` | The specified version does not exist or has already been deleted. |
| `Access denied` | The caller does not have `VersionDelete` permission on the document. |
| `Checked out by another user` | The document is currently checked out by a different user. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/DeleteDocumentVersion*
