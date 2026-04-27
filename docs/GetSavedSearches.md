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
<root success="true">
  <SearchPage id="1"  name="Advanced Search"      type="searchPage"  ownerId="0"  anonymousAccess="false" publicAccess="true" description="" />
  <SearchPage id="3"  name="My Q4 Contracts"      type="savedSearch" ownerId="12" anonymousAccess="false" publicAccess="false" description="" />
  <SearchPage id="7"  name="All Active Documents"  type="savedSearch" ownerId="0"  anonymousAccess="true"  publicAccess="true" description="System-wide saved search" />
</root>
```

### Error

```xml
<root success="false" error="Error message here" />
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

- **Search administrators** receive all entries of the requested type(s).
- **Regular users** receive system-wide entries (`ownerId = 0`) plus any private entries they own (`ownerId = their user ID`).

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

## Error Codes

| Error | Description |
|-------|-------------|
| `[901] Session expired or Invalid ticket` | Invalid or expired authentication ticket |
| Invalid searchPageType | `searchPageType` value is not `all`, `searchPage`, or `savedSearch` |

## Notes

- When `searchPageType` is `all`, results from `searchPage` are returned first, followed by `savedSearch` entries.
- The `type` attribute is always present, making it safe to filter client-side after receiving an `all` response.

## Related APIs

- `GetSavedSearch` — Get the full definition of a single entry including field-visibility configuration
- `UpdateSavedSearch` — Create or update a search page definition or saved search
- `DeleteSavedSearch` — Delete a saved search or search page by ID
- `Search` — Execute a search using XML-based criteria
