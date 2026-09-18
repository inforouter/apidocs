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
<response success="true" error="" errorCode="0" />
```

### Error Response

```xml
<response success="false" error="There are documents or folders uses this Retention and Disposition schedule that cannot be deleted. Document count: 3 Folder count: 1" />
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

`DeleteRandDSchedule` with `forceDelete`. With `false` it behaves identically; with `true` it skips
the in-use check, clears the schedule off everything that carried it, drops the open retention tasks
and deletes it.

```javascript
await call('DeleteRandDSchedule1', {
  authenticationTicket: ticket, RDdefId: 18706, forceDelete: true
});
```

A document whose schedule was cleared this way reads back from `GetDocumentRandDSchedule` as a stub
`<RetentionDispositionSchedule DefId="0" />`, where a document that never had one answers no child
element at all.

The two warnings on [DeleteRandDSchedule](DeleteRandDSchedule.md) apply here too, and the second is
worse with `forceDelete="true"`: the in-use count is the only thing that stands between `RDdefId="0"`
and the delete statements, and force skips it.

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

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4030` | the caller may not manage retention schedules - including a caller with no ticket at all |
| `4170` | `forceDelete` was false and the schedule is applied to documents or folders |
