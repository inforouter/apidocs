# CreatePropertySetDefinition API

Creates a new custom property set definition. A property set is a set of custom metadata fields that can be applied to documents, folders, and/or users. The property set name is stored in uppercase and must be unique across the system. This API always creates a **public** (non-private) property set. To create a private property set, use [CreatePropertySetDefinition1](CreatePropertySetDefinition1.md).

## Endpoint

```
/srv.asmx/CreatePropertySetDefinition
```

## Methods

- **GET** `/srv.asmx/CreatePropertySetDefinition?authenticationTicket=...&PropertySetName=...&PropertySetCaption=...&AppliestoDocuments=...&AppliestoFolders=...&AppliestoUsers=...&DomainNames=...`
- **POST** `/srv.asmx/CreatePropertySetDefinition` (form data)
- **SOAP** Action: `http://tempuri.org/CreatePropertySetDefinition`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `PropertySetName` | string | Yes | Internal name for the property set. Alphanumeric and underscore characters only (auto-converted to uppercase). Max 40 characters (23 on Oracle). Must be unique. |
| `PropertySetCaption` | string | Yes | Display label shown to users in the UI. Must be unique across all property sets. |
| `AppliestoDocuments` | boolean | Yes | `true` if this property set can be applied to documents. |
| `AppliestoFolders` | boolean | Yes | `true` if this property set can be applied to folders. |
| `AppliestoUsers` | boolean | Yes | `true` if this property set can be applied to user accounts. |
| `DomainNames` | string | No | Comma-separated list of library (domain) names to restrict the property set to. If empty or omitted, the property set is **global** (available in all libraries). Non-existent domain names are silently ignored. |

## Response

### Success Response

```xml
<response success="true" error="" />
```

### Error Response

```xml
<response success="false" error="A category with this name already exists." />
```

## Required Permissions

The calling user must be a **System Administrator**.

Anonymous access is not permitted.

## Behavior

- `PropertySetName` is trimmed and automatically converted to uppercase before storage.
- `PropertySetName` must contain only letters (A-"Z), digits (0-"9), and underscores (`_`). Special characters and spaces are not allowed.
- When `DomainNames` is empty or omitted, the property set is **global** -" available in every library.
- When `DomainNames` is specified, the property set is **domain-restricted** -" it only appears in the listed libraries.
- This API always creates the property set with `PrivatePropertySet = false` (visible to all users including anonymous). To control visibility from anonymous users, use [CreatePropertySetDefinition1](CreatePropertySetDefinition1.md).
- Internally, a new database table named `CUSTOM_<PropertySetName>` is created to store the property set rows.
- At least one of `AppliestoDocuments`, `AppliestoFolders`, or `AppliestoUsers` should be `true`; creating a property set that applies to nothing is technically allowed but has no practical use.

## Example

### GET Request

```
GET /srv.asmx/CreatePropertySetDefinition
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &PropertySetName=ProjectMetadata
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
POST /srv.asmx/CreatePropertySetDefinition HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&PropertySetName=ProjectMetadata&PropertySetCaption=Project+Metadata&AppliestoDocuments=true&AppliestoFolders=true&AppliestoUsers=false&DomainNames=Engineering
```

## Notes

- `PropertySetName` is stored as the internal key and also forms the database table name (`CUSTOM_<name>`). It cannot be changed after creation without using [UpdatePropertySetDefinition](UpdatePropertySetDefinition.md).
- `PropertySetCaption` is the visible display name in the UI.
- After creating the definition, add fields to it using [AddPropertySetField](AddPropertySetField.md).

## Related APIs

- [CreatePropertySetDefinition1](CreatePropertySetDefinition1.md) -" Same as this API but adds a `PrivatePropertySet` parameter to control anonymous access.
- [AddPropertySetField](AddPropertySetField.md) -" Add a field to the new property set definition.
- [AddPropertySetFieldOption](AddPropertySetFieldOption.md) -" Add option values to a dropdown/list/radio field.
- [DeletePropertySetDefinition](DeletePropertySetDefinition.md) -" Delete a property set definition.
- [UpdatePropertySetDefinition](UpdatePropertySetDefinition.md) -" Rename or update the properties of a property set definition.
- [GetPropertySetDefinition](GetPropertySetDefinition.md) -" Get the full definition of a property set including its fields.

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed -" invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Access Denied | Calling user is not a System Administrator. |
| Name already exists | A property set with the specified `PropertySetName` already exists. |
| Caption already exists | A property set with the specified `PropertySetCaption` already exists. |
| Invalid name | `PropertySetName` is empty, exceeds the maximum length, or contains invalid characters. |
