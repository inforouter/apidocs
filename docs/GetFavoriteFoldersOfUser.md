# GetFavoriteFoldersOfUser API

Returns a paged list of folders marked as favorites by the specified user.

## Endpoint

```
/srv.asmx/GetFavoriteFoldersOfUser
```

## Methods

- **GET** `/srv.asmx/GetFavoriteFoldersOfUser?AuthenticationTicket=...&userName=...&startingRow=...&rowCount=...`
- **POST** `/srv.asmx/GetFavoriteFoldersOfUser` (form data)
- **SOAP** Action: `http://tempuri.org/GetFavoriteFoldersOfUser`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from AuthenticateUser |
| `userName` | string | Yes | The username whose favorite folders are to be retrieved |
| `startingRow` | int | Yes | Zero-based row offset for paging. Pass `0` to start from the first result |
| `rowCount` | int | Yes | Number of rows to return (page size). Pass `0` to return all results |

## Required Permissions

- No additional permissions are required when querying the authenticated user's own favorites.
- To query another user's favorites, the caller must have the **ListingAuditLogOfUser** admin permission for the target user.

## Response

### Success Response

```xml
<root success="true" totalcount="8">
  <folder id="55" name="Annual Reports" path="/Finance/Annual Reports" ... />
  <folder id="78" name="Projects" path="/Engineering/Projects" ... />
</root>
```

### Error Response

```xml
<root success="false" error="[901] Session expired or invalid ticket" />
```

## Example

### Request (GET)

```
GET /srv.asmx/GetFavoriteFoldersOfUser?AuthenticationTicket=abc-123&userName=jsmith&startingRow=0&rowCount=25
```

### Request (POST)

```
POST /srv.asmx/GetFavoriteFoldersOfUser HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=abc-123&userName=jsmith&startingRow=0&rowCount=25
```

### SOAP 1.1 Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetFavoriteFoldersOfUser>
      <tns:AuthenticationTicket>abc-123</tns:AuthenticationTicket>
      <tns:userName>jsmith</tns:userName>
      <tns:startingRow>0</tns:startingRow>
      <tns:rowCount>25</tns:rowCount>
    </tns:GetFavoriteFoldersOfUser>
  </soap:Body>
</soap:Envelope>
```

## Notes

- Use `startingRow=0` and `rowCount=0` to retrieve all favorite folders.
- Results are returned in ascending order by folder name.
- The `totalcount` attribute on the root element reflects the total number of favorite folders for the user, regardless of paging parameters.
- To retrieve favorite **documents** for a user, use [GetFavoriteDocumentsOfUser](GetFavoriteDocumentsOfUser.md).
- To retrieve the full favorites list (documents and folders combined) for the current user, use [GetFavorites](GetFavorites.md).
