# SetOwner API

Sets the owner of the document or folder at the specified path.

## Endpoint

```
/srv.asmx/SetOwner
```

## Methods

- **GET** `/srv.asmx/SetOwner?authenticationTicket=...&Path=...&NewOwnerUserName=...&ApplytoTree=...`
- **POST** `/srv.asmx/SetOwner` (form data)
- **SOAP** Action: `http://tempuri.org/SetOwner`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full path to the document or folder. |
| `NewOwnerUserName` | string | Yes | The username of the new owner. |
| `ApplytoTree` | bool | Yes | If `true` and the path is a folder, recursively sets the owner on all subfolders and documents. Ignored for documents. |

---

## Response

### Success Response

```xml
<response success="true" error="" />
```

### Partial Success Response (folder with tree apply)

When `ApplytoTree=true` and some items could not be updated, a multi-status response is returned:

```xml
<response success="false" error="Some items could not be updated">
  <logitem path="/Finance/Reports/locked.pdf" error="Document is locked" />
  <logitem path="/Finance/Reports/subfolder" error="Access denied" />
</response>
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

---

## Required Permissions

**Change ownership permission** (ActionId 10) on the target document or folder.

---

## Example

### GET Request (set owner on a single document)

```
GET /srv.asmx/SetOwner
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports/Q4Report.pdf
  &NewOwnerUserName=jsmith
  &ApplytoTree=false
HTTP/1.1
```

### GET Request (set owner recursively on a folder)

```
GET /srv.asmx/SetOwner
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports
  &NewOwnerUserName=jsmith
  &ApplytoTree=true
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/SetOwner HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance/Reports/Q4Report.pdf
&NewOwnerUserName=jsmith
&ApplytoTree=false
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:SetOwner>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:Path>/Finance/Reports/Q4Report.pdf</tns:Path>
      <tns:NewOwnerUserName>jsmith</tns:NewOwnerUserName>
      <tns:ApplytoTree>false</tns:ApplytoTree>
    </tns:SetOwner>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Setting the owner on a **document** ignores the `ApplytoTree` parameter.
- When `ApplytoTree=true` on a **folder**, the operation attempts to update every subfolder and document. If some items fail (e.g., due to locks or permissions), a multi-status response with `<logitem>` details is returned.
- The new owner user must exist and be an active (enabled) user account.
- To retrieve the current owner, use `GetOwner`.
- To transfer ownership in bulk (along with tasks, subscriptions, etc.), consider the `TransferUser*` family of APIs.

---

## Related APIs

- [GetOwner](GetOwner.md) - Retrieve the current owner of a document or folder
- [TransferUserDocumentOwnerships](TransferUserDocumentOwnerships.md) - Bulk-transfer document ownership from one user to another
- [TransferUserFolderOwnerships](TransferUserFolderOwnerships.md) - Bulk-transfer folder ownership from one user to another
- [GetAccessList](GetAccessList.md) - Retrieve the access list for a document or folder

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Path is required | The `Path` parameter was empty or null. |
| NewOwnerUserName is required | The `NewOwnerUserName` parameter was empty or null. |
| Path not found | The specified document or folder does not exist. |
| User not found | The specified `NewOwnerUserName` does not exist. |
| Access denied | The calling user lacks permission to change ownership. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/SetOwner*
