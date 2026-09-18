# GetSavedSearch API

Returns a saved search or search page: its name, owner, access, and every field with its value and visibility. The response carries everything [UpdateSavedSearch](UpdateSavedSearch.md) needs, in the form it takes.

## Endpoint

```
/srv.asmx/GetSavedSearch
```

## Methods

- **GET** `/srv.asmx/GetSavedSearch?authenticationTicket=...&searchPageId=...`
- **POST** `/srv.asmx/GetSavedSearch` (form data)
- **SOAP** Action: `http://tempuri.org/GetSavedSearch`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `searchPageId` | int | Yes | Id of the entry. Obtain ids from `GetSavedSearches` |

## Response

### Success

```xml
<response success="true" error="">
  <SearchPage id="2138" name="Contract Search" description="Keyword, name and date only" type="searchPage"
              ownerId="0" anonymousAccess="false" publicAccess="true"
              userGroupIds="105,1062" userGroupNames="[Search &amp; Category Administrators]|Finance\Controllers">
    <SEARCH>
      <ITEM NAME="SEARCHSCOPE" VALUE="0" VISIBLE="FALSE" />
      <ITEM NAME="SEARCHFOR" VALUE="" VISIBLE="FALSE" />
      <ITEM NAME="DOCTYPE" VALUE="" VISIBLE="FALSE" />
      <ITEM NAME="KEYWORDS" VALUE="" VISIBLE="TRUE" />
      <ITEM NAME="DOCUMENTNAME" VALUE="" VISIBLE="TRUE" />
      <ITEM NAME="FOLDERDESC" VALUE="" VISIBLE="FALSE" />
      <ITEM NAME="DOCUMENTID" VALUE="" VISIBLE="FALSE" />
      <ITEM NAME="FOLDERBYID" VALUE="" VISIBLE="FALSE" />
      <ITEM NAME="USERNAME" VALUE="" VISIBLE="FALSE" />
      <ITEM NAME="FOLDER" VALUE="0" INCLUDESUBFOLDERS="TRUE" VISIBLE="FALSE" />
      <ITEM NAME="CHECKOUTSTATUS" USERNAME="0" VALUE="" VISIBLE="FALSE" />
      <ITEM NAME="DATECRITERIA" VALUE="" DATETYPE="" DATE1="" DATE2="" PREVIOUSN="0" PREVIOUSDATETYPE="" VISIBLE="TRUE" />
      <ITEM NAME="SIZEIS" VALUE="" SIZEAMOUNT="0" VISIBLE="FALSE" />
      <ITEM NAME="IMPORTANCE" VALUE="-1" OPERATOR="" VISIBLE="FALSE" />
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
      <ITEM NAME="PROPERTYSETNAME" VALUE="" ATTRIBUTES="" CONDITIONS="" VALUES="" VISIBLE="TRUE" FIELDS="TRUE" />
    </SEARCH>
  </SearchPage>
</response>
```

### Error

```xml
<response success="false" error="Search or category page cannot be found." errorcode="4041" />
```

## Response Fields

### `SearchPage` Attributes

| Attribute | Type | Description | Send to UpdateSavedSearch as |
|-----------|------|-------------|------------------------------|
| `id` | int | Entry id | `searchPageId` |
| `name` | string | Display name, without the owner id a personal entry is stored with | `name` |
| `description` | string | Description | `description` |
| `type` | string | `savedSearch` or `searchPage` | `searchPageType` |
| `ownerId` | int | `0` = system-wide; otherwise the owning user's id | `isPersonal` = `ownerId != 0` |
| `anonymousAccess` | bool | The anonymous user may use it. Always `false` for personal entries | `anonymousAccess` |
| `publicAccess` | bool | Every signed-in user may use it. Always `false` for personal entries | `publicAccess` |
| `userGroupIds` | string | Comma-separated ids of the groups it is shared with. Empty for personal entries | — |
| `userGroupNames` | string | The same groups by name, `\|`-separated, `library\group` for local groups | `userGroupNames` |

