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

Asks whether the caller may do one thing to one folder.

**It answers by succeeding or failing, not with a boolean.** Allowed is a plain success; not allowed
is a failure. So a `4030` here is the answer to the question rather than a fault to report:

```javascript
async function allowed(action, path, actionId) {
  const response = await fetch(`/srv.asmx/${action}?` + new URLSearchParams({
    authenticationTicket: ticket, Path: path, ActionId: actionId
  }));
  const root = new DOMParser().parseFromString(await response.text(), 'text/xml').documentElement;

  if (root.getAttribute('success') === 'true') return true;
  if (root.getAttribute('errorCode') === '4030') return false;

  throw new Error(root.getAttribute('error'));      // 4041, 4000 - a real problem
}
```

Both answer for the **anonymous user** when there is no ticket, rather than refusing - which is what
makes them useful to an unauthenticated client deciding what to offer.

### The actions it takes

| `ActionId` | |
|---:|---|
| `2` | Delete folder |
| `5` | Add or change meta data |
| `6` | Remove meta data |
| `7` | Set folder rules |
| `10` | Change ownership |
| `11` | Change security |
| `17` | Change folder properties |
| `26` | Read security access list |
| `33` | Move this folder within this library |
| `34` | Move this folder outside of this library |
| `37` | Create document |
| `38` | Create folder |
| `41` | List folder contents |

Anything else - including `42`, read folder statistics, which is a real action elsewhere - is refused
`4000` with the list in the message.

Use [DocumentAccessAllowed](DocumentAccessAllowed.md) for documents; this one answers `4041` for a
document path, and the two take different sets of actions.

## Notes

- Passing an invalid `ActionId` returns a `success="false"` response with a message listing the valid action IDs.
- This API checks permissions for the **calling user** (identified by the `authenticationTicket`), not for an arbitrary user.
- To check document-level permissions, use `DocumentAccessAllowed`.

---

## Related APIs

- [DocumentAccessAllowed](DocumentAccessAllowed.md) - Check whether an action is allowed on a document
- [GetAccessList](GetAccessList.md) - Retrieve the full access list for a folder
- [SetAccessList](SetAccessList.md) - Set the access list for a folder

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4030` | the caller may not do that - this is the answer to the question, not a fault |
| `4000` | `ActionId` is not one this operation takes; the message lists the ones it does |
| `4041` | no folder at that path - including a document path |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Invalid ActionId | The provided `ActionId` is not valid for folders. Response includes the list of valid values. |
| Folder not found | The specified folder path does not exist. |
| `SystemError:...` | An unexpected server-side error occurred. |

---