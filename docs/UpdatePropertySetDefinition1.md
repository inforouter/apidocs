# UpdatePropertySetDefinition1 API

Updates the metadata of an existing custom property set definition: its name, caption, which object types it applies to, domain restrictions, and the `PrivatePropertySet` flag. This variant extends [UpdatePropertySetDefinition](UpdatePropertySetDefinition.md) by adding explicit control over the `PrivatePropertySet` flag.

## Endpoint

```
/srv.asmx/UpdatePropertySetDefinition1
```

## Methods

- **GET** `/srv.asmx/UpdatePropertySetDefinition1?authenticationTicket=...&PropertySetName=...&NewPropertySetName=...&...`
- **POST** `/srv.asmx/UpdatePropertySetDefinition1` (form data)
- **SOAP** Action: `http://tempuri.org/UpdatePropertySetDefinition1`

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
| `PrivatePropertySet` | boolean | Yes | `true` to hide this property set from anonymous (guest) users in all read APIs. `false` to make it visible to anonymous users. |

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
- `PrivatePropertySet = true` hides the property set from anonymous (guest) users in [GetPropertySetDefinition](GetPropertySetDefinition.md), [GetPropertySetDefinitions](GetPropertySetDefinitions.md), [GetPropertySetDefinitions1](GetPropertySetDefinitions1.md), and [GetPropertySetFieldOptions](GetPropertySetFieldOptions.md).
- **System-managed property sets** (internal use only) cannot be updated and return an error.
- Property sets **linked to a document type** have additional restrictions:
  - They cannot be restricted to specific domains (DomainNames must be empty).
  - `AppliestoDocuments` must remain `true`.

## Example

### GET Request

```
GET /srv.asmx/UpdatePropertySetDefinition1
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &PropertySetName=PROJECTMETA
    &NewPropertySetName=PROJMETADATA
    &PropertySetCaption=Project+Metadata
    &AppliestoDocuments=true
    &AppliestoFolders=true
    &AppliestoUsers=false
    &DomainNames=Engineering,Finance
    &PrivatePropertySet=true
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/UpdatePropertySetDefinition1 HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&PropertySetName=PROJECTMETA&NewPropertySetName=PROJMETADATA&PropertySetCaption=Project+Metadata&AppliestoDocuments=true&AppliestoFolders=true&AppliestoUsers=false&DomainNames=Engineering%2CFinance&PrivatePropertySet=true
```

## Notes

- The only difference from [UpdatePropertySetDefinition](UpdatePropertySetDefinition.md) is the addition of the `PrivatePropertySet` parameter. Use [UpdatePropertySetDefinition](UpdatePropertySetDefinition.md) if you want to leave `PrivatePropertySet` unchanged.
- Renaming a property set renames the underlying `CUSTOM_xxx` table in the database. This is done atomically within a transaction.
- If `DomainNames` contains names not found in the system, those names are silently ignored.
- At least one of `AppliestoDocuments`, `AppliestoFolders`, or `AppliestoUsers` should be `true` for the property set to be usable.

## Related APIs

- [UpdatePropertySetDefinition](UpdatePropertySetDefinition.md) -" Same as this API but does not modify the `PrivatePropertySet` flag.
- [CreatePropertySetDefinition1](CreatePropertySetDefinition1.md) -" Create a property set definition with explicit PrivatePropertySet flag.
- [DeletePropertySetDefinition](DeletePropertySetDefinition.md) -" Permanently delete a property set definition.
- [GetPropertySetDefinition](GetPropertySetDefinition.md) -" Get the current definition of a property set.

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed -" invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Access Denied | Caller is not a System Administrator. |
| Property set not found | No property set with the specified `PropertySetName` exists. |
| System property sets cannot be changed or deleted | The property set is system-managed. |
| Name already exists | Another property set already uses the `NewPropertySetName`. |
| Caption already exists | Another property set already uses the `PropertySetCaption`. |
| Invalid name format | `NewPropertySetName` contains invalid characters or exceeds the maximum length. |
| Document type restriction | Property set is linked to a document type; cannot restrict to domains or unset AppliestoDocuments. |
