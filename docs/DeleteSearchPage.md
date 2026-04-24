# DeleteSearchPage API

Deletes a saved search page definition by ID.

## Endpoint

```
/srv.asmx/DeleteSearchPage
```

## Methods

- **GET** `/srv.asmx/DeleteSearchPage?authenticationTicket=...&searchPageId=...`
- **POST** `/srv.asmx/DeleteSearchPage` (form data)
- **SOAP** Action: `http://tempuri.org/DeleteSearchPage`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `searchPageId` | int | Yes | ID of the search page to delete. Obtain IDs from `GetSearchPages` |

## Response

### Success

```xml
<root success="true" />
```

### Error

```xml
<root success="false" error="Error message here" />
```

## Required Permissions

- User must be authenticated.
- **Personal pages** (`ownerId > 0`): only the page owner may delete.
- **System-wide pages** (`ownerId = 0`): requires the **Search Administrator** role.

## Example Requests

### Request (GET)

```
GET /srv.asmx/DeleteSearchPage?authenticationTicket=abc123&searchPageId=47 HTTP/1.1
```

### Request (POST)

```
POST /srv.asmx/DeleteSearchPage HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&searchPageId=47
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/DeleteSearchPage"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <DeleteSearchPage xmlns="http://tempuri.org/">
      <authenticationTicket>abc123</authenticationTicket>
      <searchPageId>47</searchPageId>
    </DeleteSearchPage>
  </soap:Body>
</soap:Envelope>
```

## Error Codes

| Error | Description |
|-------|-------------|
| `[901] Session expired or Invalid ticket` | Invalid or expired authentication ticket |
| `[921] ...` | User is not authenticated |
| `[2840] ...` | Caller is not a Search Administrator (system-wide page) |
| `[2842] ...` | The default search page (ID 1) cannot be deleted |
| `[3167] ...` | Caller is not the owner of the page (personal page) |
| `[3169] ...` | Search page not found |

## Notes

- The default system search page (ID 1, "Advanced Search") is protected and cannot be deleted by anyone.
- Use `GetSearchPages` to discover the IDs of available search pages.

## Related APIs

- `GetSearchPages` — List all search page definitions visible to the current user
- `SaveSearchPage` — Create or update a search page definition
