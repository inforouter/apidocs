# GetFavoriteDocumentsOfUser API

Returns a paged list of documents marked as favorites by the specified user.

## Endpoint

```
/srv.asmx/GetFavoriteDocumentsOfUser
```

## Methods

- **GET** `/srv.asmx/GetFavoriteDocumentsOfUser?AuthenticationTicket=...&userName=...&startingRow=...&rowCount=...`
- **POST** `/srv.asmx/GetFavoriteDocumentsOfUser` (form data)
- **SOAP** Action: `http://tempuri.org/GetFavoriteDocumentsOfUser`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from AuthenticateUser |
| `userName` | string | Yes | The username whose favorite documents are to be retrieved |
| `startingRow` | int | Yes | Zero-based row offset for paging. Pass `0` to start from the first result |
| `rowCount` | int | Yes | Number of rows to return (page size). Pass `0` to return all results |

## Required Permissions

- No additional permissions are required when querying the authenticated user's own favorites.
- To query another user's favorites, the caller must have the **ListingAuditLogOfUser** admin permission for the target user.

## Response

### Success Response

```xml
<root success="true" totalcount="15">
  <document id="101" name="Budget2024.xlsx" path="/Finance/Budget2024.xlsx" ... />
  <document id="205" name="ProjectPlan.pdf" path="/Projects/ProjectPlan.pdf" ... />
</root>
```

### Error Response

```xml
<root success="false" error="[901] Session expired or invalid ticket" />
```

## Example

### Request (GET)

```
GET /srv.asmx/GetFavoriteDocumentsOfUser?AuthenticationTicket=abc-123&userName=jsmith&startingRow=0&rowCount=25
```

### Request (POST)

```
POST /srv.asmx/GetFavoriteDocumentsOfUser HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=abc-123&userName=jsmith&startingRow=0&rowCount=25
```

### SOAP 1.1 Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetFavoriteDocumentsOfUser>
      <tns:AuthenticationTicket>abc-123</tns:AuthenticationTicket>
      <tns:userName>jsmith</tns:userName>
      <tns:startingRow>0</tns:startingRow>
      <tns:rowCount>25</tns:rowCount>
    </tns:GetFavoriteDocumentsOfUser>
  </soap:Body>
</soap:Envelope>
```

## Notes

- Use `startingRow=0` and `rowCount=0` to retrieve all favorite documents.
- Results are returned in ascending order by document name.
- The `totalcount` attribute on the root element reflects the total number of favorite documents for the user, regardless of paging parameters.
- To retrieve favorite **folders** for a user, use [GetFavoriteFoldersOfUser](GetFavoriteFoldersOfUser.md).
- To retrieve the full favorites list (documents and folders combined) for the current user, use [GetFavorites](GetFavorites.md).
