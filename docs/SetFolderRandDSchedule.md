# SetFolderRandDSchedule API

Assigns a Retention and Disposition (R&D) schedule to a folder identified by path. Optionally also assigns the schedule to all subfolders and/or all documents within the folder hierarchy.

## Endpoint

```
/srv.asmx/SetFolderRandDSchedule
```

## Methods

- **GET** `/srv.asmx/SetFolderRandDSchedule?authenticationTicket=...&Path=...&RDDefId=...&includeFolders=...&includeDocuments=...`
- **POST** `/srv.asmx/SetFolderRandDSchedule` (form data)
- **SOAP** Action: `http://tempuri.org/SetFolderRandDSchedule`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the folder (e.g. `/Finance/Reports`). |
| `RDDefId` | integer | Yes | ID of the R&D schedule definition to assign. Must be > 0. Use [GetRandDSchedules](GetRandDSchedules.md) to find valid IDs. |
| `includeFolders` | boolean | Yes | `true` to also assign the schedule to all subfolders recursively. `false` to assign only to the specified folder. |
| `includeDocuments` | boolean | Yes | `true` to also assign the schedule to all documents within the folder hierarchy. `false` to assign only to folders. |

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

### GET Request -" assign to folder only

```
GET /srv.asmx/SetFolderRandDSchedule
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &Path=/Finance/Reports
    &RDDefId=47
    &includeFolders=false
    &includeDocuments=false
HTTP/1.1
Host: yourserver
```

### GET Request -" assign to entire folder tree including documents

```
GET /srv.asmx/SetFolderRandDSchedule
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &Path=/Finance/Reports
    &RDDefId=47
    &includeFolders=true
    &includeDocuments=true
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/SetFolderRandDSchedule HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&Path=/Finance/Reports&RDDefId=47&includeFolders=true&includeDocuments=true
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

Puts a schedule on a folder, and optionally on what is inside it.

```javascript
await call('SetFolderRandDSchedule', {
  authenticationTicket: ticket,
  Path: '/Finance/Invoices',
  RDDefId: 18706,
  includeFolders: true,      // the subfolders, recursively
  includeDocuments: true     // the documents in them
});
```

With both flags false only the folder itself is touched. The answer wraps its log in a `<Value>`
element, where the document form answers a bare success.

## Notes

- Assigning a schedule to a folder triggers the calculation of retention and disposition dates for all affected folders and documents.
- If a folder or document already has a schedule assigned, it is replaced with the new one.
- To remove a schedule from a folder hierarchy, use [RemoveFolderRandDSchedule](RemoveFolderRandDSchedule.md).
- To assign a schedule to a single document, use [SetDocumentRandDSchedule](SetDocumentRandDSchedule.md).

## Related APIs

- [GetFolderRandDSchedule](GetFolderRandDSchedule.md) -" Get the R&D schedule currently assigned to a folder.
- [RemoveFolderRandDSchedule](RemoveFolderRandDSchedule.md) -" Remove the R&D schedule from a folder hierarchy.
- [SetDocumentRandDSchedule](SetDocumentRandDSchedule.md) -" Assign a schedule to a single document.
- [GetRandDSchedules](GetRandDSchedules.md) -" List all R&D schedule definitions with their IDs.
- [CreateRandDSchedule](CreateRandDSchedule.md) -" Create a new R&D schedule definition.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | no folder at that path, or no schedule by that id |
| *(none)* | the folder itself is written whoever asks, including a caller with no ticket; only the items inside are permission checked, and their refusals go in the `<Value>` log while the call reports success |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
