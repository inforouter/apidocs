# GetRdFreezeLogs API

Returns the R&D freeze flag change history for a document or folder by path. Each log entry records when the freeze flag was set or cleared, by whom, and with what comment. The path type is auto-detected.

## Endpoint

```
/srv.asmx/GetRdFreezeLogs
```

## Methods

- **GET** `/srv.asmx/GetRdFreezeLogs?authenticationTicket=...&path=...`
- **POST** `/srv.asmx/GetRdFreezeLogs` (form data)
- **SOAP** Action: `http://tempuri.org/GetRdFreezeLogs`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `path` | string | Yes | Full path of the document or folder |

## Response

### Success Response

```xml
<root success="true">
  <log rdFreezeFlag="true" actionDate="2024-01-15T10:30:00.0000000" userId="42" userFullName="John Doe" actionComments="Legal hold" />
  <log rdFreezeFlag="false" actionDate="2024-03-01T09:00:00.0000000" userId="42" userFullName="John Doe" actionComments="" />
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
| `rdFreezeFlag` | bool | `true` if the flag was set (frozen); `false` if cleared (unfrozen) |
| `actionDate` | ISO 8601 datetime | Date and time the change was made |
| `userId` | int | ID of the user who made the change |
| `userFullName` | string | Full name of the user who made the change |
| `actionComments` | string | Comment provided at the time of the change (may be empty) |

## Required Permissions

The caller must have read access to the document or folder.

## Example

### Get logs for a document (GET)

```
GET /srv.asmx/GetRdFreezeLogs?authenticationTicket=abc123-def456&path=/Library/Records/contract.pdf HTTP/1.1
```

### Get logs for a folder (POST)

```
POST /srv.asmx/GetRdFreezeLogs HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&path=/Library/Records/2020
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetRdFreezeLogs"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetRdFreezeLogs xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
      <path>/Library/Records/contract.pdf</path>
    </GetRdFreezeLogs>
  </soap:Body>
</soap:Envelope>
```

## Notes

- The path type is resolved automatically: document paths return the document's log; folder paths return the folder's log
- Log entries are returned in the order stored; most recent entries are typically last
- `actionDate` is formatted as ISO 8601 with full precision

## Related APIs

- [`SetRdFreezeFlag`](SetRdFreezeFlag.md) — Set or clear the R&D freeze flag on a document or folder
- [`GetAppliedRDScheduleLogs`](GetAppliedRDScheduleLogs.md) — Get history of R&D schedules applied to a document or folder
- [`DisposeItem`](DisposeItem.md) — Dispose a document or folder by path
