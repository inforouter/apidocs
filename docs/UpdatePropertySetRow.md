# UpdatePropertySetRow API

Updates an existing property set row on a document or folder identified by path. The path is
resolved as a document first; if no document is found, it is resolved as a folder.

**The update replaces the whole row rather than merging into it**: a field the document does
not name is written back empty, so send every field you want to keep. `rownbr` must name a
row that exists - `0` is refused, where `AddPropertySetRow` reads `0` as "a new row", and a
`rownbr` the object does not have is refused too. Until 9.0 the second one was accepted and changed
nothing, so the two ends of the same condition were answered differently.

## Endpoint

```
/srv.asmx/UpdatePropertySetRow
```

## Methods

- **GET** `/srv.asmx/UpdatePropertySetRow?authenticationTicket=...&Path=...&xmlpset=...`
- **POST** `/srv.asmx/UpdatePropertySetRow` (form data)
- **SOAP** Action: `http://tempuri.org/UpdatePropertySetRow`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the target document or folder. |
| `xmlpset` | string | Yes | XML string describing the property set rows to update. See format below. |

### `xmlpset` Format

```xml
<psets>
  <pset name="PROPERTYSETNAME">
    <row rownbr="1" FIELDNAME1="value1" FIELDNAME2="value2" />
  </pset>
</psets>
```

- `name`: Internal uppercase name of the property set.
- `rownbr`: **Required** -" identifies which existing row to update. Must be the 1-based row number of the row to update.
- Field attributes: Each field in the property set is specified as an attribute using its internal uppercase name.
- Multiple `<pset>` elements can be included to update rows in multiple property sets in one call.

## Response

### Success Response

```xml
<response success="true" error="" />
```

### Error Response

```xml
<response success="false" error="[901]Session expired or Invalid ticket" />
```

## Required Permissions

The calling user must have **MetaDataAddChange** permission on the target document or folder. For folders, the user must have **Change Properties** access.

## Example

### GET Request

```
GET /srv.asmx/UpdatePropertySetRow
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &Path=/MyLibrary/Projects/Proposal.pdf
    &xmlpset=<psets><pset+name="PROJECTMETA"><row+rownbr="1"+STATUS="Approved"+NOTES="Reviewed+by+mgmt"/></pset></psets>
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/UpdatePropertySetRow HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&Path=/MyLibrary/Projects/Proposal.pdf&xmlpset=<psets><pset name="PROJECTMETA"><row rownbr="1" STATUS="Approved" NOTES="Reviewed by mgmt"/></pset></psets>
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

Rewrites a row that is already on a document or a folder. Same document shape as
`AddPropertySetRow`, and the element names are not checked there either.

```javascript
await call('UpdatePropertySetRow', {
  authenticationTicket: ticket,
  Path: '/Finance/Projects/proposal.pdf',
  xmlpset: `
    <propertysets>
      <propertyset name="PROJECTMETADATA">
        <row rownbr="1" PROJECTCODE="PRJ-001" REGION="AMER" />
      </propertyset>
    </propertysets>`
});
```

- **The update replaces the whole row, it does not merge.** A field the document does not name is
  written back empty, so send every field you want to keep.
- **`rownbr` must name a row that exists.** `0` is refused `4000` "property set data row not found",
  where `AddPropertySetRow` reads `0` as "a new row". There is no way to say "the first row".
- **A `rownbr` that is not there is accepted and changes nothing.** So `0` fails and `99` succeeds,
  for the one condition "there is no such row".
- The answer on success carries **no `errorCode`**, the same as the other two row operations.

## Notes

- The `Path` resolves to a **document** first; if not found, it is resolved as a **folder**. If neither is found, an error is returned.
- The `rownbr` attribute is required for updates and must match an existing row number for the property set on that object.
- Only fields listed as attributes in the `<row>` element are updated. Fields not mentioned are unchanged.
- To add a new row, use [AddPropertySetRow](AddPropertySetRow.md). To remove a row, use [DeletePropertySetRow](DeletePropertySetRow.md).
- To update a property set row for a user, use [UpdatePropertySetRowForUser](UpdatePropertySetRowForUser.md).

## Related APIs

- [AddPropertySetRow](AddPropertySetRow.md) -" Add a new property set row to a document or folder.
- [DeletePropertySetRow](DeletePropertySetRow.md) -" Delete a property set row from a document or folder.
- [GetPropertySets](GetPropertySets.md) -" Get all applied property set rows for a document or folder.
- [UpdatePropertySetRowForUser](UpdatePropertySetRowForUser.md) -" Update a property set row for a user.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4041` | no document and no folder at `Path` |
| `4000` | no set by that name, `rownbr` is 0, `xmlpset` is not well formed, or there is no ticket at all |
| `4030` | the caller may not change the metadata of that document or folder |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
