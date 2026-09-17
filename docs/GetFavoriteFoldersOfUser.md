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

> **This operation does not work.** Every call fails with `5000` and the text
> `System.ArgumentException: Invalid FolderListType for folder retrieval (Parameter 'folderListType')`.
> The controller asks the shared folder-listing method for the `MyFavorites` list, and that method
> handles only `Subscriptions` and `MyDocuments` - anything else falls into its default branch and
> throws before a query is ever run. No parameter combination avoids it.
>
> Use [GetFavorites](GetFavorites.md) instead: it answers for the calling user and returns the
> favourite folders as `<folder>` elements alongside the documents.

```javascript
// What this page would have shown, done the way that works:
const root = await call('GetFavorites', {
  authenticationTicket: ticket,
  withrules: false, withpropertysets: false, withsecurity: false,
  withOwner: false, withVersions: false
});

const favouriteFolders = [...root.querySelectorAll(':scope > folder')];
```

## Notes

- Use `startingRow=0` and `rowCount=0` to retrieve all favorite folders.
- Results are returned in ascending order by folder name.
- The `totalcount` attribute on the root element reflects the total number of favorite folders for the user, regardless of paging parameters.
- To retrieve favorite **documents** for a user, use [GetFavoriteDocumentsOfUser](GetFavoriteDocumentsOfUser.md).
- To retrieve the full favorites list (documents and folders combined) for the current user, use [GetFavorites](GetFavorites.md).

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `5000` | every call; see the note above |

