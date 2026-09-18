# GetTagDefinitions API

Returns the list of all tag definitions configured in the infoRouter system. Tags are predefined text labels that can be applied to documents for categorisation, filtering, and search. Use this API to retrieve the available tag values before calling `SetTagToDocument`, or to populate a tag picker in your integration.

## Endpoint

```
/srv.asmx/GetTagDefinitions
```

## Methods

- **GET** `/srv.asmx/GetTagDefinitions?AuthenticationTicket=...`
- **POST** `/srv.asmx/GetTagDefinitions` (form data)
- **SOAP** Action: `http://tempuri.org/GetTagDefinitions`

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
GET /srv.asmx/GetTagDefinitions
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetTagDefinitions HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetTagDefinitions>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
    </tns:GetTagDefinitions>
  </soap:Body>
</soap:Envelope>
```

---

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

Lists the tags the instance suggests.

```javascript
const root = await call('GetTagDefinitions', { authenticationTicket: ticket });
const suggestions = [...root.querySelectorAll('TagDefinition')].map(d => d.textContent);
```

**The list is a set of suggestions, not a constraint.**
[SetTagToDocument](SetTagToDocument.md) takes any text, and applying one that is not on the list
neither fails nor adds to it. Nothing in this API changes the list.

## Notes

- **Server-Side Configuration:** Tag definitions are loaded from the server-side configuration file `config/tagdefs.xml` when the infoRouter service starts. Changes to the tag list require a server-side configuration update and a service restart; they cannot be managed via the API.
- **Tag Text is Case-Sensitive:** Tag values are returned exactly as configured. When calling `SetTagToDocument` or `RemoveTagFromDocument`, use the tag text exactly as returned by this API.
- **Read-Only:** This API only reads the tag list. To apply a tag to a document use `SetTagToDocument`; to remove a tag use `RemoveTagFromDocument`.
- **Replaces GetTagDefintions:** This API replaces the older [GetTagDefintions](GetTagDefintions.md) endpoint (which contained a typo in its name). Both endpoints return identical results; existing integrations using the old name will continue to work.

---

## Related APIs

- [SetTagToDocument](SetTagToDocument.md) - Apply a tag to the latest version of a document
- [RemoveTagFromDocument](RemoveTagFromDocument.md) - Remove a tag from a document

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
