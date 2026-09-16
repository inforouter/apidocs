# Saved Search and Search Page XML Reference

How the `searchParametersXml` of [CreateSavedSearch](CreateSavedSearch.md) and [UpdateSavedSearch](UpdateSavedSearch.md) is written, what [GetSavedSearch](GetSavedSearch.md) returns in its `<SEARCH>` element, a JavaScript helper that does both, and how to run a saved search through [Search](Search.md).

Everything on this page is checked by the `CreateSavedSearchApiTests`, `UpdateSavedSearchApiTests` and `GetSavedSearchApiTests` integration tests; the sample XML in them is the XML shown here.

## Saved Search or Search Page

Both are stored in the same format. What differs is what the UI does with it.

| | `savedSearch` | `searchPage` |
|---|---|---|
| Purpose | A query the user can run again | A search form: which fields it offers |
| `VALUE` | The criterion to search for | The value the field starts with (usually empty) |
| `VISIBLE` | Whether the field is shown when the user opens the search to change it | Whether the form offers the field |
| Typical owner | The user (`isPersonal=true`) | The system (`isPersonal=false`, Search Administrator) |

## Document Shape

```xml
<SEARCH>
  <ITEM NAME="KEYWORDS" VALUE="contract renewal" VISIBLE="TRUE" />
  <ITEM NAME="DATECRITERIA" VALUE="MODIFIED" DATETYPE="PREVIOUS" PREVIOUSDATETYPE="D" PREVIOUSN="30" DATE1="" DATE2="" VISIBLE="TRUE" />
</SEARCH>
```

