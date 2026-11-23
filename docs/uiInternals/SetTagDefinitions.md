---
search:
  exclude: true
---

# SetTagDefinitions API

**Available in:** infoRouter 9.0 and later

!!! warning "Internal API"
    Made for infoRouter's own user interface. It is not part of the public web API: there is no SOAP
    form and no promise of backward compatibility, and it may change or be removed in any release
    without notice. Do not use it in an integration.

Replaces the whole list of tag definitions: the tags the document library offers in its tag picker, in the order it offers them. The list is a set of suggestions, not a constraint: [SetTagToDocument](../SetTagToDocument.md) still accepts any text, and tags already applied to documents are not changed by this call.

## Endpoint

```
/api/UIInternals/SetTagDefinitions
```

## Methods

- **GET** `/api/UIInternals/SetTagDefinitions?authenticationTicket=...&tagDefinitionsXml=...`
- **POST** `/api/UIInternals/SetTagDefinitions` (form data)

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `tagDefinitionsXml` | string | Yes | The whole new list, see below. An empty `<TagDefinitions />` empties the list. |

## The list

```xml
<TagDefinitions>
  <TagDefinition>Approved</TagDefinition>
  <TagDefinition>For Review</TagDefinition>
  <TagDefinition>Draft</TagDefinition>
</TagDefinitions>
```

- Every `TagDefinition` element is read, wherever it is, so the whole answer of [GetTagDefinitions](../GetTagDefinitions.md) can be sent back as it is.
- The order of the elements is the order the picker shows.
- Each text is trimmed. Blank entries are dropped, and so are repeats, compared case-insensitively, the first one kept.
- Each text must pass the rule `SetTagToDocument` applies to a tag: at most 128 characters, letters, digits, underscore, dash and space. The first text that does not is named in a `4000` refusal and nothing is saved.
- The list is replaced in one transaction: either the whole new list is saved or nothing changes.

## Response

### Success Response

```xml
<response success="true" />
```

### Error Response

```xml
<response success="false" error="[4000] not&lt;allowed&gt;: Invalid tag text specified." errorCode="4000" />
```

| errorCode | When |
|-----------|------|
| `4000` | Malformed XML, an empty parameter, or a tag text that `SetTagToDocument` would refuse |
| `4010` | No valid ticket (an anonymous session) |
| `4030` | The caller does not have the right described below |

## Required Permissions

The `UpdateApplicationSettingsAndPolicies` administrative right: the `sysadmin` account and members of `[Administrators]`. Anyone else is refused with `4030` and nothing changes.

## Example

### Request (POST)

```
POST /api/UIInternals/SetTagDefinitions HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&tagDefinitionsXml=%3CTagDefinitions%3E%3CTagDefinition%3EApproved%3C%2FTagDefinition%3E%3CTagDefinition%3EDraft%3C%2FTagDefinition%3E%3C%2FTagDefinitions%3E
```

## JavaScript

```javascript
// Read, add one, write the whole list back.
const current = await call('GetTagDefinitions', { authenticationTicket: ticket });
const tags = [...current.querySelectorAll('TagDefinition')].map(d => d.textContent);
tags.push('Needs Translation');

const xml = '<TagDefinitions>' +
  tags.map(t => `<TagDefinition>${t}</TagDefinition>`).join('') +
  '</TagDefinitions>';

await call('SetTagDefinitions', { authenticationTicket: ticket, tagDefinitionsXml: xml });
```

## Notes

- **Storage:** from 9.0 the list is the `TAGDEFINITIONS` table. Until then it was the file `config\tagdefs.xml`, read once at start-up, with no way to change it through the API. The 9.0 upgrade copies that file into the table and deletes it; an install with no file starts with the five tags the installer always shipped (Red, Green, Yellow, Black, White).
- **When the change shows:** at once on the server that took the call. Another server of a farm reads the table again when its own cached copy expires, within 15 minutes.
- **Applied tags are untouched:** removing a definition only takes it out of the picker; documents keep the tags they have.

## Related APIs

- [GetTagDefinitions](../GetTagDefinitions.md) - Get the list
- [SetTagToDocument](../SetTagToDocument.md) - Apply a tag to a document
- [RemoveTagFromDocument](../RemoveTagFromDocument.md) - Remove a tag from a document
