# GetFoldersAndDocumentsByPage API

Returns a page of documents and folders at the specified path, with optional name filtering for both folders and documents. Each page contains up to 20 items. Use `PageNumber` to navigate through large listings.

## Endpoint

```
/srv.asmx/GetFoldersAndDocumentsByPage
```

## Methods

- **GET** `/srv.asmx/GetFoldersAndDocumentsByPage?authenticationTicket=...&Path=...&FolderFilter=...&DocumentFilter=...&PageNumber=...`
- **POST** `/srv.asmx/GetFoldersAndDocumentsByPage` (form data)
- **SOAP** Action: `http://tempuri.org/GetFoldersAndDocumentsByPage`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the folder (e.g. `/Finance/Reports`). |
| `FolderFilter` | string | No | Optional substring filter for folder names. Pass empty string or null for no filtering. |
| `DocumentFilter` | string | No | Optional substring filter for document names. Pass empty string or null for no filtering. |
| `PageNumber` | int | Yes | Page number to retrieve (1-based). Each page contains up to 20 items. |

---

## Response

### Success Response

```xml
<response success="true">
  <folder id="456" name="2024" />
  <document id="1001" name="Q1-Report.pdf" versionid="1000045" />
  <document id="1002" name="Q2-Report.pdf" versionid="1000067" />
</response>
```

### Error Response

```xml
<response success="false" error="Folder not found." />
```

---

## Required Permissions

The calling user must have **read** permission on the folder. Only accessible items are returned.

---

## Example

### GET Request (page 1, no filters)

```
GET /srv.asmx/GetFoldersAndDocumentsByPage
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports
  &FolderFilter=
  &DocumentFilter=
  &PageNumber=1
HTTP/1.1
```

### GET Request (page 2, filter for documents with "Q" in name)

```
GET /srv.asmx/GetFoldersAndDocumentsByPage
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports
  &FolderFilter=
  &DocumentFilter=Q
  &PageNumber=2
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetFoldersAndDocumentsByPage HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance/Reports
&FolderFilter=
&DocumentFilter=
&PageNumber=1
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetFoldersAndDocumentsByPage>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:Path>/Finance/Reports</tns:Path>
      <tns:FolderFilter></tns:FolderFilter>
      <tns:DocumentFilter></tns:DocumentFilter>
      <tns:PageNumber>1</tns:PageNumber>
    </tns:GetFoldersAndDocumentsByPage>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Returns only **direct** children (one level deep) of the specified path.
- Each page returns up to 20 items; folders and documents are mixed in the response.
- `FolderFilter` and `DocumentFilter` perform a case-insensitive substring match on the name.
- An empty response (no child elements) after page 1 means there are no matching items.
- For advanced filtering (by metadata, date ranges, or full-text content) and sorting, use `GetFoldersAndDocumentsByPage2`.
- For full property details per item, use `GetFoldersAndDocuments`.

---

## Related APIs

- [GetFoldersAndDocuments2](GetFoldersAndDocuments2.md) - Lightweight listing without paging
- [GetFoldersAndDocumentsByPage2](GetFoldersAndDocumentsByPage2.md) - Advanced paged listing with XML filters and sorting
- [GetFoldersByPage](GetFoldersByPage.md) - Paged listing of folders only

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Folder not found | The specified path does not resolve to an existing folder. |
| Access denied | The user does not have read permission on the folder. |
| `SystemError:...` | An unexpected server-side error occurred. |

---