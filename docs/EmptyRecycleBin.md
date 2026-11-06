# EmptyRecycleBin API

Empties the Recycle Bin of the currently authenticated user: its items move to the system recycle bin. The user no longer sees them in [GetRecycleBinContent](GetRecycleBinContent.md) and can no longer restore them; a system administrator can still find, restore or purge them there. Nothing is deleted for good. To empty every user's Recycle Bin at once, an administrator uses [EmptyAllUserRecycleBins](EmptyAllUserRecycleBins.md).

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

Moves everything in the caller's recycle bin to the system recycle bin. The caller can no longer see or restore it, and the answer does not say what went.

```javascript
// Read the bin first - after this the caller can no longer see the items.
const doomed = await call('GetRecycleBinContent', { authenticationTicket: ticket });
await call('EmptyRecycleBin', { authenticationTicket: ticket });
```

## Notes

- **Not a purge**: The emptied items move to the system recycle bin. Only a system administrator can restore them from there ([RestoreRecycleBinItem](RestoreRecycleBinItem.md)) or remove them for good ([PurgeRecycleBinItem](PurgeRecycleBinItem.md)), or the system recycle bin's automatic purge removes them.

- **Current User Only**: The API operates solely on the recycle bin of the user who owns the authentication ticket. There is no parameter to target another user's recycle bin.

- **Empty Bin is Not an Error**: If the recycle bin is already empty, the API returns `success="true"` without error.

- **Other Users' Bins**: This API cannot empty another user's bin. A system administrator empties every user's bin at once with [EmptyAllUserRecycleBins](EmptyAllUserRecycleBins.md).

- **Selective Deletion**: To permanently delete individual items rather than the entire bin, use `PurgeRecycleBinItem`.

- **Restore Before Empty**: A user who wants an item back restores it with `RestoreRecycleBinItem` before emptying, while `GetRecycleBinContent` still lists it. Afterwards only a system administrator can restore it.

---

## Related APIs

- [GetRecycleBinContent](GetRecycleBinContent.md) - List all items currently in the user's Recycle Bin

- [PurgeRecycleBinItem](PurgeRecycleBinItem.md) - Permanently delete a single item from the Recycle Bin

- [RestoreRecycleBinItem](RestoreRecycleBinItem.md) - Restore a Recycle Bin item to its original or a specified location

- [SearchRecycledItems](SearchRecycledItems.md) - Search for documents and folders in the Recycle Bin

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |

---
