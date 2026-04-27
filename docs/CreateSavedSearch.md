# CreateSavedSearch API

Creates a new saved search or search page definition.

## Endpoint

```
/srv.asmx/CreateSavedSearch
```

## Methods

- **GET** `/srv.asmx/CreateSavedSearch?authenticationTicket=...&searchPageType=...&name=...&...`
- **POST** `/srv.asmx/CreateSavedSearch` (form data)
- **SOAP** Action: `http://tempuri.org/CreateSavedSearch`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `searchPageType` | string | Yes | Type of entry: `"savedSearch"` or `"searchPage"`. See [searchPageType values](#searchpagetype-values) |
| `name` | string | Yes | Display name. Minimum 5 characters; maximum 64 characters |
| `description` | string | No | Optional description text |
| `isPersonal` | bool | Yes | `true` — private entry owned by the authenticated user. `false` — system-wide entry visible to all users (requires Search Administrator role) |
| `anonymousAccess` | bool | No | Allow anonymous (unauthenticated) users to access this entry. Ignored for personal entries. Default `false` |
| `publicAccess` | bool | No | Allow all authenticated users to access this entry. Ignored for personal entries. Default `false` |
| `userGroupNames` | string | No | Pipe-separated list of user group names whose members may access this entry. Ignored for personal entries. Empty = no group restriction. See [userGroupNames format](#usergroupnames-format) |
| `searchParametersXml` | string | No | XML defining which search criteria fields are visible. See [searchParametersXml format](#searchparametersxml-format). Pass empty to apply defaults |

## searchPageType Values

| Value | Meaning |
|-------|---------|
| `"savedSearch"` | A saved query — stores actual search criteria values for re-use |
| `"searchPage"` | A search page configuration — controls which search fields are visible on the UI search form |

The value is matched exactly (case-sensitive). Any value other than `"savedSearch"` is treated as `"searchPage"`.

## userGroupNames Format

Pipe-separate multiple group names. Groups local to a specific domain must use the domain-qualified format `domain\groupName`:

```
Accountants|HR Managers|accounting\Controllers
```

| Entry | Meaning |
|-------|---------|
| `Accountants` | Global group named "Accountants" |
| `accounting\Controllers` | Group named "Controllers" in the "accounting" domain |

If any group name cannot be resolved, the request fails and returns an error.

## searchParametersXml Format

The XML defines which search fields appear on the page and their default values. The root element is `<SEARCH>` containing `<ITEM>` elements:

```xml
<SEARCH>
  <ITEM NAME="SEARCHFOR" VALUE="" VISIBLE="TRUE" />
  <ITEM NAME="KEYWORDS" VALUE="" VISIBLE="TRUE" />
  <ITEM NAME="DOCUMENTNAME" VALUE="" VISIBLE="FALSE" />
  <!-- ... additional ITEM elements ... -->
</SEARCH>
```

Each `<ITEM>` has:
- `NAME` — field identifier
- `VALUE` — default value for the field
- `VISIBLE` — `TRUE` or `FALSE`; controls whether the field is shown

To base a new entry on an existing one, call `GetSavedSearch` with the source entry ID. Its response contains an inline `<SEARCH>` element — serialize that element to a string and pass it here. Pass an empty string to create an entry with all fields set to their default visibility.

## Response

### Success

```xml
<root success="true" id="47" />
```

The `id` attribute always contains the ID of the newly created entry.

### Error

```xml
<root success="false" error="Error message here" />
```

## Required Permissions

- User must be authenticated.
- **System-wide entries** (`isPersonal=false`) require the **Search Administrator** role.
- **Personal entries** (`isPersonal=true`) can be created by any authenticated user.

## Example Requests

### Request (POST) — create personal saved search

```
POST /srv.asmx/CreateSavedSearch HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&
searchPageType=savedSearch&
name=My Q4 Contracts&
description=Search for Q4 contract documents&
isPersonal=true&
anonymousAccess=false&
publicAccess=false&
userGroupNames=&
searchParametersXml=
```

### Request (POST) — create system-wide search page with group restrictions

```
POST /srv.asmx/CreateSavedSearch HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&
searchPageType=searchPage&
name=Contract Search&
description=Search for contract documents&
isPersonal=false&
anonymousAccess=false&
publicAccess=false&
userGroupNames=Legal|accounting%5CControllers&
searchParametersXml=
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/CreateSavedSearch"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <CreateSavedSearch xmlns="http://tempuri.org/">
      <authenticationTicket>abc123</authenticationTicket>
      <searchPageType>savedSearch</searchPageType>
      <name>My Q4 Contracts</name>
      <description>Search for Q4 contract documents</description>
      <isPersonal>true</isPersonal>
      <anonymousAccess>false</anonymousAccess>
      <publicAccess>false</publicAccess>
      <userGroupNames></userGroupNames>
      <searchParametersXml></searchParametersXml>
    </CreateSavedSearch>
  </soap:Body>
</soap:Envelope>
```

## Error Codes

| Error | Description |
|-------|-------------|
| `[901] Session expired or Invalid ticket` | Invalid or expired authentication ticket |
| Name validation error | Name is empty, too short (under 5 characters), or contains invalid characters |
| Duplicate name error | An entry with the same name already exists |
| Access denied | Caller lacks the Search Administrator role for a system-wide entry |
| Group not found | A name in `userGroupNames` could not be resolved to a user group |

## Notes

- `anonymousAccess`, `publicAccess`, and `userGroupNames` are silently ignored for personal entries (`isPersonal=true`).
- Use `%5C` to URL-encode the backslash (`\`) in domain-qualified group names when passing via query string or form data.
- `searchPageType` is case-sensitive. Only `"savedSearch"` is treated as a saved search; any other value is treated as `"searchPage"`.
- To update an existing entry, use `UpdateSavedSearch` instead.

## Related APIs

- `UpdateSavedSearch` — Update an existing saved search or search page definition
- `GetSavedSearches` — List all entries visible to the current user
- `GetSavedSearch` — Get the full definition of a single entry
- `DeleteSavedSearch` — Delete a saved search or search page by ID
