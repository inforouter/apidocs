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

- **The element names are not checked.** The parser walks the root element's children and
  their children, so `<psets><pset>` and `<propertysets><propertyset>` behave identically -
  and so does any other pair of names. Only the attributes below are read.
- Each second-level element represents one property set; its `name` attribute is the only
  thing that identifies it.
- Each third-level element represents one row. Field names are attributes of that element.
- Field names are **case-insensitive** during lookup but are stored in uppercase.
- `rownbr` only ever means "a new row". `0`, or the attribute left out, appends a row and
  numbers it from 1 up. **Naming a row that already exists is refused** - use
  [UpdatePropertySetRow](UpdatePropertySetRow.md) to change one. Until 9.0 it was accepted and did
  nothing at all.
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
<response success="false" error="[log]" errorCode="4000">
  <log><item>NOSUCHSET</item><error>Custom property not found.</error></log>
  <log><item>OTHERSET</item><error>Custom property not found.</error></log>
</response>
```

A single failure does **not** use this shape: it carries its own message in `error`.
A document naming several sets is not all-or-nothing either - the rows for the sets that do
exist are written, and the call still reports `success="false"` because one entry failed.

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
- Only fields defined in the property set definition are accepted. **An unrecognised field
  name is dropped silently** - the row is written with the fields that do exist and the
  caller is not told, so a misspelled name looks like a success.
- A field marked required and left out is refused `4000`, with `SETNAME.FIELDNAME` in the
  message. A value longer than a `CHAR` field is refused the same way.
- **The `AppliesTo` flags on the definition are not enforced here.** A set created with
  `AppliestoFolders=false` is applied to a folder without complaint.
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

Writes one or more rows of a property set onto a document or a folder. `Path` resolves to a document
first and to a folder if there is no document there.

```javascript
const rows = `
<propertysets>
  <propertyset name="PROJECTMETADATA">
    <row rownbr="0" PROJECTCODE="PRJ-001" REGION="EMEA" APPROVED="true" />
    <row rownbr="0" PROJECTCODE="PRJ-002" REGION="APAC" APPROVED="false" />
  </propertyset>
</propertysets>`;

await call('AddPropertySetRow', {
  authenticationTicket: ticket,
  Path: '/Finance/Projects/proposal.pdf',
  xmlpset: rows
});
```

Things worth knowing before you build that document:

- **The element names are not checked.** The parser walks the root element's children and their
  children and reads only the `name` attribute on the second level and `rownbr` on the third, so
  `<psets><pset>` and `<propertysets><propertyset>` behave identically.
- **`rownbr` is only ever "new".** `0`, or the attribute left out, appends a row and numbers it from
  1 up. Naming a row that already exists is **refused** - use `UpdatePropertySetRow` to change one.
  Until 9.0 it was accepted and did nothing at all, so a caller meaning to rewrite a row was told
  the call had worked and nothing had changed.
- **A field the set does not have is dropped silently.** The row is written with the fields that do
  exist and the caller is not told about the rest, so a misspelled field name looks like a success.
- **A required field left out is refused**, `4000`, with `SETNAME.FIELDNAME` in the message.
- **The `AppliesTo` flags are enforced here.** A set created with `AppliestoFolders=false` is
  refused on a folder. Until 9.0 they were recorded on the definition, reported by
  `GetPropertySetDefinition` and read by nothing, so they restricted nothing.
- A `BOOLEAN` written as `true` reads back as `Yes`.

The answer on success is `<response success="true" error="" />` - with **no `errorCode`**, unlike
most operations. A single failure carries its own message; two or more carry the literal `[log]` and
one `<log>` per failure:

```xml
<response success="false" error="[log]" errorCode="4000">
  <log><item>NOSUCHSET</item><error>Custom property not found.</error></log>
  <log><item>OTHERSET</item><error>Custom property not found.</error></log>
</response>
```

A document naming several sets is **not** all-or-nothing: the rows for the sets that do exist are
written and the call still reports `success="false"` because one entry failed.

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

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4041` | no document and no folder at `Path` |
| `4000` | no set by that name, a required field was left out, a value is longer than its field, `xmlpset` is not well formed, or there is no ticket at all |
| `4030` | the caller may not change the metadata of that document or folder |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
