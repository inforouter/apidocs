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

## Notes

- Removing an item that is **not in the queue** is a no-op and still returns `success="true"`.
- Only affects the queue of the currently authenticated user.
- To add items to the queue, use [AddToDownloadQueue](AddToDownloadQueue.md).
- To retrieve the current queue contents, use [GetDownloadQue](GetDownloadQue.md).

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed — invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Item not found | `itemPath` does not refer to an existing document or folder. |

## Related APIs

- [AddToDownloadQueue](AddToDownloadQueue.md) - Add a document or folder to the download queue.
- [GetDownloadQue](GetDownloadQue.md) - Get the current contents of the download queue.
- [DownloadZip](DownloadZip.md) - Download queued items as a ZIP archive.
