# DeleteRandDSchedule1 API

Deletes an existing Retention and Disposition (R&D) schedule definition. When `forceDelete` is `true`, the schedule is automatically unassigned from all documents and folders before deletion, bypassing the assignment check. When `false`, behaves identically to [DeleteRandDSchedule](DeleteRandDSchedule.md).

## Endpoint

```
/srv.asmx/DeleteRandDSchedule1
```

## Methods

- **GET** `/srv.asmx/DeleteRandDSchedule1?authenticationTicket=...&RDdefId=...&forceDelete=...`
- **POST** `/srv.asmx/DeleteRandDSchedule1` (form data)
- **SOAP** Action: `http://tempuri.org/DeleteRandDSchedule1`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `RDdefId` | integer | Yes | ID of the Retention and Disposition schedule definition to delete. |
| `forceDelete` | boolean | Yes | When `true`, unassigns the schedule from all documents and folders before deleting. When `false`, deletion is blocked if the schedule is still assigned. |

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

### GET Request (force delete)

```
GET /srv.asmx/DeleteRandDSchedule1
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &RDdefId=47
    &forceDelete=true
HTTP/1.1
Host: yourserver
```

### POST Request (safe delete)

```
POST /srv.asmx/DeleteRandDSchedule1 HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&RDdefId=47&forceDelete=false
```

## Notes

- When `forceDelete=true`, the schedule is removed from all assigned documents and folders **within the same transaction** before the schedule definition is deleted.
- When `forceDelete=false`, deletion is **blocked** if the schedule is assigned to any documents or folders. The error message includes the count of blocking documents and folders.
- This operation is **irreversible**. Use [CreateRandDSchedule](CreateRandDSchedule.md) to recreate the schedule if needed.
- To get the `RDdefId`, call [GetRandDSchedules](GetRandDSchedules.md) or retrieve it from the response of [CreateRandDSchedule](CreateRandDSchedule.md).

## Related APIs

- [DeleteRandDSchedule](DeleteRandDSchedule.md) - Delete an R&D schedule (blocked if assigned).
- [GetRandDSchedules](GetRandDSchedules.md) - List all defined R&D schedule definitions with their IDs.
- [UpdateRandDSchedule](UpdateRandDSchedule.md) - Update an existing schedule definition.
- [RemoveDocumentRandDSchedule](RemoveDocumentRandDSchedule.md) - Unassign a schedule from a document.
- [RemoveFolderRandDSchedule](RemoveFolderRandDSchedule.md) - Unassign a schedule from a folder hierarchy.

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed - invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Access Denied | Caller is not a Retention & Disposition Manager or System Administrator. |
| Schedule in use | The schedule is assigned to documents or folders and `forceDelete` is `false`. |
| Schedule not found | No schedule with the specified `RDdefId` exists. |
