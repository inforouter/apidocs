# DeletePropertySetRow API

Deletes a property set row from a document or folder. The target object is resolved by path -" the system checks for a document first, then a folder. The row to delete can be identified by its row number (`rownbr`) or by matching field values. Multiple rows and multiple property sets can be targeted in a single call.

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

A row can be identified in one of two ways:

**By row number** (preferred):

```xml
<row rownbr="2" />
```

**By field values** (when row number is unknown):

```xml
<row PROJECT_CODE="PRJ-2024-001" STATUS="Active" />
```

When `rownbr` is `0` or omitted, the system matches rows by comparing the provided field attribute values. When `rownbr` is specified and greater than `0`, the system deletes the row with that exact row number.

### Multiple Rows and Property Sets

```xml
<psets>
  <pset name="ProjectMetadata">
    <row rownbr="1" />
    <row rownbr="3" />
  </pset>
  <pset name="AuditInfo">
    <row AUDITOR="jsmith" />
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

## Notes

- The `Path` resolves to a **document** first; if no document is found, it is resolved as a **folder**.
- When identifying rows by field values instead of `rownbr`, all specified fields must match for the row to be deleted.
- To delete property set rows from a user account, use [DeletePropertySetRowForUser](DeletePropertySetRowForUser.md).
- To add a row, use [AddPropertySetRow](AddPropertySetRow.md). To update a row, use [UpdatePropertySetRow](UpdatePropertySetRow.md).

## Related APIs

- [AddPropertySetRow](AddPropertySetRow.md) -" Add a new property set row to a document or folder.
- [UpdatePropertySetRow](UpdatePropertySetRow.md) -" Update an existing property set row on a document or folder.
- [DeletePropertySetRowForUser](DeletePropertySetRowForUser.md) -" Delete a property set row from a user account.
- [GetPropertySets](GetPropertySets.md) -" Get the property sets applied to a document or folder.
- [GetPropertySetDefinition](GetPropertySetDefinition.md) -" Get the full property set definition including field names.

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed -" invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Access Denied | The calling user does not have Remove Metadata access on the target. |
| Path not found | No document or folder was found at the specified `Path`. |
| Property set not found | No property set with the specified name exists. |
| System property set | Cannot manually operate on a system-managed property set. |
| Required property set | Cannot delete the last row of a property set that is required by the document's document type. |
