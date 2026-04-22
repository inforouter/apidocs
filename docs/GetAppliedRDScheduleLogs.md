# GetAppliedRDScheduleLogs API

Returns the history of Retention and Disposition (R&D) schedules that have been applied to a document or folder by path. Each log entry records which schedule was assigned, by whom, and when. The path type is auto-detected.

## Endpoint

```
/srv.asmx/GetAppliedRDScheduleLogs
```

## Methods

- **GET** `/srv.asmx/GetAppliedRDScheduleLogs?authenticationTicket=...&path=...`
- **POST** `/srv.asmx/GetAppliedRDScheduleLogs` (form data)
- **SOAP** Action: `http://tempuri.org/GetAppliedRDScheduleLogs`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `path` | string | Yes | Full path of the document or folder |

## Response

### Success Response

```xml
<root success="true">
  <log rdDefId="5" rdName="7-Year Retention" appliedById="42" appliedByName="John Doe" dateApplied="2023-06-01T00:00:00.0000000" />
  <log rdDefId="7" rdName="10-Year Retention" appliedById="42" appliedByName="John Doe" dateApplied="2024-01-15T10:30:00.0000000" />
</root>
```

Returns an empty `<root success="true" />` if no log entries exist.

### Error Response

```xml
<root success="false" error="[ErrorCode] Error message" />
```

## Log Entry Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `rdDefId` | int | ID of the R&D schedule definition that was applied |
| `rdName` | string | Name of the R&D schedule definition |
| `appliedById` | int | ID of the user who applied the schedule |
| `appliedByName` | string | Full name of the user who applied the schedule |
| `dateApplied` | ISO 8601 datetime | Date and time the schedule was applied |

## Required Permissions

The caller must have read access to the document or folder.

## Example

### Get logs for a document (GET)

```
GET /srv.asmx/GetAppliedRDScheduleLogs?authenticationTicket=abc123-def456&path=/Library/Records/contract.pdf HTTP/1.1
```

### Get logs for a folder (POST)

```
POST /srv.asmx/GetAppliedRDScheduleLogs HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&path=/Library/Records/2020
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetAppliedRDScheduleLogs"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetAppliedRDScheduleLogs xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
      <path>/Library/Records/contract.pdf</path>
    </GetAppliedRDScheduleLogs>
  </soap:Body>
</soap:Envelope>
```

## Notes

- The path type is resolved automatically: document paths return the document's log; folder paths return the folder's log
- Log entries are returned in the order stored; most recent entries are typically last
- `dateApplied` is formatted as ISO 8601 with full precision

## Related APIs

- [`SetDocumentRandDSchedule`](SetDocumentRandDSchedule.md) — Assign an R&D schedule to a document
- [`SetFolderRandDSchedule`](SetFolderRandDSchedule.md) — Assign an R&D schedule to a folder
- [`GetRdFreezeLogs`](GetRdFreezeLogs.md) — Get the R&D freeze flag change history for a document or folder
- [`DisposeItem`](DisposeItem.md) — Dispose a document or folder by path
