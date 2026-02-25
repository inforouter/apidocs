# GetTagDefintions API

> **Note:** The API method name contains a typo (`Defintions` instead of `Definitions`). This is the canonical name and must be used exactly as shown.

Returns the list of all tag definitions configured in the infoRouter system. Tags are predefined text labels that can be applied to documents for categorisation, filtering, and search. Use this API to retrieve the available tag values before calling `SetTagToDocument`, or to populate a tag picker in your integration.

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

When no tags have been configured in the system:

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

Any **authenticated user** with a valid ticket may call this API. No additional permissions are required. The tag definitions are system-level configuration and are readable by all authenticated users.

---

## Example

### GET Request

```
GET /srv.asmx/GetTagDefintions
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetTagDefintions HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetTagDefintions>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
    </tns:GetTagDefintions>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- **Server-Side Configuration**: Tag definitions are loaded from the server-side configuration file `config/tagdefs.xml` when the infoRouter service starts. Changes to the tag list require a server-side configuration update and a service restart; they cannot be managed via the API.
- **Tag Text is Case-Sensitive**: Tag values are returned exactly as configured. When calling `SetTagToDocument` or `RemoveTagFromDocument`, use the tag text exactly as returned by this API.
- **Read-Only**: This API only reads the tag list. To apply a tag to a document use `SetTagToDocument`; to remove a tag use `RemoveTagFromDocument`.
- **Typo in Method Name**: The API method is named `GetTagDefintions` (missing the second `i` in "Definitions"). This is a known issue and the misspelling must be used in all calls.

---

## Related APIs

- [SetTagToDocument](SetTagToDocument.md) - Apply a tag to the latest version of a document
- [RemoveTagFromDocument](RemoveTagFromDocument.md) - Remove a tag from a document

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `SystemError:...` | An unexpected server-side error occurred (e.g. tag definitions file is missing or corrupt). |

---
