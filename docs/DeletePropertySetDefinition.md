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

Deletes the set, its fields, its options and every row of it on every document, folder and user,
along with the table behind it.

```javascript
await call('DeletePropertySetDefinition', {
  authenticationTicket: ticket,
  PropertySetName: 'PROJECTMETADATA'
});
```

There is no undo. A set that is not there is reported `4000`, where `GetPropertySetDefinition`
reports `4041` for the identical condition.

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

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4000` | no set by that name, **or** the caller is not a system administrator - the message says which, the code does not |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
