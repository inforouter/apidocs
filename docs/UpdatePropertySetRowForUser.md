# UpdatePropertySetRowForUser API

Updates an existing property set row for the specified user.

## Endpoint

```
/srv.asmx/UpdatePropertySetRowForUser
```

## Methods

- **GET** `/srv.asmx/UpdatePropertySetRowForUser?authenticationTicket=...&userName=...&xmlpset=...`
- **POST** `/srv.asmx/UpdatePropertySetRowForUser` (form data)
- **SOAP** Action: `http://tempuri.org/UpdatePropertySetRowForUser`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `userName` | string | Yes | Username of the user whose property set row should be updated. |
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

**System administrator** or a user with permission to manage the target user's property sets.

## Example

### GET Request

```
GET /srv.asmx/UpdatePropertySetRowForUser
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &userName=jsmith
    &xmlpset=<psets><pset+name="HRDATA"><row+rownbr="1"+DEPARTMENT="Engineering"+LOCATION="HQ"/></pset></psets>
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/UpdatePropertySetRowForUser HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&userName=jsmith&xmlpset=<psets><pset name="HRDATA"><row rownbr="1" DEPARTMENT="Engineering" LOCATION="HQ"/></pset></psets>
```

## Notes

- The `rownbr` attribute is required and must match an existing row number for the property set on that user.
- Only fields listed as attributes in the `<row>` element are updated. Fields not mentioned are unchanged.
- The property set must have `AppliesToUsers = true` to be applicable to user objects.
- To add a new row for a user, use [AddPropertySetRowForUser](AddPropertySetRowForUser.md). To remove a row, use [DeletePropertySetRowForUser](DeletePropertySetRowForUser.md).
- To update a property set row on a document or folder, use [UpdatePropertySetRow](UpdatePropertySetRow.md).

## Related APIs

- [AddPropertySetRowForUser](AddPropertySetRowForUser.md) -" Add a new property set row to a user.
- [DeletePropertySetRowForUser](DeletePropertySetRowForUser.md) -" Delete a property set row from a user.
- [UpdatePropertySetRow](UpdatePropertySetRow.md) -" Update a property set row on a document or folder.
- [GetPropertySets](GetPropertySets.md) -" Get all applied property set rows for a document or folder.

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed -" invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Access Denied | Caller does not have permission to manage the target user's property sets. |
| User not found | No user with the specified `userName` exists. |
| Property set not found | The property set named in `xmlpset` does not exist or is not applied to the user. |
| Row not found | The specified `rownbr` does not exist for this property set on this user. |
