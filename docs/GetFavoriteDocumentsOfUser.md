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

Documents come back as the full `<document>` element. Since 9.0 it also carries `AIEnhanced` and
`AIExtractConfidence`. The first says which of the document's attributes infoRouter Connect
produced, as a set of bits - `0` when none did; the second how sure it was about the weakest value
it put in a property set, as a percentage. See [AIEnhanced](GetDocument.md#aienhanced) and
[AIExtractConfidence](GetDocument.md#aiextractconfidence).

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

Lists the documents one named user has marked as favourites, a page at a time.

```javascript
const root = await call('GetFavoriteDocumentsOfUser', {
  authenticationTicket: ticket,
  userName: 'jsmith',
  startingRow: 0,
  rowCount: 100
});

console.log(root.getAttribute('recordCount'), 'favourites in total');
```

`rowCount=0` means **every row**, not none, and the answer reports `rowCount` as the total rather than
the zero that was sent. The root carries `recordCount`, the total ignoring the paging, alongside the
`startingRow` and `rowCount` that were applied.

Asking about somebody other than yourself needs the **ListingAuditLogOfUser** administrative right.

## Notes

- Use `startingRow=0` and `rowCount=0` to retrieve all favorite documents.
- Results are returned in ascending order by document name.
- The `totalcount` attribute on the root element reflects the total number of favorite documents for the user, regardless of paging parameters.
- To retrieve favorite **folders** for a user, use [GetFavoriteFoldersOfUser](GetFavoriteFoldersOfUser.md).
- To retrieve the full favorites list (documents and folders combined) for the current user, use [GetFavorites](GetFavorites.md).
- Each `<document>` element includes a `UserViewStatus` integer attribute: `0` = never viewed, `1` = viewed but the published version has since changed, `2` = viewed the current published version. See `GetDocument` for the full attribute reference.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4000` | no user by that name |
| `4010` | the caller has no ticket; the list is about the signed-in user and there is not one |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

