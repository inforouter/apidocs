# ApplyInheritedAccessList API

Applies the inherited (parent) access list to the specified document or folder, overwriting any custom security settings.

## Endpoint

```
/srv.asmx/ApplyInheritedAccessList
```

## Methods

- **GET** `/srv.asmx/ApplyInheritedAccessList?authenticationTicket=...&Path=...`
- **POST** `/srv.asmx/ApplyInheritedAccessList` (form data)
- **SOAP** Action: `http://tempuri.org/ApplyInheritedAccessList`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full path to the document or folder. |

---

## Response

### Success Response

```xml
<response success="true" error="" />
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

---

## Required Permissions

**Change security permission** on the target document or folder.

---

## Example

### GET Request

```
GET /srv.asmx/ApplyInheritedAccessList
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports/Q4Report.pdf
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/ApplyInheritedAccessList HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance/Reports/Q4Report.pdf
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:ApplyInheritedAccessList>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:Path>/Finance/Reports/Q4Report.pdf</tns:Path>
    </tns:ApplyInheritedAccessList>
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

Throws away an item's own access list so that it inherits the one above it again.

```javascript
await call('ApplyInheritedAccessList', {
  authenticationTicket: ticket,
  Path: '/Finance/Reports'
});

// InheritedSecurity is "true" again afterwards
```

The undo for [SetAccessList](SetAccessList.md). It takes a document as readily as a folder, and an
item that is already inheriting is a success rather than an error.

## Notes

- This operation removes any custom access list entries on the target item and reverts it to inherit security from its parent folder.
- For **documents**: the document's security is reset to inherited mode.
- For **folders**: the folder's security is reset to inherited mode.
- Once applied, the item's effective permissions will be determined by the nearest ancestor with a custom access list.
- To set a custom access list, use `SetAccessList`.
- To view the current access list, use `GetAccessList`.

---

## Related APIs

- [SetAccessList](SetAccessList.md) - Set a custom access list on a document or folder
- [GetAccessList](GetAccessList.md) - Retrieve the current access list
- [GetOwner](GetOwner.md) - Retrieve the owner of a document or folder

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | nothing at that path - including one the caller may not see |
| `4030` | the caller may not change security on this item |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Path not found | The specified document or folder does not exist. |
| Access denied | The calling user lacks permission to change security on this item. |
| `SystemError:...` | An unexpected server-side error occurred. |

---