# GetPropertySetDefinition API

Returns the full definition of a single property set, including all field definitions, domain restrictions, and metadata flags. Private property sets are not accessible to anonymous users.

## Endpoint

```
/srv.asmx/GetPropertySetDefinition
```

## Methods

- **GET** `/srv.asmx/GetPropertySetDefinition?authenticationTicket=...&PropertySetName=...`
- **POST** `/srv.asmx/GetPropertySetDefinition` (form data)
- **SOAP** Action: `http://tempuri.org/GetPropertySetDefinition`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `PropertySetName` | string | Yes | Internal name of the property set to retrieve. |

## Response

### Success Response

```xml
<response success="true" error="">
  <PropertySet
      Name="PROJECTMETADATA"
      Caption="Project Metadata"
      AppliesToDocuments="TRUE"
      AppliesToFolders="TRUE"
      AppliesToUsers="FALSE"
      SystemUseOnly="FALSE"
      PrivatePropertySet="FALSE">
    <DomainRestrictions Global="FALSE">
      <Domain Name="Engineering" />
      <Domain Name="Finance" />
    </DomainRestrictions>
    <Fields>
      <field
          FieldName="PROJECT_CODE"
          Caption="Project Code"
          DataType="CHAR"
          DataLength="20"
          Required="TRUE"
          ControlSize="20"
          ControlOrder="1"
          ControlType="TEXT BOX" />
      <field
          FieldName="STATUS"
          Caption="Status"
          DataType="CHAR"
          DataLength="30"
          Required="FALSE"
          ControlSize="30"
          ControlOrder="2"
          ControlType="COMBO BOX" />
    </Fields>
  </PropertySet>
</response>
```

### For LOOKUP Fields

Fields with `ControlType="LOOKUP"` include an additional `<lookupparams>` child element. The `dbconnectionparams` sub-element is only included when the calling user is a System Administrator (connection passwords are always masked as `****`).

```xml
<field FieldName="CATEGORY" Caption="Category" DataType="CHAR" DataLength="50"
       Required="FALSE" ControlSize="50" ControlOrder="3" ControlType="LOOKUP">
  <lookupparams looktype="database">
    <dbconnectionparams dbtype="SQLSERVER" servername="dbserver" username="user"
                        password="****" databasename="RefData" />
    <sqlsentence>SELECT CategoryName FROM Categories WHERE Active=1</sqlsentence>
  </lookupparams>
</field>
```

### Error Response

```xml
<response success="false" error="Category not found." />
```

## PropertySet Attributes

| Attribute | Values | Description |
|-----------|--------|-------------|
| `Name` | string | Internal uppercase name (e.g., `PROJECTMETADATA`). |
| `Caption` | string | Display label shown in the UI. |
| `AppliesToDocuments` | `TRUE` / `FALSE` | Whether this property set can be applied to documents. |
| `AppliesToFolders` | `TRUE` / `FALSE` | Whether this property set can be applied to folders. |
| `AppliesToUsers` | `TRUE` / `FALSE` | Whether this property set can be applied to user accounts. |
| `SystemUseOnly` | `TRUE` / `FALSE` | Whether this is a system-managed property set (cannot be modified). |
| `PrivatePropertySet` | `TRUE` / `FALSE` | Whether this property set is hidden from anonymous users. |

## DomainRestrictions

| Attribute | Values | Description |
|-----------|--------|-------------|
| `Global` | `TRUE` / `FALSE` | `TRUE` means available in all libraries; `FALSE` means restricted to the listed `<Domain>` elements. |

## Field Attributes

| Attribute | Description |
|-----------|-------------|
| `FieldName` | Internal field name (uppercase). |
| `Caption` | Display label. |
| `DataType` | `BOOLEAN`, `NUMBER`, `CHAR`, or `DATE`. |
| `DataLength` | Maximum character length for `CHAR` fields; fixed for other types. |
| `Required` | `TRUE` if the field must be filled in. |
| `ControlSize` | Display width of the UI control. |
| `ControlOrder` | Display position within the property set form. |
| `ControlType` | `TEXT BOX`, `COMBO BOX`, `LIST BOX`, `RADIO BUTTON`, `CHECK BOX`, or `LOOKUP`. |

## Required Permissions

Any authenticated user may call this API.

Anonymous access is **blocked for private property sets** (`PrivatePropertySet = TRUE`).

## Example

### GET Request

```
GET /srv.asmx/GetPropertySetDefinition
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &PropertySetName=ProjectMetadata
HTTP/1.1
Host: yourserver
```

## Notes

- `PropertySetName` lookup is **case-insensitive**.
- This is the only property set read API that returns the full field list. [GetPropertySetDefinitions](GetPropertySetDefinitions.md) and [GetPropertySetDefinitions1](GetPropertySetDefinitions1.md) return definitions without field details.
- Lookup connection parameters (server, username, SQL sentence) are only included in the response when the caller is a System Administrator. Passwords are always masked as `****`.

## Related APIs

- [GetPropertySetDefinitions](GetPropertySetDefinitions.md) -" List all property set definitions (without field details).
- [GetPropertySetDefinitions1](GetPropertySetDefinitions1.md) -" Filtered list of property set definitions.
- [GetPropertySetFieldOptions](GetPropertySetFieldOptions.md) -" Get option values for a specific field.
- [AddPropertySetField](AddPropertySetField.md) -" Add a field to this property set.

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed -" invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Property set not found | No property set with the specified `PropertySetName` exists. |
| Access Denied | Property set is private and the caller is anonymous. |
