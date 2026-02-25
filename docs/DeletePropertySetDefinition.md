# DeletePropertySetDefinition API

Permanently deletes a custom property set definition and all data associated with it. This includes all field definitions, field options, all property set rows that have been applied to documents, folders, and users, and the underlying database table. **This operation cannot be undone.**

## Endpoint

```
/srv.asmx/DeletePropertySetDefinition
```

## Methods

- **GET** `/srv.asmx/DeletePropertySetDefinition?authenticationTicket=...&PropertySetName=...`
- **POST** `/srv.asmx/DeletePropertySetDefinition` (form data)
- **SOAP** Action: `http://tempuri.org/DeletePropertySetDefinition`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `PropertySetName` | string | Yes | Internal name of the property set to delete. |

## Response

### Success Response

```xml
<response success="true" error="" />
```

### Error Response

```xml
<response success="false" error="A custom property set that associated with a document type cannot be deleted." />
```

## Required Permissions

The calling user must be a **System Administrator**.

Anonymous access is not permitted.

## What Gets Deleted

Deleting a property set definition is a cascading, irreversible operation:

| Item Deleted | Description |
|---|---|
| Field definitions | All fields defined in the property set (from `CATEGORYDETAILS`). |
| Field options | All static option values for dropdown/list/radio fields (from `PROPERTYOPTIONS`). |
| Applied rows | All property set data rows applied to documents, folders, and users (from `CUSTOM_<name>` table). |
| Domain associations | All library-scoped assignments of this property set. |
| Class assignments | The document/folder/user target configuration. |
| Lookup config files | Any lookup field XML definition files on disk. |
| Database table | The `CUSTOM_<PropertySetName>` table is `DROP`ped from the database. |
| Folder auto-assign | Any folders set to automatically apply this property set have that configuration cleared. |

## Constraints

- **System property sets** (built-in, managed by infoRouter) cannot be deleted. Attempting to do so returns an error.
- A property set that is **associated with a document type** as its required property set cannot be deleted. Disassociate it from any document types first.

## Example

### GET Request

```
GET /srv.asmx/DeletePropertySetDefinition
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &PropertySetName=ProjectMetadata
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/DeletePropertySetDefinition HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&PropertySetName=ProjectMetadata
```

## Notes

- All applied property set data for all documents, folders, and users is permanently lost when the definition is deleted.
- The underlying `CUSTOM_<PropertySetName>` database table is physically dropped.
- This operation is transactional -" either everything is deleted or nothing is (in case of a database error).

## Related APIs

- [CreatePropertySetDefinition](CreatePropertySetDefinition.md) -" Create a new property set definition.
- [GetPropertySetDefinition](GetPropertySetDefinition.md) -" Get the full definition before deleting.
- [GetPropertySetDefinitions](GetPropertySetDefinitions.md) -" List all property set definitions.
- [DeletePropertySetField](DeletePropertySetField.md) -" Delete a single field from a property set (less destructive).

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed -" invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Access Denied | Calling user is not a System Administrator. |
| Property set not found | No property set with the specified `PropertySetName` exists. |
| System property set | Cannot delete a system-managed property set. |
| Document type association | The property set is assigned to one or more document types and cannot be deleted. |
