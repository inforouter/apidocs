# GetSavedSearch API

Returns the full definition of a single saved search or search page by ID, including its field-visibility configuration.

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
| `searchPageId` | int | Yes | ID of the search page to retrieve. Obtain IDs from `GetSavedSearches` |

## Response

### Success

```xml
<root success="true">
  <SearchPage id="47" name="Contract Search" description="Search for contract documents"
              ownerId="0" anonymousAccess="false" publicAccess="true" userGroupIds="12,34">
    <SEARCH>
      <ITEM NAME="SEARCHFOR" VALUE="" VISIBLE="TRUE" />
      <ITEM NAME="KEYWORDS" VALUE="" VISIBLE="TRUE" />
      <ITEM NAME="DOCUMENTNAME" VALUE="" VISIBLE="FALSE" />
      ...
    </SEARCH>
  </SearchPage>
</root>
```

### Error

```xml
<root success="false" error="Error message here" />
```

## Response Fields

### `SearchPage` attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | int | Search page ID |
| `name` | string | Display name |
| `description` | string | Optional description |
| `ownerId` | int | `0` = system-wide page; `> 0` = private page owned by that user ID |
| `anonymousAccess` | bool | Whether anonymous users can access this page. Always `false` for personal pages |
| `publicAccess` | bool | Whether all authenticated users can access this page. Always `false` for personal pages |
| `userGroupIds` | string | Comma-separated group IDs that have explicit access. Empty = no group restriction. Always empty for personal pages |

### `SEARCH` child element

An inline XML element containing the field-visibility configuration. Each `<ITEM>` child defines one search field:

```xml
<SEARCH>
  <ITEM NAME="SEARCHFOR" VALUE="" VISIBLE="TRUE" />
  <ITEM NAME="KEYWORDS" VALUE="" VISIBLE="FALSE" />
  ...
</SEARCH>
```

To clone or update the search page via `UpdateSavedSearch`, serialize this `<SEARCH>` element to a string and pass it as the `searchParametersXml` parameter.

## Required Permissions

- User must be authenticated.

## Example Requests

### Request (GET)

```
GET /srv.asmx/GetSavedSearch?authenticationTicket=abc123&searchPageId=47 HTTP/1.1
```

### Request (POST)

```
POST /srv.asmx/GetSavedSearch HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&searchPageId=47
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetSavedSearch"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetSavedSearch xmlns="http://tempuri.org/">
      <authenticationTicket>abc123</authenticationTicket>
      <searchPageId>47</searchPageId>
    </GetSavedSearch>
  </soap:Body>
</soap:Envelope>
```

## Error Codes

| Error | Description |
|-------|-------------|
| `[901] Session expired or Invalid ticket` | Invalid or expired authentication ticket |
| `[3169] ...` | Search page not found |

## Notes

- Use `GetSavedSearches` first to discover available search page IDs.
- The `searchParametersXml` output can be modified and passed back to `UpdateSavedSearch` to create a variant of an existing page.
- `userGroupIds` contains numeric IDs. To resolve group names, use the user group management APIs.

## Related APIs

- `GetSavedSearches` — List all search page definitions visible to the current user
- `UpdateSavedSearch` — Create or update a search page definition
- `DeleteSavedSearch` — Delete a saved search or search page by ID
