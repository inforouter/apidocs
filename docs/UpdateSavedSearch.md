# UpdateSavedSearch API

Replaces the name, description, access and fields of a saved search or search page. With `searchPageId=0` it creates one instead, exactly as [CreateSavedSearch](CreateSavedSearch.md) does.

## Endpoint

```
/srv.asmx/UpdateSavedSearch
```

## Methods

- **GET** `/srv.asmx/UpdateSavedSearch?authenticationTicket=...&searchPageId=...&searchPageType=...&name=...&...`
- **POST** `/srv.asmx/UpdateSavedSearch` (form data)
- **SOAP** Action: `http://tempuri.org/UpdateSavedSearch`

Prefer POST: `searchParametersXml` is usually too long for a query string.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `searchPageId` | int | Yes | The entry to update. `0` creates a new entry |
| `searchPageType` | string | Yes | `savedSearch` or `searchPage`, in any case. Must be the entry's current type: an update cannot change it |
| `name` | string | Yes | Display name, 5 to 64 characters, unique among entries of the same type. Rules as in [CreateSavedSearch](CreateSavedSearch.md#names) |
| `description` | string | No | Description. Empty clears it |
| `isPersonal` | bool | Yes | Used only when creating (`searchPageId=0`). An update keeps the entry's owner whatever is sent |
| `anonymousAccess` | bool | No | System-wide entries: the anonymous user may use it. Ignored for personal entries |
| `publicAccess` | bool | No | System-wide entries: every signed-in user may use it. Ignored for personal entries |
| `userGroupNames` | string | No | System-wide entries: the groups, separated by `\|` (`library\group` for a local group). **Replaces** the current groups; empty removes them all. Ignored for personal entries |
| `searchParametersXml` | string | No | The fields and their values. **Replaces** the stored definition; empty resets every field to shown with no value. See [SavedSearchXmlReference](SavedSearchXmlReference.md) |

## An Update Replaces Everything

UpdateSavedSearch does not merge. Every parameter you send, or leave empty, becomes the entry's new state. To change one thing:

1. Read the entry with [GetSavedSearch](GetSavedSearch.md).
2. Change what the user changed.
3. Send all of it back: `type` as `searchPageType`, `userGroupNames` as they came, and the `<SEARCH>` element serialized as `searchParametersXml`.

`GetSavedSearch` returns every value in the form this API takes, so an unchanged round trip stores exactly what was there.

## Response

### Success (update)

```xml
<response success="true" error="" />
```

### Success (create, `searchPageId=0`)

```xml
<response success="true" error="" id="2138" />
```

### Error

```xml
<response success="false" error="Search or category page cannot be found." errorcode="4041" />
```

## Required Permissions

- Signed-in user.
- **Personal entry:** its owner only. A search administrator cannot update another user's personal entry.
- **System-wide entry:** members of the `[Search & Category Administrators]` role group.
- Creating (`searchPageId=0`): as in [CreateSavedSearch](CreateSavedSearch.md#required-permissions).

## Examples

### POST: Rename a Saved Search and Change Its Keywords

```
POST /srv.asmx/UpdateSavedSearch HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&searchPageId=2138&searchPageType=savedSearch&name=My+Q4+Contract+Terminations
&description=&isPersonal=true&anonymousAccess=false&publicAccess=false&userGroupNames=
&searchParametersXml=%3CSEARCH%3E%3CITEM+NAME%3D%22KEYWORDS%22+VALUE%3D%22contract+termination%22+VISIBLE%3D%22TRUE%22+%2F%3E%3C%2FSEARCH%3E
```

This replaces the whole definition with a single keyword field; the other fields become shown with no value. Send the full `<SEARCH>` element to keep them.

### POST: Share a Search Page with Everyone

```
POST /srv.asmx/UpdateSavedSearch HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&searchPageId=2140&searchPageType=searchPage&name=Contract+Search
&description=Keyword%2C+name+and+date+only&isPersonal=false&anonymousAccess=false&publicAccess=true
&userGroupNames=Legal%7CFinance%5CControllers&searchParametersXml=...
```

### SOAP 1.1

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/UpdateSavedSearch"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <UpdateSavedSearch xmlns="http://tempuri.org/">
      <authenticationTicket>abc123</authenticationTicket>
      <searchPageId>2138</searchPageId>
      <searchPageType>savedSearch</searchPageType>
      <name>My Q4 Contract Terminations</name>
      <description></description>
      <isPersonal>true</isPersonal>
      <anonymousAccess>false</anonymousAccess>
      <publicAccess>false</publicAccess>
      <userGroupNames></userGroupNames>
      <searchParametersXml>&lt;SEARCH&gt;&lt;ITEM NAME="KEYWORDS" VALUE="contract termination" VISIBLE="TRUE" /&gt;&lt;/SEARCH&gt;</searchParametersXml>
    </UpdateSavedSearch>
  </soap:Body>
</soap:Envelope>
```

### JavaScript: Read, Change One Field, Save

Plain `fetch` and DOM. The entry is read, one `ITEM` is changed in place, and everything is sent back.

```js
async function changeKeywords(ticket, searchPageId, keywords) {
  const post = async (action, params) => {
    const response = await fetch(`/srv.asmx/${action}`, {
      method: 'POST',
      body: new URLSearchParams({ authenticationTicket: ticket, ...params }),
    });
    const root = new DOMParser().parseFromString(await response.text(), 'text/xml').documentElement;
    if (root.getAttribute('success') !== 'true') throw new Error(root.getAttribute('error'));
    return root;
  };

  // 1. Read.
  const page = (await post('GetSavedSearch', { searchPageId })).getElementsByTagName('SearchPage')[0];
  const search = page.getElementsByTagName('SEARCH')[0];

  // 2. Change one field.
  const item = Array.from(search.getElementsByTagName('ITEM')).find((i) => i.getAttribute('NAME') === 'KEYWORDS');
  item.setAttribute('VALUE', keywords);

  // 3. Send everything back.
  await post('UpdateSavedSearch', {
    searchPageId,
    searchPageType: page.getAttribute('type'),
    name: page.getAttribute('name'),
    description: page.getAttribute('description'),
    isPersonal: page.getAttribute('ownerId') !== '0' ? 'true' : 'false',
    anonymousAccess: page.getAttribute('anonymousAccess'),
    publicAccess: page.getAttribute('publicAccess'),
    userGroupNames: page.getAttribute('userGroupNames'),
    searchParametersXml: new XMLSerializer().serializeToString(search),
  });
}
```

### JavaScript: With the Helper

`createInfoRouterClient` is in [SavedSearchXmlReference](SavedSearchXmlReference.md#javascript-helper). `getSavedSearch` returns an object `updateSavedSearch` takes back.

```js
const ir = createInfoRouterClient('', ticket);

// Change the keywords and the date range of a saved search.
const entry = await ir.getSavedSearch(savedSearchId);
entry.items.KEYWORDS.VALUE = 'contract termination';
entry.items.DATECRITERIA = { VALUE: 'MODIFIED', DATETYPE: 'PREVIOUS', PREVIOUSDATETYPE: 'D', PREVIOUSN: '90', VISIBLE: true };
await ir.updateSavedSearch(savedSearchId, entry);

// Make a search page public and offer one more field, keeping its groups.
const page = await ir.getSavedSearch(searchPageId);
page.publicAccess = true;
page.items.DOCTYPE.VISIBLE = true;
await ir.updateSavedSearch(searchPageId, page);

// Rename.
const renamed = await ir.getSavedSearch(savedSearchId);
renamed.name = 'My Q4 Contract Terminations';
await ir.updateSavedSearch(savedSearchId, renamed);
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

Rewrites a saved search. Every parameter of
[CreateSavedSearch](CreateSavedSearch.md) applies, plus the id.

```javascript
await call('UpdateSavedSearch', {
  authenticationTicket: ticket,
  searchPageId: 20800,
  searchPageType: 'savedSearch',
  name: 'Overdue invoices',
  description: 'Anything still open after 30 days',
  isPersonal: true,
  anonymousAccess: false,
  publicAccess: false,
  userGroupNames: '',
  searchParametersXml: criteria
});
```

Two things the update does **not** do, both on purpose:

- **`isPersonal` is ignored.** The owner is taken from the stored row, so an update can never move a
  page between personal and system.
- **The sharing flags are not written onto a personal page.** `anonymousAccess` and `publicAccess`
  reach a system page only; on a personal one they are left as they are.

`searchPageType` has to match the stored page's type as well as being one of the two literals - a
mismatch is a `4041`, not a `4000`.

## Notes

- An update cannot turn a personal entry into a system-wide one or the other way round, nor change the type. Create a new entry and delete the old one.
- The default search page (id `1`, "Advanced Search") keeps its name and description; send `Advanced Search` as `name`. Its access, groups and fields can be updated.
- The same name may be sent back unchanged; it only has to be unique against other entries.
- A property set named in `PROPERTYSETNAME` that does not exist is dropped without an error.
- REST: send every parameter, even empty ones; empty values are accepted.

## Related APIs

- [GetSavedSearch](GetSavedSearch.md) — Read an entry before changing it
- [CreateSavedSearch](CreateSavedSearch.md) — Create an entry
- [GetSavedSearches](GetSavedSearches.md) — List the entries the user may use
- [DeleteSavedSearch](DeleteSavedSearch.md) — Delete an entry
- [SavedSearchXmlReference](SavedSearchXmlReference.md) — Field reference, JavaScript helper, running a saved search

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | no saved search by that id, or `searchPageType` does not match its type |
| `4000` | `searchPageType` is not `savedSearch` or `searchPage`, or `name` is empty |
| `4090` | another page of that name and type already exists |
| `4030` | the caller neither owns the page nor is a search administrator |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
