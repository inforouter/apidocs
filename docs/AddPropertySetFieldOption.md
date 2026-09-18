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
<response success="true" error="" errorCode="0" />
```

### Error Response

```xml
<response success="false" error="Property option is already exists." />
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

Adds one value to the list a field offers. Only a `COMBO BOX`, a `LIST BOX` and a `RADIO BUTTON`
have options; a `TEXT BOX` or a `CHECK BOX` is refused.

```javascript
for (const region of ['EMEA', 'APAC', 'AMER']) {
  await call('AddPropertySetFieldOption', {
    authenticationTicket: ticket,
    PropertySetName: 'PROJECTMETADATA',
    FieldName: 'REGION',
    OptionValue: region
  });
}
```

The options come back under the field in `GetPropertySetDefinition`, as
`<options><option value="EMEA" /></options>`.

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

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4030` | the caller is not a system administrator - including a caller with no ticket at all |
| `4041` | no set by that name, or the set has no such field |
| `4090` | the field already offers that value |
| `4000` | the field's control type does not take options |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
