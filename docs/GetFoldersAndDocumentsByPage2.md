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
| `SortBy` | string | Yes | Column to sort by, or `PROPERTYSETNAME.FIELDNAME` to sort by a custom field. Case-insensitive. One of: `DOCUMENTNAME`, `DOCUMENTSIZE`, `MIMETYPEDESCRIPTION`, `MODIFICATIONDATE`, `STATUSCODE`, `FOLDERNAME`, `LASTVERSIONNUMBER`, `PERCENTCOMPLETE`, `CREATIONDATE`, `MODIFIEDBYNAME`, `DESCRIPTION`, `OWNERNAME`, `FLOWNAME`, `VIEW`, `CHECKEDOUTBYNAME`, `COMPLETIONDATE`, `IMPORTANCE`, `RDDEFID`, `CLEVEL`, `DECLASSIFYON`, `DOWNGRADEON`, `DISPOSITIONDATE`, `LASTISOREVIEW`, `NEXTISOREVIEW`. Anything else is refused with `4000`, and the message lists the accepted values. |
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

### Relevance and Where the Term Was Found

Because this call returns no items, it carries no per-document relevance either. Both arrive with
the items: page the prepared session with [GetNextSearchPage](GetNextSearchPage.md), and every
document a full-text `KEYWORDS` filter ranked carries a `<RankInfo>` child element giving `Rank`
(higher is a closer match) and where the term was found: `FoundIn` is `1` for the document's own
text (in the version `FoundInVersionNumber` names), `2` for its properties or comments, `3` for an
e-mail attachment, `4` for a workflow history entry. A document matched by field criteria alone
carries no `<RankInfo>` element. See
[GetNextSearchPage](GetNextSearchPage.md#rankinfo-element-full-text-search-results) for the full
attribute table.

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

Despite the name, this one returns no page. It opens a search over the folder and answers how many
items matched; the items themselves come from `GetNextSearchPage` on the same session.

`Path` is a non-nullable string on the REST action, so an empty one is refused by model binding with
HTTP 400 before the operation runs - there is no error document to read in that case.

`SortBy` is a non-nullable string too, so an empty one is refused the same way. Sort names are
case-insensitive, and a name that is not on the list is refused with `4000` and a message naming the
ones that are.

```javascript
const opened = await call('GetFoldersAndDocumentsByPage2', {
  authenticationTicket: ticket,
  Path: '/Public/ApiTests',
  filterXml: '',
  SortBy: 'MODIFICATIONDATE',
  AscendingOrder: false
});

console.log(opened.getAttribute('count'), 'items matched');

// The count is all this call returns. Read the items a page at a time.
const page = await call('GetNextSearchPage', {
  authenticationTicket: ticket,
  withrules: false,
  withPropertySets: false,
  withSecurity: false,
  withOwner: false,
  withVersions: false
});
```

`filterXml` is optional, but it is parsed as XML when it is not empty, and a value that is not
well-formed is refused with `4000` carrying the parser's own message.

## Notes

- Returns only **direct** children (one level deep) of the specified path.
- The API response contains a `count` and creates a server-side search session. Use the search session to retrieve paginated results.
- `filterXml` syntax is defined by the infoRouter search filter format -" the same format used by the `Search` API.
- **`Rank` is not an accepted `SortBy` value here**, despite being one wherever search results are ranked: passing it is answered `4000`. `ranksorted` on the response reports whether the prepared session ended up rank-sorted; the rank of each individual document, and the part of the document the term was found in, come back on the pages as `<RankInfo>`.
- This API requires the infoRouter content search service to be configured and running for full-text filtering.
- For simpler paged listings (name filter only), use `GetFoldersAndDocumentsByPage`.

---

## Related APIs

- [GetFoldersAndDocumentsByPage](GetFoldersAndDocumentsByPage.md) - Simpler paged listing with text filters
- [GetFoldersAndDocuments2](GetFoldersAndDocuments2.md) - Ultra-fast listing without paging
- [Search](Search.md) - Full system-wide search with the same XML filter format
- [GetNextSearchPage](GetNextSearchPage.md) - Retrieve the prepared results page by page, with `<RankInfo>` on each ranked document

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4041` | no folder at that path - including one the caller may not see, which is not told apart from one that does not exist |
| `4000` | `SortBy` is not one of the accepted sort names; the message lists them |
| `4000` | the document was not well-formed XML; the message carries the parser's own words |
| `HTTP 400` | `Path` was empty; refused by model binding, so there is no error document |
| `HTTP 400` | `SortBy` was empty; also refused by model binding |

A call with no ticket at all is not automatically refused: it signs in as the anonymous user, so a
library flagged as anonymous can be listed without authenticating. Everything else answers `4041`,
because a folder the anonymous user cannot see is not told apart from one that does not exist.

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Folder not found | The specified path does not resolve to an existing folder. |
| Access denied | The user does not have read permission on the folder. |
| `SystemError:...` | An unexpected server-side error occurred. |

---