# GetSubFoldersCount API

Returns the count of direct subfolders within the specified folder. This is a lightweight alternative to `GetFolderStatistics` when only the subfolder count is needed.

## Endpoint

```
/srv.asmx/GetSubFoldersCount
```

## Methods

- **GET** `/srv.asmx/GetSubFoldersCount?authenticationTicket=...&Path=...`
- **POST** `/srv.asmx/GetSubFoldersCount` (form data)
- **SOAP** Action: `http://tempuri.org/GetSubFoldersCount`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the folder (e.g. `/Finance/Reports`). |

---

## Response

### Success Response

```xml
<response success="true" SubFolderCount="5" />
```

### Error Response

```xml
<response error="Folder not found." />
```

| Attribute | Description |
|-----------|-------------|
| `success` | `"true"` if the count was retrieved successfully. |
| `SubFolderCount` | Number of direct subfolders in the specified folder. |

---

## Required Permissions

The calling user must have **read** permission on the folder.

---

## Example

### GET Request

```
GET /srv.asmx/GetSubFoldersCount
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetSubFoldersCount HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance/Reports
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetSubFoldersCount>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:Path>/Finance/Reports</tns:Path>
    </tns:GetSubFoldersCount>
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

Counts the direct subfolders of one folder - children only, not the whole tree.

```javascript
const root = await call('GetSubFoldersCount', {
  authenticationTicket: ticket,
  Path: '/Finance/Reports'
});

console.log(Number(root.getAttribute('SubFolderCount')));
```

For the documents as well, and the totals down the whole tree, use
[GetFolderStatistics](GetFolderStatistics.md).

## Notes

- Returns only the count of direct subfolders, not recursive subfolder counts.
- For full statistics including total document count and storage size, use `GetFolderStatistics`.

---

## Related APIs

- [GetFolderStatistics](GetFolderStatistics.md) - Get comprehensive folder statistics
- [GetFolders](GetFolders.md) - Get the list of subfolders

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4041` | no folder at that path - including one the caller may not see |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

A call with no ticket is not automatically refused: it signs in as the anonymous user, so a folder in
a library flagged as anonymous can be read without authenticating. The writes in this group refuse it
with `4010`.

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Folder not found | The specified path does not resolve to an existing folder. |
| Access denied | The user does not have read permission on the folder. |
| `SystemError:...` | An unexpected server-side error occurred. |

---