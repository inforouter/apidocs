# FolderExists API

Determines whether a folder exists at the specified path. Returns success if the path resolves to an existing folder, or an error if the folder is not found or cannot be accessed.

## Endpoint

```
/srv.asmx/FolderExists
```

## Methods

- **GET** `/srv.asmx/FolderExists?authenticationTicket=...&Path=...`
- **POST** `/srv.asmx/FolderExists` (form data)
- **SOAP** Action: `http://tempuri.org/FolderExists`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to check (e.g. `/Finance/Reports/2024`). |

---

## Response

### Success Response -" Folder Exists

```xml
<response success="true" />
```

### Error Response -" Folder Does Not Exist

```xml
<response error="Folder not found." />
```

The API returns `success="true"` if and only if the path resolves to an existing folder. If the folder does not exist, an error response is returned.

---

## Required Permissions

The calling user must be authenticated. The path must be accessible to the user.

---

## Example

### GET Request

```
GET /srv.asmx/FolderExists
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports/2024
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/FolderExists HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance/Reports/2024
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:FolderExists>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:Path>/Finance/Reports/2024</tns:Path>
    </tns:FolderExists>
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

Asks whether a path names a folder.

**It does not return a boolean.** A folder that is there is a plain success with nothing in it, and a
folder that is not is a `4041` failure. `success` is the answer; there is no `exists` attribute to
read, and a failure here is the expected result rather than a fault to report.

```javascript
async function folderExists(path) {
  const response = await fetch('/srv.asmx/FolderExists?' + new URLSearchParams({
    authenticationTicket: ticket, Path: path
  }));
  const root = new DOMParser().parseFromString(await response.text(), 'text/xml').documentElement;

  if (root.getAttribute('success') === 'true') return true;
  if (root.getAttribute('errorCode') === '4041') return false;

  throw new Error(`${root.getAttribute('errorCode')}: ${root.getAttribute('error')}`);
}
```

A document path is not a folder, so `FolderExists` on one answers `4041` just as a path that names
nothing at all does.

## Notes

- This API only checks for folders. To check for a document, use `DocumentExists`.
- The response does not include a `folderExists` attribute -" existence is indicated by whether `success="true"` or an error is returned.
- Use `FolderExists1` to check for a subfolder by parent path and folder name as separate parameters.

---

## Related APIs

- [FolderExists1](FolderExists1.md) - Check folder existence by parent path and name
- [DocumentExists](DocumentExists.md) - Check whether a document exists
- [GetFolder](GetFolder.md) - Retrieve folder properties
- [CreateFolder](CreateFolder.md) - Create a folder

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4041` | the path does not name a folder - including a path that names a document, and one the caller may not see |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |


| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Folder not found | The specified path does not resolve to an existing folder. |
| `SystemError:...` | An unexpected server-side error occurred. |

---