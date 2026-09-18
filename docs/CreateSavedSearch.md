# CreateSavedSearch API

Creates a saved search or a search page. A **saved search** stores criteria a user can run again. A **search page** defines a search form: which fields it offers and what they start with. Both are new in infoRouter 9.

## Endpoint

```
/srv.asmx/CreateSavedSearch
```

## Methods

- **GET** `/srv.asmx/CreateSavedSearch?authenticationTicket=...&searchPageType=...&name=...&...`
- **POST** `/srv.asmx/CreateSavedSearch` (form data)
- **SOAP** Action: `http://tempuri.org/CreateSavedSearch`

Prefer POST: `searchParametersXml` is usually too long for a query string.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `searchPageType` | string | Yes | `savedSearch` or `searchPage`, in any case. Anything else is refused |
| `name` | string | Yes | Display name, 5 to 64 characters. Unique among entries of the same type (see [Names](#names)) |
| `description` | string | No | Description. Empty or omitted = none |
| `isPersonal` | bool | Yes | `true`: private to the caller. `false`: system-wide, requires the Search Administrator role |
| `anonymousAccess` | bool | No | System-wide entries: the anonymous user may use it. Ignored for personal entries. Default `false` |
| `publicAccess` | bool | No | System-wide entries: every signed-in user may use it. Ignored for personal entries. Default `false` |
| `userGroupNames` | string | No | System-wide entries: groups whose members may use it, separated by `\|`. A library's local group is written `library\group`. Ignored for personal entries |
| `searchParametersXml` | string | No | The fields and their values. See [SavedSearchXmlReference](SavedSearchXmlReference.md). Empty = every field shown, no values |

## searchParametersXml

A `<SEARCH>` element with one `<ITEM>` per field. The full field list, accepted values and the rules are in [SavedSearchXmlReference](SavedSearchXmlReference.md). What matters most:

- A field the XML leaves out is **shown**. To hide a field, list it with `VISIBLE="FALSE"`.
- Ids, not names: `FOLDER` takes a folder id, `USERNAME` and `CHECKOUTSTATUS USERNAME` take user ids.
- A value outside a field's list fails the request and nothing is saved.

### Sample: Saved Search

Documents mentioning a contract renewal, named `*.pdf` or `*contract*`, PDF, modified in the last 30 days, of high importance or above, at least 1 MB, published, not checked out, in English. The fields the search does not use are hidden.

```xml
<SEARCH>
  <ITEM NAME="SEARCHSCOPE" VALUE="0" VISIBLE="TRUE" />
  <ITEM NAME="SEARCHFOR" VALUE="DOCUMENTSONLY" VISIBLE="TRUE" />
  <ITEM NAME="KEYWORDS" VALUE="contract renewal" VISIBLE="TRUE" />
  <ITEM NAME="DOCUMENTNAME" VALUE="*.pdf|*contract*" VISIBLE="TRUE" />
  <ITEM NAME="DOCUMENTFORMAT" VALUE="application/pdf" VISIBLE="TRUE" />
  <ITEM NAME="DATECRITERIA" VALUE="MODIFIED" DATETYPE="PREVIOUS" PREVIOUSDATETYPE="D" PREVIOUSN="30" DATE1="" DATE2="" VISIBLE="TRUE" />
  <ITEM NAME="IMPORTANCE" OPERATOR="GT-EQ" VALUE="HIGH" VISIBLE="TRUE" />
  <ITEM NAME="SIZEIS" VALUE="AT LEAST" SIZEAMOUNT="1024" VISIBLE="TRUE" />
  <ITEM NAME="PUBLISHSTATUS" VALUE="2" VISIBLE="TRUE" />
  <ITEM NAME="CHECKOUTSTATUS" VALUE="0" USERNAME="0" VISIBLE="TRUE" />
  <ITEM NAME="DOCLANG" VALUE="en" VISIBLE="TRUE" />
  <ITEM NAME="AIENHANCED" VALUE="" VISIBLE="FALSE" />
  <ITEM NAME="DOCTYPE" VALUE="" VISIBLE="FALSE" />
  <ITEM NAME="FOLDERDESC" VALUE="" VISIBLE="FALSE" />
  <ITEM NAME="DOCUMENTID" VALUE="" VISIBLE="FALSE" />
  <ITEM NAME="FOLDERBYID" VALUE="" VISIBLE="FALSE" />
  <ITEM NAME="USERNAME" VALUE="" VISIBLE="FALSE" />
  <ITEM NAME="FOLDER" VALUE="0" INCLUDESUBFOLDERS="TRUE" VISIBLE="FALSE" />
  <ITEM NAME="CLEVEL" VALUE="" VISIBLE="FALSE" />
  <ITEM NAME="VIEWCRITERIA" VALUE="" USERNAME="0" VISIBLE="FALSE" />
  <ITEM NAME="DOCSRC" VALUE="" VISIBLE="FALSE" />
  <ITEM NAME="DOCAUTHOR" VALUE="" VISIBLE="FALSE" />
  <ITEM NAME="TAGTEXT" VALUE="" VISIBLE="FALSE" />
  <ITEM NAME="RDDEFID" VALUE="0" VISIBLE="FALSE" />
  <ITEM NAME="PROPERTYSETNAME" VALUE="" ATTRIBUTES="" CONDITIONS="" VALUES="" VISIBLE="FALSE" />
</SEARCH>
```

### Sample: Search Page

A simple form offering keywords, name, a date and property set fields. The scope is fixed to online libraries and hidden; every other field is hidden.

```xml
<SEARCH>
  <ITEM NAME="SEARCHSCOPE" VALUE="0" VISIBLE="FALSE" />
  <ITEM NAME="KEYWORDS" VALUE="" VISIBLE="TRUE" />
  <ITEM NAME="DOCUMENTNAME" VALUE="" VISIBLE="TRUE" />
  <ITEM NAME="DATECRITERIA" VALUE="" DATETYPE="" PREVIOUSDATETYPE="" PREVIOUSN="0" DATE1="" DATE2="" VISIBLE="TRUE" />
  <ITEM NAME="PROPERTYSETNAME" VALUE="" ATTRIBUTES="" CONDITIONS="" VALUES="" VISIBLE="TRUE" />
  <ITEM NAME="SEARCHFOR" VALUE="" VISIBLE="FALSE" />
  <ITEM NAME="DOCTYPE" VALUE="" VISIBLE="FALSE" />
  <ITEM NAME="FOLDERDESC" VALUE="" VISIBLE="FALSE" />
  <ITEM NAME="DOCUMENTID" VALUE="" VISIBLE="FALSE" />
  <ITEM NAME="FOLDERBYID" VALUE="" VISIBLE="FALSE" />
  <ITEM NAME="USERNAME" VALUE="" VISIBLE="FALSE" />
  <ITEM NAME="FOLDER" VALUE="0" INCLUDESUBFOLDERS="TRUE" VISIBLE="FALSE" />
  <ITEM NAME="CHECKOUTSTATUS" VALUE="" USERNAME="0" VISIBLE="FALSE" />
  <ITEM NAME="SIZEIS" VALUE="" SIZEAMOUNT="0" VISIBLE="FALSE" />
  <ITEM NAME="IMPORTANCE" OPERATOR="" VALUE="-1" VISIBLE="FALSE" />
  <ITEM NAME="CLEVEL" VALUE="" VISIBLE="FALSE" />
  <ITEM NAME="DOCUMENTFORMAT" VALUE="" VISIBLE="FALSE" />
  <ITEM NAME="VIEWCRITERIA" VALUE="" USERNAME="0" VISIBLE="FALSE" />
  <ITEM NAME="DOCSRC" VALUE="" VISIBLE="FALSE" />
  <ITEM NAME="DOCLANG" VALUE="" VISIBLE="FALSE" />
  <ITEM NAME="DOCAUTHOR" VALUE="" VISIBLE="FALSE" />
  <ITEM NAME="TAGTEXT" VALUE="" VISIBLE="FALSE" />
  <ITEM NAME="RDDEFID" VALUE="0" VISIBLE="FALSE" />
  <ITEM NAME="PUBLISHSTATUS" VALUE="0" VISIBLE="FALSE" />
  <ITEM NAME="AIENHANCED" VALUE="" VISIBLE="FALSE" />
</SEARCH>
```

### Sample: Only the Fields a Search Uses

Shorter XML is accepted too. Remember that the fields not listed are then shown.

```xml
<SEARCH>
  <ITEM NAME="FOLDER" VALUE="1234" INCLUDESUBFOLDERS="TRUE" VISIBLE="TRUE" />
  <ITEM NAME="CHECKOUTSTATUS" VALUE="USER" USERNAME="1005" VISIBLE="TRUE" />
  <ITEM NAME="DATECRITERIA" VALUE="CREATED" DATETYPE="BETWEEN" DATE1="2026-01-01" DATE2="2026-03-31" VISIBLE="TRUE" />
  <ITEM NAME="PROPERTYSETNAME" VALUE="INVOICE" ATTRIBUTES="CUSTOMER|INVOICEAMOUNT" CONDITIONS="CONTAINS|EQGT" VALUES="Acme|1000" VISIBLE="TRUE" />
</SEARCH>
```

## Response

### Success

```xml
<response success="true" error="" id="2138" />
```

`id` is the new entry's id. Use it with `GetSavedSearch`, `UpdateSavedSearch` and `DeleteSavedSearch`.

### Error

```xml
<response success="false" error="A search page with this name already exists. Please choose a different name" errorcode="4090" />
```

## Required Permissions

- Signed-in user. The anonymous user cannot create entries.
- **Personal entries** (`isPersonal=true`): any signed-in user.
- **System-wide entries** (`isPersonal=false`): members of the `[Search & Category Administrators]` role group. Being the system administrator is not enough on its own.

## Names

- 5 to 64 characters, counted as the caller typed them.
- At least one letter or digit. No `<` or `>`, no leading or trailing space, no tab or line break, no `../`, `..\`, `/..` or `\..`.
- Unique among entries of the same type: a saved search and a search page may share a name.
- A personal entry is stored with the owner's user id in front of its name (`4My Q4 Contracts`), so two users can each have "My Q4 Contracts". The APIs always return the name without it. Because the id counts towards the 64 characters of the column, a personal name can be up to 64 minus the length of the user id.

## Examples

### POST: Personal Saved Search

```
POST /srv.asmx/CreateSavedSearch HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&searchPageType=savedSearch&name=My+Q4+Contracts
&description=Contract+documents+changed+recently&isPersonal=true&anonymousAccess=false
&publicAccess=false&userGroupNames=
&searchParametersXml=%3CSEARCH%3E%3CITEM+NAME%3D%22KEYWORDS%22+VALUE%3D%22contract+renewal%22+VISIBLE%3D%22TRUE%22+%2F%3E%3C%2FSEARCH%3E
```

### POST: System-Wide Search Page for Two Groups

```
POST /srv.asmx/CreateSavedSearch HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&searchPageType=searchPage&name=Contract+Search
&description=Keyword%2C+name+and+date+only&isPersonal=false&anonymousAccess=false
&publicAccess=false&userGroupNames=Legal%7CFinance%5CControllers
&searchParametersXml=...
```

### SOAP 1.1

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/CreateSavedSearch"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <CreateSavedSearch xmlns="http://tempuri.org/">
      <authenticationTicket>abc123</authenticationTicket>
      <searchPageType>savedSearch</searchPageType>
      <name>My Q4 Contracts</name>
      <description></description>
      <isPersonal>true</isPersonal>
      <anonymousAccess>false</anonymousAccess>
      <publicAccess>false</publicAccess>
      <userGroupNames></userGroupNames>
      <searchParametersXml>&lt;SEARCH&gt;&lt;ITEM NAME="KEYWORDS" VALUE="contract renewal" VISIBLE="TRUE" /&gt;&lt;/SEARCH&gt;</searchParametersXml>
    </CreateSavedSearch>
  </soap:Body>
</soap:Envelope>
```

The XML travels as text, so it is escaped inside the envelope.

### JavaScript: Save What the User Searched For

Plain `fetch`. `URLSearchParams` does the form encoding, including the XML.

```js
async function saveCurrentSearch(ticket, name, criteria) {
  const xml = `<SEARCH>
  <ITEM NAME="KEYWORDS" VALUE="${escapeXml(criteria.keywords)}" VISIBLE="TRUE" />
  <ITEM NAME="DATECRITERIA" VALUE="MODIFIED" DATETYPE="PREVIOUS" PREVIOUSDATETYPE="D" PREVIOUSN="${criteria.days}" VISIBLE="TRUE" />
</SEARCH>`;

  const response = await fetch('/srv.asmx/CreateSavedSearch', {
    method: 'POST',
    body: new URLSearchParams({
      authenticationTicket: ticket,
      searchPageType: 'savedSearch',
      name,
      description: '',
      isPersonal: 'true',
      anonymousAccess: 'false',
      publicAccess: 'false',
      userGroupNames: '',
      searchParametersXml: xml,
    }),
  });

  const root = new DOMParser().parseFromString(await response.text(), 'text/xml').documentElement;
  if (root.getAttribute('success') !== 'true') throw new Error(root.getAttribute('error'));
  return Number(root.getAttribute('id'));
}

function escapeXml(text) {
  return String(text ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
```

### JavaScript: With the Helper

`createInfoRouterClient` and `buildSearchXml` are in [SavedSearchXmlReference](SavedSearchXmlReference.md#javascript-helper). The helper writes every field, so fields you do not pass are hidden.

```js
const ir = createInfoRouterClient('', ticket);

// A personal saved search.
const savedSearchId = await ir.createSavedSearch({
  type: 'savedSearch',
  name: 'My Q4 Contracts',
  description: 'Contract documents changed in the last 30 days',
  isPersonal: true,
  items: {
    SEARCHFOR: { VALUE: 'DOCUMENTSONLY' },
    KEYWORDS: { VALUE: 'contract renewal' },
    DOCUMENTNAME: { VALUE: '*.pdf|*contract*' },
    DATECRITERIA: { VALUE: 'MODIFIED', DATETYPE: 'PREVIOUS', PREVIOUSDATETYPE: 'D', PREVIOUSN: '30' },
    IMPORTANCE: { VALUE: 'HIGH', OPERATOR: 'GT-EQ' },
    PUBLISHSTATUS: { VALUE: '2' },
  },
});

// A search page shared with two groups, offering four fields.
const searchPageId = await ir.createSavedSearch({
  type: 'searchPage',
  name: 'Contract Search',
  description: 'Keyword, name and date only',
  isPersonal: false,
  userGroupNames: ['Legal', 'Finance\\Controllers'],
  items: {
    SEARCHSCOPE: { VALUE: '0', VISIBLE: false },
    KEYWORDS: {},
    DOCUMENTNAME: {},
    DATECRITERIA: {},
    PROPERTYSETNAME: {},
  },
});
```


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

Keeps a set of criteria for later, as a saved search or as a search page.

```javascript
const created = await call('CreateSavedSearch', {
  authenticationTicket: ticket,
  searchPageType: 'savedSearch',      // or 'searchPage'
  name: 'Overdue invoices',
  description: 'Anything still open',
  isPersonal: true,                   // false makes it a system page
  anonymousAccess: false,
  publicAccess: false,
  userGroupNames: '',                 // comma separated; "Library\\Group" for a library's own
  searchParametersXml: criteria       // the same document Search takes
});

const searchPageId = created.getAttribute('id');
```

`searchPageType` is declared optional and is not: it is checked against the two literals
`savedSearch` and `searchPage`, so an empty one is refused `4000` with both names in the message.
`isPersonal` decides the owner - `true` gives it to the caller, `false` makes it a system page,
which needs the search administrator role.

## Notes

- `anonymousAccess`, `publicAccess` and `userGroupNames` are ignored for personal entries; `GetSavedSearch` returns them as `false` and empty.
- A system-wide entry with none of `anonymousAccess`, `publicAccess` and `userGroupNames` is available to search administrators only.
- A property set named in `PROPERTYSETNAME` that does not exist is dropped without an error; the rest is saved.
- To copy an entry, read it with `GetSavedSearch` and send its `<SEARCH>` element here as a string with a new name.
- REST: send every parameter, even empty ones. Empty values are accepted; older servers answered an empty `description`, `userGroupNames` or `searchParametersXml` with HTTP 400.
- There is no API that runs a saved search by id. See [Running a Saved Search](SavedSearchXmlReference.md#running-a-saved-search).

## Related APIs

- [UpdateSavedSearch](UpdateSavedSearch.md) — Change an existing entry
- [GetSavedSearch](GetSavedSearch.md) — Read one entry with its fields
- [GetSavedSearches](GetSavedSearches.md) — List the entries the user may use
- [DeleteSavedSearch](DeleteSavedSearch.md) — Delete an entry
- [SavedSearchXmlReference](SavedSearchXmlReference.md) — Field reference, JavaScript helper, running a saved search

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4000` | `searchPageType` is not `savedSearch` or `searchPage`, or `name` is empty |
| `4041` | one of `userGroupNames` is not a group |
| `4090` | a page of that name and type already exists |
| `4030` | `isPersonal` was false and the caller is not a search administrator |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
