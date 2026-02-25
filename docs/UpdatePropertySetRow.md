# UpdatePropertySetRow API

Updates an existing property set row on a document or folder identified by path. The path is resolved as a document first; if no document is found, it is resolved as a folder.

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

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed -" invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Access Denied | Caller does not have MetaDataAddChange permission on the target document or folder. |
| Path not found | No document or folder was found at the specified `Path`. |
| Property set not found | The property set named in `xmlpset` does not exist or is not applied to the object. |
| Row not found | The specified `rownbr` does not exist for this property set on this object. |
