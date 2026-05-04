# GetTagDefintions API

> **Obsolete:** This API name contains a typo (`Defintions` instead of `Definitions`). It is kept for backward compatibility only. Use **[GetTagDefinitions](GetTagDefinitions.md)** for all new integrations.

Returns the list of all tag definitions configured in the infoRouter system. Tags are predefined text labels that can be applied to documents for categorisation, filtering, and search.

## Endpoint

```
/srv.asmx/GetTagDefintions
```

## Methods

- **GET** `/srv.asmx/GetTagDefintions?AuthenticationTicket=...`
- **POST** `/srv.asmx/GetTagDefintions` (form data)
- **SOAP** Action: `http://tempuri.org/GetTagDefintions`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |

---

## Response

### Success Response

Returns a `<response>` element with `success="true"` containing a `<TagDefinitions>` element with zero or more `<TagDefinition>` child elements. Each `<TagDefinition>` element's text content is the tag label string.

```xml
<response success="true" error="">
  <TagDefinitions>
    <TagDefinition>Approved</TagDefinition>
    <TagDefinition>For Review</TagDefinition>
    <TagDefinition>Draft</TagDefinition>
    <TagDefinition>Confidential</TagDefinition>
    <TagDefinition>Final</TagDefinition>
  </TagDefinitions>
</response>
```

### No Tags Configured Response

```xml
<response success="true" error="">
  <TagDefinitions />
</response>
```

### Error Response

```xml
<response success="false" error="[900] Authentication failed." />
```

---

## Required Permissions

Any **authenticated user** with a valid ticket may call this API. No additional permissions are required.

---

## Notes

- **Obsolete:** Use [GetTagDefinitions](GetTagDefinitions.md) for all new integrations. This endpoint is retained only for backward compatibility with existing integrations.
- **Tag Text is Case-Sensitive:** Tag values are returned exactly as configured. Use the tag text exactly as returned when calling `SetTagToDocument` or `RemoveTagFromDocument`.
- **Read-Only:** This API only reads the tag list.

---

## Related APIs

- [GetTagDefinitions](GetTagDefinitions.md) - Correctly-spelled replacement for this API
- [SetTagToDocument](SetTagToDocument.md) - Apply a tag to the latest version of a document
- [RemoveTagFromDocument](RemoveTagFromDocument.md) - Remove a tag from a document

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `SystemError:...` | An unexpected server-side error occurred. |
