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
<response success="true" error="" recordCount="8" startingRow="0" rowCount="2">
  <folder FolderID="1055" ParentID="1001" Name="Annual Reports" Path="\Finance\Annual Reports"
          Description="" CreationDate="2024-01-15T09:00:00.000Z"
          OwnerName="System Administrator" DomainId="1001"
          ClassificationLevel="NoMarkings" ClassificationLevelId="0" DeclassifyOn="" DowngradeOn=""
          RDDefId="0" RetentionDate="" DispositionDate="" CutoffDate="" />
  <folder FolderID="1078" ParentID="1070" Name="Projects" ...same attributes... />
</response>
```

A user with no favorite folders:

```xml
<response success="true" error="" recordCount="0" startingRow="0" rowCount="0" />
```

### `<response>` attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `recordCount` | integer | Total number of favorite folders of the user, regardless of paging. |
| `startingRow` | integer | The `startingRow` sent in the request, echoed back. |
| `rowCount` | integer | Number of `<folder>` elements in this response; may be less than the `rowCount` requested. |

### `<folder>` element

Each favorite folder is a `<folder>` element as [GetFolder](GetFolder.md) returns it with all its flags
off - see its [attribute table](GetFolder.md#folder-attributes). There are no child elements.

### Error Response

```xml
<response success="false" error="Session expired or invalid ticket" errorCode="4010" />
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

```javascript
const root = await call('GetFavoriteFoldersOfUser', {
  AuthenticationTicket: ticket,
  userName: 'jsmith',
  startingRow: 0,
  rowCount: 25
});

const total = Number(root.getAttribute('recordCount'));
for (const folder of root.querySelectorAll(':scope > folder')) {
  console.log(folder.getAttribute('FolderID'), folder.getAttribute('Name'), folder.getAttribute('Path'));
}
```

## Notes

- Use `startingRow=0` and `rowCount=0` to retrieve all favorite folders.
- Results are returned in ascending order by folder name.
- The `recordCount` attribute on the root element reflects the total number of favorite folders for the user, regardless of paging parameters.
- To retrieve favorite **documents** for a user, use [GetFavoriteDocumentsOfUser](GetFavoriteDocumentsOfUser.md).
- To retrieve the full favorites list (documents and folders combined) for the current user, use [GetFavorites](GetFavorites.md).

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4000` | no user by that name - the same code [GetSubscribedFoldersByUser](GetSubscribedFoldersByUser.md) answers, as both run the same server method |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

