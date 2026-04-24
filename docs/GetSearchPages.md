# GetSearchPages API

Returns all search page definitions visible to the authenticated user.

## Endpoint

```
/srv.asmx/GetSearchPages
```

## Methods

- **GET** `/srv.asmx/GetSearchPages?authenticationTicket=...`
- **POST** `/srv.asmx/GetSearchPages` (form data)
- **SOAP** Action: `http://tempuri.org/GetSearchPages`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |

## Response

### Success

```xml
<root success="true">
  <SearchPage id="1" name="Advanced Search" description="" ownerId="0" anonymousAccess="false" publicAccess="false" />
  <SearchPage id="12" name="Contract Search" description="Search for contract documents" ownerId="0" anonymousAccess="true" publicAccess="true" />
  <SearchPage id="47" name="My Custom Search" description="" ownerId="23" anonymousAccess="false" publicAccess="false" />
</root>
```

### Error

```xml
<root success="false" error="Error message here" />
```

## Response Attributes (per `SearchPage` element)

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | int | Unique search page ID |
| `name` | string | Display name of the search page |
| `description` | string | Optional description |
| `ownerId` | int | User ID of the owner. `0` = system-wide (shared) page; `>0` = private page owned by that user |
| `anonymousAccess` | bool | Whether anonymous (unauthenticated) users can use this search page. Always `false` for private pages (`ownerId > 0`) |
| `publicAccess` | bool | Whether all authenticated users can use this search page. Always `false` for private pages (`ownerId > 0`) |

## Visibility Rules

- **Search administrators** receive all search page definitions in the system.
- **Regular users** receive system-wide pages (`ownerId = 0`) plus any private pages they own (`ownerId = their user ID`).

The filtering is applied automatically by the server; no additional parameter is needed.

## Required Permissions

- User must be authenticated.

## Example Requests

### Request (GET)

```
GET /srv.asmx/GetSearchPages?authenticationTicket=abc123 HTTP/1.1
```

### Request (POST)

```
POST /srv.asmx/GetSearchPages HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetSearchPages"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetSearchPages xmlns="http://tempuri.org/">
      <authenticationTicket>abc123</authenticationTicket>
    </GetSearchPages>
  </soap:Body>
</soap:Envelope>
```

## Error Codes

| Error | Description |
|-------|-------------|
| `[901] Session expired or Invalid ticket` | Invalid or expired authentication ticket |

## Related APIs

- `SaveSearchPage` — Create or update a search page definition
- `DeleteSearchPage` — Delete a saved search page by ID
- `GetCategories` — List saved search categories