- One `<ITEM>` per field, identified by `NAME`. Other attributes carry the field's value.
- `NAME` and `VISIBLE` are case-insensitive (`VISIBLE="true"` works). The root element's name is not checked; `<SEARCH>` is what the server writes.
- **A field the XML leaves out is shown, with no value.** A search page that hides fields must list them with `VISIBLE="FALSE"`. The JavaScript helper below always writes every field.
- An `ITEM` with a `NAME` not in the table below is ignored. Comments are allowed.
- An empty `searchParametersXml` gives every field shown with no value.
- The XML replaces the whole definition. An update with an empty `searchParametersXml` resets it; it does not keep the stored one.
- An invalid value fails the whole request and nothing is stored (see [Errors](#errors)).

## Field Reference

| NAME | Attributes | Accepted values |
|------|------------|-----------------|
| `SEARCHSCOPE` | `VALUE` | Libraries to search: `0` online, `1` all, `2` archived, `3` online and hidden. Empty or unknown → `1`. Leaving the item out → `0` |
| `SEARCHFOR` | `VALUE` | Empty (documents and folders), `DOCUMENTSONLY`, `FOLDERSONLY` |
| `DOCTYPE` | `VALUE` | A document type name, or `GENERIC` for documents without a type. Not checked against the defined types |
| `KEYWORDS` | `VALUE` | Full-text search words |
| `DOCUMENTNAME` | `VALUE` | Document or folder names, `*` as wildcard, several separated by `\|`: `*.pdf\|*contract*` |
| `FOLDERDESC` | `VALUE` | Text in a folder's description (folders only) |
| `DOCUMENTID` | `VALUE` | Comma-separated document ids: `101,102` |
| `FOLDERBYID` | `VALUE` | Comma-separated folder ids |
| `USERNAME` | `VALUE` | Comma-separated **user ids** of the document or folder owner: `4,1005` |
| `FOLDER` | `VALUE`, `INCLUDESUBFOLDERS` | Folder **id** to search in (`0` = anywhere); `INCLUDESUBFOLDERS` `TRUE`/`FALSE` |
| `CHECKOUTSTATUS` | `VALUE`, `USERNAME` | Empty, `ALL` (checked out by anyone), `0` (not checked out), `ME`, `USER` (checked out by the user whose **id** is in `USERNAME`) |
| `DATECRITERIA` | `VALUE`, `DATETYPE`, `PREVIOUSDATETYPE`, `PREVIOUSN`, `DATE1`, `DATE2` | See [Date criteria](#date-criteria) |
| `SIZEIS` | `VALUE`, `SIZEAMOUNT` | `VALUE` empty, `AT LEAST` or `AT MOST`; `SIZEAMOUNT` in **kilobytes** (`1024` = 1 MB) |
| `IMPORTANCE` | `VALUE`, `OPERATOR` | `VALUE` `LOW`/`0`, `NORMAL`/`1`, `HIGH`/`2`, `VITAL`/`3` (`-1` or empty = none). `OPERATOR` `EQ`, `GT-EQ`, `GT`, `LT`, `LT-EQ`; an empty operator stores no importance criterion |
| `CLEVEL` | `VALUE` | Classification level: empty, `0` no markings, `1` declassified, `2` confidential, `3` secret, `4` top secret |
| `DOCUMENTFORMAT` | `VALUE` | Comma-separated MIME types: `application/pdf,text/plain` |
| `VIEWCRITERIA` | `VALUE`, `USERNAME` | Empty, `NOVIEW` (never viewed), `UPDATED` (has a newer version than the last one viewed), `SAW` (viewed); `USERNAME` is the **id** of the user whose views count (`0` = the user running the search) |
| `DOCSRC` | `VALUE` | Document source text |
| `DOCLANG` | `VALUE` | Language code: `en`, `de`, `es`, `fr`, `da`, `el`, `et`, `he`, `hi`, `hu`, `id`, `it`, `ja`, `ko`, `nl`, `no`, `pl`, `pt`, `ro`, `ru`, `sv`, `tk`, `tr`, `uk`, `ur`, `uz`, `vi`, `zh` |
| `DOCAUTHOR` | `VALUE` | Document author text |
| `TAGTEXT` | `VALUE` | Tag text |
| `RDDEFID` | `VALUE` | Retention and disposition schedule id (`0` = none) |
| `PUBLISHSTATUS` | `VALUE` | `0` any, `1` unpublished, `2` published |
| `AIENHANCED` | `VALUE` | What infoRouter Connect produced: empty, `ANY`, `ALL`, `NONE`, or attribute names `Summary`, `Description`, `Keywords`, `OcrText`, `DocumentType`, `Abstract`, `ExtractedData`, `Markdown`, `RedactedText` comma-separated (documents carrying all of them) |
| `PROPERTYSETNAME` | `VALUE`, `ATTRIBUTES`, `CONDITIONS`, `VALUES` | See [Property set criteria](#property-set-criteria) |

### Date Criteria

`VALUE` names the date and `DATETYPE` how it is compared.

| Attribute | Values |
|-----------|--------|
| `VALUE` | Empty (no date criterion), `REGISTERDATE`, `CREATED`, `MODIFIED`, `CREATED OR MODIFIED`, `COMPLETED ON`, `DECLASSIFY ON`, `DOWNGRADE ON`, `DOWNGRADE DATE`, `RETAIN UNTIL`, `LAST ISO REVIEW DATE`, `NEXT ISO REVIEW DATE`, `DISPOSITION DATE`, `EXPIRATION DATE`, `CUTOFF DATE` |
| `DATETYPE` | `BETWEEN` (`DATE1` to `DATE2`, at least one required), `TODAY`, `PREVIOUS` (the last `PREVIOUSN` periods up to today), `NEXT` (the next `PREVIOUSN` periods from tomorrow) |
| `PREVIOUSDATETYPE` | Period for `PREVIOUS` and `NEXT`: `D` days, `W` weeks, `M` months, `Y` years |
| `PREVIOUSN` | Number of periods |
| `DATE1`, `DATE2` | Dates for `BETWEEN`. Send `yyyy-MM-dd`; other formats are read in the server's culture |

```xml
<ITEM NAME="DATECRITERIA" VALUE="CREATED" DATETYPE="BETWEEN" DATE1="2026-01-01" DATE2="2026-03-31" VISIBLE="TRUE" />
<ITEM NAME="DATECRITERIA" VALUE="EXPIRATION DATE" DATETYPE="NEXT" PREVIOUSDATETYPE="W" PREVIOUSN="2" VISIBLE="TRUE" />
```

`PREVIOUS` and `NEXT` are relative: the saved search keeps meaning "the last 30 days" whenever it is run.

### Property Set Criteria

`ATTRIBUTES`, `CONDITIONS` and `VALUES` are parallel lists separated by `|`: the n-th condition and value belong to the n-th field. Give all three the same number of entries.

```xml
<ITEM NAME="PROPERTYSETNAME" VALUE="INVOICE"
      ATTRIBUTES="CUSTOMER|INVOICEAMOUNT|INVOICEDATE"
      CONDITIONS="CONTAINS|EQGT|BETWEEN"
      VALUES="Acme|1000|2026-01-01;2026-03-31"
      VISIBLE="TRUE" />
```

A condition may be written as its name or its number. The numbers differ by field type, and **the server writes numbers back**:

| Field type | Conditions (number = name) | Value |
|------------|----------------------------|-------|
| `CHAR` | `0` NONE, `1` CONTAINS, `2` EQ, `3` NULL, `4` NOTNULL, `5` NOTCONTAINS, `6` NEQ | Text, up to 255 characters |
| `NUMBER` | `0` NONE, `1` EQ, `2` NEQ, `3` EQLT, `4` EQGT, `5` GT, `6` LT, `7` NOTNULL, `8` NULL, `9` BETWEEN | Number; `BETWEEN` takes `low;high` |
| `DATE` | `0` NONE, `1` ANYTIME, `2` YESTERDAY, `3` TODAY, `4` LAST7DAYS, `5` NEXT7DAYS, `6` LASTWEEK, `7` THISWEEK, `8` NEXTWEEK, `9` LASTMONTH, `10` THISMONTH, `11` NEXTMONTH, `12` EQ, `13` EQGT, `14` EQLT, `15` NULL, `16` BETWEEN | Date for `EQ`, `EQGT`, `EQLT`; `from;to` for `BETWEEN`; empty for the others |
| `BOOLEAN` | `0` NONE, `1` EQ, `2` NOTNULL, `3` NULL | `1`, `true`, `yes`, `on` or `0`, `false`, `no`, `off` |

- A value with no condition (`NONE`) is an error, and so is a value on `NULL`, `NOTNULL` or a relative date condition.
- A property set that does not exist is dropped without an error: the entry is saved without the property set criterion. Check the name first with `GetPropertySetDefinition`.
- The stored criterion lists **every field of the property set**, in the set's own order, with condition `0` for the fields the request did not name. Match fields by name, not position.

## What Comes Back

`GetSavedSearch` returns all 25 fields, in a fixed order, normalized:

| Sent | Returned |
|------|----------|
| A field left out | `VALUE` empty (or `0`/`-1`), `VISIBLE="TRUE"` |
| `IMPORTANCE VALUE="HIGH"` | `VALUE="2"` |
| `DOCUMENTFORMAT VALUE="application/pdf"` | `VALUE="APPLICATION/PDF"` |
| `SEARCHFOR VALUE="documentsonly"` | `VALUE="DOCUMENTSONLY"` |
| `DATE1="2026-01-01"` | A UTC timestamp, `DATE1="2025-12-31T21:00:00.000Z"` on a UTC+3 server. `new Date(value)` gives the date back in local time |
| `CHECKOUTSTATUS`, `VIEWCRITERIA` without `USERNAME` | `USERNAME="0"` |
| `PROPERTYSETNAME` conditions by name | Condition numbers, one per field of the set |
| `PROPERTYSETNAME` | An extra `FIELDS` attribute, equal to `VISIBLE`. Ignored on the way in |

Sending the returned `<SEARCH>` element back unchanged stores the same definition.

## Errors

| Cause | Error text (English) | `errorcode` |
|-------|----------------------|-------------|
| Malformed XML | `System.Xml.XmlException:...` | `5000` |
| A value outside a fixed list (`SEARCHFOR`, `DATECRITERIA`, `SIZEIS`, `IMPORTANCE`, `CLEVEL`, `VIEWCRITERIA`, `DOCLANG`) | `Unmatched field value` | `4000` |
| `CHECKOUTSTATUS` value | `Invalid checkout status: possible values are 'ALL','ME','USER','0',''` | `4000` |
| Non-numeric id in `DOCUMENTID`, `FOLDERBYID`, `USERNAME` | `Invalid integer list` | `4000` |
| `BETWEEN` without dates | `Empty date1 and date2` | `4000` |
| Unknown `AIENHANCED` word | `Unmatched field value` | `4000` |
| Property set condition or value | `Invalid condition specified for the field: INVOICE.INVOICEAMOUNT:` followed by the reason | `4000` |

The field value errors above are English whatever the user's language; the other errors on the API pages follow the calling user's language. `Unmatched field value` does not say which field; check the values against the table above.

## JavaScript Helper

A dependency-free helper for the browser (`fetch`, `DOMParser`, `URLSearchParams`). It builds and reads the XML, wraps the five saved search APIs, and runs a saved search. Every function here is exercised end to end against a server.

```js
/*
 * infoRouter saved searches and search pages - browser helper, no dependencies.
 *
 * Works in any modern browser (fetch, DOMParser, URLSearchParams). Copy it as it is,
 * or take the functions you need.
 *
 *   const ir = createInfoRouterClient('https://yourserver', ticket);
 *   const id = await ir.createSavedSearch({ type: 'savedSearch', name: 'My Q4 Contracts', isPersonal: true, items });
 */

/** Every field a definition carries, with the value an unused field has. */
const SEARCH_ITEM_DEFAULTS = {
  SEARCHSCOPE:     { VALUE: '0' },
  SEARCHFOR:       { VALUE: '' },
  DOCTYPE:         { VALUE: '' },
  KEYWORDS:        { VALUE: '' },
  DOCUMENTNAME:    { VALUE: '' },
  FOLDERDESC:      { VALUE: '' },
  DOCUMENTID:      { VALUE: '' },
  FOLDERBYID:      { VALUE: '' },
  USERNAME:        { VALUE: '' },
  FOLDER:          { VALUE: '0', INCLUDESUBFOLDERS: 'TRUE' },
  CHECKOUTSTATUS:  { VALUE: '', USERNAME: '0' },
  DATECRITERIA:    { VALUE: '', DATETYPE: '', PREVIOUSDATETYPE: '', PREVIOUSN: '0', DATE1: '', DATE2: '' },
  SIZEIS:          { VALUE: '', SIZEAMOUNT: '0' },
  IMPORTANCE:      { VALUE: '-1', OPERATOR: '' },
  CLEVEL:          { VALUE: '' },
  DOCUMENTFORMAT:  { VALUE: '' },
  VIEWCRITERIA:    { VALUE: '', USERNAME: '0' },
  DOCSRC:          { VALUE: '' },
  DOCLANG:         { VALUE: '' },
  DOCAUTHOR:       { VALUE: '' },
  TAGTEXT:         { VALUE: '' },
  RDDEFID:         { VALUE: '0' },
  PUBLISHSTATUS:   { VALUE: '0' },
  AIENHANCED:      { VALUE: '' },
  PROPERTYSETNAME: { VALUE: '', ATTRIBUTES: '', CONDITIONS: '', VALUES: '' },
};

function escapeXml(text) {
  return String(text ?? '')
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&apos;');
}

/**
 * Builds the searchParametersXml string.
 *
 * items: { KEYWORDS: { VALUE: 'budget', VISIBLE: true }, FOLDER: { VALUE: '1234', INCLUDESUBFOLDERS: 'FALSE' }, ... }
 *
 * Every field is written, because a field the XML leaves out is shown. A field you do not
 * pass gets its unused value and `defaultVisible` (default false), so for a search page
 * you only list the fields the page offers.
 */
function buildSearchXml(items = {}, { defaultVisible = false } = {}) {
  const lines = Object.keys(SEARCH_ITEM_DEFAULTS).map((name) => {
    const given = items[name] ?? {};
    const attributes = { NAME: name, ...SEARCH_ITEM_DEFAULTS[name] };
    for (const [key, value] of Object.entries(given)) {
      if (key !== 'VISIBLE') attributes[key] = value;
    }
    const visible = given.VISIBLE ?? (items[name] ? true : defaultVisible);
    attributes.VISIBLE = visible ? 'TRUE' : 'FALSE';
    const text = Object.entries(attributes).map(([k, v]) => `${k}="${escapeXml(v)}"`).join(' ');
    return `  <ITEM ${text} />`;
  });
  return `<SEARCH>\n${lines.join('\n')}\n</SEARCH>`;
}

/** Reads a <SEARCH> element (from GetSavedSearch) into the same shape buildSearchXml takes. */
function parseSearchElement(searchElement) {
  const items = {};
  if (!searchElement) return items;
  for (const item of Array.from(searchElement.getElementsByTagName('ITEM'))) {
    const entry = {};
    for (const attribute of Array.from(item.attributes)) {
      if (attribute.name === 'NAME') continue;
      entry[attribute.name] = attribute.name === 'VISIBLE' ? attribute.value.toUpperCase() === 'TRUE' : attribute.value;
    }
    items[item.getAttribute('NAME')] = entry;
  }
  return items;
}

class InfoRouterError extends Error {}

function createInfoRouterClient(baseUrl, ticket) {
  /** POSTs a form to /srv.asmx/{action} and returns the root element; throws when success is not "true". */
  async function call(action, params = {}) {
    const body = new URLSearchParams({ authenticationTicket: ticket });
    for (const [key, value] of Object.entries(params)) body.append(key, value === undefined || value === null ? '' : String(value));

    const response = await fetch(`${baseUrl}/srv.asmx/${action}`, { method: 'POST', body });
    const text = await response.text();
    if (!response.ok) throw new InfoRouterError(`${action}: HTTP ${response.status} ${text.slice(0, 200)}`);

    const root = new DOMParser().parseFromString(text, 'text/xml').documentElement;
    if (root.getAttribute('success') !== 'true') throw new InfoRouterError(`${action}: ${root.getAttribute('error')}`);
    return root;
  }

  function entryForm(entry) {
    return {
      searchPageType: entry.type,                        // 'savedSearch' or 'searchPage'
      name: entry.name,
      description: entry.description ?? '',
      isPersonal: entry.isPersonal ? 'true' : 'false',
      anonymousAccess: entry.anonymousAccess ? 'true' : 'false',
      publicAccess: entry.publicAccess ? 'true' : 'false',
      userGroupNames: (entry.userGroupNames ?? []).join('|'),   // ['Legal', 'Finance\\Controllers']
      searchParametersXml: entry.searchParametersXml ?? buildSearchXml(entry.items ?? {}, { defaultVisible: entry.defaultVisible }),
    };
  }

  return {
    call,

    /** Creates an entry and returns its id. */
    async createSavedSearch(entry) {
      const root = await call('CreateSavedSearch', entryForm(entry));
      return Number(root.getAttribute('id'));
    },

    /** Replaces an entry. Send every property: a missing definition resets the fields, missing groups remove them. */
    async updateSavedSearch(id, entry) {
      await call('UpdateSavedSearch', { searchPageId: id, ...entryForm(entry) });
    },

    /** Reads an entry into the shape createSavedSearch and updateSavedSearch take. */
    async getSavedSearch(id) {
      const page = (await call('GetSavedSearch', { searchPageId: id })).getElementsByTagName('SearchPage')[0];
      const groups = page.getAttribute('userGroupNames');
      return {
        id: Number(page.getAttribute('id')),
        type: page.getAttribute('type'),
        name: page.getAttribute('name'),
        description: page.getAttribute('description'),
        ownerId: Number(page.getAttribute('ownerId')),
        isPersonal: page.getAttribute('ownerId') !== '0',
        anonymousAccess: page.getAttribute('anonymousAccess') === 'true',
        publicAccess: page.getAttribute('publicAccess') === 'true',
        userGroupNames: groups ? groups.split('|') : [],
        items: parseSearchElement(page.getElementsByTagName('SEARCH')[0]),
      };
    },

    /** Lists what the user may use: type 'savedSearch', 'searchPage' or 'all'. */
    async listSavedSearches(type = 'all') {
      const root = await call('GetSavedSearches', { searchPageType: type });
      return Array.from(root.getElementsByTagName('SearchPage')).map((page) => ({
        id: Number(page.getAttribute('id')),
        type: page.getAttribute('type'),
        name: page.getAttribute('name'),
        description: page.getAttribute('description'),
        isPersonal: page.getAttribute('ownerId') !== '0',
      }));
    },

    async deleteSavedSearch(id) {
      await call('DeleteSavedSearch', { searchPageId: id });
    },

    /**
     * Runs a saved search: translates its fields into Search API criteria and calls Search.
     * Returns { count, criteriaXml, skipped }. Read the results with GetNextSearchPage.
     */
    // sortBy: a Search API sort field. Not empty - the REST endpoint rejects an empty SortBy.
    async runSavedSearch(id, { sortBy = 'DOCUMENTNAME', ascending = true } = {}) {
      const { items } = await this.getSavedSearch(id);
      const { criteriaXml, skipped } = await toSearchCriteriaXml(items, (name) => this.getPropertySetFieldTypes(name));
      const root = await call('Search', { xmlcriteria: criteriaXml, SortBy: sortBy, AscendingOrder: ascending ? 'true' : 'false' });
      return { count: Number(root.getAttribute('count')), criteriaXml, skipped };
    },

    /** { FIELDNAME: 'CHAR' | 'NUMBER' | 'DATE' | 'BOOLEAN' } for a property set. */
    async getPropertySetFieldTypes(propertySetName) {
      const root = await call('GetPropertySetDefinition', { PropertySetName: propertySetName });
      const types = {};
      for (const field of Array.from(root.getElementsByTagName('field'))) {
        types[field.getAttribute('FieldName').toUpperCase()] = field.getAttribute('DataType').toUpperCase();
      }
      return types;
    },
  };
}

// ---------------------------------------------------------------------------------------------
// Saved search fields -> Search API criteria.
//
// A saved search stores the server's own form of a search, which is not the <criteria> form the
// Search API reads: a folder is an id rather than a path, CHECKOUTSTATUS says ME rather than
// CHECKEDOUTBYME, a relative date says PREVIOUS 30 D rather than a date range. This turns one into
// the other. Ids are passed as short references (~F1234 for a folder, ~U4 for a user), which the
// Search API resolves itself.
// ---------------------------------------------------------------------------------------------

const SCOPE_WORDS = { 0: 'ONLINE', 1: 'ALL', 2: 'ARCHIVE', 3: 'ONLINE-HIDDENS' };
const CHECKOUT_WORDS = { ALL: 'CHECKEDOUT', 0: 'NOTCHECKEDOUT', ME: 'CHECKEDOUTBYME', USER: 'CHECKEDOUTBYUSER' };
const CLEVEL_WORDS = { 0: 'NOMARKINGS', 1: 'DECLASSIFIED', 2: 'CONFIDENTIAL', 3: 'SECRET', 4: 'TOPSECRET' };

// Property set conditions are stored as numbers whose meaning depends on the field's type.
// null marks a condition the Search API has no operator for.
const PROPERTY_OPERATORS = {
  DATE: { 1: 'ANYTIME', 2: 'YESTERDAY', 3: 'TODAY', 4: 'LAST7DAYS', 5: 'NEXT7DAYS', 6: 'LASTWEEK', 7: 'THISWEEK',
          8: 'NEXTWEEK', 9: 'LASTMONTH', 10: 'THISMONTH', 11: 'NEXTMONTH', 12: 'EQ', 13: 'EQGT', 14: 'EQLT', 15: 'NULL', 16: null },
  NUMBER: { 1: 'EQ', 2: 'NOTEQ', 3: 'EQLT', 4: 'EQGT', 5: 'GT', 6: 'LT', 7: 'NOTNULL', 8: 'NULL', 9: null },
  CHAR: { 1: 'LIKE', 2: 'EQ', 3: 'NULL', 4: 'NOTNULL', 5: null, 6: null },
  BOOLEAN: { 1: 'EQ', 2: 'NOTNULL', 3: 'NULL' },
};

function localDate(date) {
  const pad = (n) => String(n).padStart(2, '0');
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}`;
}

function addPeriod(date, unit, n) {
  const d = new Date(date.getFullYear(), date.getMonth(), date.getDate());
  if (unit === 'D') d.setDate(d.getDate() + n);
  if (unit === 'W') d.setDate(d.getDate() + 7 * n);
  if (unit === 'M') d.setMonth(d.getMonth() + n);
  if (unit === 'Y') d.setFullYear(d.getFullYear() + n);
  return d;
}

/** A stored DATE1/DATE2 (a UTC timestamp) as the local calendar date it was saved as. */
function storedDate(value) {
  return value ? localDate(new Date(value)) : '';
}

/**
 * items: what getSavedSearch returned. propertySetFieldTypes: async (name) => { FIELD: 'CHAR', ... }.
 * Returns { criteriaXml, skipped } - skipped names what the Search API cannot express.
 */
async function toSearchCriteriaXml(items, propertySetFieldTypes) {
  const out = [];
  const skipped = [];
  const add = (attributes, children = '') => {
    const text = Object.entries(attributes).map(([k, v]) => `${k}="${escapeXml(v)}"`).join(' ');
    out.push(children ? `  <criteria ${text}>\n${children}  </criteria>` : `  <criteria ${text} />`);
  };
  const value = (name) => (items[name]?.VALUE ?? '').trim();

  if (items.SEARCHSCOPE) add({ NAME: 'SEARCHSCOPE', VALUE: SCOPE_WORDS[value('SEARCHSCOPE')] ?? 'ONLINE' });
  if (value('SEARCHFOR')) add({ NAME: 'SEARCHFOR', VALUE: value('SEARCHFOR') });
  if (value('DOCTYPE')) add({ NAME: 'DOCTYPE', VALUE: value('DOCTYPE') });
  if (value('KEYWORDS')) add({ NAME: 'KEYWORDS', VALUE: value('KEYWORDS') });
  for (const name of value('DOCUMENTNAME').split('|').map((s) => s.trim()).filter(Boolean)) add({ NAME: 'DOCUMENTNAME', VALUE: name });
  if (value('FOLDERDESC')) add({ NAME: 'FOLDERDESCRIPTION', VALUE: value('FOLDERDESC') });
  if (value('DOCUMENTID')) add({ NAME: 'DOCUMENTID', VALUE: value('DOCUMENTID') });
  if (value('FOLDERBYID')) add({ NAME: 'FOLDERBYID', VALUE: value('FOLDERBYID') });
  if (value('DOCUMENTFORMAT')) add({ NAME: 'DOCUMENTFORMAT', VALUE: value('DOCUMENTFORMAT') });
  if (value('DOCSRC')) add({ NAME: 'DOCSRC', VALUE: value('DOCSRC') });
  if (value('DOCLANG')) add({ NAME: 'DOCLANG', VALUE: value('DOCLANG') });
  if (value('DOCAUTHOR')) add({ NAME: 'DOCAUTHOR', VALUE: value('DOCAUTHOR') });
  if (Number(value('RDDEFID')) > 0) add({ NAME: 'RDDEFID', VALUE: value('RDDEFID') });
  if (Number(value('PUBLISHSTATUS')) > 0) add({ NAME: 'PUBLISHSTATUS', VALUE: value('PUBLISHSTATUS') });
  if (value('AIENHANCED')) add({ NAME: 'AIENHANCED', VALUE: value('AIENHANCED') });
  if (value('TAGTEXT')) skipped.push('TAGTEXT: the Search API has no tag criterion');

  // Authors: the Search API takes one user.
  const authors = value('USERNAME').split(',').map((s) => s.trim()).filter(Boolean);
  if (authors.length > 0) add({ NAME: 'USERNAME', VALUE: `~U${authors[0]}` });
  if (authors.length > 1) skipped.push(`USERNAME: only the first of ${authors.length} authors is searched`);

  if (Number(value('FOLDER')) > 0) {
    add({ NAME: 'FOLDER', VALUE: `~F${value('FOLDER')}` });
    add({ NAME: 'INCLUDESUBFOLDERS', VALUE: (items.FOLDER.INCLUDESUBFOLDERS ?? 'TRUE').toUpperCase() === 'TRUE' ? 'true' : 'false' });
  }

  if (value('CHECKOUTSTATUS')) {
    const criterion = { NAME: 'CHECKOUTSTATUS', VALUE: CHECKOUT_WORDS[value('CHECKOUTSTATUS').toUpperCase()] };
    if (criterion.VALUE === 'CHECKEDOUTBYUSER') criterion.USERNAME = `~U${items.CHECKOUTSTATUS.USERNAME}`;
    add(criterion);
  }

  if (value('VIEWCRITERIA')) {
    const criterion = { NAME: 'VIEWCRITERIA', VALUE: value('VIEWCRITERIA') };
    if (Number(items.VIEWCRITERIA.USERNAME) > 0) criterion.USERNAME = `~U${items.VIEWCRITERIA.USERNAME}`;
    add(criterion);
  }

  if (value('SIZEIS')) {
    add({ NAME: 'SIZEIS', OPERATOR: value('SIZEIS').toUpperCase() === 'AT MOST' ? 'EQLT' : 'EQGT', VALUE: items.SIZEIS.SIZEAMOUNT ?? '0' });
  }

  if (Number(value('IMPORTANCE')) >= 0 && items.IMPORTANCE.OPERATOR) {
    add({ NAME: 'IMPORTANCE', OPERATOR: items.IMPORTANCE.OPERATOR, VALUE: value('IMPORTANCE') });
  }

  if (value('CLEVEL')) add({ NAME: 'CLEVEL', VALUE: CLEVEL_WORDS[value('CLEVEL')] });

  if (value('DATECRITERIA')) {
    // The same ranges the server computes for a saved search, in the browser's local time.
    const d = items.DATECRITERIA;
    const today = new Date();
    const n = Number(d.PREVIOUSN ?? 0);
    const subtype = value('DATECRITERIA');
    switch ((d.DATETYPE ?? '').toUpperCase()) {
      case 'BETWEEN': {
        const from = storedDate(d.DATE1);
        const to = storedDate(d.DATE2);
        if (from && to) add({ NAME: 'DATECRITERIA', SUBTYPE: subtype, OPERATOR: 'BETWEEN', VALUE: `${from}|${to}` });
        else if (from) add({ NAME: 'DATECRITERIA', SUBTYPE: subtype, OPERATOR: 'EQGT', VALUE: from });
        else if (to) add({ NAME: 'DATECRITERIA', SUBTYPE: subtype, OPERATOR: 'EQLT', VALUE: to });
        break;
      }
      case 'TODAY':
        add({ NAME: 'DATECRITERIA', SUBTYPE: subtype, OPERATOR: 'EQ', VALUE: localDate(today) });
        break;
      case 'PREVIOUS':
        add({ NAME: 'DATECRITERIA', SUBTYPE: subtype, OPERATOR: 'BETWEEN',
              VALUE: `${localDate(addPeriod(today, d.PREVIOUSDATETYPE, -n))}|${localDate(today)}` });
        break;
      case 'NEXT':
        add({ NAME: 'DATECRITERIA', SUBTYPE: subtype, OPERATOR: 'BETWEEN',
              VALUE: `${localDate(addPeriod(today, 'D', 1))}|${localDate(addPeriod(addPeriod(today, d.PREVIOUSDATETYPE, n), 'D', -1))}` });
        break;
    }
  }

  if (value('PROPERTYSETNAME')) {
    const p = items.PROPERTYSETNAME;
    const fields = (p.ATTRIBUTES ?? '').split('|');
    const conditions = (p.CONDITIONS ?? '').split('|');
    const values = (p.VALUES ?? '').split('|');
    const types = await propertySetFieldTypes(value('PROPERTYSETNAME'));
    let children = '';
    fields.forEach((field, i) => {
      const condition = Number(conditions[i] ?? 0);
      if (!field || condition === 0) return;
      const operator = PROPERTY_OPERATORS[types[field.toUpperCase()]]?.[condition];
      if (!operator) {
        skipped.push(`PROPERTYSETNAME: ${field} condition ${condition} has no Search API operator`);
        return;
      }
      const fieldValue = (values[i] ?? '').replace(/&PIPE;/g, '|');
      children += `    <criteria NAME="${escapeXml(field)}" OPERATOR="${operator}" VALUE="${escapeXml(fieldValue)}" />\n`;
    });
    if (children) add({ NAME: 'PROPERTYSETNAME', VALUE: value('PROPERTYSETNAME') }, children);
  }

  return { criteriaXml: `<search>\n${out.join('\n')}\n</search>`, skipped };
}

if (typeof module !== 'undefined') {
  module.exports = { SEARCH_ITEM_DEFAULTS, buildSearchXml, parseSearchElement, createInfoRouterClient, toSearchCriteriaXml, InfoRouterError };
}
```

### Usage

```js
// Sign in once and keep the ticket.
const login = await fetch('/srv.asmx/AuthenticateUser', { method: 'POST', body: new URLSearchParams({ UID: user, PWD: password }) });
const ticket = new DOMParser().parseFromString(await login.text(), 'text/xml').documentElement.getAttribute('ticket');
const ir = createInfoRouterClient('', ticket);   // '' = same origin

// Save what the user searched for as a personal saved search.
const id = await ir.createSavedSearch({
  type: 'savedSearch',
  name: 'My Q4 Contracts',
  description: 'Contract documents changed in the last 30 days',
  isPersonal: true,
  items: {
    SEARCHFOR: { VALUE: 'DOCUMENTSONLY' },
    KEYWORDS: { VALUE: 'contract renewal' },
    DATECRITERIA: { VALUE: 'MODIFIED', DATETYPE: 'PREVIOUS', PREVIOUSDATETYPE: 'D', PREVIOUSN: '30' },
    IMPORTANCE: { VALUE: 'HIGH', OPERATOR: 'GT-EQ' },
  },
});

// Edit: read, change, send everything back.
const entry = await ir.getSavedSearch(id);
entry.items.KEYWORDS.VALUE = 'contract termination';
await ir.updateSavedSearch(id, entry);

// Run it, then page through the results.
const { count, skipped } = await ir.runSavedSearch(id);
const firstPage = await ir.call('GetNextSearchPage', { withrules: false, withPropertySets: false, withSecurity: false, withOwner: false, withVersions: false });
```

### Rendering a Search Page

```js
const page = await ir.getSavedSearch(searchPageId);
for (const [name, item] of Object.entries(page.items)) {
  if (!item.VISIBLE) continue;
  renderField(name, item);   // your control for KEYWORDS, DATECRITERIA, ... prefilled with item.VALUE
}
```

## Running a Saved Search

There is no API that runs a saved search by id. Run it by reading it with `GetSavedSearch` and passing its fields to [Search](Search.md) as `<criteria>` elements. The two formats differ, so the fields must be translated; `toSearchCriteriaXml` in the helper does this, and `runSavedSearch` calls it.

| Saved search `ITEM` | Search API `criteria` |
|---------------------|------------------------|
| `SEARCHSCOPE VALUE="0"` / `1` / `2` / `3` | `SEARCHSCOPE VALUE="ONLINE"` / `ALL` / `ARCHIVE` / `ONLINE-HIDDENS` |
| `DOCUMENTNAME VALUE="a\|b"` | One `DOCUMENTNAME` per name |
| `FOLDERDESC` | `FOLDERDESCRIPTION` |
| `FOLDER VALUE="1234" INCLUDESUBFOLDERS="FALSE"` | `FOLDER VALUE="~F1234"` and `INCLUDESUBFOLDERS VALUE="false"` |
| `USERNAME VALUE="4"` | `USERNAME VALUE="~U4"` (one user only) |
| `CHECKOUTSTATUS VALUE="ALL"` / `0` / `ME` / `USER` | `CHECKEDOUT` / `NOTCHECKEDOUT` / `CHECKEDOUTBYME` / `CHECKEDOUTBYUSER` with `USERNAME="~U4"` |
| `VIEWCRITERIA USERNAME="4"` | `VIEWCRITERIA USERNAME="~U4"` |
| `SIZEIS VALUE="AT LEAST" SIZEAMOUNT="1024"` | `SIZEIS OPERATOR="EQGT" VALUE="1024"` (`AT MOST` → `EQLT`; kilobytes in both) |
| `IMPORTANCE OPERATOR="GT-EQ" VALUE="2"` | Same |
| `CLEVEL VALUE="2"` | `CLEVEL VALUE="CONFIDENTIAL"` |
| `DATECRITERIA VALUE="MODIFIED" DATETYPE="BETWEEN"` | `DATECRITERIA SUBTYPE="MODIFIED" OPERATOR="BETWEEN" VALUE="from\|to"` (`EQGT`/`EQLT` when one date is empty) |
| `DATETYPE="TODAY"` / `PREVIOUS` / `NEXT` | `EQ` today / `BETWEEN` the computed range, in the browser's local date |
| `PROPERTYSETNAME` conditions | Child `criteria` with the Search API operator: `CHAR` 1 → `LIKE`, `NUMBER` 2 → `NOTEQ`, other names as in the table above |
| `KEYWORDS`, `SEARCHFOR`, `DOCTYPE`, `DOCUMENTID`, `FOLDERBYID`, `DOCUMENTFORMAT`, `DOCSRC`, `DOCLANG`, `DOCAUTHOR`, `RDDEFID`, `PUBLISHSTATUS`, `AIENHANCED` | Same name and value |

The Search API cannot express everything a saved search can store. `toSearchCriteriaXml` leaves these out and lists them in `skipped`:

- `TAGTEXT`: the Search API has no tag criterion.
- More than one id in `USERNAME`: only the first owner is searched.
- Property set conditions `CHAR` NOTCONTAINS and NEQ, `NUMBER` BETWEEN, `DATE` BETWEEN.

Pass a `SortBy` value such as `DOCUMENTNAME` to `Search`: its REST endpoint rejects an empty `SortBy` with HTTP 400.

## Related APIs

- [CreateSavedSearch](CreateSavedSearch.md), [UpdateSavedSearch](UpdateSavedSearch.md), [GetSavedSearch](GetSavedSearch.md), [GetSavedSearches](GetSavedSearches.md), [DeleteSavedSearch](DeleteSavedSearch.md)
- [Search](Search.md), [GetNextSearchPage](GetNextSearchPage.md)
- [GetPropertySetDefinition](GetPropertySetDefinition.md) — field names and types of a property set
