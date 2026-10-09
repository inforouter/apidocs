# GetPreviousSearchPage1 API

Retrieves the previous page of results from a previously prepared search, with the number of rows chosen for this call. It is [GetPreviousSearchPage](GetPreviousSearchPage.md) with one more parameter, `rowCount`; the response is the same.

## Endpoint

```
/srv.asmx/GetPreviousSearchPage1
```

## Methods

- **GET** `/srv.asmx/GetPreviousSearchPage1?authenticationTicket=...&withrules=...&withPropertySets=...&withSecurity=...&withOwner=...&withVersions=...&rowCount=...`
- **POST** `/srv.asmx/GetPreviousSearchPage1` (form data)
- **SOAP** Action: `http://tempuri.org/GetPreviousSearchPage1`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. Must belong to the same session that executed the `Search` call. |
| `withrules` | bool | Yes | `true` to include folder rules (`<Rules>` child element) in each folder result. |
| `withPropertySets` | bool | Yes | `true` to include applied custom property set data in each result. |
| `withSecurity` | bool | Yes | `true` to include the access control list (`<AccessList>` child element) in each result. |
| `withOwner` | bool | Yes | `true` to include owner user information in each result. |
| `withVersions` | bool | Yes | `true` to include document version history in each document result. |
| `rowCount` | int | Yes | How many rows this page holds. `0` or less uses the system **Search Page Size** setting. More than `500` is served as `500`. |

## Response

The same document as [GetPreviousSearchPage](GetPreviousSearchPage.md): `FirstPage`, `LastPage`, `from` and `to` on the root, and one `<folder>` or `<document>` element per row.

### Success Response

```xml
<response success="true" error="" FirstPage="true" from="1" to="3" LastPage="false">
  <document DocumentID="13620" Name="page1.htm" ... />
  <document DocumentID="13621" Name="page2.htm" ... />
  <document DocumentID="13622" Name="page3.htm" ... />
</response>
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

## Required Permissions

Any authenticated user. Results are filtered to the items the caller may read.

## Example

### Request (POST)

```
POST /srv.asmx/GetPreviousSearchPage1 HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&withrules=false&withPropertySets=false&withSecurity=false&withOwner=false&withVersions=false&rowCount=3
```

## Notes

- The page ends where the last page served began, and holds `rowCount` rows before that. After rows 4-5, a call with `rowCount=3` returns rows 1-3.
- When fewer than `rowCount` rows lie before the last page served, the page starts at row 1 and may overlap it. On the first page, the first page is returned again.
- `rowCount` may change from one call to the next, and calls may be mixed with `GetPreviousSearchPage`, which always uses the system page size.

- Each `<document>` carries the ISO reviewer (`ISOReviewById`, `ISOReviewByName`, `ISOReviewWorkflowName`); see the notes of [GetNextSearchPage](GetNextSearchPage.md).

## Related APIs

- [Search](Search.md) - Prepare the search these pages are read from
- [GetPreviousSearchPage](GetPreviousSearchPage.md) - The same call with the system page size
- [GetNextSearchPage1](GetNextSearchPage1.md) - Get the next page with a row count for the call

## Error Codes

| `errorCode` | When |
|---:|---|
| `4000` | No search has been run in this session, or its result has expired |
| `4010` | `[901]` the ticket is expired or unknown |
