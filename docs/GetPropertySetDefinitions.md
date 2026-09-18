# GetPropertySetDefinitions API

Returns the property set definitions the caller may see, **without** their field definitions -
use [GetPropertySetDefinition](GetPropertySetDefinition.md) for those.

The list is filtered by visibility: a private set is left out for a caller with no ticket, and
a set restricted to a library is left out for somebody who is not a member of it. The sets
marked `SystemUseOnly="TRUE"` are included, and no operation may change those.

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

Lists every definition the caller may see, **without** the field definitions - use
`GetPropertySetDefinition` for those.

```javascript
const root = await call('GetPropertySetDefinitions', { authenticationTicket: ticket });

for (const set of root.querySelectorAll('PropertySets > PropertySet')) {
  if (set.getAttribute('SystemUseOnly') === 'TRUE') { continue; }   // infoRouter's own, do not edit
  console.log(set.getAttribute('Name'), set.getAttribute('Caption'));
}
```

The list is filtered by what the caller may see: a private set is left out for a caller with no
ticket, and a set restricted to a library is left out for somebody who is not in it. It does include
the sets marked `SystemUseOnly="TRUE"`, which no operation may change.

## Notes

- The result includes all property sets in the system with no filtering by library, object type, or privacy.
- Field definitions are not included. Use [GetPropertySetDefinition](GetPropertySetDefinition.md) to get a full definition with fields for a specific property set.
- To filter by library, object type (documents/folders/users), use [GetPropertySetDefinitions1](GetPropertySetDefinitions1.md).

## Related APIs

- [GetPropertySetDefinitions1](GetPropertySetDefinitions1.md) -" Filtered list of property set definitions.
- [GetPropertySetDefinition](GetPropertySetDefinition.md) -" Full definition of a single property set including fields.
- [CreatePropertySetDefinition](CreatePropertySetDefinition.md) -" Create a new property set definition.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
