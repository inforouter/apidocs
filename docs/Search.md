# Search API



Prepares a search result set using criteria provided in XML format. The search is executed server-side and the results are stored in the user's session. Use `GetNextSearchPage` and `GetPreviousSearchPage` to page through the results after calling `Search`.



## Endpoint



```

/srv.asmx/Search

```



## Methods



- **GET** `/srv.asmx/Search?authenticationTicket=...&xmlcriteria=...&SortBy=...&AscendingOrder=...`

- **POST** `/srv.asmx/Search` (form data)

- **SOAP** Action: `http://tempuri.org/Search`



## Parameters



| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `xmlcriteria` | string | Yes | XML document describing the search criteria. See the **XML Criteria Reference** section below for all supported elements. Pass an empty string to return all accessible documents. |
| `SortBy` | string | Yes | Field by which results are sorted. See **Sort Field Values** below. Pass an empty string to use the default sort order. |
| `AscendingOrder` | bool | Yes | `true` to sort ascending, `false` to sort descending. |


### Sort Field Values



| Value | Description |
|-------|-------------|
| `DOCUMENTNAME` | Sort by document or folder name |
| `DOCUMENTSIZE` | Sort by file size |
| `MIMETYPEDESCRIPTION` | Sort by MIME type / file format description |
| `MODIFICATIONDATE` | Sort by last modification date |
| `STATUSCODE` | Sort by approval/completion status code |
| `FOLDERNAME` | Sort by parent folder name |
| `LASTVERSIONNUMBER` | Sort by latest version number |
| `PERCENTCOMPLETE` | Sort by percent complete |
| `CREATIONDATE` | Sort by creation date |
| `MODIFIEDBYNAME` | Sort by the name of the user who last modified the item |
| `DESCRIPTION` | Sort by description |
| `OWNERNAME` | Sort by owner name |
| `FLOWNAME` | Sort by workflow name |
| `VIEW` | Sort by last view date |
| `CHECKEDOUTBYNAME` | Sort by the name of the user who checked out the document |
| `COMPLETIONDATE` | Sort by completion date |
| `IMPORTANCE` | Sort by importance level |
| `RDDEFID` | Sort by Retention & Disposition definition ID |
| `CLEVEL` | Sort by classification level |
| `DECLASSIFYON` | Sort by declassification date |
| `DOWNGRADEON` | Sort by downgrade date |
| `DISPOSITIONDATE` | Sort by disposition date |
| `LASTISOREVIEW` | Sort by last ISO review date |
| `NEXTISOREVIEW` | Sort by next ISO review date |
| `STEPNUMBER` | Sort by workflow step number |
| `STEPNAME` | Sort by workflow step name |
| `PROPERTSETNAME.FIELDNAME` | Sort by a custom property set field (use dot notation, e.g. `MyPSet.MyField`) |


---



## XML Criteria Reference



The `xmlcriteria` parameter must be a well-formed XML document. The root element may have any name; each child `<criteria>` element defines one search condition.



**Envelope:**

```xml

<criteria>

  <criteria NAME="..." OPERATOR="..." VALUE="..." />

  ...

</criteria>

```



Each element uses three attributes:



| Attribute | Description |
|-----------|-------------|
| `NAME` | The criterion name (case-insensitive, see table below). |
| `OPERATOR` | Comparison operator -" only required for criteria that support it. |
| `VALUE` | The criterion value. |



### Supported Criteria Elements



