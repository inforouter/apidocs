# GetAddInPart API

Downloads the installation package (a ZIP archive) for the specified infoRouter client Add-in. Add-in clients call this API to retrieve the latest version of their installation files so they can self-update. Unlike most infoRouter APIs, the response is **raw binary data** (the contents of `parts.zip`), not an XML document.

> **Two things to know before calling this.**
>
> It takes **no authentication ticket** - there is no parameter for one - so the add-in's installer
> payload is served in full to any unauthenticated caller who can reach the server.
>
> The REST body is **a JSON string of base64**, not the bytes: it opens and closes with a double
> quote and is a third larger than the file. Decode it before saving, or what you save is not a
> zip. The SOAP form returns a proper `byte[]`.
>
> An add-in that is not installed is answered with a single zero byte - `"AA=="` - and HTTP 200,
> so there is no way to tell "no such add-in" from "an add-in with an empty parts file".

## Endpoint

```
/srv.asmx/GetAddInPart
```

## Methods

- **GET** `/srv.asmx/GetAddInPart?AddInName=...`
- **POST** `/srv.asmx/GetAddInPart` (form data)
- **SOAP** Action: `http://tempuri.org/GetAddInPart`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AddInName` | string | Yes | The name of the add-in whose installation package should be downloaded (e.g. `WORDADDIN`, `OUTLOOKADDIN`). The name is case-insensitive; the server converts it to uppercase before searching. Must match the name of an add-in directory deployed on the server. |

---

## Response

### Success Response

**Over REST the body is a JSON string of base64**, not the bytes: the action's return type is
`byte[]` and MVC's JSON formatter is what writes it, so the body opens and closes with a double
quote and is a third larger than the file. Decode it before saving, or what is saved is not a zip.

```
HTTP/1.1 200 OK
Content-Type: application/json

"UEsDBBQAAAAIAO...=="
```

Over SOAP the same operation returns a proper `byte[]`, base64 encoded by the SOAP serializer in
the usual way, so a SOAP client gets the file without doing anything special.

### Not Found / Error Response

When the add-in directory does not exist, `parts.zip` is not present inside it, or the name holds a
path, the failure is reported on the HTTP response. The body is the empty JSON string, as for the
document downloads, and the status and headers say what went wrong.

```
HTTP/1.1 404 Not Found
Content-Type: application/json
X-InfoRouter-ErrorCode: 4041
X-InfoRouter-Error: No add-in of that name is installed on this server.

""
```

Until 9.0 every one of those was **a single byte with value `0x00`** and HTTP 200 - over REST the
six character body `"AA=="` - so there was no way to tell "no such add-in" from "an add-in whose
parts file is empty", and nothing to report to whoever asked.

---

## Required Permissions

**No authentication is possible.** This API has no authentication ticket parameter, so every caller is anonymous - which means the add-in's installer payload is served in full to anybody who can reach the server. It is meant for infoRouter client add-ins updating themselves, before anyone has signed in; if that payload is not something the instance wants to hand out, the endpoint has to be blocked in front of the application.

---

## Example

### GET Request

```
GET /srv.asmx/GetAddInPart?AddInName=WORDADDIN HTTP/1.1
```

**Success response:** a JSON string of base64 holding the `parts.zip` contents, HTTP 200.  
**Not-found response:** the empty JSON string `""`, HTTP 404, with the error in the headers.

### POST Request

```
POST /srv.asmx/GetAddInPart HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AddInName=WORDADDIN
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetAddInPart>
      <tns:AddInName>WORDADDIN</tns:AddInName>
    </tns:GetAddInPart>
  </soap:Body>
</soap:Envelope>
```

**SOAP response:** The byte array is returned inside the SOAP response body as a base64-encoded element.

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

Downloads one add-in's `parts.zip`.

```javascript
// No ticket, and the body is a JSON string of base64 rather than the bytes.
const response = await fetch(`/srv.asmx/GetAddInPart?${new URLSearchParams({ AddInName: 'OFFICEADDIN2017' })}`);
const base64 = JSON.parse(await response.text());          // strips the surrounding quotes
const bytes = Uint8Array.from(atob(base64), c => c.charCodeAt(0));

if (bytes.length <= 1) {
  throw new Error('no such add-in, or it ships no parts file');
}
```

## Notes

- **Binary response, not XML**: Unlike all other infoRouter APIs, `GetAddInPart` returns raw binary data. Do not attempt to parse the response as XML.
- **Case-insensitive name**: `AddInName` is converted to uppercase before lookup. `wordaddin`, `WordAddin`, and `WORDADDIN` all resolve to the same directory.
- **No authentication ticket**: this endpoint has no `AuthenticationTicket` parameter and is intended to be called before a user session is established. [GetAddIns](GetAddIns.md), which lists the same add-ins, does take one.
- **Failures are on the HTTP response**: if the add-in directory or `parts.zip` does not exist, the status is `404` and `X-InfoRouter-ErrorCode` is `4041`. Until 9.0 the answer was a single `0x00` byte with HTTP 200, so callers had to check the decoded length.
- **Server-side file location**: The `parts.zip` file must be present inside a subdirectory named after the add-in (uppercase) within the server's configured add-in path. Use [GetAddInInfo](GetAddInInfo.md) first to verify the add-in is deployed before downloading its parts.
- **Self-update workflow**: The typical client flow is: (1) call `GetAddInInfo` to read the current server version, (2) compare with the locally installed version, (3) if the server version is newer, call `GetAddInPart` to download and install the update.

---

## Related APIs

- [GetAddInInfo](GetAddInInfo.md) - Get version and description metadata for a deployed client Add-in

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `HTTP 400` | `AddInName` was empty; refused by model binding |
| `*none*` | every other case answers HTTP 200 - there is no error document, see the warning above |

| Response | Description |
|----------|-------------|
| Single byte `0x00` | The specified add-in directory was not found, `parts.zip` does not exist in that directory, or a server-side exception occurred. |
