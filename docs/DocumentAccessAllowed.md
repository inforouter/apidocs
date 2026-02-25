# DocumentAccessAllowed API

Returns whether the currently authenticated user is allowed to perform the specified action on a given document.

## Endpoint

```
/srv.asmx/DocumentAccessAllowed
```

## Methods

- **GET** `/srv.asmx/DocumentAccessAllowed?authenticationTicket=...&Path=...&ActionId=...`
- **POST** `/srv.asmx/DocumentAccessAllowed` (form data)
- **SOAP** Action: `http://tempuri.org/DocumentAccessAllowed`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full path to the document to check. |
| `ActionId` | int | Yes | The action to check. See valid values below. |

### Valid ActionId Values

| ActionId | Action |
|----------|--------|
| `4` | Check out document |
| `5` | Add/Change metadata |
| `6` | Remove metadata |
| `8` | Change document properties |
| `10` | Change ownership |
| `11` | Change security |
| `23` | Read document |
| `26` | Read security access list |
| `46` | Read unpublished documents |

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

A `success="true"` response means the calling user **has** the specified permission on the document. A `success="false"` response means the user **does not** have that permission, or an error occurred.

---

## Required Permissions

Any authenticated user. The response reflects the calling user's own permissions.

---

## Example

### GET Request (check if user can read a document)

```
GET /srv.asmx/DocumentAccessAllowed
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports/Q4Report.pdf
  &ActionId=23
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/DocumentAccessAllowed HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance/Reports/Q4Report.pdf
&ActionId=23
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:DocumentAccessAllowed>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:Path>/Finance/Reports/Q4Report.pdf</tns:Path>
      <tns:ActionId>23</tns:ActionId>
    </tns:DocumentAccessAllowed>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Passing an invalid `ActionId` returns a `success="false"` response with a message listing the valid action IDs.
- This API checks permissions for the **calling user** (identified by the `authenticationTicket`), not for an arbitrary user.
- To check folder-level permissions, use `FolderAccessAllowed`.

---

## Related APIs

- [FolderAccessAllowed](FolderAccessAllowed.md) - Check whether an action is allowed on a folder
- [GetAccessList](GetAccessList.md) - Retrieve the full access list for a document
- [SetAccessList](SetAccessList.md) - Set the access list for a document

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Invalid ActionId | The provided `ActionId` is not valid for documents. Response includes the list of valid values. |
| Document not found | The specified document path does not exist. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/DocumentAccessAllowed*
