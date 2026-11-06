# RunMaintenanceJob API

Runs one maintenance job now, on the caller's request, the way the scheduler runs it: the start and the end go to the job log, so `GetMaintenanceJobsStatus` shows the run. The call answers when the job is through. Administrators only.

## Endpoint

```
/srv.asmx/RunMaintenanceJob
```

## Methods

- **GET** `/srv.asmx/RunMaintenanceJob?authenticationTicket=...&jobId=14`
- **POST** `/srv.asmx/RunMaintenanceJob` (form data)
- **SOAP** Action: `http://tempuri.org/RunMaintenanceJob`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `jobId` | int | Yes | The job, by the `JobId` that `GetMaintenanceJobsStatus` lists. An unknown id is refused with `4000` and the refusal lists the ids there are. |

## Response Structure

### Success Response

```xml
<response success="true" JobId="14" JobName="Purge the system recycle bin" Success="true" TimeElapsedMs="2310.5" />
```

| Attribute | Type | Description |
|-----------|------|-------------|
| `JobId` | integer | The job that ran |
| `JobName` | string | Its name in the caller's language |
| `Success` | boolean | What the job reported. `false` means the job ran and said it did not finish its work; the server log has the reason |
| `TimeElapsedMs` | double | How long the job ran |

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

## Required Permissions

- Administrators only: the `sysadmin` account and members of `[Administrators]`.
- Anyone else is refused with `errorCode="4030"`.

## Example Requests

### Request (GET)

```
GET /srv.asmx/RunMaintenanceJob?authenticationTicket=abc123-def456&jobId=14 HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/RunMaintenanceJob HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&jobId=14
```

## Notes

- The job runs on the request, not on the maintenance service, and the call lasts as long as the job. A purge of a full recycle bin can take minutes; set the client's timeout accordingly.
- The scheduler does not know about the run. A job the scheduler is running at that moment runs a second time beside it; both log what they could not do. Use it on a test server, or in a quiet hour.
- The purge job (`14`) purges up to 1,000 queued items a run. Items reach the queue through `PurgeRecycleBinItem`, `DisposeItem` and the system recycle bin's automatic purge (`SystemRecycleBinAutoPurgeOption`), not through `EmptyRecycleBin`, which only moves items to the system recycle bin; call the job again until the queue is empty.
- Made for the load tool of the IRTRANS removal plan, which needs the purge to run when it says, not once a day.
