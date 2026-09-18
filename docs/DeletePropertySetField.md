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

Removes a field from the definition and its column from the table behind it, so every row that
carried a value for it loses that value. The rows themselves stay.

```javascript
await call('DeletePropertySetField', {
  authenticationTicket: ticket,
  PropertySetName: 'PROJECTMETADATA',
  FieldName: 'REGION'
});
```

There is no confirmation step and no undo.

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

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4030` | the caller is not a system administrator - including a caller with no ticket at all |
| `4041` | no set by that name, or the set has no such field |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
