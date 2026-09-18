# GetSavedSearches API

Lists saved searches and/or search page definitions visible to the authenticated user.

## Endpoint

```
/srv.asmx/GetSavedSearches
```

## Methods

- **GET** `/srv.asmx/GetSavedSearches?authenticationTicket=...&searchPageType=...`
- **POST** `/srv.asmx/GetSavedSearches` (form data)
- **SOAP** Action: `http://tempuri.org/GetSavedSearches`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `searchPageType` | string | No | Type filter: `all`, `searchPage`, or `savedSearch`. Case-insensitive. Empty or omitted defaults to `all` |

### `searchPageType` values

| Value | Returns |
|-------|---------|
| `all` | Both search page definitions and saved searches (default) |
| `searchPage` | Search page definitions only (UI field-visibility configurations) |
| `savedSearch` | Saved searches only (user-defined saved query criteria) |

## Response

### Success

```xml
<response success="true" error="">
  <SearchPage id="1"    name="Advanced Search"      description=""                         type="searchPage"  ownerId="0"  anonymousAccess="false" publicAccess="true" />
  <SearchPage id="7"    name="All Active Documents" description="System-wide saved search" type="savedSearch" ownerId="0"  anonymousAccess="true"  publicAccess="true" />
  <SearchPage id="2138" name="My Q4 Contracts"      description=""                         type="savedSearch" ownerId="12" anonymousAccess="false" publicAccess="false" />
</response>
```

### Error

```xml
<response success="false" error="Invalid parameter value in field (searchPageType). Accepted values are: savedSearch, searchPage, all" errorcode="4000" />
```

## Response Attributes (per `SearchPage` element)

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | int | Unique ID. Pass to `GetSavedSearch`, `UpdateSavedSearch`, or `DeleteSavedSearch` |
| `name` | string | Display name |
| `description` | string | Optional description |
| `type` | string | `searchPage` or `savedSearch` |
| `ownerId` | int | `0` = system-wide; `> 0` = private, owned by that user ID |
| `anonymousAccess` | bool | Whether anonymous (unauthenticated) users can use this entry. Always `false` for personal entries |
| `publicAccess` | bool | Whether all authenticated users can use this entry. Always `false` for personal entries |

## Visibility Rules

- **Every signed-in user** receives their own personal entries. Nobody receives another user's personal entries.
- **Search administrators** (members of `[Search & Category Administrators]`) also receive every system-wide entry.
- **Other users** also receive the system-wide entries that are public (`publicAccess=true`) or shared with one of their groups.
- **The anonymous user** receives the system-wide entries with `anonymousAccess=true`.

[GetSavedSearch](GetSavedSearch.md) lets a user read exactly the entries this list returns.

## Required Permissions

- User must be authenticated.

## Example Requests

### Request (GET) — all types

```
GET /srv.asmx/GetSavedSearches?authenticationTicket=abc123 HTTP/1.1
```

### Request (GET) — saved searches only

```
GET /srv.asmx/GetSavedSearches?authenticationTicket=abc123&searchPageType=savedSearch HTTP/1.1
```

### Request (POST)

```
POST /srv.asmx/GetSavedSearches HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&searchPageType=searchPage
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetSavedSearches"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetSavedSearches xmlns="http://tempuri.org/">
      <authenticationTicket>abc123</authenticationTicket>
      <searchPageType>all</searchPageType>
    </GetSavedSearches>
  </soap:Body>
</soap:Envelope>
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

Lists the saved searches or the search pages - one type per call.

```javascript
const root = await call('GetSavedSearches', {
  authenticationTicket: ticket, searchPageType: 'savedSearch'
});

for (const page of root.querySelectorAll('SearchPage')) {
  console.log(page.getAttribute('id'), page.getAttribute('name'), page.getAttribute('ownerId'));
}
```

An `ownerId` of `0` is a system page; anything else is that user's personal one. The list is a
summary - no criteria and no group names; [GetSavedSearch](GetSavedSearch.md) carries those.

## Notes

- Entries are ordered by name, whatever their type. A personal entry sorts by its stored name, which begins with the owner's user id.
- The `type` attribute is always present, making it safe to filter client-side after receiving an `all` response.

## Related APIs

- `GetSavedSearch` — Get the full definition of a single entry including field-visibility configuration
- `CreateSavedSearch` — Create a saved search or search page
- `UpdateSavedSearch` — Change a saved search or search page
- [SavedSearchXmlReference](SavedSearchXmlReference.md) — Field reference, JavaScript helper, running a saved search
- `DeleteSavedSearch` — Delete a saved search or search page by ID
- `Search` — Execute a search using XML-based criteria

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