| NAME | OPERATOR | VALUE | Description |
|------|----------|-------|-------------|
| `SEARCHSCOPE` | -" | `ONLINE` / `ALL` / `ARCHIVE` / `ONLINE-HIDDENS` | Limits search to online, all, archived, or online-including-hidden libraries. Default: `ONLINE`. |
| `KEYWORDS` | -" | Full-text search string | Searches document content and metadata keywords. |
| `DOCUMENTNAME` | -" | Document or folder name (may include wildcards) | Filters by name. |
| `DOCUMENTID` | -" | Comma-separated integer document IDs | Retrieves specific documents by ID. |
| `FOLDERBYID` | -" | Comma-separated integer folder IDs | Retrieves specific folders by ID. |
| `FOLDERDESCRIPTION` | -" | Text string | Filters folders by description. |
| `DOCUMENTFORMAT` | -" | MIME type or extension string | Filters by file format/MIME type. |
| `SEARCHFOR` / `OBJECTTYPENAME` | -" | `DOCUMENTSONLY` / `FOLDERSONLY` / `<DocumentTypeName>` | Limits results to documents, folders, or a specific document type. |
| `DOCTYPE` | -" | Document type name | Alias -" limits to a specific document type. |
| `FOLDER` | -" | Full infoRouter folder path | Limits search to a specific folder. |
| `INCLUDESUBFOLDERS` | -" | `true` / `false` | When used with `FOLDER`, controls whether sub-folders are included. |
| `VIEWCRITERIA` | -" | `NOVIEW` / `UPDATED` / `SAW` | Filters by view state. Add `USERNAME="username"` attribute to filter by another user's view state. |
| `CHECKOUTSTATUS` | -" | `CHECKEDOUT` / `NOTCHECKEDOUT` / `CHECKEDOUTBYME` / `CHECKEDOUTBYUSER` | Filters by checkout status. `CHECKEDOUTBYUSER` also requires a `USERNAME="username"` attribute on the element. |
| `USERNAME` | -" | infoRouter username | Filters documents by author (owner). |
| `SIZEIS` | `EQLT` (at least) / `EQGT` (at most) | Size in bytes | Filters by file size. |
| `IMPORTANCE` | `EQ` / `GT-EQ` / `GT` / `LT` / `LT-EQ` | `LOW` / `NORMAL` / `HIGH` / `VITAL` | Filters by document importance. |
| `CLEVEL` | -" | `NOMARKINGS` / `DECLASSIFIED` / `CONFIDENTIAL` / `SECRET` / `TOPSECRET` | Filters by classification level. |
| `DATECRITERIA` | `EQ` / `EQLT` / `EQGT` / `BETWEEN` | Date string `yyyy-MM-dd`; for `BETWEEN` use `date1\|date2` | Filters by a date field. Add `SUBTYPE` attribute to specify which date field (see **Date Criteria Subtypes** below). |
| `DOCSRC` | -" | Source string | Filters by document source. |
| `DOCLANG` | -" | Language code (see **Document Language Values** below) | Filters by document language. |
| `DOCAUTHOR` | -" | Author name string | Filters by document author metadata field. |
| `RDDEFID` | -" | Integer Retention & Disposition definition ID | Filters by retention schedule definition. |
| `PUBLISHSTATUS` | -" | `0` (ignore) / `1` (unpublished) / `2` (published) | Filters by publish status. |
| `SUBSCRIPTIONSOF` | -" | infoRouter username | Returns items (documents and folders) that the specified user is subscribed to. |
| `FAVORITESOF` | -" | infoRouter username | Returns items in the specified user's favorites list. |
| `RECENTDOCUMENTS` | -" | -" | Returns the current user's recent documents. No `VALUE` attribute is required; the presence of this element is sufficient. |
| `DOWNLOADQUEOF` | -" | infoRouter username | Returns items currently in the specified user's download queue. |
| `PROPERTYSETNAME` | -" | Property set name (child elements define field criteria) | Filters by custom property set values. See **Property Set Criteria** below. |


### Date Criteria Subtypes



The `DATECRITERIA` element requires a `SUBTYPE` attribute to specify which date field to filter by:


| SUBTYPE value | Description |
|---------------|-------------|
| `REGISTERDATE` | Date the document was registered/added to the system |
| `CREATED` | Document creation date |
| `MODIFIED` | Last modification date |
| `CREATED OR MODIFIED` | Either the creation or modification date |
| `COMPLETED ON` | Workflow completion date |
| `DECLASSIFY ON` | Scheduled declassification date |
| `DOWNGRADE ON` | Scheduled downgrade date |
| `DOWNGRADE DATE` | Actual downgrade date |
| `RETAIN UNTIL` | Retention expiration date |
| `LAST ISO REVIEW DATE` | Date of the last ISO compliance review |
| `NEXT ISO REVIEW DATE` | Date of the next scheduled ISO compliance review |
| `DISPOSITION DATE` | Scheduled disposition date |
| `EXPIRATION DATE` | Document expiration date |
| `CUTOFF DATE` | Records cutoff date |

**Example:**

```xml

<criteria NAME="DATECRITERIA" OPERATOR="EQGT" SUBTYPE="CREATED" VALUE="2025-01-01" />

<criteria NAME="DATECRITERIA" OPERATOR="BETWEEN" SUBTYPE="MODIFIED" VALUE="2024-01-01|2024-12-31" />

```



### Document Language Values



The `DOCLANG` criterion accepts the following ISO 639-1 language codes:



`en`, `de`, `es`, `fr`, `da`, `el`, `et`, `he`, `hi`, `hu`, `id`, `it`, `ja`, `ko`, `nl`, `no`, `pl`, `pt`, `ro`, `ru`, `sv`, `tk`, `tr`, `uk`, `ur`, `uz`, `vi`, `zh`



### Property Set Criteria



To filter by a custom property set, use the `PROPERTYSETNAME` element with child elements for each field:



