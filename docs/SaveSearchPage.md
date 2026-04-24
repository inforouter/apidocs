# SaveSearchPage API

Creates a new search page definition or updates an existing one.

## Endpoint

```
/srv.asmx/SaveSearchPage
```

## Methods

- **GET** `/srv.asmx/SaveSearchPage?authenticationTicket=...&searchPageId=...&name=...&...`
- **POST** `/srv.asmx/SaveSearchPage` (form data)
- **SOAP** Action: `http://tempuri.org/SaveSearchPage`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `searchPageId` | int | Yes | `0` to create a new search page; the existing search page ID to update |
| `name` | string | Yes | Display name. Minimum 5 characters; maximum 64 characters |
| `description` | string | No | Optional description text |
| `isPersonal` | bool | Yes | `true` — private page owned by the authenticated user. `false` — system-wide page visible to all users (requires Search Administrator role) |
| `anonymousAccess` | bool | No | Allow anonymous (unauthenticated) users to use this search page. Ignored for personal pages. Default `false` |
| `publicAccess` | bool | No | Allow all authenticated users to use this search page. Ignored for personal pages. Default `false` |
| `userGroupNames` | string | No | Pipe-separated list of user group names whose members may access this search page. Ignored for personal pages. Empty = no group restriction. See [userGroupNames format](#usergroupnames-format) |
| `searchParametersXml` | string | No | XML defining which search criteria fields are visible on this page. See [searchParametersXml format](#searchparametersxml-format). Pass empty to apply defaults (all fields visible with no default values) |

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
  <ITEM NAME="DOCTYPE" VALUE="" VISIBLE="FALSE" />
  <!-- ... additional ITEM elements ... -->
</SEARCH>
```

Each `<ITEM>` has:
- `NAME` — field identifier (see field names in the infoRouter search engine)
- `VALUE` — default value for the field
- `VISIBLE` — `TRUE` or `FALSE`; controls whether the field is shown on the search page

To obtain a valid XML string for an existing search page, call `GetSearchPages` to get the page ID and then render it in the UI to copy its configuration. Pass an empty string to create a page with all fields set to their default visibility.

## Response

### Success (create — `searchPageId` was `0`)

```xml
<root success="true" id="47" />
```

### Success (update — `searchPageId` was `> 0`)

```xml
<root success="true" />
```

### Error

```xml
<root success="false" error="Error message here" />
```

## Required Permissions

- User must be authenticated.
- **System-wide pages** (`isPersonal=false`) require the **Search Administrator** role.
- **Personal pages** (`isPersonal=true`) can be created by any authenticated user.
- Only the owner of a personal page may update it. Search administrators may update system-wide pages.

## Example Requests

### Request (POST) — create personal search page

```
POST /srv.asmx/SaveSearchPage HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&
searchPageId=0&
name=My Document Search&
description=Search for documents by keyword&
isPersonal=true&
anonymousAccess=false&
publicAccess=false&
userGroupNames=&
searchParametersXml=
```

### Request (POST) — create system-wide search page with group restrictions

```
POST /srv.asmx/SaveSearchPage HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&
searchPageId=0&
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
SOAPAction: "http://tempuri.org/SaveSearchPage"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <SaveSearchPage xmlns="http://tempuri.org/">
      <authenticationTicket>abc123</authenticationTicket>
      <searchPageId>0</searchPageId>
      <name>My Document Search</name>
      <description>Search for documents by keyword</description>
      <isPersonal>true</isPersonal>
      <anonymousAccess>false</anonymousAccess>
      <publicAccess>false</publicAccess>
      <userGroupNames></userGroupNames>
      <searchParametersXml></searchParametersXml>
    </SaveSearchPage>
  </soap:Body>
</soap:Envelope>
```

## Error Codes

| Error | Description |
|-------|-------------|
| `[901] Session expired or Invalid ticket` | Invalid or expired authentication ticket |
| Name validation error | Name is empty, too short (under 5 characters), or contains invalid characters |
| Duplicate name error | A search page with the same name already exists |
| Access denied | Caller lacks the Search Administrator role for a system-wide page, or is not the owner of a personal page |
| Group not found | A name in `userGroupNames` could not be resolved to a user group |
| `[2842] ...` | Attempted to rename the default search page (ID 1) |

## Notes

- The name of the default system search page (ID 1, "Advanced Search") cannot be changed.
- `anonymousAccess`, `publicAccess`, and `userGroupNames` are silently ignored for personal pages (`isPersonal=true`).
- Use `%5C` to URL-encode the backslash (`\`) in domain-qualified group names when passing via query string or form data.

## Related APIs

- `GetSearchPages` — List all search page definitions visible to the current user
- `DeleteSearchPage` — Delete a saved search page by ID
