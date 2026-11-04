# GetTransactionStatistics API

Returns the transaction runner's counters: for every database operation that runs inside a retried transaction, how many times it ran, how each call ended, how often it was retried after a deadlock, how long it waited for the serialization lock and how long it held it. The counters start when the server starts, or at the last reset. Restricted to callers who may view the server status.

## Endpoint

```
/srv.asmx/GetTransactionStatistics
```

## Methods

- **GET** `/srv.asmx/GetTransactionStatistics?authenticationTicket=...&reset=false`
- **POST** `/srv.asmx/GetTransactionStatistics` (form data)
- **SOAP** Action: `http://tempuri.org/GetTransactionStatistics`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `reset` | bool | No | `true` starts the counters again after this snapshot is taken. The answer is the snapshot before the reset. Default `false`. |

## Response Structure

### Success Response

```xml
<response success="true" Since="2026-11-04T09:12:30" Serialization="Global" Database="SqlServer">
  <Transaction Operation="FolderMoveOperation.RunAsync" Calls="41" Committed="40" RolledBack="1" Failed="0" Retries="2" RetriesExhausted="0" RefusedAsBusy="0" WaitedAvgMs="3.1" WaitedMaxMs="48" HeldAvgMs="210.5" HeldMaxMs="1840" HeldTotalMs="8630" />
  <Transaction Operation="DocumentImportOperation.ImportAsync" Calls="1200" Committed="1200" RolledBack="0" Failed="0" Retries="0" RetriesExhausted="0" RefusedAsBusy="0" WaitedAvgMs="0.4" WaitedMaxMs="12" HeldAvgMs="6.2" HeldMaxMs="95" HeldTotalMs="7440" />
  <!-- one element per operation, the one that held the lock longest in total first -->
</response>
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

## Response Attributes

On the root:

| Attribute | Type | Description |
|-----------|------|-------------|
| `Since` | DateTime | When the counters started: server start or the last reset |
| `Serialization` | string | The `TransactionSerialization` setting the server runs with: `Global` (the heavy transactions take one lock) or `Off` |
| `Database` | string | The database engine: `SqlServer`, `MySQL` or `Oracle` |

On each `Transaction`:

| Attribute | Type | Description |
|-----------|------|-------------|
| `Operation` | string | The operation, as file and method: `DocumentPurgeOperation.PurgeAsync` |
| `Calls` | integer | How many times it ran. Every call ends as exactly one of the next five |
| `Committed` | integer | Calls that committed |
| `RolledBack` | integer | Calls the operation itself rolled back, with a refusal for the caller and no exception |
| `Failed` | integer | Calls that ended in an exception that was not a deadlock, a taken name for instance |
| `RetriesExhausted` | integer | Calls whose every attempt was a deadlock victim or a lock-wait timeout, answered `5030` |
| `RefusedAsBusy` | integer | Calls that waited the whole limit for the serialization lock and were answered `5030` |
| `Retries` | integer | Attempts beyond the first, over all calls: how often a deadlock made an operation run again |
| `WaitedAvgMs`, `WaitedMaxMs` | double | Time spent waiting for the serialization lock, average and longest. 0 for an operation that takes no lock |
| `HeldAvgMs`, `HeldMaxMs`, `HeldTotalMs` | double | Time from taking the lock, or from the start of the body for an unlocked operation, to the commit or rollback |

## Required Permissions

- Callers with the `ViewServerStatus` administrative permission: the `sysadmin` account and members of `[Administrators]`.
- Anyone else is refused with `errorCode="4030"`.

## Example Requests

### Request (GET)

```
GET /srv.asmx/GetTransactionStatistics?authenticationTicket=abc123-def456&reset=false HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/GetTransactionStatistics HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&reset=true
```

## Notes

- The counters live in the server process. A restart starts them again, and on a farm each server answers its own.
- The same totals are written to the Maintenance log once a day by the maintenance run.
- `reset` is for measuring one period on its own, as the load tool does: reset at the start, read at the end.
