# DeletePropertySetField API

Permanently deletes a field from a custom property set definition. This drops the column from the underlying database table, removes all stored values for that field across every document, folder, and user that had this property set applied, and deletes any associated lookup configuration. **This operation cannot be undone.**

## Endpoint

```
/srv.asmx/DeletePropertySetField
```

## Methods

- **GET** `/srv.asmx/DeletePropertySetField?authenticationTicket=...&PropertySetName=...&FieldName=...`
- **POST** `/srv.asmx/DeletePropertySetField` (form data)
- **SOAP** Action: `http://tempuri.org/DeletePropertySetField`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `PropertySetName` | string | Yes | Name of the property set that contains the field. |
| `FieldName` | string | Yes | Internal name of the field to delete. Case-insensitive (converted to uppercase internally). |

## Response

### Success Response

```xml
<response success="true" error="" />
```

### Error Response

```xml
<response success="false" error="Custom Property field not found." />
```

## Required Permissions

The calling user must be a **System Administrator**.

Anonymous access is not permitted.

## What Gets Deleted

| Item | Description |
|------|-------------|
| Field definition | The field record in `CATEGORYDETAILS`. |
| Field options | All static option values for this field (from `PROPERTYOPTIONS`). |
| Stored values | The column is `ALTER TABLE ... DROP COLUMN`-ed from `CUSTOM_<PropertySetName>`, permanently removing all values stored in this field. |
| Lookup config | Any lookup field XML definition file on disk for this field. |

## Constraints

- **System property sets** (attributes = 2) cannot be modified. Attempting to delete a field from one returns an error.
- `FieldName` must contain only letters (A-"Z), digits (0-"9), and underscores. Invalid names cause an exception.

## Example

### GET Request

```
GET /srv.asmx/DeletePropertySetField
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &PropertySetName=ProjectMetadata
    &FieldName=STATUS
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/DeletePropertySetField HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&PropertySetName=ProjectMetadata&FieldName=STATUS
```

## Notes

- `FieldName` is matched case-insensitively -" the system converts it to uppercase before looking it up.
- All previously stored values for this field across all objects are permanently lost when the column is dropped.
- To delete just the option values from a dropdown/list/radio field without removing the field itself, use [DeletePropertySetFieldOption](DeletePropertySetFieldOption.md).
- To delete the entire property set, use [DeletePropertySetDefinition](DeletePropertySetDefinition.md).

## Related APIs

- [AddPropertySetField](AddPropertySetField.md) -" Add a new field to a property set definition.
- [DeletePropertySetFieldOption](DeletePropertySetFieldOption.md) -" Remove a single option value from a field.
- [DeletePropertySetDefinition](DeletePropertySetDefinition.md) -" Delete the entire property set definition.
- [GetPropertySetDefinition](GetPropertySetDefinition.md) -" Get the full definition including all fields.

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed -" invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Access Denied | Calling user is not a System Administrator. |
| Property set not found | No property set with the specified `PropertySetName` exists. |
| System property set | Cannot modify a system-managed property set. |
| Field not found | No field with the specified `FieldName` exists in the property set. |
| Invalid field name | `FieldName` contains characters other than letters, digits, and underscores. |
