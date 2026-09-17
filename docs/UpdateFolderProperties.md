# UpdateFolderProperties API

Updates the name and/or description of the specified folder. The folder itself must already exist; only its metadata is changed.

## Endpoint

```
/srv.asmx/UpdateFolderProperties
```

## Methods

- **GET** `/srv.asmx/UpdateFolderProperties?authenticationTicket=...&Path=...&NewFolderName=...&NewDescription=...`
- **POST** `/srv.asmx/UpdateFolderProperties` (form data)
- **SOAP** Action: `http://tempuri.org/UpdateFolderProperties`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the existing folder (e.g. `/Finance/Reports`). |
| `NewFolderName` | string | Yes | New name for the folder. Unlike folder creation, which sanitises silently, an unusable name is **refused** here with `4000`. Empty, or nothing but spaces, is refused by model binding with HTTP 400. |
| `NewDescription` | string | No | New description for the folder. Pass empty string or null to clear the description. |

---

## Response

### Success Response

```xml
<response success="true" error="" />
```

### Error Response

```xml
<response success="false" error="Folder not found." />
```

---

## Required Permissions

The calling user must have **write** (modify) permission on the folder.

---

## Example

### GET Request

```
GET /srv.asmx/UpdateFolderProperties
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports
  &NewFolderName=Financial Reports
  &NewDescription=All financial reports including quarterly and annual summaries
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/UpdateFolderProperties HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance/Reports
&NewFolderName=Financial Reports
&NewDescription=All financial reports including quarterly and annual summaries
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:UpdateFolderProperties>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:Path>/Finance/Reports</tns:Path>
      <tns:NewFolderName>Financial Reports</tns:NewFolderName>
      <tns:NewDescription>All financial reports including quarterly and annual summaries</tns:NewDescription>
    </tns:UpdateFolderProperties>
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

Renames a folder and sets its description. Both are written every time: there is no way to change one
and leave the other, so a caller changing the name has to send the current description back with it or
it is cleared.

```javascript
// Read what is there, change one thing, write both back.
const folder = (await call('GetFolder', {
  authenticationTicket: ticket, Path: '/Finance/Reports',
  WithRules: false, withPropertySets: false, withSecurity: false, withOwner: false
})).querySelector('folder');

await call('UpdateFolderProperties', {
  authenticationTicket: ticket,
  Path: '/Finance/Reports',
  NewFolderName: 'Quarterly Reports',
  NewDescription: folder.getAttribute('Description')
});
```

**It refuses a name that [CreateFolder1](CreateFolder1.md) would have cleaned up.** Creating a folder
called `Q3*` silently produces `Q3_`; renaming an existing folder to `Q3*` is answered `4000` with a
message naming the characters a folder may not carry. The two disagree, so a client that creates and
renames with the same name-building code will find one path works and the other does not.

An empty `NewFolderName`, or one of nothing but spaces, is refused by model binding with HTTP 400.
`NewDescription` may be empty; that clears the description.

## Notes

- Renaming a folder changes the folder's path. Any references to the old path will need to be updated.
- The folder name is sanitized: carriage returns and line feeds are stripped.
- The description supports multi-line text; line ending characters are normalized.
- To change folder rules, use `SetFolderRules`.

---

## Related APIs

- [GetFolder](GetFolder.md) - Retrieve current folder name and description
- [SetFolderRules](SetFolderRules.md) - Update folder behavior rules
- [CreateFolder](CreateFolder.md) - Create a new folder

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all - the anonymous user is told "Anonymous users cannot perform this action" |
| `4041` | no folder at that path - including one the caller may not see |
| `4090` | a folder of that name is already in the parent |
| `4000` | `NewFolderName` carries one of `/ \ : * ? " < > | # % & +` or a tab |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Folder not found | The specified path does not resolve to an existing folder. |
| Access denied | The user does not have write permission on the folder. |
| `SystemError:...` | An unexpected server-side error occurred. |

---