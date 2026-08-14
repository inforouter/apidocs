# GetLogStatistics1 API

Returns log dates and entry counts for a specified log type over a caller-supplied lookback window. Returns one entry per day in the window, including days with zero entries. Use this API to discover which dates have log data before calling `GetLogs` to retrieve the actual entries.

For a fixed 365-day window, use [`GetLogStatistics`](GetLogStatistics.md).

## Endpoint

```
/srv.asmx/GetLogStatistics1
```

## Methods

- **GET** `/srv.asmx/GetLogStatistics1?authenticationTicket=...&logType=...&lastNDays=...`
- **POST** `/srv.asmx/GetLogStatistics1` (form data)
- **SOAP** Action: `http://tempuri.org/GetLogStatistics1`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `logType` | string | Yes | The type of log to query (see valid values below) |
| `lastNDays` | int | Yes | Number of days to look back from today. Valid range: 1–365. Pass `0` to use the maximum (365 days). Values greater than 365 return an error. |

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

## lastNDays Behaviour

| Value | Result |
|-------|--------|
| `0` | Defaults to 365 days |
| `1`–`365` | Returns exactly that many days |
| `> 365` | Returns error: `'lastNDays' value cannot be greater than 365 days` |

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
| `Statistics` | container | Contains one `Value` entry per day in the requested window |
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
GET /srv.asmx/GetLogStatistics1?authenticationTicket=abc123-def456&logType=Errors&lastNDays=30 HTTP/1.1
```

### Request (POST)

```
POST /srv.asmx/GetLogStatistics1 HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&logType=Logins&lastNDays=7
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetLogStatistics1"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetLogStatistics1 xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
      <logType>Errors</logType>
      <lastNDays>30</lastNDays>
    </GetLogStatistics1>
  </soap:Body>
</soap:Envelope>
```

## Notes

- Every day in the requested window is returned, including days with `Count=0`
- `Count` is the number of XML child elements in the log file for that date
- Use returned `LogDate` values as the `logDate` parameter when calling `GetLogs`
