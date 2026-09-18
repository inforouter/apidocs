# GetAddInInfo API

Returns version and description information for the specified infoRouter client Add-in. Add-in clients (such as the Microsoft Word or Outlook add-ins) call this API at startup to check whether their installed version is current. You can also call it programmatically to verify whether a particular add-in has been deployed to the server and to read its published version metadata.

> **This operation takes no authentication ticket.** There is no parameter for one, so every
> caller is anonymous and the installed add-ins and their versions can be read by anybody who can
> reach the server. [GetAddIns](GetAddIns.md), which lists the same facts, does take a ticket.

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

The version and description of one add-in.

```javascript
// No ticket: this operation has no authenticationTicket parameter.
const response = await fetch(`/srv.asmx/GetAddInInfo?${new URLSearchParams({ AddInName: 'SCANSTATION' })}`);
const root = new DOMParser().parseFromString(await response.text(), 'text/xml').documentElement;

root.getAttribute('Name');          // upper cased, whatever case was asked for
root.getAttribute('Version');
root.getAttribute('DLLVersion');
root.getAttribute('Description');
```

This is what a client calls to find out whether the copy it has is current. The name is upper
cased before the folder is looked for, so case does not matter.

## Notes

- **Case-insensitive name**: The `AddInName` parameter is converted to uppercase before the server looks up the add-in directory. `wordaddin`, `WordAddin`, and `WORDADDIN` all resolve to the same directory.
- **No authentication ticket**: unlike nearly all other infoRouter APIs, this endpoint has no `AuthenticationTicket` parameter at all, so the installed add-ins and their versions can be read by anybody who can reach the server. It is designed to be called by the add-in before a user has logged in. [GetAddIns](GetAddIns.md), which lists the same facts, does take a ticket.
- **Server-side file location**: The add-in metadata is read from an `info.ini` file inside a subdirectory named after the add-in (uppercase) within the server's configured add-in path. If the directory or file does not exist the API returns the "not found" error message.
- **Non-standard error message**: When the add-in is not found, the error string is a literal multi-line message (using `\r\n` as line separators) intended to be displayed directly to the end user, rather than a numeric error code.
- **Version fields may be empty**: If `Version`, `DLLVersion`, or `Description` keys are absent from `info.ini` the corresponding attributes are returned as empty strings.

---

## Related APIs

- [GetAddInPart](GetAddInPart.md) - Download the add-in installation package (parts.zip) as a byte array

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4041` | no add-in folder by that name |
| `4000` | `AddInName` contains a path - a name holding `..` or a separator is refused |
| `HTTP 400` | `AddInName` was empty; refused by model binding, so there is no error document |

The not-found message carries its line breaks as the literal characters `\r\n` rather than as
line breaks, so a client that shows it shows the backslashes.
