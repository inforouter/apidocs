# RemoveFromDownloadQueue API

Removes a document or folder from the current user's download queue by path.

## Endpoint

```
/srv.asmx/RemoveFromDownloadQueue
```

## Methods

- **GET** `/srv.asmx/RemoveFromDownloadQueue?authenticationTicket=...&itemPath=...`
- **POST** `/srv.asmx/RemoveFromDownloadQueue` (form data)
- **SOAP** Action: `http://tempuri.org/RemoveFromDownloadQueue`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `itemPath` | string | Yes | Full infoRouter path of the document or folder to remove (e.g. `/Finance/Reports/Q1Summary.pdf` or `/Finance/Reports`). |

## Response

### Success Response

```xml
<root success="true" />
```

### Error Response

```xml
<root success="false" error="Error message" />
```

## Required Permissions

Any authenticated user may call this API. The item is removed from the queue of the **currently authenticated user** only.

## Resolution Order

The `itemPath` is resolved as a **document first**. If no document exists at that path, it is resolved as a **folder**. If neither is found, an error is returned.

## Examples

### Remove a document (POST)

```
POST /srv.asmx/RemoveFromDownloadQueue HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
&itemPath=%2FCorporate%2FContracts%2Fagreement.pdf
```

### Remove a folder (GET)

```
GET /srv.asmx/RemoveFromDownloadQueue
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &itemPath=%2FCorporate%2FContracts
HTTP/1.1
Host: yourserver
```

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

Takes a document or folder off the calling user's download queue.

```javascript
await call('RemoveFromDownloadQueue', {
  authenticationTicket: ticket,
  itemPath: '/Finance/Reports/Q1.pdf'
});
```

Removing something that is not on the list is a success, so this is safe to call without checking
first. A path that names nothing at all is `4041`.

**An unticketed caller is answered success rather than refused.** The anonymous user has no lists, so
nothing is removed and nothing is at risk, but a client cannot tell that apart from a removal that
happened. Every other write in this area refuses an unticketed call with `4010`.

## Notes

- Removing an item that is **not in the queue** is a no-op and still returns `success="true"`.
- Only affects the queue of the currently authenticated user.
- To add items to the queue, use [AddToDownloadQueue](AddToDownloadQueue.md).
- To retrieve the current queue contents, use [GetDownloadQue](GetDownloadQue.md).

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | nothing at that path |
| `none` | an unticketed caller is answered success |

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed — invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Item not found | `itemPath` does not refer to an existing document or folder. |

## Related APIs

- [AddToDownloadQueue](AddToDownloadQueue.md) - Add a document or folder to the download queue.
- [GetDownloadQue](GetDownloadQue.md) - Get the current contents of the download queue.
- [DownloadZip](DownloadZip.md) - Download queued items as a ZIP archive.
