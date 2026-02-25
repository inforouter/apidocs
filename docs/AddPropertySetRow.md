# AddPropertySetRow API

Adds a new property set row to a document or folder. The target object is resolved by path -" the system first checks if the path refers to a document, then a folder. Multiple property sets and multiple rows per property set can be submitted in a single call.

## Endpoint

```
/srv.asmx/AddPropertySetRow
```

## Methods

- **GET** `/srv.asmx/AddPropertySetRow?authenticationTicket=...&Path=...&xmlpset=...`
- **POST** `/srv.asmx/AddPropertySetRow` (form data)
- **SOAP** Action: `http://tempuri.org/AddPropertySetRow`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the target document or folder (e.g., `/MyLibrary/Projects/spec.pdf` or `/MyLibrary/Projects`). |
| `xmlpset` | string | Yes | XML document describing the property set rows to add. See **xmlpset Format** below. |

## xmlpset Format

```xml
<psets>
  <pset name="PropertySetName">
    <row FIELDNAME1="value1" FIELDNAME2="value2" />
  </pset>
</psets>
```

### XML Structure Rules

- The root element must be `<psets>`.
- Each `<pset>` child element represents one property set. The `name` attribute specifies the property set name.
- Each `<row>` child element inside a `<pset>` represents one row to add. Field names are specified as XML attributes of the `<row>` element.
- Field names are **case-insensitive** during lookup but are stored in uppercase.
- An optional `rownbr` attribute on `<row>` specifies the row number to assign. If omitted or `0`, the system assigns the next available row number automatically.
- Multiple `<pset>` elements may be included in a single call.
- Multiple `<row>` elements may be included in a single `<pset>` for multi-row property sets.

### Example

```xml
<psets>
  <pset name="ProjectMetadata">
    <row PROJECT_CODE="PRJ-2024-001" STATUS="Active" NOTES="Initial entry" />
  </pset>
</psets>
```

### Example with explicit row number

```xml
<psets>
  <pset name="ProjectMetadata">
    <row rownbr="3" PROJECT_CODE="PRJ-2024-003" STATUS="Draft" />
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
  <item name="document.pdf (D123)" error="Access denied." />
  <item name="ProjectMetadata" error="Property set not found." />
</response>
```

> **Note**: This API uses `<response>` as the root element, not `<root>`.

## Required Permissions

### For documents

The calling user must have the **Change Metadata** access right on the target document (infoRouter action: `MetaDataAddChange`).

### For folders

The calling user must have the **Change Metadata** access right on the target folder.

Anonymous access is not permitted.

## Constraints

- **System property sets** (managed internally by infoRouter) cannot be applied or removed manually. Attempting to do so returns an error.
- The property set must be defined in the same infoRouter library as the target document or folder.
- Only fields defined in the property set definition are accepted. Unrecognized field names are ignored.
- After successfully adding a row to a document, infoRouter sends an `ON_UPDATE` notification to all document subscribers.

## Example

### GET Request

```
GET /srv.asmx/AddPropertySetRow
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &Path=/MyLibrary/Projects/Proposal.pdf
    &xmlpset=%3Cpsets%3E%3Cpset+name%3D%22ProjectMetadata%22%3E%3Crow+PROJECT_CODE%3D%22PRJ-001%22+STATUS%3D%22Draft%22%2F%3E%3C%2Fpset%3E%3C%2Fpsets%3E
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/AddPropertySetRow HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&Path=/MyLibrary/Projects/Proposal.pdf&xmlpset=<psets><pset name="ProjectMetadata"><row PROJECT_CODE="PRJ-001" STATUS="Draft"/></pset></psets>
```

## Notes

- The `Path` parameter resolves to a **document** first; if no document is found at that path, it is resolved as a **folder**.
- Field names inside `<row>` attributes are not case-sensitive but are matched against the uppercase field names stored in the property set definition.
- Pipe characters (`|`) in field values are automatically escaped internally and do not need special handling in the XML.
- For property sets that allow multiple rows, include multiple `<row>` elements within the same `<pset>`, or make multiple API calls.
- To update an existing row, use [UpdatePropertySetRow](UpdatePropertySetRow.md).
- To delete a row, use [DeletePropertySetRow](DeletePropertySetRow.md).
- To add property set rows to a user account, use [AddPropertySetRowForUser](AddPropertySetRowForUser.md).

## Related APIs

- [UpdatePropertySetRow](UpdatePropertySetRow.md) -" Update an existing property set row on a document or folder.
- [DeletePropertySetRow](DeletePropertySetRow.md) -" Remove a property set row from a document or folder.
- [AddPropertySetRowForUser](AddPropertySetRowForUser.md) -" Add a property set row to a user account.
- [GetPropertySetDefinition](GetPropertySetDefinition.md) -" Get the full definition of a property set including its fields.
- [GetPropertySets](GetPropertySets.md) -" Get the property sets applied to a document or folder.

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed -" invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Access Denied | The calling user does not have Change Metadata access on the target. |
| Path not found | No document or folder was found at the specified `Path`. |
| Property set not found | No property set with the specified name exists. |
| System property set | Cannot manually apply a system-managed property set. |
