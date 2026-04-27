# DeleteSavedSearch API

Deletes a saved search or search page definition by ID.

## Endpoint

```
/srv.asmx/DeleteSavedSearch
```

## Methods

- **GET** `/srv.asmx/DeleteSavedSearch?authenticationTicket=...&searchPageId=...`
- **POST** `/srv.asmx/DeleteSavedSearch` (form data)
- **SOAP** Action: `http://tempuri.org/DeleteSavedSearch`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `searchPageId` | int | Yes | ID of the entry to delete. Obtain IDs from `GetSavedSearches` |

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
- **Personal entries** (`isPersonal=true`): only the entry owner may delete.
- **System-wide entries** (`isPersonal=false`): requires the **Search Administrator** role.

## Example Requests

### Request (GET)

```
GET /srv.asmx/DeleteSavedSearch?authenticationTicket=abc123&searchPageId=47 HTTP/1.1
```

### Request (POST)

```
POST /srv.asmx/DeleteSavedSearch HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&searchPageId=47
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/DeleteSavedSearch"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <DeleteSavedSearch xmlns="http://tempuri.org/">
      <authenticationTicket>abc123</authenticationTicket>
      <searchPageId>47</searchPageId>
    </DeleteSavedSearch>
  </soap:Body>
</soap:Envelope>
```

## Error Codes

| Error | Description |
|-------|-------------|
| `[901] Session expired or Invalid ticket` | Invalid or expired authentication ticket |
| `[921] ...` | User is not authenticated |
| `[2840] ...` | Caller is not a Search Administrator (system-wide entry) |
| `[2842] ...` | The default search page (ID 1) cannot be deleted |
| `[3167] ...` | Caller is not the owner of the entry (personal entry) |
| `[3169] ...` | Entry not found |

## Notes

- The default system search page (ID 1, "Advanced Search") is protected and cannot be deleted by anyone.
- Use `GetSavedSearches` to discover the IDs of available entries.

## Related APIs

- `GetSavedSearches` — List all saved searches and search page definitions visible to the current user
- `CreateSavedSearch` — Create a new saved search or search page definition
- `UpdateSavedSearch` — Update an existing saved search or search page definition
