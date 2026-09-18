# GetLocalizedResources API

Returns the localized display strings for the named message resources. infoRouter keeps its UI text, error messages and labels in the `IRBase.Messages` resource set, whose keys are **names** - `AccessDenied`, `Abort`, `DocumentNotFound` - and this operation looks a comma separated list of those names up in the language of the caller's session. Client add-ins and integrations call it so that their own screens read in the same language as the rest of infoRouter. Without a ticket the server's default language is used.

> **`resourceIds` takes resource *names*, not numbers**, despite what the parameter is called.
> The lookup is done against the `IRBase.Messages` resource set, whose keys are names such as
> `AccessDenied` and `Abort`. A numeric id resolves to nothing.
>
> **"Nothing" is reported as the string `-`, inside a successful response.** A name that does not
> resolve is still returned, with `-` as its value, which a caller cannot tell from a resource
> whose text is really a dash.
>
> **Spaces are not trimmed.** The list is split on commas and nothing else, so
> `AccessDenied, Abort` looks up `" Abort"` with its leading space and gets `-`.

## Endpoint

```
/srv.asmx/GetLocalizedResources
```

## Methods

- **GET** `/srv.asmx/GetLocalizedResources?authenticationTicket=...&resourceIds=...`
- **POST** `/srv.asmx/GetLocalizedResources` (form data)
- **SOAP** Action: `http://tempuri.org/GetLocalizedResources`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | No | Authentication ticket obtained from `AuthenticateUser`. Optional -" if omitted, the server's default language is used. If supplied, the returned strings are localised to the language of the user's session. |
| `resourceIds` | string | Yes | Comma-separated list of resource **names** (e.g. `AccessDenied,Abort,DocumentNotFound`). Despite the parameter name these are not numbers: a numeric id resolves to nothing. Write the list with no spaces after the commas - nothing is trimmed. A name that does not resolve is still returned, with `-` as its value. Duplicates are returned once per entry. Required: an empty list is refused with HTTP 400. |

---

## Response

### Success Response

Returns a `<response success="true">` element containing a `<Resources>` child with one `<Res>` element per entry asked for, resolved or not, in the order they were given.

```xml
<response success="true">
  <Resources>
    <Res>
      <ResourceName>DocumentNotFound</ResourceName>
      <Value>Document not found.</Value>
    </Res>
    <Res>
      <ResourceName>InsufficientRightsAnonymousUsers</ResourceName>
      <Value>Insufficient rights. Anonymous users cannot perform this action.</Value>
    </Res>
  </Resources>
</response>
```

### Names that do not resolve

A name the resource set does not have is **not** left out: it comes back with `-` as its value,
inside a successful response. There is no way to tell that apart from a resource whose text really
is a dash.

```xml
<response success="true">
  <Resources>
    <Res>
      <ResourceName>NoSuchKey</ResourceName>
      <Value>-</Value>
    </Res>
  </Resources>
</response>
```

### Error Response

```xml
<response success="false" error="[901] Session expired or Invalid ticket" />
```

### Response Element Reference

| Element / Attribute | Description |
|---------------------|-------------|
| `Resources` | Container element holding one `<Res>` child per returned resource. |
| `Res/ResourceName` | The resource name exactly as supplied in the request, including any leading space. |
| `Res/Value` | The localised string in the language of the session, or the server default language if no ticket was provided. `-` when the name is not a resource. |

---

## Required Permissions

**No elevated permissions required.** The API can be called with or without an authentication ticket. An invalid or expired ticket will return an authentication error. Unauthenticated callers receive strings in the server's default language.

---

## Example

### GET Request

```
GET /srv.asmx/GetLocalizedResources
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &resourceIds=AccessDenied,Abort,NoSuchKey
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetLocalizedResources HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&resourceIds=AccessDenied,Abort,NoSuchKey
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetLocalizedResources>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:resourceIds>AccessDenied,Abort,NoSuchKey</tns:resourceIds>
    </tns:GetLocalizedResources>
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

Looks up message resources by name and returns them in the caller's language.

```javascript
const root = await call('GetLocalizedResources', {
  authenticationTicket: ticket,
  resourceIds: 'AccessDenied,Abort,DocumentNotFound',   // names, not numbers; no spaces
});

const strings = Object.fromEntries(
  [...root.querySelectorAll('Res')].map(r => [
    r.querySelector('ResourceName').textContent,
    r.querySelector('Value').textContent,
  ]));

strings.AccessDenied;   // "Access denied." - or "-" if the name is not a resource
```

## Notes

- **Language selection**: The language used to look up resource strings is determined by the authenticated user's session. If no ticket is provided, the server's installed default language is used.
- **Nothing is filtered out**: a name that does not resolve is returned with the value `-`. Empty entries between commas are dropped, so `Abort,,,Abstract` returns two resources.
- **No deduplication**: a name given twice is returned twice.
- **Order is kept**: the `<Res>` elements come back in the order the names were given.
- **Resource names are internal**: they are the keys of `IRBase.Messages`, shipped with the server. There is no operation that lists them; take the ones you need from the SDK or from the source.
- **Empty `resourceIds`**: refused with HTTP 400 before the operation is reached - the parameter is declared without a question mark, so there is no way to ask for none.

---

## Related APIs

- [GetAddInInfo](GetAddInInfo.md) - Get version metadata for a deployed client Add-in (also language-neutral system info)

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `HTTP 400` | `resourceIds` was empty; refused by model binding, so there is no way to ask for none |

Empty entries between commas are dropped, so `Abort,,,Abstract` returns two resources. A name
given twice is returned twice - nothing removes a repeat - and the order is the order asked for.
