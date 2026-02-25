# GetFoldersAndDocumentsByPage2 API

Returns a paged list of documents and folders at the specified path using an advanced XML-based filter and sort criteria. This API integrates with the infoRouter full-text search engine and supports complex multi-field filtering and relevance ranking. After this call, use the search session to retrieve results page by page.

## Endpoint

```
/srv.asmx/GetFoldersAndDocumentsByPage2
```

## Methods

- **GET** `/srv.asmx/GetFoldersAndDocumentsByPage2?authenticationTicket=...&Path=...&filterXml=...&SortBy=...&AscendingOrder=...`
- **POST** `/srv.asmx/GetFoldersAndDocumentsByPage2` (form data)
- **SOAP** Action: `http://tempuri.org/GetFoldersAndDocumentsByPage2`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the folder to list (e.g. `/Finance/Reports`). Only direct children are included. |
| `filterXml` | string | No | Optional XML filter criteria. Defines field-level filters, date ranges, and full-text query terms. Pass empty string or null for no filtering. |
| `SortBy` | string | Yes | Field name to sort results by (e.g. `DocumentName`, `ModificationDate`, `Rank`). |
| `AscendingOrder` | bool | Yes | Sort direction. `true` = ascending (A-'Z, oldest first), `false` = descending (Z-'A, newest first). |

---

## Response

The initial response returns a result count and session information, **not** the items themselves. Use the search session to retrieve the actual results page by page.

### Success Response

```xml
<response success="true" error="" count="42" ranksorted="false" />
```

### Error Response

```xml
<response success="false" error="Folder not found." />
```

| Attribute | Description |
|-----------|-------------|
| `success` | `"true"` if the search executed successfully. |
| `count` | Total number of matching items found. |
| `ranksorted` | `"true"` if results are sorted by relevance rank (full-text search); `"false"` for field-sorted results. |

---

## Required Permissions

The calling user must have **read** permission on the folder. Only accessible items are included in the results.

---

## Example

### GET Request (sort by modification date, descending)

```
GET /srv.asmx/GetFoldersAndDocumentsByPage2
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports
  &filterXml=
  &SortBy=ModificationDate
  &AscendingOrder=false
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetFoldersAndDocumentsByPage2 HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance/Reports
&filterXml=
&SortBy=ModificationDate
&AscendingOrder=false
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetFoldersAndDocumentsByPage2>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:Path>/Finance/Reports</tns:Path>
      <tns:filterXml></tns:filterXml>
      <tns:SortBy>ModificationDate</tns:SortBy>
      <tns:AscendingOrder>false</tns:AscendingOrder>
    </tns:GetFoldersAndDocumentsByPage2>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Returns only **direct** children (one level deep) of the specified path.
- The API response contains a `count` and creates a server-side search session. Use the search session to retrieve paginated results.
- `filterXml` syntax is defined by the infoRouter search filter format -" the same format used by the `Search` API.
- When `SortBy=Rank`, results are sorted by full-text search relevance; `ranksorted="true"` is returned in the response.
- This API requires the infoRouter content search service to be configured and running for full-text filtering.
- For simpler paged listings (name filter only), use `GetFoldersAndDocumentsByPage`.

---

## Related APIs

- [GetFoldersAndDocumentsByPage](GetFoldersAndDocumentsByPage.md) - Simpler paged listing with text filters
- [GetFoldersAndDocuments2](GetFoldersAndDocuments2.md) - Ultra-fast listing without paging
- [Search](Search.md) - Full system-wide search with the same XML filter format

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