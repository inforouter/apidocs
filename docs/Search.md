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
| `SIZEIS` | `EQLT` (at most) / `EQGT` (at least) | Size in bytes | Filters by file size. |
| `IMPORTANCE` | `EQ` / `GT-EQ` / `GT` / `LT` / `LT-EQ` | `LOW` / `NORMAL` / `HIGH` / `VITAL` | Filters by document importance. |
| `CLEVEL` | -" | `NOMARKINGS` / `DECLASSIFIED` / `CONFIDENTIAL` / `SECRET` / `TOPSECRET` | Filters by classification level. |
| `DATECRITERIA` | `EQ` / `EQLT` / `EQGT` / `BETWEEN` | Date string `yyyy-MM-dd`; for `BETWEEN` use <code>date1&#124;date2</code> | Filters by a date field. Add `SUBTYPE` attribute to specify which date field (see **Date Criteria Subtypes** below). |
| `DOCSRC` | -" | Source string | Filters by document source. |
| `DOCLANG` | -" | Language code (see **Document Language Values** below) | Filters by document language. |
| `DOCAUTHOR` | -" | Author name string | Filters by document author metadata field. |
| `RDDEFID` | -" | Integer Retention & Disposition definition ID | Filters by retention schedule definition. |
| `PUBLISHSTATUS` | -" | `0` (ignore) / `1` (unpublished) / `2` (published) | Filters by publish status. |
| `AIENHANCED` | -" | `ANY` / `ALL` / `NONE`, or a comma-separated list of attribute names (see **AI Enhanced Criteria** below) | Filters by which of a document's attributes infoRouter Connect produced. Documents only. |
| `SUBSCRIPTIONSOF` | -" | infoRouter username | Returns items (documents and folders) that the specified user is subscribed to. |
| `FAVORITESOF` | -" | infoRouter username | Returns items in the specified user's favorites list. |
| `RECENTDOCUMENTS` | -" | -" | Returns the current user's recent documents. No `VALUE` attribute is required; the presence of this element is sufficient. |
| `DOWNLOADQUEOF` | -" | infoRouter username | Returns items currently in the specified user's download queue. |
| `TEMPLATEPATH` | -" | Full infoRouter document path of the template, or `~D<id>` short form. Use `~D999` for HTML documents. | Filters documents rendered from the specified template. Use `~D999` to find all HTML form documents. |
| `PROPERTYSETNAME` | -" | Property set name (child elements define field criteria) | Filters by custom property set values. See **Property Set Criteria** below. |

### AI Enhanced Criteria

`AIENHANCED` filters on which of a document's attributes infoRouter Connect produced. Everything
is said in `VALUE`; there is no `OPERATOR`.

| `VALUE` | Matches |
|---------|---------|
| `ANY` | Documents where Connect produced **at least one** attribute. |
| `ALL` | Documents where Connect produced **every** attribute it can produce. |
| `NONE` | Documents where Connect produced **nothing**. |
| A list of attribute names | Documents carrying **all** of the named attributes. |

