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
<root success="true" />
```

### Error Response

```xml
<root success="false" error="[901]Session expired or Invalid ticket" />
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

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed -" invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Access Denied | Caller does not have write access to the folder. |
| Folder not found | No folder was found at the specified `Path`. |
