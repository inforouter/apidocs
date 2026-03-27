# GetDocumentsOwnedByUser API

Returns a paged list of documents owned by the specified user, sorted by document name ascending. Supports offset-based paging via `startingRow` and `rowCount`.

## Endpoint

```
/srv.asmx/GetDocumentsOwnedByUser
```

## Methods

- **GET** `/srv.asmx/GetDocumentsOwnedByUser?authenticationTicket=...&userName=...&startingRow=...&rowCount=...`
- **POST** `/srv.asmx/GetDocumentsOwnedByUser` (form data)
- **SOAP** Action: `http://tempuri.org/GetDocumentsOwnedByUser`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `userName` | string | Yes | The username whose owned documents are to be retrieved. |
| `startingRow` | int | Yes | Zero-based row offset. Pass `0` to start from the first result. Pass `100` to skip the first 100 results. |
| `rowCount` | int | Yes | Number of rows to return (page size). |

---

## Required Permissions

| Scenario | Required permission |
|----------|---------------------|
| Caller queries their own documents | None — authenticated user only |
| Caller queries another user's documents | **ListingAuditLogOfUser** admin permission for the target user |

---

## Response

### Success Response

Returns a `<response>` element with `success="true"` containing zero or more `<document>` child elements. Results are sorted by document name **ascending**.

```xml
<response success="true">
  <document id="1234" name="AnnualReport.docx" size="245760"
            modificationDate="2026-02-01T14:30:00"
            publishedVersionAuthorName="John Smith"
            path="\MyLibrary\Reports" domainid="1" ... />
  <document id="1235" name="Invoice_001.pdf" size="102400"
            modificationDate="2026-01-15T09:00:00"
            publishedVersionAuthorName="John Smith"
            path="\MyLibrary\Finance" domainid="1" ... />
</response>
```

### Document Attribute Reference

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | int | Unique document identifier. |
| `name` | string | Document file name. |
| `size` | long | Document size in bytes. |
| `modificationDate` | DateTime | Date and time of last modification. |
| `publishedVersionAuthorName` | string | Full name of the published version author. |
| `path` | string | Full parent path of the document. |
| `domainid` | int | Internal ID of the library the document belongs to. |

Additional standard document attributes are included based on document type and system configuration.

### Empty Result

```xml
<response success="true" />
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

`startingRow` is the number of records to **skip**. `rowCount` is the number of records to **return**. The total number of owned documents can be retrieved separately to calculate the total page count.

---

## Example Requests

### GET — first page

```
GET /srv.asmx/GetDocumentsOwnedByUser?authenticationTicket=abc123-def456&userName=jsmith&startingRow=0&rowCount=50 HTTP/1.1
Host: server.example.com
```

### GET — second page

```
GET /srv.asmx/GetDocumentsOwnedByUser?authenticationTicket=abc123-def456&userName=jsmith&startingRow=50&rowCount=50 HTTP/1.1
Host: server.example.com
```

### POST

```
POST /srv.asmx/GetDocumentsOwnedByUser HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&userName=jsmith&startingRow=0&rowCount=50
```

### SOAP 1.1

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetDocumentsOwnedByUser"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetDocumentsOwnedByUser xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
      <userName>jsmith</userName>
      <startingRow>0</startingRow>
      <rowCount>50</rowCount>
    </GetDocumentsOwnedByUser>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Results are always sorted by document name **ascending** regardless of paging parameters.
- `startingRow` is zero-based: `startingRow=0` returns from the first record, `startingRow=50` skips the first 50.
- To retrieve all documents without paging, pass `startingRow=0` and a sufficiently large `rowCount`.
- Ownership is determined by the document owner field, not the author (creator). See `GetAuthoredDocuments` for author-based retrieval.

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Insufficient rights.` | The caller does not have `ListingAuditLogOfUser` permission for the target user. |
| User not found | The specified `userName` does not exist. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

## Related APIs

- [GetFoldersOwnedByUser](GetFoldersOwnedByUser.md) - Get a paged list of folders owned by a user
- [GetAuthoredDocuments](GetAuthoredDocuments.md) - Get documents authored (created) by a user
- [GetCheckedoutDocumentsByUser](GetCheckedoutDocumentsByUser.md) - Get documents currently checked out by a user