```xml

<criteria NAME="PROPERTYSETNAME" VALUE="MyPropertySet">

  <criteria NAME="FieldName" OPERATOR="LIKE" VALUE="Annual Report" />

  <criteria NAME="Amount"    OPERATOR="EQGT" VALUE="1000" />

</criteria>

```



Supported operators per field data type:



| Data Type | Operators |
|-----------|-----------|
| `CHAR` (text) | `LIKE`, `EQ`, `NULL`, `NOTNULL` |
| `NUMBER` | `EQ`, `NOTEQ`, `EQLT`, `EQGT`, `GT`, `LT`, `NULL`, `NOTNULL` |
| `DATE` | `ANYTIME`, `YESTERDAY`, `TODAY`, `LAST7DAYS`, `NEXT7DAYS`, `LASTWEEK`, `THISWEEK`, `NEXTWEEK`, `LASTMONTH`, `THISMONTH`, `NEXTMONTH`, `EQ`, `EQGT`, `EQLT`, `NULL` |
| `BOOLEAN` | `EQ`, `NULL`, `NOTNULL` |


---



## Response



`Search` prepares the result set and stores it in the session. The response confirms the query was accepted and includes metadata about the total result counts.



### Success Response



```xml

<root success="true" ranksorted="false" />

```



| Attribute | Description |
|-----------|-------------|
| `success` | `true` if the query was prepared successfully. |
| `ranksorted` | `true` if results are sorted by full-text relevance rank; `false` otherwise. |



After a successful `Search` call, use `GetNextSearchPage` to retrieve the first page of results.



### Error Response



```xml

<root success="false" error="[ErrorCode] Error message" />

```



---



## Required Permissions



Any authenticated user may call this API. Results are automatically filtered to items the user has at least **Read** permission for. Read-only users may also use this API.



---



## Example



### GET Request



```

GET /srv.asmx/Search?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

  &xmlcriteria=%3Ccriteria%3E%3Ccriteria+NAME%3D%22KEYWORDS%22+VALUE%3D%22annual+report%22%2F%3E%3C%2Fcriteria%3E

  &SortBy=MODIFICATIONDATE

  &AscendingOrder=false

HTTP/1.1

```



### POST Request



```

POST /srv.asmx/Search HTTP/1.1

Content-Type: application/x-www-form-urlencoded



authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

&xmlcriteria=<criteria>

    <criteria NAME="FOLDER"            VALUE="/Finance/Reports" />

    <criteria NAME="INCLUDESUBFOLDERS" VALUE="true" />

    <criteria NAME="DATECRITERIA"      OPERATOR="EQGT" SUBTYPE="MODIFIED" VALUE="2025-01-01" />

    <criteria NAME="SEARCHFOR"         VALUE="DOCUMENTSONLY" />

  </criteria>

&SortBy=MODIFICATIONDATE

&AscendingOrder=false

```



### SOAP Request



```xml

<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"

               xmlns:tns="http://tempuri.org/">

  <soap:Body>

    <tns:Search>

      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>

      <tns:xmlcriteria>&lt;criteria&gt;

        &lt;criteria NAME="KEYWORDS" VALUE="annual report"/&gt;

      &lt;/criteria&gt;</tns:xmlcriteria>

      <tns:SortBy>MODIFICATIONDATE</tns:SortBy>

      <tns:AscendingOrder>false</tns:AscendingOrder>

    </tns:Search>

  </soap:Body>

</soap:Envelope>

```



### Full Criteria Example -" Advanced Search



```xml

<criteria>

  <criteria NAME="SEARCHSCOPE"       VALUE="ONLINE" />

  <criteria NAME="KEYWORDS"          VALUE="quarterly budget" />

  <criteria NAME="FOLDER"            VALUE="/Finance/Reports" />

  <criteria NAME="INCLUDESUBFOLDERS" VALUE="true" />

  <criteria NAME="SEARCHFOR"         VALUE="DOCUMENTSONLY" />

  <criteria NAME="DATECRITERIA"      OPERATOR="BETWEEN" SUBTYPE="MODIFIED" VALUE="2024-01-01|2024-12-31" />

  <criteria NAME="IMPORTANCE"        OPERATOR="EQ" VALUE="HIGH" />

  <criteria NAME="PUBLISHSTATUS"     VALUE="2" />

  <criteria NAME="PROPERTYSETNAME"   VALUE="ProjectMetadata">

    <criteria NAME="Department" OPERATOR="EQ"   VALUE="Finance" />

    <criteria NAME="Budget"     OPERATOR="EQGT" VALUE="50000" />

  </criteria>

</criteria>

```



### User-Scoped Search Examples



