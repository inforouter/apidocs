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
        <Log AppliedById="1042" AppliedBy="jsmith" DateApplied="2024-03-15 14:32" ReviewState="NotExtracted" />
      </propertyrow>
      <propertyrow RowNbr="2"
                   PROJECT_CODE="PRJ-2024-002"
                   STATUS="Draft"
                   NOTES="">
        <Log AppliedById="4" AppliedBy="admin" DateApplied="2024-03-16 09:10" ReviewState="NotExtracted" />
      </propertyrow>
    </propertyset>
    <propertyset Name="AUDITINFO">
      <propertyrow RowNbr="1"
                   AUDITOR="bjones"
                   AUDIT_DATE="2024-01-01">
        <Log AppliedById="3" AppliedBy="infoRouter Connect" DateApplied="2024-01-05 08:00" AIConfidence="87" ReviewState="NotReviewed" />
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
| `AppliedById` | ID of the user who last saved this row. Use this to identify the user - a username is a label, not a key, and `0` where the row predates this being recorded. `3`, the system account, when infoRouter Connect wrote the row and nobody has saved it since. |
| `AppliedBy` | Username of the user who last saved this row. |
| `DateApplied` | Date and time the row was last saved, in `YYYY-MM-DD HH:mm` UTC format. |
| `AIConfidence` | How sure infoRouter Connect was about the row when it extracted it, as a percentage `1` - `100`: the weakest of the fields it filled. **Omitted** when the row is not Connect's work. Written once and never changed by a person's save. Since 9.0. |
| `ReviewState` | `NotExtracted`, `NotReviewed` or `Reviewed`; see [Reviewing values Connect extracted](#reviewing-values-connect-extracted). Since 9.0. |

## Reviewing values Connect extracted

A row infoRouter Connect extracted carries the service's confidence in it, and - like every row - who saved it last. The two together are the row's review state; nothing else is stored:

| `ReviewState` | `AIConfidence` | `AppliedById` | Meaning |
|---|---|---|---|
| `NotExtracted` | omitted | anyone | A person typed the row, or it was applied or inherited from a folder. |
| `NotReviewed` | present | `3` (the system account) | Connect wrote it and nobody has saved it since. |
| `Reviewed` | present | anybody else | Connect wrote it and `AppliedBy` saved it on `DateApplied`, changed or not. |

A person **saving the row is the review** ([UpdatePropertySetRow](UpdatePropertySetRow.md), or the user interface): the saver is restamped and the confidence left alone. Saving the row unchanged reviews it as much as correcting it does; whether anything was changed is not recorded. Connect filling empty fields of the row again - a new version, a re-run - puts the system account back as saver, so the row is to be reviewed again. A row Connect wrote and a person then removed is simply gone; a folder apply that overwrites the row with the folder's values takes the confidence with them.

The confidence is what the service claimed at the time and is never rewritten: after a review it still says how sure Connect was, not whether the reviewer agreed. Suggested bands for showing it, as half-open intervals so they tile with no gap:

| Band | Range |
|------|-------|
| Poor | `1` - `69` |
| Low | `70` - `79` |
| Medium | `80` - `89` |
| High | `90` - `100` |

> There is no confidence threshold. Whatever Connect finds is written, however unsure it was, on the reasoning that a value a person is going to review is worth more than the blank it would otherwise leave. So a row can report `12`, and that row is exactly the one to send somebody to. A written value never reports `0`: the lowest is `1`.

The document summarises its rows in the `ExtractedDataReviewPending` bit of `AIEnhanced` - see [GetDocument](GetDocument.md#reviewing-values-connect-extracted) - which [Search](Search.md#ai-enhanced-criteria) can filter on, so the documents with a row still to review can be listed without reading every row.

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

Reads the property set rows a document or a folder carries. `Path` resolves to a document first and
to a folder if there is no document there.

```javascript
const root = await call('GetPropertySets', {
  authenticationTicket: ticket,
  Path: '/Finance/Projects/proposal.pdf'
});

for (const set of root.querySelectorAll('Propertysets > propertyset')) {
  for (const row of set.querySelectorAll('propertyrow')) {
    console.log(set.getAttribute('Name'),
                row.getAttribute('RowNbr'),
                row.getAttribute('PROJECTCODE'),
                row.querySelector('Log').getAttribute('AppliedBy'),
                row.querySelector('Log').getAttribute('DateApplied'));
  }
}
```

Every field of the set is present on the row, and one that was never written comes back as an empty
attribute rather than a missing one. An object with no rows answers an empty `<Propertysets />`.

The element names here are not the ones `GetPropertySetDefinition` uses: rows live under
`<Propertysets><propertyset Name="..."><propertyrow RowNbr="...">`, while the definition reader
answers `<PropertySet Name="..."><Fields><field FieldName="...">`.

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

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4041` | no document and no folder at `Path` |
| `4000` | the ticket is unknown - this operation reports 4000 where its neighbours report 4010 |
| `4030` | the caller may not see that document or folder |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
