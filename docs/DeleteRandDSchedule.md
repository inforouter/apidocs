# DeleteRandDSchedule API

Deletes an existing Retention and Disposition (R&D) schedule definition. The schedule cannot be deleted if it is currently assigned to any documents or folders.

## Endpoint

```
/srv.asmx/DeleteRandDSchedule
```

## Methods

- **GET** `/srv.asmx/DeleteRandDSchedule?authenticationTicket=...&RDdefId=...`
- **POST** `/srv.asmx/DeleteRandDSchedule` (form data)
- **SOAP** Action: `http://tempuri.org/DeleteRandDSchedule`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `RDdefId` | integer | Yes | ID of the Retention and Disposition schedule definition to delete. |

## Response

### Success Response

```xml
<root success="true" />
```

### Error Response

```xml
<root success="false" error="There are documents or folders uses this Retention and Disposition schedule that cannot be deleted. Document count: 3 Folder count: 1" />
```

## Required Permissions

**Retention & Disposition Manager** or **System Administrator**. Regular users receive an access denied error.

## Example

### GET Request

```
GET /srv.asmx/DeleteRandDSchedule
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &RDdefId=47
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/DeleteRandDSchedule HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&RDdefId=47
```

## Notes

- Deletion is **blocked** if the schedule is currently assigned to any documents or folders. The error message includes the count of blocking documents and folders.
- Before deleting, use [RemoveDocumentRandDSchedule](RemoveDocumentRandDSchedule.md) or [RemoveFolderRandDSchedule](RemoveFolderRandDSchedule.md) to unassign the schedule from all objects.
- This operation is **irreversible**. Use [CreateRandDSchedule](CreateRandDSchedule.md) to recreate the schedule if needed.
- To get the `RDdefId`, call [GetRandDSchedules](GetRandDSchedules.md) or retrieve it from the response of [CreateRandDSchedule](CreateRandDSchedule.md).

## Related APIs

- [GetRandDSchedules](GetRandDSchedules.md) -" List all defined R&D schedule definitions with their IDs.
- [UpdateRandDSchedule](UpdateRandDSchedule.md) -" Update an existing schedule definition.
- [RemoveDocumentRandDSchedule](RemoveDocumentRandDSchedule.md) -" Unassign a schedule from a document.
- [RemoveFolderRandDSchedule](RemoveFolderRandDSchedule.md) -" Unassign a schedule from a folder hierarchy.

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed -" invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Access Denied | Caller is not a Retention & Disposition Manager or System Administrator. |
| Schedule in use | The schedule is assigned to documents or folders and cannot be deleted. |
| Schedule not found | No schedule with the specified `RDdefId` exists. |