### `SEARCH` Element

All 25 fields in a fixed order, each with its value and `VISIBLE`. Values come back normalized (importance as a number, MIME types in upper case, dates as UTC timestamps, property set conditions as numbers). Field meanings and the normalization table are in [SavedSearchXmlReference](SavedSearchXmlReference.md#what-comes-back).

Serialize the element to a string to send it as `searchParametersXml`; unchanged, it stores the same definition.

## Required Permissions

A user may read the entries [GetSavedSearches](GetSavedSearches.md) lists for them:

| Entry | Who may read it |
|-------|-----------------|
| Personal | Its owner only. Not search administrators |
| System-wide, `publicAccess=true` | Every signed-in user |
| System-wide, shared with groups | Members of those groups |
| System-wide, any | Members of the `[Search & Category Administrators]` role group |
| System-wide, `anonymousAccess=true` | The anonymous user |

Anyone else gets `4030 Access denied.`

## Examples

### GET

```
GET /srv.asmx/GetSavedSearch?authenticationTicket=abc123&searchPageId=2138 HTTP/1.1
```

### POST

```
POST /srv.asmx/GetSavedSearch HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&searchPageId=2138
```

### SOAP 1.1

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetSavedSearch"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetSavedSearch xmlns="http://tempuri.org/">
      <authenticationTicket>abc123</authenticationTicket>
      <searchPageId>2138</searchPageId>
    </GetSavedSearch>
  </soap:Body>
</soap:Envelope>
```

### JavaScript

```js
const response = await fetch('/srv.asmx/GetSavedSearch', {
  method: 'POST',
  body: new URLSearchParams({ authenticationTicket: ticket, searchPageId: 2138 }),
});
const root = new DOMParser().parseFromString(await response.text(), 'text/xml').documentElement;
if (root.getAttribute('success') !== 'true') throw new Error(root.getAttribute('error'));

const page = root.getElementsByTagName('SearchPage')[0];
const visibleFields = Array.from(page.getElementsByTagName('ITEM'))
  .filter((item) => item.getAttribute('VISIBLE').toUpperCase() === 'TRUE')
  .map((item) => item.getAttribute('NAME'));
```

`getSavedSearch` in the [JavaScript helper](SavedSearchXmlReference.md#javascript-helper) returns the same as an object.


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

Reads one saved search, its criteria included.

```javascript
const root = await call('GetSavedSearch', { authenticationTicket: ticket, searchPageId: 20800 });

const page = root.querySelector('SearchPage');
console.log(page.getAttribute('name'), page.getAttribute('userGroupNames'));

for (const item of page.querySelectorAll('ITEM')) {
  if (item.getAttribute('VALUE')) { console.log(item.getAttribute('NAME'), item.getAttribute('VALUE')); }
}
```

**The stored form holds every criterion, not only the ones that were sent.** The ones with a value
are marked `VISIBLE="FALSE"` and the empty ones `VISIBLE="TRUE"` - the flag drives the search form's
layout, not whether the criterion counts. `userGroupNames` comes back in the shape
[UpdateSavedSearch](UpdateSavedSearch.md) takes, so a page read here can be written straight back.

## Notes

- A group deleted after the entry was saved no longer appears in `userGroupNames`.
- A property set deleted after the entry was saved comes back as an empty `PROPERTYSETNAME`.
- There is no API that runs a saved search by id. See [Running a Saved Search](SavedSearchXmlReference.md#running-a-saved-search).

## Related APIs

- [GetSavedSearches](GetSavedSearches.md) — List the entries the user may use
- [UpdateSavedSearch](UpdateSavedSearch.md) — Change an entry
- [CreateSavedSearch](CreateSavedSearch.md) — Create an entry
- [DeleteSavedSearch](DeleteSavedSearch.md) — Delete an entry
- [SavedSearchXmlReference](SavedSearchXmlReference.md) — Field reference, JavaScript helper, running a saved search

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | no saved search by that id |
