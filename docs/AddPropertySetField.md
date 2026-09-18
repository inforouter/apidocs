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
| `FieldLength` | integer | Yes | Maximum length of the field value. `BOOLEAN`, `NUMBER` and `DATE` each fix it - 1, 4 and 8 - and a different value is refused `4000`; send `0` to take the type's own. Until 9.0 whatever was sent was overwritten in silence, so a twenty digit `NUMBER` became a four digit one and the caller was told the call had worked. |
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
<response success="true" error="" errorCode="0" />
```

### Error Response

```xml
<response success="false" error="Property field already exists." />
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

Adds one field. `FieldType` is one of `BOOLEAN`, `NUMBER`, `CHAR` and `DATE`; `ControlType` one of
`TEXT BOX`, `COMBO BOX`, `LIST BOX`, `RADIO BUTTON`, `CHECK BOX` and `LOOKUP`. Both are upper cased
before they are checked, and so is `FieldName`; `FieldCaption` is kept as written.

```javascript
await call('AddPropertySetField', {
  authenticationTicket: ticket,
  PropertySetName: 'PROJECTMETADATA',
  FieldName: 'PROJECTCODE',
  FieldCaption: 'Project code',
  FieldType: 'CHAR',
  FieldLength: 32,
  isRequired: true,
  ControlSize: 20,
  ControlOrder: 1,
  ControlType: 'TEXT BOX'
});
```

**Only `CHAR` keeps the `FieldLength` and `ControlSize` you send.** The other three overwrite both,
whatever the caller asked for, and two of them overwrite `ControlType` as well:

| `FieldType` | `FieldLength` | `ControlSize` | `ControlType` |
|---|---:|---:|---|
| `CHAR` | as given, 1 to 255 | as given | as given |
| `NUMBER` | forced to 4 | forced to 10 | as given |
| `BOOLEAN` | forced to 1 | forced to 0 | forced to `CHECK BOX` |
| `DATE` | forced to 8 | forced to 12 | forced to `TEXT BOX` |

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

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4030` | the caller is not a system administrator - including a caller with no ticket at all |
| `4041` | no set by that name |
| `4090` | the set already has a field of that name |
| `4000` | `FieldType` or `ControlType` is not one of the accepted names, a `CHAR` `FieldLength` is outside 1 to 255, `FieldName` uses a character outside `0-9A-Z_`, `FieldName` is one of the six reserved names, or `FieldCaption` is empty |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