```xml

<!-- Items subscribed to by a user -->

<criteria>

  <criteria NAME="SUBSCRIPTIONSOF" VALUE="jsmith" />

</criteria>



<!-- Items in a user's favorites -->

<criteria>

  <criteria NAME="FAVORITESOF" VALUE="jsmith" />

</criteria>



<!-- Current user's recent documents -->

<criteria>

  <criteria NAME="RECENTDOCUMENTS" />

</criteria>



<!-- Items in a user's download queue -->

<criteria>

  <criteria NAME="DOWNLOADQUEOF" VALUE="jsmith" />

</criteria>

```



---



## Notes



- The `Search` API only **prepares** the result set; it does not return document listings. Call `GetNextSearchPage` immediately after to retrieve the first page.

- Result sets are stored server-side in the user's session and expire with the session (30-day sliding window).

- Passing an empty string for `xmlcriteria` returns all documents and folders accessible to the user, subject to permissions.

- Passing an empty string for `SortBy` uses the system default sort (by document name, ascending).

- Full-text search (`KEYWORDS`) requires a content search service (Windows Search, DTSearch, or Remote Search) to be configured and running. If no content search service is available, keyword searches return only metadata matches.

- The `DATECRITERIA` value for `BETWEEN` uses a pipe (`|`) separator: `startDate|endDate` in `yyyy-MM-dd` format.

- The `DATECRITERIA` operator `EQLT` means "on or before the given date"; `EQGT` means "on or after the given date"; `EQ` means exactly on the given date.

- The `CHECKOUTSTATUS` value `CHECKEDOUTBYUSER` requires an additional `USERNAME` attribute on the same element specifying the target user's login name.

- The `VIEWCRITERIA` criterion can optionally include a `USERNAME` attribute to filter by another user's view history (requires appropriate permissions).

- The `SUBSCRIPTIONSOF`, `FAVORITESOF`, and `DOWNLOADQUEOF` criteria require the `VALUE` attribute to be a valid infoRouter username; an error is returned if the user is not found.

- The `RECENTDOCUMENTS` criterion returns recent documents for the currently authenticated user only; no `VALUE` attribute is required.

- Property set field names are case-insensitive, but the property set name must match an existing definition in the system.



---



## Related APIs



- [GetNextSearchPage](GetNextSearchPage.md) - Retrieves the next page of the prepared search results

- [GetPreviousSearchPage](GetPreviousSearchPage.md) - Retrieves the previous page of the prepared search results

- [GetFoldersAndDocuments](GetFoldersAndDocuments.md) - Lists documents and folders in a specific path without a search query

- [GetDocuments](GetDocuments.md) - Returns documents in a specific folder path



---



## Error Codes



| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Folder not found` | The path specified in `FOLDER` criterion does not exist or is not accessible. |
| `Possible values for SEARCHSCOPE: ONLINE, ALL, ARCHIVE, ONLINE-HIDDENS` | Invalid `SEARCHSCOPE` value. |
| `Possible Sort Options: DOCUMENTNAME, DOCUMENTSIZE, ...` | Invalid `SortBy` field name. |
| `Possible values for CLEVEL: NOMARKINGS, DECLASSIFIED, CONFIDENTIAL, SECRET, TOPSECRET` | Invalid `CLEVEL` value. |
| `Possible operators for DATECRITERIA: EQ, EQLT, EQGT, BETWEEN` | Invalid `DATECRITERIA` operator. |
| `Possible values for PUBLISHSTATUS: 0, 1, 2` | Invalid `PUBLISHSTATUS` value. |
| `Possible operator values for SIZEIS: EQLT, EQGT` | Invalid `SIZEIS` operator. |
| `Property set field cannot be found` | The specified property set or field name does not exist. |
| `CHECKOUTSTATUS: CHECKEDOUTBYUSER requires criteria USERNAME attribute` | Missing `USERNAME` attribute when using `CHECKEDOUTBYUSER`. |
| `VALUE attribute cannot be blank for SUBSCRIPTIONSOF criteria.` | Missing `VALUE` for `SUBSCRIPTIONSOF`. |
| `VALUE attribute cannot be blank for FAVORITESOF criteria.` | Missing `VALUE` for `FAVORITESOF`. |
| `VALUE attribute cannot be blank for DOWNLOADQUEOF criteria.` | Missing `VALUE` for `DOWNLOADQUEOF`. |
| `Specified user cannot be found specified SUBSCRIPTIONSOF attribute.` | User specified in `SUBSCRIPTIONSOF` does not exist. |
| `Specified user cannot be found specified FAVORITESOF attribute.` | User specified in `FAVORITESOF` does not exist. |
| `Specified user cannot be found specified DOWNLOADQUEOF attribute.` | User specified in `DOWNLOADQUEOF` does not exist. |

---


