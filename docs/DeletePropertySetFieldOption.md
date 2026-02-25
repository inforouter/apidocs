# DeletePropertySetFieldOption API

Removes a static option value from a property set field. Only fields with a `COMBO BOX`, `LIST BOX`, or `RADIO BUTTON` control type have option values. This operation is idempotent -" if the option does not exist, the call succeeds without error.

## Endpoint

```
/srv.asmx/DeletePropertySetFieldOption
```

## Methods

- **GET** `/srv.asmx/DeletePropertySetFieldOption?authenticationTicket=...&PropertySetName=...&FieldName=...&OptionValue=...`
- **POST** `/srv.asmx/DeletePropertySetFieldOption` (form data)
- **SOAP** Action: `http://tempuri.org/DeletePropertySetFieldOption`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `PropertySetName` | string | Yes | Name of the property set that contains the field. |
| `FieldName` | string | Yes | Internal name of the field. |
| `OptionValue` | string | Yes | The exact option value to remove. Case-sensitive. |

## Response

### Success Response

```xml
<response success="true" error="" />
```

### Error Response

```xml
<response success="false" error="Access denied." />
```

## Required Permissions

The calling user must be a **System Administrator**.

Anonymous access is not permitted.

## Behavior

- The option is matched and deleted by exact value. The comparison is **case-sensitive**.
- If the specified option does not exist in the field, the operation still succeeds (idempotent).
- Removing an option does not affect any existing property set rows that already have this value stored -" those stored values are not changed or cleared.
- The property set and field must both exist; if either is not found, an error is returned.

## Example

### GET Request

```
GET /srv.asmx/DeletePropertySetFieldOption
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &PropertySetName=ProjectMetadata
    &FieldName=STATUS
    &OptionValue=In+Progress
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/DeletePropertySetFieldOption HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&PropertySetName=ProjectMetadata&FieldName=STATUS&OptionValue=In+Progress
```

## Notes

- `OptionValue` matching is **case-sensitive** -" `"active"` and `"Active"` are treated as different values.
- If the option does not exist, no error is returned (idempotent delete behavior).
- Existing property set row data that references this option value is **not modified** by this call. The option is only removed from the available list, not from stored data.
- To add an option, use [AddPropertySetFieldOption](AddPropertySetFieldOption.md).
- To view all current options for a field, use [GetPropertySetFieldOptions](GetPropertySetFieldOptions.md).

## Related APIs

- [AddPropertySetFieldOption](AddPropertySetFieldOption.md) -" Add a static option value to a field.
- [GetPropertySetFieldOptions](GetPropertySetFieldOptions.md) -" List all option values for a field.
- [DeletePropertySetField](DeletePropertySetField.md) -" Delete the entire field (and all its options and stored values).
- [GetPropertySetDefinition](GetPropertySetDefinition.md) -" Get the full property set definition including field definitions.

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed -" invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Access Denied | Calling user is not a System Administrator. |
| Property set not found | No property set with the specified `PropertySetName` exists. |
| Field not found | No field with the specified `FieldName` exists in the property set. |
