# GetNextSearchPage1 API

Retrieves the next page of results from a previously prepared search, with the number of rows chosen for this call. It is [GetNextSearchPage](GetNextSearchPage.md) with one more parameter, `rowCount`; the response is the same.

## Endpoint

```
/srv.asmx/GetNextSearchPage1
```

## Methods

- **GET** `/srv.asmx/GetNextSearchPage1?authenticationTicket=...&withrules=...&withPropertySets=...&withSecurity=...&withOwner=...&withVersions=...&rowCount=...`
- **POST** `/srv.asmx/GetNextSearchPage1` (form data)
- **SOAP** Action: `http://tempuri.org/GetNextSearchPage1`

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

The same document as [GetNextSearchPage](GetNextSearchPage.md): `FirstPage`, `LastPage`, `from` and `to` on the root, and one `<folder>` or `<document>` element per row.

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
POST /srv.asmx/GetNextSearchPage1 HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&withrules=false&withPropertySets=false&withSecurity=false&withOwner=false&withVersions=false&rowCount=3
```

## Notes

- The page starts where the last page served ended, whatever size that page was. `from` and `to` say which rows came back.
- `rowCount` may change from one call to the next, and calls may be mixed with `GetNextSearchPage`, which always uses the system page size.
- After the last page (`LastPage="true"`), another call starts again from where that last page started.
- [GetPreviousSearchPage1](GetPreviousSearchPage1.md) steps back with a row count of its own.

- Each `<document>` carries the ISO reviewer (`ISOReviewById`, `ISOReviewByName`, `ISOReviewWorkflowName`); see the notes of [GetNextSearchPage](GetNextSearchPage.md).

## Related APIs

- [Search](Search.md) - Prepare the search these pages are read from
- [GetNextSearchPage](GetNextSearchPage.md) - The same call with the system page size
- [GetPreviousSearchPage1](GetPreviousSearchPage1.md) - Get the previous page with a row count for the call

## Error Codes

| `errorCode` | When |
|---:|---|
| `4000` | No search has been run in this session, or its result has expired |
| `4010` | `[901]` the ticket is expired or unknown |
