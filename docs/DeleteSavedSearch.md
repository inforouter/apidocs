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
<response success="true" error="" />
```

### Error

```xml
<response success="false" error="Access denied. Only search administrators can perform this operation." errorcode="4030" />
```

## Required Permissions

- User must be authenticated.
- **Personal entries**: the owner, or a member of the `[Search & Category Administrators]` role group.
- **System-wide entries**: members of the `[Search & Category Administrators]` role group.

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

| `errorcode` | Error (English) | Cause |
|-------------|-----------------|-------|
| `4010` | `[901]Session expired or Invalid ticket` | Missing, invalid or expired ticket |
| `4041` | `Search or category page cannot be found.` | No entry with `searchPageId` |
| `4030` | `Access denied. Only search administrators can perform this operation.` | Not the owner of a personal entry, or a system-wide entry, and not a search administrator |
| `4030` | `Advanced search page cannot be renamed or deleted.` | `searchPageId` is `1` |

## Notes

- The default system search page (ID 1, "Advanced Search") is protected and cannot be deleted by anyone.
- Use `GetSavedSearches` to discover the IDs of available entries.

## Related APIs

- `GetSavedSearches` — List all saved searches and search page definitions visible to the current user
- `CreateSavedSearch` — Create a new saved search or search page definition
- `UpdateSavedSearch` — Update an existing saved search or search page definition
