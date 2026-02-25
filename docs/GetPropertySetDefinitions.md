# GetPropertySetDefinitions API

Returns a list of all property set definitions in the system. No filtering is applied -" all property sets are returned regardless of which object types they apply to or which libraries they belong to. Private property sets are excluded for anonymous callers.

For filtered results, use [GetPropertySetDefinitions1](GetPropertySetDefinitions1.md).

## Endpoint

```
/srv.asmx/GetPropertySetDefinitions
```

## Methods

- **GET** `/srv.asmx/GetPropertySetDefinitions?authenticationTicket=...`
- **POST** `/srv.asmx/GetPropertySetDefinitions` (form data)
- **SOAP** Action: `http://tempuri.org/GetPropertySetDefinitions`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |

## Response

### Success Response

```xml
<response success="true" error="">
  <PropertySets>
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
      </DomainRestrictions>
    </PropertySet>
    <PropertySet
        Name="HRRECORDS"
        Caption="HR Records"
        AppliesToDocuments="TRUE"
        AppliesToFolders="FALSE"
        AppliesToUsers="TRUE"
        SystemUseOnly="FALSE"
        PrivatePropertySet="TRUE">
      <DomainRestrictions Global="TRUE" />
    </PropertySet>
  </PropertySets>
</response>
```

> **Note**: Field definitions are **not** included in this response. To retrieve field details, call [GetPropertySetDefinition](GetPropertySetDefinition.md) for each property set individually.

### Error Response

```xml
<response success="false" error="[901]Session expired or Invalid ticket" />
```

## PropertySet Attributes

| Attribute | Values | Description |
|-----------|--------|-------------|
| `Name` | string | Internal uppercase name. |
| `Caption` | string | Display label shown in the UI. |
| `AppliesToDocuments` | `TRUE` / `FALSE` | Whether the property set can be applied to documents. |
| `AppliesToFolders` | `TRUE` / `FALSE` | Whether the property set can be applied to folders. |
| `AppliesToUsers` | `TRUE` / `FALSE` | Whether the property set can be applied to user accounts. |
| `SystemUseOnly` | `TRUE` / `FALSE` | System-managed property sets (cannot be modified). |
| `PrivatePropertySet` | `TRUE` / `FALSE` | Hidden from anonymous users when `TRUE`. |

## DomainRestrictions

| Attribute | Description |
|-----------|-------------|
| `Global="TRUE"` | Property set is available in all libraries. |
| `Global="FALSE"` | Property set is restricted to the listed `<Domain>` elements. |

## Required Permissions

Any authenticated user may call this API.

Anonymous callers receive all non-private property sets (those with `PrivatePropertySet = FALSE`).

## Example

### GET Request

```
GET /srv.asmx/GetPropertySetDefinitions
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
HTTP/1.1
Host: yourserver
```

## Notes

- The result includes all property sets in the system with no filtering by library, object type, or privacy.
- Field definitions are not included. Use [GetPropertySetDefinition](GetPropertySetDefinition.md) to get a full definition with fields for a specific property set.
- To filter by library, object type (documents/folders/users), use [GetPropertySetDefinitions1](GetPropertySetDefinitions1.md).

## Related APIs

- [GetPropertySetDefinitions1](GetPropertySetDefinitions1.md) -" Filtered list of property set definitions.
- [GetPropertySetDefinition](GetPropertySetDefinition.md) -" Full definition of a single property set including fields.
- [CreatePropertySetDefinition](CreatePropertySetDefinition.md) -" Create a new property set definition.

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed -" invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
