# DeletePropertySetRow API

Deletes a property set row from a document or folder. The target object is resolved by path -" the system checks for a document first, then a folder. The row to delete is identified by its row number (`rownbr`); omitting it removes **every** row of that property set from the object. Multiple rows and multiple property sets can be targeted in a single call.

## Endpoint

```
/srv.asmx/DeletePropertySetRow
```

## Methods

- **GET** `/srv.asmx/DeletePropertySetRow?authenticationTicket=...&Path=...&xmlpset=...`
- **POST** `/srv.asmx/DeletePropertySetRow` (form data)
- **SOAP** Action: `http://tempuri.org/DeletePropertySetRow`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the target document or folder. |
| `xmlpset` | string | Yes | XML identifying the property set rows to delete. See **xmlpset Format** below. |

## xmlpset Format

```xml
<psets>
  <pset name="PropertySetName">
    <row rownbr="N" />
  </pset>
</psets>
```

### Row Identification

A row is identified by its row number:

```xml
<row rownbr="2" />
```

To remove every row of the property set from the object, omit `rownbr` (or give it as `0`):

```xml
<row />
```

When `rownbr` is specified and greater than `0`, the system deletes the row with that exact row number. When it is `0` or omitted, **all** rows of that property set are removed from the object -" field attributes are not used to select rows on delete, whatever else the row element carries. The one exception is the property set the document's document type requires: that cannot be emptied, and the call reports it instead.

### Multiple Rows and Property Sets

```xml
<psets>
  <pset name="ProjectMetadata">
    <row rownbr="1" />
    <row rownbr="3" />
  </pset>
  <pset name="AuditInfo">
    <row />
  </pset>
</psets>
```

## Response

### Success Response

```xml
<response success="true" error="" />
```

### Error Response (single error)

```xml
<response success="false" error="Access denied." />
```

### Error Response (multiple errors)

```xml
<response success="false" error="[log]">
  <item name="document.pdf (D123)" error="Required custom property for the document type cannot be deleted." />
</response>
```

> **Note**: This API uses `<response>` as the root element, not `<root>`.

## Required Permissions

### For documents

The calling user must have the **Remove Metadata** access right on the target document (infoRouter action: `MetaDataRemove`).

### For folders

The calling user must have the **Change Properties** access right on the target folder.

Anonymous access is not permitted.

## Constraints

- **Required property set protection**: If the document has a document type with a required property set, the last remaining row of that property set cannot be deleted. At least one row must remain.
- **System property sets** cannot be operated on manually.
- After successfully deleting a row from a document, infoRouter sends an `ON_UPDATE` notification to all document subscribers.

## Example

### GET Request -" delete by row number

```
GET /srv.asmx/DeletePropertySetRow
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &Path=/MyLibrary/Projects/Proposal.pdf
    &xmlpset=%3Cpsets%3E%3Cpset+name%3D%22ProjectMetadata%22%3E%3Crow+rownbr%3D%221%22%2F%3E%3C%2Fpset%3E%3C%2Fpsets%3E
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/DeletePropertySetRow HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&Path=/MyLibrary/Projects/Proposal.pdf&xmlpset=<psets><pset name="ProjectMetadata"><row rownbr="1"/></pset></psets>
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

Removes rows of a property set from a document or a folder. Same document shape as
`AddPropertySetRow`; only `name` and `rownbr` are read.

```javascript
// One row.
await call('DeletePropertySetRow', {
  authenticationTicket: ticket,
  Path: '/Finance/Projects/proposal.pdf',
  xmlpset: '<propertysets><propertyset name="PROJECTMETADATA"><row rownbr="2" /></propertyset></propertysets>'
});

// Every row of that set: leave rownbr out.
await call('DeletePropertySetRow', {
  authenticationTicket: ticket,
  Path: '/Finance/Projects/proposal.pdf',
  xmlpset: '<propertysets><propertyset name="PROJECTMETADATA"><row /></propertyset></propertysets>'
});
```

A `rownbr` that is not there is **accepted** and removes nothing, so the result does not tell you
whether there was a row. The answer on success carries no `errorCode`, the same as
`AddPropertySetRow`.

## Notes

- The `Path` resolves to a **document** first; if no document is found, it is resolved as a **folder**.
- Field attributes on a `<row>` element are ignored on delete: the row number alone selects the row, and without one every row of that property set is removed.
- To delete property set rows from a user account, use [DeletePropertySetRowForUser](DeletePropertySetRowForUser.md).
- To add a row, use [AddPropertySetRow](AddPropertySetRow.md). To update a row, use [UpdatePropertySetRow](UpdatePropertySetRow.md).

## Related APIs

- [AddPropertySetRow](AddPropertySetRow.md) -" Add a new property set row to a document or folder.
- [UpdatePropertySetRow](UpdatePropertySetRow.md) -" Update an existing property set row on a document or folder.
- [DeletePropertySetRowForUser](DeletePropertySetRowForUser.md) -" Delete a property set row from a user account.
- [GetPropertySets](GetPropertySets.md) -" Get the property sets applied to a document or folder.
- [GetPropertySetDefinition](GetPropertySetDefinition.md) -" Get the full property set definition including field names.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4041` | no document and no folder at `Path` |
| `4000` | no set by that name, or `xmlpset` is not well formed |
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4030` | the caller may not change the metadata of that document or folder |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
