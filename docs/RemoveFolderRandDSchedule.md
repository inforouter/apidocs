# RemoveFolderRandDSchedule API

Removes (unassigns) the Retention and Disposition (R&D) schedule from a folder identified by path. Optionally also removes the schedule from all subfolders and/or all documents within the folder hierarchy.

## Endpoint

```
/srv.asmx/RemoveFolderRandDSchedule
```

## Methods

- **GET** `/srv.asmx/RemoveFolderRandDSchedule?authenticationTicket=...&Path=...&includeFolders=...&includeDocuments=...`
- **POST** `/srv.asmx/RemoveFolderRandDSchedule` (form data)
- **SOAP** Action: `http://tempuri.org/RemoveFolderRandDSchedule`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the folder (e.g. `/Finance/Reports`). |
| `includeFolders` | boolean | Yes | `true` to also remove the schedule from all subfolders recursively. `false` to remove only from the specified folder. |
| `includeDocuments` | boolean | Yes | `true` to also remove the schedule from all documents within the folder hierarchy. `false` to remove only from folders. |

## Response

### Success Response

```xml
<response success="true" />
```

### Error Response

```xml
<response success="false" error="[901]Session expired or Invalid ticket" />
```

## Required Permissions

The calling user must have write access to the folder.

## Example

### GET Request -" remove from folder only

```
GET /srv.asmx/RemoveFolderRandDSchedule
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &Path=/Finance/Reports
    &includeFolders=false
    &includeDocuments=false
HTTP/1.1
Host: yourserver
```

### GET Request -" remove from entire folder tree including documents

```
GET /srv.asmx/RemoveFolderRandDSchedule
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &Path=/Finance/Reports
    &includeFolders=true
    &includeDocuments=true
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/RemoveFolderRandDSchedule HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&Path=/Finance/Reports&includeFolders=true&includeDocuments=true
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

Takes the schedule off a folder, and optionally off what is inside it.

```javascript
await call('RemoveFolderRandDSchedule', {
  authenticationTicket: ticket,
  Path: '/Finance/Invoices',
  includeFolders: true,
  includeDocuments: true
});
```

> **A caller with no ticket can clear a folder's schedule**, the same hole as
> [SetFolderRandDSchedule](SetFolderRandDSchedule.md) seen from the other side: an unauthenticated
> request removes a records management control from a folder, and the call reports success.

## Notes

- If the folder has no schedule assigned, the call succeeds without error (no-op).
- Removing a schedule clears the computed retention and disposition dates from all affected folders and documents.
- This operation is required before deleting the schedule definition via [DeleteRandDSchedule](DeleteRandDSchedule.md) if the schedule is assigned to folders.
- To assign a schedule to a folder, use [SetFolderRandDSchedule](SetFolderRandDSchedule.md).
- To remove a schedule from a single document, use [RemoveDocumentRandDSchedule](RemoveDocumentRandDSchedule.md).

## Related APIs

- [SetFolderRandDSchedule](SetFolderRandDSchedule.md) -" Assign an R&D schedule to a folder hierarchy.
- [GetFolderRandDSchedule](GetFolderRandDSchedule.md) -" Get the R&D schedule currently assigned to a folder.
- [RemoveDocumentRandDSchedule](RemoveDocumentRandDSchedule.md) -" Remove the R&D schedule from a single document.
- [DeleteRandDSchedule](DeleteRandDSchedule.md) -" Delete an R&D schedule definition.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | no folder at that path |
| *(none)* | the folder itself is cleared whoever asks, including a caller with no ticket |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