The attribute names are the ones the `AIEnhanced` attribute reports on each document -
`SUMMARY`, `DESCRIPTION`, `KEYWORDS`, `OCRTEXT`, `DOCUMENTTYPE`, `ABSTRACT`, `EXTRACTEDDATA`,
`MARKDOWN`, `REDACTEDTEXT`. See [AIEnhanced](GetDocument.md#aienhanced) for what each one means.
Case and spacing do not matter.

```xml
<!-- documents a model has touched at all -->
<criteria NAME="AIENHANCED" VALUE="ANY" />

<!-- documents no model has touched -->
<criteria NAME="AIENHANCED" VALUE="NONE" />

<!-- documents whose summary Connect wrote -->
<criteria NAME="AIENHANCED" VALUE="SUMMARY" />

<!-- documents carrying both a generated summary and a generated abstract -->
<criteria NAME="AIENHANCED" VALUE="SUMMARY,ABSTRACT" />
```

Notes:

- **Documents only.** The flag lives on documents, so a search carrying this criterion returns
  no folders and no shortcuts, in the same way `DOCTYPE` and `IMPORTANCE` already do.
- A list means **all** of the names, not any of them. `SUMMARY,ABSTRACT` is a document carrying
  both. To find documents with either, run the two searches.
- `ANY`, `ALL` and `NONE` cover every attribute, including ones added in later releases, so a
  search written today keeps meaning what it says.
- A `VALUE` that is neither one of the three words nor a known attribute name is rejected, and the
  error lists what it could have been. A misspelt attribute fails rather than quietly narrowing
  the search.

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

To filter by the values of a custom property set, add a `PROPERTYSETNAME` element whose `VALUE` is the
property set name, with one child element per field to filter on:

```xml
<criteria NAME="PROPERTYSETNAME" VALUE="Invoice">
  <criteria NAME="Customer" OPERATOR="LIKE"    VALUE="Acme" />
  <criteria NAME="Amount"   OPERATOR="BETWEEN" VALUE="1000|5000" />
  <criteria NAME="DueOn"    OPERATOR="BETWEEN" VALUE="2026-01-01|2026-03-31" />
  <criteria NAME="Paid"     OPERATOR="EQ"      VALUE="false" />
</criteria>
```

A document matches only if it meets **every** field condition (they are combined with AND). Field names
are not case sensitive. A field of the set that has no child element puts no condition on the search.

#### Operators by field type

| Field type | `OPERATOR` | `VALUE` | Matches |
|---|---|---|---|
| Text (`CHAR`) | `LIKE` (or `CONTAINS`) | text | the field contains the text |
| | `NOTCONTAINS` | text | the field does not contain the text |
| | `EQ` | text | the field is exactly the text |
| | `NEQ` | text | the field is anything but the text |
| | `NOTNULL` | empty | the field has a value |
| | `NULL` | empty | the field has no value |
| Number (`NUMBER`) | `EQ` | number | equal to |
| | `NOTEQ` (or `NEQ`) | number | not equal to |
| | `GT` / `LT` | number | greater than / less than |
| | `EQGT` / `EQLT` | number | at least / at most |
| | `BETWEEN` | <code>low&#124;high</code> | from `low` to `high`, both included |
| | `NOTNULL` | empty | the field has a value |
| | `NULL` | empty | the field has no value |
| Date (`DATE`) | `EQ` | date | on that day |
| | `EQGT` / `EQLT` | date | on or after / on or before that day |
| | `BETWEEN` | <code>start&#124;end</code> | from `start` to `end`, both days included |
| | `TODAY`, `YESTERDAY` | empty | relative to today |
| | `LAST7DAYS`, `NEXT7DAYS` | empty | the 7 days before / after today |
| | `LASTWEEK`, `THISWEEK`, `NEXTWEEK` | empty | the calendar week |
| | `LASTMONTH`, `THISMONTH`, `NEXTMONTH` | empty | the calendar month |
| | `ANYTIME` | empty | the field has a date |
| | `NULL` | empty | the field has no date |
| Yes/No (`BOOLEAN`) | `EQ` | `true` / `false` | the field has that value |
| | `NOTNULL` | empty | the field has a value |
| | `NULL` | empty | the field has no value |

- Operators are not case sensitive.
- **`BETWEEN`** takes two values separated by `|`, as `DATECRITERIA` does; `;` is accepted as well.
  Both ends are included. For a date written without a time, the end date counts as the whole day:
  `2026-01-01|2026-03-31` includes documents dated 31 March. An end date with a time is taken at that time.
- Write dates as `yyyy-MM-dd`. `EQ`, `EQGT` and `EQLT` compare whole days; a time in the value is ignored.
- An operator that does not exist for the field's type is refused, for example `BETWEEN` on a text field
  or `NOTNULL` on a date field (use `ANYTIME`).
- An operator that takes no value (`NULL`, `NOTNULL`, `ANYTIME`, `TODAY`, ...) must be sent with an empty
  `VALUE`; a value is refused.

#### Examples by field type

The examples use a property set `Invoice` with a text field `Customer`, a number field `Amount`, a date
field `DueOn` and a yes/no field `Paid`. Each `PROPERTYSETNAME` element below is one complete property set
criterion; put it inside the `<criteria>` root with any other criteria.

**Text (`CHAR`)**

```xml
<criteria NAME="PROPERTYSETNAME" VALUE="Invoice">
  <criteria NAME="Customer" OPERATOR="LIKE"        VALUE="Acme" />      <!-- contains "Acme" -->
</criteria>

<criteria NAME="PROPERTYSETNAME" VALUE="Invoice">
  <criteria NAME="Customer" OPERATOR="EQ"          VALUE="Acme Ltd" />  <!-- exactly "Acme Ltd" -->
</criteria>

<criteria NAME="PROPERTYSETNAME" VALUE="Invoice">
  <criteria NAME="Customer" OPERATOR="NOTCONTAINS" VALUE="Test" />      <!-- does not contain "Test" -->
</criteria>

<criteria NAME="PROPERTYSETNAME" VALUE="Invoice">
  <criteria NAME="Customer" OPERATOR="NULL"        VALUE="" />          <!-- no customer entered -->
</criteria>
```

**Number (`NUMBER`)**

```xml
<criteria NAME="PROPERTYSETNAME" VALUE="Invoice">
  <criteria NAME="Amount" OPERATOR="BETWEEN" VALUE="1000|5000" />  <!-- 1000 to 5000, both included -->
</criteria>

<criteria NAME="PROPERTYSETNAME" VALUE="Invoice">
  <criteria NAME="Amount" OPERATOR="EQGT"    VALUE="10000" />      <!-- 10000 or more -->
</criteria>

<criteria NAME="PROPERTYSETNAME" VALUE="Invoice">
  <criteria NAME="Amount" OPERATOR="NOTEQ"   VALUE="0" />          <!-- anything but 0 -->
</criteria>
```

**Date (`DATE`)**

```xml
<criteria NAME="PROPERTYSETNAME" VALUE="Invoice">
  <criteria NAME="DueOn" OPERATOR="BETWEEN"   VALUE="2026-01-01|2026-03-31" />  <!-- the first quarter, 31 March included -->
</criteria>

<criteria NAME="PROPERTYSETNAME" VALUE="Invoice">
  <criteria NAME="DueOn" OPERATOR="EQLT"      VALUE="2026-06-30" />             <!-- on or before 30 June -->
</criteria>

<criteria NAME="PROPERTYSETNAME" VALUE="Invoice">
  <criteria NAME="DueOn" OPERATOR="NEXT7DAYS" VALUE="" />                       <!-- due in the coming week -->
</criteria>

<criteria NAME="PROPERTYSETNAME" VALUE="Invoice">
  <criteria NAME="DueOn" OPERATOR="ANYTIME"   VALUE="" />                       <!-- has a due date at all -->
</criteria>
```

**Yes/No (`BOOLEAN`)**

```xml
<criteria NAME="PROPERTYSETNAME" VALUE="Invoice">
  <criteria NAME="Paid" OPERATOR="EQ"   VALUE="false" />  <!-- not paid -->
</criteria>

<criteria NAME="PROPERTYSETNAME" VALUE="Invoice">
  <criteria NAME="Paid" OPERATOR="NULL" VALUE="" />       <!-- never set -->
</criteria>
```

**Several fields at once.** All conditions must hold: unpaid invoices of Acme between 1,000 and 5,000,
due in the first quarter.

```xml
<criteria>
  <criteria NAME="SEARCHFOR" VALUE="DOCUMENTSONLY" />
  <criteria NAME="PROPERTYSETNAME" VALUE="Invoice">
    <criteria NAME="Customer" OPERATOR="LIKE"    VALUE="Acme" />
    <criteria NAME="Amount"   OPERATOR="BETWEEN" VALUE="1000|5000" />
    <criteria NAME="DueOn"    OPERATOR="BETWEEN" VALUE="2026-01-01|2026-03-31" />
    <criteria NAME="Paid"     OPERATOR="EQ"      VALUE="false" />
  </criteria>
</criteria>
```

#### When `OPERATOR` is missing or `VALUE` is empty

| Field element | Result |
|---|---|
| no `OPERATOR` (or `OPERATOR=""`) and an empty `VALUE` | No condition on that field; the search runs as if the field were not listed. |
| no `OPERATOR` but a `VALUE` | Refused with `4000`: *A search field value cannot be specified without a valid operator.* (For a date field the message says the value must be empty for the operator.) |
| an operator that needs a value, with an empty `VALUE` | No condition on that field. It is **not** refused. |
| `BETWEEN` without both ends (`VALUE="500"`, <code>"500&#124;"</code> or empty) | Refused with `4000`: *Invalid condition specified for the field: SET.FIELD: BETWEEN needs two values separated by \|: the low end and the high end.* |

An operator other than `BETWEEN` sent with an empty value is not refused, so a search built from a form
with empty inputs silently matches more documents rather than failing. Leave a field out, or check its
value, before sending it.

#### Errors

| Case | Result |
|---|---|
| A field name the property set does not have | Refused with `4000`: *Property set field cannot be found : SET.FIELD* |
| An operator the field type does not have | Refused with `4000`: *Invalid condition specified for the field: SET.FIELD: Invalid operator for text field* (or number, date, boolean) |
| A value that is not a number or a date where one is needed | Refused with `4000`: *Invalid condition specified for the field: SET.FIELD: ...* |
| A property set name that does not exist | Refused with `4041`. |

---

## Response

`Search` prepares the result set and stores it in the session. The response confirms the query was accepted and includes metadata about the total result counts.

### Success Response

```xml

<response success="true" ranksorted="false" />

```

| Attribute | Description |
|-----------|-------------|
| `success` | `true` if the query was prepared successfully. |
| `ranksorted` | `true` if results are sorted by full-text relevance rank; `false` otherwise. |

After a successful `Search` call, use `GetNextSearchPage` to retrieve the first page of results.

### Relevance and Where the Term Was Found

`Search` itself returns no items, so it carries no per-document relevance either - only
`ranksorted`, which says whether the pages that follow will come back in relevance order. The
relevance of each document, and which part of it the term was found in, arrive with the items
themselves: every document a full-text `KEYWORDS` search ranked carries a `<RankInfo>` child
element in the `GetNextSearchPage` and `GetPreviousSearchPage` responses.

```xml

<RankInfo Rank="95" FoundIn="1" FoundInVersionNumber="3000000" />

```

A higher `Rank` is a closer match. `FoundIn` says where the term was found, as a number: `1` the
text of the document itself (in the version `FoundInVersionNumber` names), `2` its properties or
comments, `3` an e-mail attachment, `4` a workflow history entry, `0` unknown. A document matched
by database criteria alone - no `KEYWORDS` element in the criteria, or a keyword the content search
engine did not rank - carries no `<RankInfo>` element at all. See
[GetNextSearchPage](GetNextSearchPage.md#rankinfo-element-full-text-search-results) for the full
attribute table and suggested captions.

### Error Response

```xml

<response success="false" error="Error message" errorCode="4000" />

```

---

## Required Permissions

Any authenticated user may call this API. Read-only users may also use it.

Results are always limited to libraries the user can view. Whether each hit is also checked against the item's own permissions depends on the server setting `Search:CheckSecurityOnSearch`, which is **off** by default. With it off, a hit in a library the user belongs to is returned even when the item's permissions would deny reading it; opening the item still fails. With it on, every hit is checked for **Read** (documents) or **List** (folders) permission before it is returned.

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

  <criteria NAME="AIENHANCED"        VALUE="SUMMARY" />

  <!-- One condition per field type: text, number (BETWEEN), date (BETWEEN) and yes/no -->

  <criteria NAME="PROPERTYSETNAME"   VALUE="ProjectMetadata">

    <criteria NAME="Department" OPERATOR="EQ"      VALUE="Finance" />

    <criteria NAME="Budget"     OPERATOR="BETWEEN" VALUE="50000|250000" />

    <criteria NAME="StartDate"  OPERATOR="BETWEEN" VALUE="2024-01-01|2024-06-30" />

    <criteria NAME="Approved"   OPERATOR="EQ"      VALUE="true" />

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

Runs a search and answers **how many things matched** - not the things themselves. The rows come
from [GetNextSearchPage](GetNextSearchPage.md), which reads the result your session is holding, so
the two are always used together.

```javascript
const criteria = `
<criteria>
  <item NAME="FOLDER" OPERATOR="" VALUE="/Finance/Invoices" />
  <item NAME="INCLUDESUBFOLDERS" OPERATOR="" VALUE="true" />
  <item NAME="KEYWORDS" OPERATOR="" VALUE="overdue" />
</criteria>`;

const found = await call('Search', {
  authenticationTicket: ticket,
  xmlcriteria: criteria,
  SortBy: 'DOCUMENTNAME',
  AscendingOrder: true
});
console.log(found.getAttribute('count'), found.getAttribute('ranksorted'));

const page = await call('GetNextSearchPage', {
  authenticationTicket: ticket,
  withrules: false, withPropertySets: false,
  withSecurity: false, withOwner: false, withVersions: false
});
for (const document of page.querySelectorAll('document')) {
  console.log(document.getAttribute('Name'), document.getAttribute('Path'));
}
```

### xmlcriteria

A root element whose children each carry `NAME`, `OPERATOR` and `VALUE` attributes. The element
names themselves are not read. A name the parser does not know is refused `4000` and the message
quotes it. An **empty** `<criteria />` matches nothing rather than everything.

The names include `SEARCHSCOPE`, `SEARCHFOR`, `KEYWORDS`, `DOCUMENTNAME`, `DOCUMENTID`, `FOLDER`,
`FOLDERBYID`, `INCLUDESUBFOLDERS`, `FOLDERDESCRIPTION`, `DOCUMENTFORMAT`, `DOCTYPE`, `FOLDERSONLY`,
`DOCUMENTSONLY`, `OBJECTTYPENAME`, `VIEWCRITERIA`, `CHECKOUTSTATUS`, `USERNAME`, `SIZEIS`,
`IMPORTANCE`, `CLEVEL`, `DATECRITERIA`, `DOCSRC`, `DOCLANG`, `DOCAUTHOR`, `RDDEFID`,
`TEMPLATEPATH`, `PUBLISHSTATUS`, `AIENHANCED`, `SUBSCRIPTIONSOF`, `FAVORITESOF`,
`RECENTDOCUMENTS`, `DOWNLOADQUEOF` and `PROPERTYSETNAME`.

### SortBy

Required - it is a non-nullable string, so it cannot be left out even though the search has a
default sort of its own. A column it does not know is refused `4000` and the message lists them all:
`DOCUMENTNAME`, `DOCUMENTSIZE`, `MIMETYPEDESCRIPTION`, `MODIFICATIONDATE`, `STATUSCODE`,
`FOLDERNAME`, `LASTVERSIONNUMBER`, `PERCENTCOMPLETE`, `CREATIONDATE`, `MODIFIEDBYNAME`,
`DESCRIPTION`, `OWNERNAME`, `FLOWNAME`, `VIEW`, `CHECKEDOUTBYNAME`, `COMPLETIONDATE`, `IMPORTANCE`,
`RDDEFID`, `CLEVEL`, `DECLASSIFYON`, `DOWNGRADEON`, `DISPOSITIONDATE`, `LASTISOREVIEW`,
`NEXTISOREVIEW`, and `PROPERTYSETNAME.FIELDNAME` for a custom field.

A criteria document that is not well formed is refused with `4000`, the same as a criterion name
the parser does not recognise.

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

- Property set field names are case-insensitive. A property set name that does not exist is refused with `4041`.

- The `TEMPLATEPATH` criterion accepts either a full infoRouter document path (e.g. `/Finance/Templates/mytemplate.htm`) or the short-form `~D<id>` notation (e.g. `~D42`). Use `~D999` as the reserved identifier for all HTML form documents — it matches any document whose template is the built-in HTML document type regardless of which specific template file was used.

---

## Related APIs

- [GetNextSearchPage](GetNextSearchPage.md) - Retrieves the next page of the prepared search results

- [GetPreviousSearchPage](GetPreviousSearchPage.md) - Retrieves the previous page of the prepared search results

- [GetFoldersAndDocuments](GetFoldersAndDocuments.md) - Lists documents and folders in a specific path without a search query

- [GetDocuments](GetDocuments.md) - Returns documents in a specific folder path

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4000` | a criterion name the parser does not know, or a `SortBy` that is not one of the columns |
| `4000` | the document was not well-formed XML; the message carries the parser's own words |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
