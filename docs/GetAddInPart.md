# GetAddInPart API

Downloads the installation package (a ZIP archive) for the specified infoRouter client Add-in. Add-in clients call this API to retrieve the latest version of their installation files so they can self-update. Unlike most infoRouter APIs, the response is **raw binary data** (the contents of `parts.zip`), not an XML document.

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

Returns the raw binary content of the add-in's `parts.zip` file. The response body is a ZIP archive containing the add-in installation files. There is no XML wrapper.

```
HTTP/1.1 200 OK
Content-Type: application/octet-stream

[binary ZIP data]
```

### Not Found / Error Response

When the add-in directory does not exist, `parts.zip` is not present inside it, or any server-side error occurs, the API returns a **single byte with value `0x00`** instead of throwing an error or returning XML. Callers must check the response length to distinguish a valid ZIP (typically many kilobytes) from this "not found" sentinel value.

```
HTTP/1.1 200 OK
Content-Type: application/octet-stream

[0x00]
```

> **Important:** This API never returns an HTTP error status code. Both success and failure always return HTTP 200. The only way to detect failure is to check whether the response body is a single zero byte.

---

## Required Permissions

**No authentication is required.** This API does not accept an authentication ticket and can be called anonymously. It is designed for use by infoRouter client add-ins during their self-update process.

---

## Example

### GET Request

```
GET /srv.asmx/GetAddInPart?AddInName=WORDADDIN HTTP/1.1
```

**Success response:** Binary stream of `parts.zip` contents.  
**Not-found response:** Single byte `0x00`.

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

## Notes

- **Binary response, not XML**: Unlike all other infoRouter APIs, `GetAddInPart` returns raw binary data. Do not attempt to parse the response as XML.
- **Case-insensitive name**: `AddInName` is converted to uppercase before lookup. `wordaddin`, `WordAddin`, and `WORDADDIN` all resolve to the same directory.
- **No authentication ticket**: This endpoint does not require an `AuthenticationTicket` and is intended to be called before a user session is established.
- **Sentinel zero byte on failure**: If the add-in directory or `parts.zip` does not exist -" or if an exception occurs -" the API returns a single `0x00` byte. The HTTP status code is still `200`. Always check the response length before treating the result as a ZIP archive.
- **Server-side file location**: The `parts.zip` file must be present inside a subdirectory named after the add-in (uppercase) within the server's configured add-in path. Use [GetAddInInfo](GetAddInInfo.md) first to verify the add-in is deployed before downloading its parts.
- **Self-update workflow**: The typical client flow is: (1) call `GetAddInInfo` to read the current server version, (2) compare with the locally installed version, (3) if the server version is newer, call `GetAddInPart` to download and install the update.

---

## Related APIs

- [GetAddInInfo](GetAddInInfo.md) - Get version and description metadata for a deployed client Add-in

---

## Error Codes

| Response | Description |
|----------|-------------|
| Single byte `0x00` | The specified add-in directory was not found, `parts.zip` does not exist in that directory, or a server-side exception occurred. |
