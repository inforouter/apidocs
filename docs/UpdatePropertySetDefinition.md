# UpdatePropertySetDefinition API

Updates the metadata of an existing custom property set definition: its name, caption, which object types it applies to, and its domain restrictions. The `PrivatePropertySet` flag is **not** changed by this variant -" use [UpdatePropertySetDefinition1](UpdatePropertySetDefinition1.md) to update it.

## Endpoint

```
/srv.asmx/UpdatePropertySetDefinition
```

## Methods

- **GET** `/srv.asmx/UpdatePropertySetDefinition?authenticationTicket=...&PropertySetName=...&NewPropertySetName=...&...`
- **POST** `/srv.asmx/UpdatePropertySetDefinition` (form data)
- **SOAP** Action: `http://tempuri.org/UpdatePropertySetDefinition`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `PropertySetName` | string | Yes | Current internal name of the property set to update. |
| `NewPropertySetName` | string | Yes | New internal name. Trimmed and uppercased automatically. Must contain only letters, digits, and underscores (`A-"Z`, `0-"9`, `_`). Maximum 40 characters (23 on Oracle). Must be unique across all property sets. |
| `PropertySetCaption` | string | Yes | New display caption. Must be unique across all property sets. |
| `AppliestoDocuments` | boolean | Yes | `true` if this property set should be applicable to documents. |
| `AppliestoFolders` | boolean | Yes | `true` if this property set should be applicable to folders. |
| `AppliestoUsers` | boolean | Yes | `true` if this property set should be applicable to users. |
| `DomainNames` | string | No | Comma-separated list of library (domain) names to restrict this property set to. Empty or omitted = globally available. |

## Response

### Success Response

```xml
<response success="true" error="" />
```

### Error Response

```xml
<response success="false" error="[901]Session expired or Invalid ticket" />
```

## Required Permissions

**System Administrator** only. Non-admin callers receive an access denied error.

## Behavior

- The internal name (`NewPropertySetName`) is trimmed and converted to uppercase. If the name changes, the corresponding `CUSTOM_<name>` database table is renamed accordingly.
- The property set caption must be unique system-wide. If unchanged from its current value the uniqueness check is skipped.
- Domain restrictions are **fully replaced**: all existing domain associations are deleted and the new list is inserted.
- `AppliesTo*` settings are **fully replaced**: all existing object-type associations are deleted and the new set is inserted.
- The `PrivatePropertySet` flag is **not modified** by this API. Use [UpdatePropertySetDefinition1](UpdatePropertySetDefinition1.md) to update it.
- **System-managed property sets** (internal use only) cannot be updated and return an error.
- Property sets **linked to a document type** have additional restrictions:
  - They cannot be restricted to specific domains (DomainNames must be empty).
  - `AppliestoDocuments` must remain `true`.

## Example

### GET Request

```
GET /srv.asmx/UpdatePropertySetDefinition
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &PropertySetName=PROJECTMETA
    &NewPropertySetName=PROJMETADATA
    &PropertySetCaption=Project+Metadata
    &AppliestoDocuments=true
    &AppliestoFolders=true
    &AppliestoUsers=false
    &DomainNames=Engineering,Finance
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/UpdatePropertySetDefinition HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&PropertySetName=PROJECTMETA&NewPropertySetName=PROJMETADATA&PropertySetCaption=Project+Metadata&AppliestoDocuments=true&AppliestoFolders=true&AppliestoUsers=false&DomainNames=Engineering%2CFinance
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

Rewrites a definition's name, caption, the three `AppliesTo` flags and its library restriction. It
does **not** touch the private flag - use `UpdatePropertySetDefinition1` for that.

```javascript
await call('UpdatePropertySetDefinition', {
  authenticationTicket: ticket,
  PropertySetName: 'PROJECTMETADATA',
  NewPropertySetName: 'PROJECTMETADATA',   // a different name renames the set
  PropertySetCaption: 'Project metadata',
  AppliestoDocuments: true,
  AppliestoFolders: true,
  AppliestoUsers: false,
  DomainNames: 'Finance'                   // empty releases the restriction
});
```

Renaming keeps the fields, the options and every row already applied - the rows follow the set.
An empty `DomainNames` **clears** the restriction back to global rather than leaving it alone.

## Notes

- To also update the `PrivatePropertySet` flag in a single call, use [UpdatePropertySetDefinition1](UpdatePropertySetDefinition1.md).
- Renaming a property set renames the underlying `CUSTOM_xxx` table in the database. This is done atomically within a transaction.
- If `DomainNames` contains names not found in the system, those names are silently ignored.
- At least one of `AppliestoDocuments`, `AppliestoFolders`, or `AppliestoUsers` should be `true` for the property set to be usable.

## Related APIs

- [UpdatePropertySetDefinition1](UpdatePropertySetDefinition1.md) -" Same as this API but also updates the `PrivatePropertySet` flag.
- [CreatePropertySetDefinition](CreatePropertySetDefinition.md) -" Create a new public property set definition.
- [CreatePropertySetDefinition1](CreatePropertySetDefinition1.md) -" Create a property set definition with explicit PrivatePropertySet flag.
- [DeletePropertySetDefinition](DeletePropertySetDefinition.md) -" Permanently delete a property set definition.
- [GetPropertySetDefinition](GetPropertySetDefinition.md) -" Get the current definition of a property set.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4030` | the caller is not a system administrator - including a caller with no ticket at all |
| `4041` | no set by that name |
| `4090` | `NewPropertySetName` is already the name of another set |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
