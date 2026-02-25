# EmptyRecycleBin API

Permanently deletes all items in the Recycle Bin of the currently authenticated user. Once emptied, the items cannot be recovered. Use this API to programmatically clean up a user's recycle bin as part of maintenance routines or end-of-period housekeeping.

## Endpoint

```
/srv.asmx/EmptyRecycleBin
```

## Methods

- **GET** `/srv.asmx/EmptyRecycleBin?AuthenticationTicket=...`
- **POST** `/srv.asmx/EmptyRecycleBin` (form data)
- **SOAP** Action: `http://tempuri.org/EmptyRecycleBin`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. The recycle bin emptied is always that of the user who owns this ticket. |

---

## Response

### Success Response

```xml
<response success="true" error="" />
```

### Error Response

```xml
<response success="false" error="[901] Session expired or Invalid ticket." />
```

---

## Required Permissions

Any authenticated user can empty their own Recycle Bin. A user cannot empty another user's Recycle Bin -" the operation is always scoped to the authenticated user identified by the ticket.

---

## Example

### GET Request

```
GET /srv.asmx/EmptyRecycleBin
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/EmptyRecycleBin HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:EmptyRecycleBin>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
    </tns:EmptyRecycleBin>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- **Irreversible**: Once the recycle bin is emptied, all deleted documents and folders are permanently removed and cannot be recovered.
- **Current User Only**: The API operates solely on the recycle bin of the user who owns the authentication ticket. There is no parameter to target another user's recycle bin.
- **Empty Bin is Not an Error**: If the recycle bin is already empty, the API returns `success="true"` without error.
- **Admin Recycle Bin**: System administrators with access to the admin recycle bin must use the administration interface to empty other users' bins; this API cannot do so.
- **Selective Deletion**: To permanently delete individual items rather than the entire bin, use `PurgeRecycleBinItem`.
- **Restore Before Empty**: To recover items before emptying, use `RestoreRecycleBinItem` first.

---

## Related APIs

- [GetRecycleBinContent](GetRecycleBinContent.md) - List all items currently in the user's Recycle Bin
- [PurgeRecycleBinItem](PurgeRecycleBinItem.md) - Permanently delete a single item from the Recycle Bin
- [RestoreRecycleBinItem](RestoreRecycleBinItem.md) - Restore a Recycle Bin item to its original or a specified location
- [SearchRecycledItems](SearchRecycledItems.md) - Search for documents and folders in the Recycle Bin

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `SystemError:...` | An unexpected server-side error occurred. |

---
