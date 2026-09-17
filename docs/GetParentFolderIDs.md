# GetParentFolderIDs API

Returns the chain of parent folder IDs for the specified folder, from the root down to the folder's immediate parent. This is useful for building breadcrumb navigation or resolving a folder's full ancestry.

## Endpoint

```
/srv.asmx/GetParentFolderIDs
```

## Methods

- **GET** `/srv.asmx/GetParentFolderIDs?authenticationTicket=...&FolderID=...`
- **POST** `/srv.asmx/GetParentFolderIDs` (form data)
- **SOAP** Action: `http://tempuri.org/GetParentFolderIDs`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `FolderID` | int | Yes | The internal folder ID to look up the parent chain for. Use `GetFolder` to obtain a folder's ID from its path. |

---

## Response

### Success Response

```xml
<response success="true" idpath="10/25/100/456" />
```

### Error Response

```xml
<response error="[901] Session expired or Invalid ticket" />
```

| Attribute | Description |
|-----------|-------------|
| `success` | `"true"` if the ID path was resolved. |
| `idpath` | A forward-slash-separated string of folder IDs from the root to the specified folder (e.g. `"10/25/100/456"`). |

---

## Required Permissions

The calling user must be authenticated.

---

## Example

### GET Request

```
GET /srv.asmx/GetParentFolderIDs
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &FolderID=456
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetParentFolderIDs HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&FolderID=456
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetParentFolderIDs>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:FolderID>456</tns:FolderID>
    </tns:GetParentFolderIDs>
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

Reports where a folder sits, as a comma-separated chain of folder ids running from its library down
to and **including the folder itself**.

```javascript
const root = await call('GetParentFolderIDs', {
  authenticationTicket: ticket,
  FolderID: 1329
});

const chain = root.getAttribute('idpath').split(',');   // e.g. ["1001", "1329"]
const parents = chain.slice(0, -1);                     // the folder's own id is the last entry
```

**A folder that does not exist is not an error.** The answer is `success="true"` with `idpath=""`, and
`FolderID=0` gives the same, so a caller cannot tell "no such folder" from a valid empty chain by
looking at `success`. Check for an empty `idpath` as well.

## Notes

- The `idpath` value contains folder IDs separated by `/`, ordered from the system root to the target folder.
- This API is useful for implementing breadcrumb navigation or resolving folder ancestry.
- To look up a folder ID from its path, use `GetFolder`.

---

## Related APIs

- [GetFolder](GetFolder.md) - Get folder metadata by path (returns the folder ID)
- [GetFolders](GetFolders.md) - List subfolders

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `none` | an id that does not exist, and `0`, are answered `success="true"` with an empty `idpath` rather than a failure |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `SystemError:...` | An unexpected server-side error occurred. |

---