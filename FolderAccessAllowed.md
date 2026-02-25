# FolderAccessAllowed API

Returns whether the currently authenticated user is allowed to perform the specified action on a given folder.

## Endpoint

```
/srv.asmx/FolderAccessAllowed
```

## Methods

- **GET** `/srv.asmx/FolderAccessAllowed?authenticationTicket=...&Path=...&ActionId=...`
- **POST** `/srv.asmx/FolderAccessAllowed` (form data)
- **SOAP** Action: `http://tempuri.org/FolderAccessAllowed`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full path to the folder to check. |
| `ActionId` | int | Yes | The action to check. See valid values below. |

### Valid ActionId Values

| ActionId | Action |
|----------|--------|
| `2` | Delete folder |
| `5` | Add/Change metadata |
| `6` | Remove metadata |
| `7` | Set folder rules |
| `10` | Change ownership |
| `11` | Change security |
| `17` | Change folder properties |
| `26` | Read security access list |
| `33` | Move folder within library |
| `34` | Move folder outside library |
| `37` | Create document |
| `38` | Create folder |
| `41` | List folder contents |

---

## Response

### Access Allowed

```xml
<response success="true" error="" />
```

### Access Denied or Error

```xml
<response success="false" error="Access denied" />
```

A `success="true"` response means the calling user **has** the specified permission on the folder. A `success="false"` response means the user **does not** have that permission, or an error occurred.

---

## Required Permissions

Any authenticated user. The response reflects the calling user's own permissions.

---

## Example

### GET Request (check if user can create documents in a folder)

```
GET /srv.asmx/FolderAccessAllowed
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports
  &ActionId=37
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/FolderAccessAllowed HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance/Reports
&ActionId=37
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:FolderAccessAllowed>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:Path>/Finance/Reports</tns:Path>
      <tns:ActionId>37</tns:ActionId>
    </tns:FolderAccessAllowed>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Passing an invalid `ActionId` returns a `success="false"` response with a message listing the valid action IDs.
- This API checks permissions for the **calling user** (identified by the `authenticationTicket`), not for an arbitrary user.
- To check document-level permissions, use `DocumentAccessAllowed`.

---

## Related APIs

- [DocumentAccessAllowed](DocumentAccessAllowed) - Check whether an action is allowed on a document
- [GetAccessList](GetAccessList) - Retrieve the full access list for a folder
- [SetAccessList](SetAccessList) - Set the access list for a folder

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Invalid ActionId | The provided `ActionId` is not valid for folders. Response includes the list of valid values. |
| Folder not found | The specified folder path does not exist. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/FolderAccessAllowed*
