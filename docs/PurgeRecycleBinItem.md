# PurgeRecycleBinItem API

Permanently and irreversibly deletes a single document or folder from the system Recycle Bin. The item is identified by its `Handler` value, which is obtained from `GetRecycleBinContent`. Use this API to selectively remove individual items rather than emptying the entire bin. This is an administrator-only operation.

## Endpoint

```

/srv.asmx/PurgeRecycleBinItem

```

## Methods

- **GET** `/srv.asmx/PurgeRecycleBinItem?AuthenticationTicket=...&ItemHandler=...`

- **POST** `/srv.asmx/PurgeRecycleBinItem` (form data)

- **SOAP** Action: `http://tempuri.org/PurgeRecycleBinItem`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. The authenticated user must be a system administrator. |
| `ItemHandler` | string | Yes | Handler string identifying the recycled item to purge. Obtained from the `Handler` attribute of a `<document>` or `<folder>` element returned by `GetRecycleBinContent`. Format: `D{id}` for a document (e.g. `D9871`), `F{id}` for a folder (e.g. `F4312`). Case-insensitive. |

---

## Response

### Success Response

```xml

<response success="true" error="" />

```

### Error Response

```xml

<response success="false" error="Invalid ItemHandler" />

```

### Partial Failure Response

If the item cannot be purged (e.g. a storage error for one file within a folder), a log response is returned:

```xml

<response success="false" error="[log]">

  <logitem name="Q1-2024-Report.pdf" message="Unable to delete file from storage." />

</response>

```

---

## Required Permissions

**System administrators only.** Regular users and domain managers cannot call this API. Attempting to call it as a non-administrator returns a permission error.

---

## Example

### GET Request

```

GET /srv.asmx/PurgeRecycleBinItem

  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

  &ItemHandler=D9871

HTTP/1.1

```

### POST Request

```

POST /srv.asmx/PurgeRecycleBinItem HTTP/1.1

Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

&ItemHandler=D9871

```

### SOAP Request

```xml

<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"

               xmlns:tns="http://tempuri.org/">

  <soap:Body>

    <tns:PurgeRecycleBinItem>

      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>

      <tns:ItemHandler>D9871</tns:ItemHandler>

    </tns:PurgeRecycleBinItem>

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

Destroys one item in the bin for good. There is no undo.

```javascript
await call('PurgeRecycleBinItem', { authenticationTicket: ticket, ItemHandler: 'D4512' });
```

Purging a handler that is no longer in the bin is a success, where restoring the same handler is
refused with `4000` - the two neighbours answer the same condition differently, so do not read a
success here as proof that something was destroyed by this call.

## Notes

- **Admin Only**: The authenticated user must be a system administrator. The check is enforced server-side regardless of how the API is called.

- **Irreversible**: Once purged, the item is permanently deleted from storage and cannot be recovered. Always confirm the correct `ItemHandler` before calling.

- **Handler Source**: The `ItemHandler` value must be obtained from the `Handler` attribute of a recycled item returned by `GetRecycleBinContent` or `SearchRecycledItems`. Constructing a handler manually (e.g. `D9871`) is possible but not recommended.

- **Handler Format**: The prefix letter determines the object type (`D` = document, `F` = folder). The prefix is case-insensitive. The numeric part must be a valid integer object ID.

- **Invalid Handler**: If the `ItemHandler` string cannot be parsed, or refers to an object type other than document or folder, `"Invalid ItemHandler"` is returned.

- **Item Not Found**: If the item no longer exists in the recycle bin (already purged or restored), an error is returned.

- **Folder Purge**: Purging a folder recursively deletes all documents and sub-folders contained within it. This is a deep, permanent deletion.

- **EmptyRecycleBin vs PurgeRecycleBinItem**: `EmptyRecycleBin` removes all items for a specific user but requires the user themselves (not admin). `PurgeRecycleBinItem` removes a single item and requires admin rights.

---

## Related APIs

- [GetRecycleBinContent](GetRecycleBinContent.md) - List recycled items (use to obtain the `Handler` value)

- [SearchRecycledItems](SearchRecycledItems.md) - Search for recycled items across all users (admin)

- [RestoreRecycleBinItem](RestoreRecycleBinItem.md) - Restore a recycled item instead of permanently deleting it

- [EmptyRecycleBin](EmptyRecycleBin.md) - Permanently delete all items in the current user's Recycle Bin

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4000` | `ItemHandler` is not a handler: the letter and the id are checked before the lookup, and the message naming the parameter is an English literal that is not translated |
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

An item in the bin is named by its **handler**: the letter `D` and a document id, or the letter
`F` and a folder id - `D4512`, `F183`. It is read off the `Handler` attribute of an item returned
by [GetRecycleBinContent](GetRecycleBinContent.md) or
[SearchRecycledItems](SearchRecycledItems.md); there is no other way to build one, because the ids
are not the ones a caller sees anywhere else.

---
