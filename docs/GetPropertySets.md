# GetPropertySets API

Returns all property set rows that have been applied to a document or folder identified by path. The path is resolved as a document first; if no document is found, it is resolved as a folder. Each applied property set is returned with all its data rows and audit information.

## Endpoint

```
/srv.asmx/GetPropertySets
```

## Methods

- **GET** `/srv.asmx/GetPropertySets?authenticationTicket=...&Path=...`
- **POST** `/srv.asmx/GetPropertySets` (form data)
- **SOAP** Action: `http://tempuri.org/GetPropertySets`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the target document or folder. |

## Response

### Success Response

```xml
<response success="true" error="">
  <Propertysets>
    <propertyset Name="PROJECTMETADATA">
      <propertyrow RowNbr="1"
                   PROJECT_CODE="PRJ-2024-001"
                   STATUS="Active"
                   NOTES="Initial entry">
        <Log AppliedBy="jsmith" DateApplied="2024-03-15 14:32" />
      </propertyrow>
      <propertyrow RowNbr="2"
                   PROJECT_CODE="PRJ-2024-002"
                   STATUS="Draft"
                   NOTES="">
        <Log AppliedBy="admin" DateApplied="2024-03-16 09:10" />
      </propertyrow>
    </propertyset>
    <propertyset Name="AUDITINFO">
      <propertyrow RowNbr="1"
                   AUDITOR="bjones"
                   AUDIT_DATE="2024-01-01">
        <Log AppliedBy="admin" DateApplied="2024-01-05 08:00" />
      </propertyrow>
    </propertyset>
  </Propertysets>
</response>
```

### No Applied Property Sets

If the document or folder has no property set rows applied, the `<Propertysets>` element is empty:

```xml
<response success="true" error="">
  <Propertysets />
</response>
```

### Error Response

```xml
<response success="false" error="[901]Session expired or Invalid ticket" />
```

## Response Structure

### `<Propertysets>`
Container element listing all property sets applied to the object.

### `<propertyset>`
| Attribute | Description |
|-----------|-------------|
| `Name` | Internal uppercase name of the property set (e.g., `PROJECTMETADATA`). |

### `<propertyrow>`
| Attribute | Description |
|-----------|-------------|
| `RowNbr` | Row number within this property set for this object. |
| `FIELDNAME` | Each field in the property set is an attribute. Names are uppercase. Values are strings; empty string if no value is stored. |

### `<Log>` (child of `<propertyrow>`)
| Attribute | Description |
|-----------|-------------|
| `AppliedBy` | Username of the user who last saved this row. |
| `DateApplied` | Date and time the row was last saved, in `YYYY-MM-DD HH:mm` UTC format. |

## Required Permissions

The calling user must have at least **read** access to the target document or folder.

Anonymous access is supported if the document or folder is publicly accessible.

## Example

### GET Request

```
GET /srv.asmx/GetPropertySets
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &Path=/MyLibrary/Projects/Proposal.pdf
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/GetPropertySets HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&Path=/MyLibrary/Projects/Proposal.pdf
```

## Notes

- The `Path` resolves to a **document** first; if not found, it is resolved as a **folder**. If neither is found, an error is returned.
- Only property sets that have actually been applied (have at least one row) are included in the response.
- Field values are returned as attribute strings. Date and number values are returned in their stored string representation.
- To add a property set row, use [AddPropertySetRow](AddPropertySetRow.md). To update one, use [UpdatePropertySetRow](UpdatePropertySetRow.md). To remove one, use [DeletePropertySetRow](DeletePropertySetRow.md).

## Related APIs

- [AddPropertySetRow](AddPropertySetRow.md) -" Add a property set row to a document or folder.
- [UpdatePropertySetRow](UpdatePropertySetRow.md) -" Update an existing property set row.
- [DeletePropertySetRow](DeletePropertySetRow.md) -" Delete a property set row from a document or folder.
- [GetPropertySetDefinition](GetPropertySetDefinition.md) -" Get the field definitions of a property set.
- [GetPropertySetDefinitions1](GetPropertySetDefinitions1.md) -" List property sets filtered by library and object type.

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed -" invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Path not found | No document or folder was found at the specified `Path`. |
