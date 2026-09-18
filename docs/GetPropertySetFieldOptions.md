# GetPropertySetFieldOptions API

Returns the available option values for a property set field. For static fields (`COMBO BOX`,
`LIST BOX`, `RADIO BUTTON`), returns the list of stored option values, sorted alphabetically
rather than in the order they were added. For `LOOKUP` fields, executes the configured
external database query and returns the live results.

**`OptionFilter` only reaches a `LOOKUP` query.** A non-empty filter on a field of any other
control type is refused `4000`; until 9.0 it was accepted and did nothing, so a `COMBO BOX` returned
all of its values whatever the filter said.

A field whose control type has no options - a `TEXT BOX` or a `CHECK BOX` - answers a
successful empty `<options />`, although adding an option to one of those is refused `4000`.

## Endpoint

```
/srv.asmx/GetPropertySetFieldOptions
```

## Methods

- **GET** `/srv.asmx/GetPropertySetFieldOptions?authenticationTicket=...&PropertySetName=...&PropertyFieldName=...&OptionFilter=...`
- **POST** `/srv.asmx/GetPropertySetFieldOptions` (form data)
- **SOAP** Action: `http://tempuri.org/GetPropertySetFieldOptions`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `PropertySetName` | string | Yes | Internal name of the property set. |
| `PropertyFieldName` | string | Yes | Internal name of the field whose options to retrieve. |
| `OptionFilter` | string | No | Filter string to narrow results. Used as a SQL `WHERE` clause parameter for `LOOKUP` fields. Refused `4000` on a field of any other control type, which cannot use one. |

## Response

### Static Field Response (COMBO BOX, LIST BOX, RADIO BUTTON)

Options are returned alphabetically sorted by value.

```xml
<response success="true" error="">
  <options>
    <option value="Active" />
    <option value="Draft" />
    <option value="In Progress" />
    <option value="Rejected" />
  </options>
</response>
```

### LOOKUP Field Response

For external database lookup fields, columns from the SQL query result are returned as attributes. The column names in the result set become attribute names on each `<option>` element.

```xml
<response success="true" error="">
  <options>
    <option CategoryName="Engineering" CategoryCode="ENG" />
    <option CategoryName="Finance" CategoryCode="FIN" />
    <option CategoryName="Legal" CategoryCode="LEG" />
  </options>
</response>
```

### Error Response

```xml
<response success="false" error="Custom Property field not found." />
```

## Required Permissions

Any authenticated user may call this API.

Anonymous callers are **blocked from accessing private property sets** (`PrivatePropertySet = TRUE`).

## Eligible Field Control Types

| Control Type | Supports GetPropertySetFieldOptions |
|-------------|-------------------------------------|
| `COMBO BOX` | Yes -" returns static option list |
| `LIST BOX` | Yes -" returns static option list |
| `RADIO BUTTON` | Yes -" returns static option list |
| `LOOKUP` | Yes -" executes the configured database query |
| `TEXT BOX` | Yes -" returns empty `<options/>` (no options defined) |
| `CHECK BOX` | Yes -" returns empty `<options/>` (no options defined) |

## Example

### GET Request -" static field

```
GET /srv.asmx/GetPropertySetFieldOptions
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &PropertySetName=ProjectMetadata
    &PropertyFieldName=STATUS
HTTP/1.1
Host: yourserver
```

### GET Request -" lookup field with filter

```
GET /srv.asmx/GetPropertySetFieldOptions
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &PropertySetName=ProjectMetadata
    &PropertyFieldName=CATEGORY
    &OptionFilter=Eng
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/GetPropertySetFieldOptions HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&PropertySetName=ProjectMetadata&PropertyFieldName=STATUS&OptionFilter=
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

Reads the values a field offers: the stored list for a `COMBO BOX`, a `LIST BOX` or a
`RADIO BUTTON`, and the live result of the configured query for a `LOOKUP`.

```javascript
const root = await call('GetPropertySetFieldOptions', {
  authenticationTicket: ticket,
  PropertySetName: 'PROJECTMETADATA',
  PropertyFieldName: 'REGION',
  OptionFilter: ''
});

const values = [...root.querySelectorAll('option')].map(o => o.getAttribute('value'));
console.log(values);   // ["AMER", "APAC", "EMEA"] - alphabetical, not the order they were added
```

**`OptionFilter` is only for a `LOOKUP`.** It is put on the field before the values are read, and
only a `LOOKUP` query looks at it - so a non-empty filter on any other control type is refused
`4000` rather than accepted and ignored. An empty filter reads the whole list, whatever the type.

A field whose control type has no options - a `TEXT BOX` or a `CHECK BOX` - answers a successful
empty `<options />`, although *adding* an option to one of those is refused `4000`.

## Notes

- `PropertyFieldName` lookup is **case-insensitive** -" the field name is matched against the uppercase field names stored in the property set.
- Static options are returned sorted **alphabetically** by value.
- For `LOOKUP` fields, the `OptionFilter` value is passed to the configured SQL query's filter parameter. The exact behavior depends on the SQL sentence configured for the field.
- To add a static option, use [AddPropertySetFieldOption](AddPropertySetFieldOption.md). To remove one, use [DeletePropertySetFieldOption](DeletePropertySetFieldOption.md).
- To configure a `LOOKUP` field's data source, use [SetPropertySetLookupFieldParametersForSQLServer](SetPropertySetLookupFieldParametersForSQLServer.md), [SetPropertySetLookupFieldParametersForMYSQL](SetPropertySetLookupFieldParametersForMYSQL.md), or [SetPropertySetLookupFieldParametersForORACLE](SetPropertySetLookupFieldParametersForORACLE.md).

## Related APIs

- [AddPropertySetFieldOption](AddPropertySetFieldOption.md) -" Add a static option value to a field.
- [DeletePropertySetFieldOption](DeletePropertySetFieldOption.md) -" Remove a static option value from a field.
- [GetPropertySetDefinition](GetPropertySetDefinition.md) -" Get the full property set definition including field metadata.
- [SetPropertySetLookupFieldParametersForSQLServer](SetPropertySetLookupFieldParametersForSQLServer.md) -" Configure a LOOKUP field to query SQL Server.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4041` | no set by that name, or the set has no such field |
| `4200` | the field is a `LOOKUP` and has no parameters configured, or the query against the external database failed |
| `4010` | the set is private and the caller has no ticket |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
