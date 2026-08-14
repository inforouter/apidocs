# GetLogStatistics API

Returns log dates and entry counts for a specified log type over the last 365 days. Returns one entry per day in the window, including days with zero entries. Use this API to discover which dates have log data before calling `GetLogs` to retrieve the actual entries.

To control the lookback window explicitly, use [`GetLogStatistics1`](GetLogStatistics1.md).

## Endpoint

```
/srv.asmx/GetLogStatistics
```

## Methods

- **GET** `/srv.asmx/GetLogStatistics?authenticationTicket=...&logType=...`
- **POST** `/srv.asmx/GetLogStatistics` (form data)
- **SOAP** Action: `http://tempuri.org/GetLogStatistics`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `logType` | string | Yes | The type of log to query (see valid values below) |

## Valid logType Values

| Value | Description |
|-------|-------------|
| `Errors` | Application error logs |
| `LoginAttempts` | Failed login attempt logs |
| `Logins` | Successful login logs |
| `Notifications` | Email notification logs |
| `Information` | Informational entries |
| `Warning` | Warnings |
| `Upgrade` | What an upgrade did |
| `Maintenance` | What the daily maintenance jobs did |
| `IRConnect` | One record per infoRouter Connect call — see below |

> **New in 9.2.** `Information`, `Warning`, `Upgrade` and `Maintenance` have always been written by
> the server but could not be read back through this API until 9.2. `IRConnect` is new.

### The `IRConnect` log

One record per call to the infoRouter Connect AI service, written when the call finishes — success
or failure — and **only when the instance has switched it on**. It is off by default, so an
instance that has not configured `IRConnect.CallLogging` will find no records here at all.

Each record carries which document, which operation, how long the call waited and took, what it
returned in sizes and counts, and the token counts it was charged for. At the `Full` level it also
carries the text sent and the content returned, which means document content on disk; see the
`IRConnect.CallLogging` setting.

The `logType` parameter is case-insensitive.

## Response

### Success Response

```xml
<root success="true">
  <Statistics>
    <Value>
      <LogDate>2025-01-13</LogDate>
      <Count>5</Count>
    </Value>
    <Value>
      <LogDate>2025-01-14</LogDate>
      <Count>0</Count>
    </Value>
    <Value>
      <LogDate>2025-01-15</LogDate>
      <Count>12</Count>
    </Value>
  </Statistics>
</root>
```

### Response Elements

| Element | Type | Description |
|---------|------|-------------|
| `Statistics` | container | Contains one `Value` entry per day in the 365-day window |
| `Value` | container | A single date entry |
| `LogDate` | string | The date in `yyyy-MM-dd` format, counting back from today |
| `Count` | int | Number of log entries for that date; `0` when no log file exists for the date |

### Error Response

```xml
<root success="false" error="[ErrorCode] Error message" />
```

## Required Permissions

The caller must be a **System Administrator**.

## Example

### Request (GET)

```
GET /srv.asmx/GetLogStatistics?authenticationTicket=abc123-def456&logType=Errors HTTP/1.1
```

### Request (POST)

```
POST /srv.asmx/GetLogStatistics HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&logType=Logins
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetLogStatistics"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetLogStatistics xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
      <logType>Errors</logType>
    </GetLogStatistics>
  </soap:Body>
</soap:Envelope>
```

## Notes

- Always returns the last **365 days**, one entry per day
- Every day in the window is returned, including days with `Count=0`
- `Count` is the number of XML child elements in the log file for that date
- Use returned `LogDate` values as the `logDate` parameter when calling `GetLogs`
- To use a custom lookback window, use [`GetLogStatistics1`](GetLogStatistics1.md)
