# AddPropertySetFieldOption API

Adds a static option value to a property set field. Only fields with a `COMBO BOX`, `LIST BOX`, or `RADIO BUTTON` control type support options.

## Endpoint

```
/srv.asmx/AddPropertySetFieldOption
```

## Methods

- **GET** `/srv.asmx/AddPropertySetFieldOption?authenticationTicket=...&PropertySetName=...&FieldName=...&OptionValue=...`
- **POST** `/srv.asmx/AddPropertySetFieldOption` (form data)
- **SOAP** Action: `http://tempuri.org/AddPropertySetFieldOption`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `PropertySetName` | string | Yes | Name of the property set that contains the field. |
| `FieldName` | string | Yes | Internal name of the field to add the option to. |
| `OptionValue` | string | Yes | The option value to add. Tabs and newlines are normalized to spaces. Trimmed before storage. Cannot be empty. Truncated silently if it exceeds the field's maximum length. |

## Response

### Success Response

```xml
<root success="true" />
```

### Error Response

```xml
<root success="false" error="Property option is already exists." />
```

## Required Permissions

The calling user must be a **System Administrator**.

Anonymous access is not permitted.

## Eligible Field Control Types

Options can only be added to fields with the following control types:

| Control Type | Supports Options |
|-------------|-----------------|
| `COMBO BOX` | Yes |
| `LIST BOX` | Yes |
| `RADIO BUTTON` | Yes |
| `TEXT BOX` | No |
| `CHECK BOX` | No |
| `LOOKUP` | No |

## Example

### GET Request

```
GET /srv.asmx/AddPropertySetFieldOption
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &PropertySetName=ProjectMetadata
    &FieldName=STATUS
    &OptionValue=In+Progress
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/AddPropertySetFieldOption HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&PropertySetName=ProjectMetadata&FieldName=STATUS&OptionValue=In+Progress
```

## Notes

- `OptionValue` is case-sensitive and must be unique within the field.
- Tab characters and line breaks in `OptionValue` are replaced with spaces before storage.
- If `OptionValue` exceeds the field's maximum character length, it is silently truncated (no error returned).
- Option values apply to static dropdown lists. For dynamic lookup fields (connected to an external database), use [SetPropertySetLookupFieldParametersForSQLServer](SetPropertySetLookupFieldParametersForSQLServer.md), [SetPropertySetLookupFieldParametersForMYSQL](SetPropertySetLookupFieldParametersForMYSQL.md), or [SetPropertySetLookupFieldParametersForORACLE](SetPropertySetLookupFieldParametersForORACLE.md) instead.
- To remove an option, use [DeletePropertySetFieldOption](DeletePropertySetFieldOption.md).
- To view existing options, use [GetPropertySetFieldOptions](GetPropertySetFieldOptions.md).

## Related APIs

- [AddPropertySetField](AddPropertySetField.md) -" Add a new field to a property set definition.
- [DeletePropertySetFieldOption](DeletePropertySetFieldOption.md) -" Remove an option value from a field.
- [GetPropertySetFieldOptions](GetPropertySetFieldOptions.md) -" Get all option values for a field.
- [GetPropertySetDefinition](GetPropertySetDefinition.md) -" Get the full definition of a property set including its fields.

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed -" invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Access Denied | Calling user is not a System Administrator. |
| Property set not found | No property set with the specified `PropertySetName` exists. |
| Field not found | No field with the specified `FieldName` exists in the property set. |
| Wrong control type | The field's control type does not support options (must be COMBO BOX, LIST BOX, or RADIO BUTTON). |
| Empty option value | `OptionValue` is empty after trimming. |
| Option already exists | An option with the same value already exists on this field. |
