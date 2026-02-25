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

## Notes

- The `idpath` value contains folder IDs separated by `/`, ordered from the system root to the target folder.
- This API is useful for implementing breadcrumb navigation or resolving folder ancestry.
- To look up a folder ID from its path, use `GetFolder`.

---

## Related APIs

- [GetFolder](GetFolder) - Get folder metadata by path (returns the folder ID)
- [GetFolders](GetFolders) - List subfolders

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/GetParentFolderIDs*
