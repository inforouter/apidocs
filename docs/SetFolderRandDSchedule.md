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
<root success="true" />
```

### Error Response

```xml
<root success="false" error="[901]Session expired or Invalid ticket" />
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

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed -" invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Access Denied | Caller does not have write access to the folder. |
| Folder not found | No folder was found at the specified `Path`. |
| Schedule not found | No R&D schedule with the specified `RDDefId` exists. |
