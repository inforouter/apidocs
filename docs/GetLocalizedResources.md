# GetLocalizedResources API

Returns the localized display strings for the specified infoRouter resource IDs. infoRouter stores all UI text, error messages, and label strings in an internal resource table keyed by integer ID. Client add-ins and integrations call this API to retrieve human-readable, language-aware strings -" for example, to display status labels or error messages in the user's configured language. If an authentication ticket is provided, the strings are returned in the language configured for that user's session; without a ticket the server's default language is used.

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
| `resourceIds` | string | Yes | Comma-separated list of integer resource IDs whose localized strings should be returned (e.g. `1001,1002,2730`). Non-numeric entries and IDs that do not exist in the resource table are silently ignored. Duplicate IDs are deduplicated. |

---

## Response

### Success Response

Returns a `<response success="true">` element containing a `<Resources>` child with one `<Res>` element per valid, resolved ID.

```xml
<response success="true">
  <Resources>
    <Res>
      <Id>1001</Id>
      <Value>Document not found.</Value>
    </Res>
    <Res>
      <Id>2730</Id>
      <Value>Insufficient rights. Anonymous users cannot perform this action.</Value>
    </Res>
  </Resources>
</response>
```

### Empty Result

If `resourceIds` contains no valid integers, or all supplied IDs are invalid, the `<Resources>` element is returned empty.

```xml
<response success="true">
  <Resources />
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
| `Res/Id` | The integer resource ID as supplied in the request. |
| `Res/Value` | The localised string for this resource ID in the language of the session (or the server default language if no ticket was provided). |

---

## Required Permissions

**No elevated permissions required.** The API can be called with or without an authentication ticket. An invalid or expired ticket will return an authentication error. Unauthenticated callers receive strings in the server's default language.

---

## Example

### GET Request

```
GET /srv.asmx/GetLocalizedResources
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &resourceIds=1001,2730,9999
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetLocalizedResources HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&resourceIds=1001,2730,9999
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetLocalizedResources>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:resourceIds>1001,2730,9999</tns:resourceIds>
    </tns:GetLocalizedResources>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- **Language selection**: The language used to look up resource strings is determined by the authenticated user's session. If no ticket is provided, the server's installed default language is used.
- **Silent filtering**: Non-numeric values in `resourceIds` and IDs that do not resolve to a string are silently discarded. No error is returned for unrecognised IDs -" the `<Resources>` list simply omits them.
- **Deduplication**: If the same ID appears more than once in `resourceIds`, it is returned only once in the response.
- **Order not guaranteed**: The order of `<Res>` elements in the response may not match the order the IDs were supplied.
- **Resource IDs are internal**: The integer IDs correspond to infoRouter's internal string resource table. They are typically known to the infoRouter client SDK or determined by examining API error responses from other endpoints.
- **Empty `resourceIds`**: Passing an empty string returns a successful response with an empty `<Resources />` element.

---

## Related APIs

- [GetAddInInfo](GetAddInInfo.md) - Get version metadata for a deployed client Add-in (also language-neutral system info)

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | The supplied ticket is invalid. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `SystemError:...` | An unexpected server-side error occurred. |
