# AddPropertySetField API

Adds a new field to an existing custom property set definition. The field name is stored in uppercase and must be unique within the property set. Fields cannot be added to system-managed property sets.

## Endpoint

```
/srv.asmx/AddPropertySetField
```

## Methods

- **GET** `/srv.asmx/AddPropertySetField?authenticationTicket=...&PropertySetName=...&FieldName=...&FieldCaption=...&FieldType=...&FieldLength=...&isRequired=...&ControlSize=...&ControlOrder=...&ControlType=...`
- **POST** `/srv.asmx/AddPropertySetField` (form data)
- **SOAP** Action: `http://tempuri.org/AddPropertySetField`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `PropertySetName` | string | Yes | Name of the property set to add the field to. |
| `FieldName` | string | Yes | Internal name for the field. Alphanumeric and underscore characters only (auto-converted to uppercase). Must not be a reserved name. |
| `FieldCaption` | string | Yes | Display label shown to users in the UI. |
| `FieldType` | string | Yes | Data type of the field. See **Field Types** table below. |
| `FieldLength` | integer | Yes | Maximum length of the field value. For `BOOLEAN`, `NUMBER`, and `DATE` types, this is set automatically and the provided value is ignored. |
| `isRequired` | boolean | Yes | `true` if the field must be filled in; `false` if optional. |
| `ControlSize` | integer | Yes | Display width of the input control in the UI. For `BOOLEAN` and `DATE` types, this is set automatically. |
| `ControlOrder` | integer | Yes | Display order position of the field within the property set form. |
| `ControlType` | string | Yes | UI control type. See **Control Types** table below. For `BOOLEAN` type, forced to `CHECK BOX`; for `DATE`, forced to `TEXT BOX`. |

### Field Types

| Value | Description | FieldLength | ControlSize |
|-------|-------------|-------------|-------------|
| `BOOLEAN` | True/false checkbox | 1 (auto) | 0 (auto) |
| `NUMBER` | Integer number | 4 (auto) | 10 (auto) |
| `CHAR` | Text string | 1-"255 (required) | Specify |
| `DATE` | Date value | 8 (auto) | 12 (auto) |

### Control Types

| Value | Description |
|-------|-------------|
| `TEXT BOX` | Free-text input field |
| `COMBO BOX` | Dropdown with typed input allowed |
| `LIST BOX` | Scrollable selection list |
| `RADIO BUTTON` | Single-select radio buttons |
| `CHECK BOX` | Checkbox (required for `BOOLEAN` type) |
| `LOOKUP` | Value looked up from a database or static list |

### Reserved Field Names

The following names cannot be used as `FieldName`:

`OBJECTID`, `OBJECTTYPE`, `ROWNBR`, `CPSETSAVEDBYID`, `CPSETSAVEDBYNAME`, `CPSETSAVEDDATE`

## Response

### Success Response

```xml
<root success="true" />
```

### Error Response

```xml
<root success="false" error="Property field already exists." />
```

## Required Permissions

The calling user must be a **System Administrator**.

Anonymous access is not permitted.

## Example

### GET Request -" adding a required text field

```
GET /srv.asmx/AddPropertySetField
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &PropertySetName=ProjectMetadata
    &FieldName=PROJECT_CODE
    &FieldCaption=Project+Code
    &FieldType=CHAR
    &FieldLength=20
    &isRequired=true
    &ControlSize=20
    &ControlOrder=1
    &ControlType=TEXT+BOX
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/AddPropertySetField HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&PropertySetName=ProjectMetadata&FieldName=PROJECT_CODE&FieldCaption=Project+Code&FieldType=CHAR&FieldLength=20&isRequired=true&ControlSize=20&ControlOrder=1&ControlType=TEXT+BOX
```

## Notes

- `FieldName` is automatically converted to uppercase and trimmed before storage.
- `FieldName` must only contain letters (A-"Z), digits (0-"9), and underscores (`_`). Special characters and spaces are not allowed.
- `FieldName` must contain at least one letter or digit.
- For `COMBO BOX`, `LIST BOX`, `RADIO BUTTON`, and `LOOKUP` control types, add valid option values after creating the field using [AddPropertySetFieldOption](AddPropertySetFieldOption.md).
- Fields cannot be added to system property sets (built-in sets managed by infoRouter).

## Related APIs

- [CreatePropertySetDefinition](CreatePropertySetDefinition.md) -" Create a new property set definition.
- [AddPropertySetFieldOption](AddPropertySetFieldOption.md) -" Add an option value to a dropdown/list field.
- [DeletePropertySetField](DeletePropertySetField.md) -" Delete a field from a property set definition.
- [GetPropertySetDefinition](GetPropertySetDefinition.md) -" Get the full definition of a property set including its fields.
- [UpdatePropertySetDefinition](UpdatePropertySetDefinition.md) -" Update a property set's name or description.

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed -" invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Access Denied | Calling user is not a System Administrator. |
| Property set not found | No property set with the specified `PropertySetName` exists. |
| System property set | Cannot modify a system-managed property set. |
| Invalid field name | `FieldName` is empty, contains invalid characters, or is a reserved name. |
| Invalid field type | `FieldType` is not `BOOLEAN`, `NUMBER`, `CHAR`, or `DATE`. |
| Invalid field length | `FieldType` is `CHAR` and `FieldLength` is not between 1 and 255. |
| Invalid control type | `ControlType` is not one of the six valid values. |
| Field already exists | A field with the specified `FieldName` already exists in the property set. |
