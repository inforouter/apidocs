# GetAddInInfo API

Returns version and description information for the specified infoRouter client Add-in. Add-in clients (such as the Microsoft Word or Outlook add-ins) call this API at startup to check whether their installed version is current. You can also call it programmatically to verify whether a particular add-in has been deployed to the server and to read its published version metadata.

## Endpoint

```
/srv.asmx/GetAddInInfo
```

## Methods

- **GET** `/srv.asmx/GetAddInInfo?AddInName=...`
- **POST** `/srv.asmx/GetAddInInfo` (form data)
- **SOAP** Action: `http://tempuri.org/GetAddInInfo`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AddInName` | string | Yes | The name of the add-in to look up (e.g. `WORDADDIN`, `OUTLOOKADDIN`). The name is case-insensitive; the server converts it to uppercase before searching. Must match the name of an add-in directory deployed on the server. |

---

## Response

### Success Response

Returns a `<response>` element with `success="true"` and the add-in metadata as attributes. The `Name` attribute is always returned in uppercase.

```xml
<response success="true"
          Name="WORDADDIN"
          Version="8.1.150"
          DLLVersion="8.1.150.0"
          Description="infoRouter Word Add-in" />
```

### Response Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `Name` | string | The add-in name in uppercase, as stored on the server. |
| `Version` | string | The setup/installer version of the add-in (read from the `Version` key in `info.ini`). |
| `DLLVersion` | string | The assembly DLL version of the add-in (read from the `DLLVersion` key in `info.ini`). |
| `Description` | string | A human-readable description of the add-in (read from the `Description` key in `info.ini`). |

### Error Response -" Add-in Not Found

```xml
<response success="false" error="A request to check for a newer version of the infoRouter Add-in failed.\r\nThe add-in information could not be found on the server.\r\nPlease contact your Administrator." />
```

### Error Response -" Server Error

```xml
<response success="false" error="SystemError: ..." />
```

---

## Required Permissions

**No authentication is required.** This API does not accept an authentication ticket and can be called anonymously. It is intended for use by infoRouter client add-ins during their startup version check.

---

## Example

### GET Request

```
GET /srv.asmx/GetAddInInfo?AddInName=WORDADDIN HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetAddInInfo HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AddInName=WORDADDIN
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetAddInInfo>
      <tns:AddInName>WORDADDIN</tns:AddInName>
    </tns:GetAddInInfo>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- **Case-insensitive name**: The `AddInName` parameter is converted to uppercase before the server looks up the add-in directory. `wordaddin`, `WordAddin`, and `WORDADDIN` all resolve to the same directory.
- **No authentication ticket**: Unlike nearly all other infoRouter APIs, this endpoint does not require an `AuthenticationTicket`. It is designed to be called by the add-in before a user has logged in.
- **Server-side file location**: The add-in metadata is read from an `info.ini` file inside a subdirectory named after the add-in (uppercase) within the server's configured add-in path. If the directory or file does not exist the API returns the "not found" error message.
- **Non-standard error message**: When the add-in is not found, the error string is a literal multi-line message (using `\r\n` as line separators) intended to be displayed directly to the end user, rather than a numeric error code.
- **Version fields may be empty**: If `Version`, `DLLVersion`, or `Description` keys are absent from `info.ini` the corresponding attributes are returned as empty strings.

---

## Related APIs

- [GetAddInPart](GetAddInPart.md) - Download the add-in installation package (parts.zip) as a byte array

---

## Error Codes

| Error | Description |
|-------|-------------|
| `A request to check for a newer version of the infoRouter Add-in failed...` | The specified `AddInName` directory was not found on the server. |
| `SystemError:...` | An unexpected server-side error occurred. |
