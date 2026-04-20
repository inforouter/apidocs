# AddToDownloadQueue API

Adds a document or folder to the current user's download queue by path.

## Endpoint

```
/srv.asmx/AddToDownloadQueue
```

## Methods

- **GET** `/srv.asmx/AddToDownloadQueue?authenticationTicket=...&itemPath=...`
- **POST** `/srv.asmx/AddToDownloadQueue` (form data)
- **SOAP** Action: `http://tempuri.org/AddToDownloadQueue`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `itemPath` | string | Yes | Full infoRouter path of the document or folder to add (e.g. `/Finance/Reports/Q1Summary.pdf` or `/Finance/Reports`). |

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

Any authenticated user may call this API. The item is added to the queue of the **currently authenticated user** only. No special permissions are required beyond being able to see the item.

## Resolution Order

The `itemPath` is resolved as a **document first**. If no document exists at that path, it is resolved as a **folder**. If neither is found, an error is returned.

## Examples

### Add a document (POST)

```
POST /srv.asmx/AddToDownloadQueue HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
&itemPath=%2FCorporate%2FContracts%2Fagreement.pdf
```

### Add a folder (GET)

```
GET /srv.asmx/AddToDownloadQueue
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &itemPath=%2FCorporate%2FContracts
HTTP/1.1
Host: yourserver
```

## Notes

- Returns an error if the item is already in the queue.
- To retrieve the current queue contents, use [GetDownloadQue](GetDownloadQue.md).
- To remove an item from the queue, use [RemoveFromDownloadQueue](RemoveFromDownloadQueue.md).
- To download the queued items as a ZIP archive, use [DownloadZip](DownloadZip.md).

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed — invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Item not found | `itemPath` does not refer to an existing document or folder. |
| Already in queue | The item is already present in the user's download queue. |

## Related APIs

- [RemoveFromDownloadQueue](RemoveFromDownloadQueue.md) - Remove an item from the download queue.
- [GetDownloadQue](GetDownloadQue.md) - Get the current contents of the download queue.
- [DownloadZip](DownloadZip.md) - Download queued items as a ZIP archive.
