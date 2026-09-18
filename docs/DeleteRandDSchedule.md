# DeleteRandDSchedule API

> **Enhanced version available:** [DeleteRandDSchedule1](DeleteRandDSchedule1.md) adds a `forceDelete` parameter that automatically unassigns the schedule from all documents and folders before deletion. Prefer the new API for new integrations.

Deletes an existing Retention and Disposition (R&D) schedule definition. The schedule cannot be
deleted if it is currently assigned to any documents or folders.

> **An id that matches no schedule is reported as a success.** Nothing checks that the
> schedule is there, so a caller cannot tell a delete that happened from one that did not.
> `RDdefId="0"` is not "no schedule" either: zero is what an item with no schedule carries,
> so the in-use check counts every one of them.

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
<response success="true" error="" errorCode="0" />
```

### Error Response

```xml
<response success="false" error="There are documents or folders uses this Retention and Disposition schedule that cannot be deleted. Document count: 3 Folder count: 1" />
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

Deletes a schedule, provided nothing is using it. The refusal counts what is.

```javascript
try {
  await call('DeleteRandDSchedule', { authenticationTicket: ticket, RDdefId: 18706 });
} catch (error) {
  // 4170: still applied to documents or folders. The message carries both counts.
  console.log(error.message);
}
```

Two things to know before calling it:

- **An id that matches no schedule is reported as a success.** Nothing checks that the schedule is
  there: the delete statements run against an id that matches no row and the call answers
  `success="true"`, where `GetRandDScheduleInfo` answers `4041` for the same id. A caller cannot tell
  a delete that happened from one that did not.
- **`RDdefId="0"` is not "no schedule", it is a value the in-use check counts.** Zero is what a
  document or folder with no schedule carries, so the check finds every one of them and the refusal
  quotes a number that has nothing to do with any schedule.

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

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4030` | the caller may not manage retention schedules - including a caller with no ticket at all |
| `4170` | the schedule is applied to documents or folders; the message counts them |
