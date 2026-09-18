# GetPropertySetDefinitions1 API

Returns a filtered list of property set definitions, **without** their field definitions.

The three `AppliesTo` flags are an **OR**, not an AND: a set is listed when it applies to any
of the types asked for. All three false does not mean "nothing" - it means "do not filter by
type", and every definition comes back.

`DomainNameFilter` leaves out the sets restricted to some other library; a global set belongs
to every library, so no filter ever hides one, and an empty filter does not filter by library
at all. Private property sets are excluded for anonymous callers.

This is an extended version of [GetPropertySetDefinitions](GetPropertySetDefinitions.md) with filtering capabilities.

## Endpoint

```
/srv.asmx/GetPropertySetDefinitions1
```

## Methods

- **GET** `/srv.asmx/GetPropertySetDefinitions1?authenticationTicket=...&DomainNameFilter=...&AppliesToDocuments=...&AppliesToFolders=...&AppliesToUsers=...`
- **POST** `/srv.asmx/GetPropertySetDefinitions1` (form data)
- **SOAP** Action: `http://tempuri.org/GetPropertySetDefinitions1`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DomainNameFilter` | string | No | Library (domain) name to filter by. Only property sets assigned to this library (or global ones) are returned. Empty or null = no domain filter. |
| `AppliesToDocuments` | boolean | Yes | When `true`, only property sets that apply to documents are returned. When `false`, this filter is inactive. |
| `AppliesToFolders` | boolean | Yes | When `true`, only property sets that apply to folders are returned. When `false`, this filter is inactive. |
| `AppliesToUsers` | boolean | Yes | When `true`, only property sets that apply to user accounts are returned. When `false`, this filter is inactive. |

## Filter Behavior

| Parameter | `true` | `false` |
|-----------|--------|---------|
| `AppliesToDocuments` | Only include psets that apply to documents | No filter on this dimension |
| `AppliesToFolders` | Only include psets that apply to folders | No filter on this dimension |
| `AppliesToUsers` | Only include psets that apply to users | No filter on this dimension |
| `DomainNameFilter` | Only include psets for this library or global psets | No domain filter |

Multiple filters are ANDed together. A property set must pass all active filters to be included.

Global property sets (available in all libraries) are always included when `DomainNameFilter` is specified.

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
  </PropertySets>
</response>
```

> **Note**: Field definitions are **not** included. Use [GetPropertySetDefinition](GetPropertySetDefinition.md) for full field details.

### Error Response

```xml
<response success="false" error="[901]Session expired or Invalid ticket" />
```

## Required Permissions

Any authenticated user may call this API.

Anonymous callers receive only non-private property sets (`PrivatePropertySet = FALSE`).

## Example

### GET Request -" retrieve all property sets that apply to documents in the "Engineering" library

```
GET /srv.asmx/GetPropertySetDefinitions1
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &DomainNameFilter=Engineering
    &AppliesToDocuments=true
    &AppliesToFolders=false
    &AppliesToUsers=false
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/GetPropertySetDefinitions1 HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&DomainNameFilter=Engineering&AppliesToDocuments=true&AppliesToFolders=false&AppliesToUsers=false
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

`GetPropertySetDefinitions` with filters. Like it, the list carries no field definitions.

```javascript
const root = await call('GetPropertySetDefinitions1', {
  authenticationTicket: ticket,
  DomainNameFilter: 'Finance',   // empty means every library
  AppliesToDocuments: true,
  AppliesToFolders: false,
  AppliesToUsers: false
});

for (const set of root.querySelectorAll('PropertySets > PropertySet')) {
  console.log(set.getAttribute('Name'), set.getAttribute('Caption'));
}
```

**The three flags are an OR, not an AND.** A set is listed when it applies to *any* of the types
asked for, so `AppliesToDocuments=true` alone lists every set a document can carry, whatever else it
also applies to. **All three false does not mean "nothing"** - it means "do not filter by type", and
every definition comes back.

`DomainNameFilter` leaves out the sets restricted to some other library. A global set belongs to
every library, so no filter ever hides one; an empty filter does not filter by library at all.

## Notes

- `DomainNameFilter` is matched **case-insensitively** against library names.
- Setting all three `AppliesTo*` flags to `false` returns all property sets with no object-type filter (equivalent to [GetPropertySetDefinitions](GetPropertySetDefinitions.md) but still supports `DomainNameFilter`).
- Field definitions are not included in the response.

## Related APIs

- [GetPropertySetDefinitions](GetPropertySetDefinitions.md) -" All definitions without filtering.
- [GetPropertySetDefinition](GetPropertySetDefinition.md) -" Full definition of a single property set including fields.
- [CreatePropertySetDefinition](CreatePropertySetDefinition.md) -" Create a new property set definition.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
