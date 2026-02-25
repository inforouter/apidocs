# GetLogStatistics API

Returns the available log dates and entry counts for a specified log type. Use this API to discover which dates have log data before calling `GetLogs` to retrieve the actual entries.

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
| `logType` | string | Yes | The type of log to retrieve statistics for (see valid values below) |

## Valid logType Values

| Value | Description |
|-------|-------------|
| `Errors` | Application error logs |
| `LoginAttempts` | Failed login attempt logs |
| `Logins` | Successful login logs |
| `Notifications` | Email notification logs |

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
      <Count>12</Count>
    </Value>
    <Value>
      <LogDate>2025-01-15</LogDate>
      <Count>3</Count>
    </Value>
  </Statistics>
</root>
```

### Response Elements

| Element | Type | Description |
|---------|------|-------------|
| `Statistics` | container | Contains all log date entries |
| `Value` | container | A single date entry |
| `LogDate` | string | The log date in `yyyy-MM-dd` format |
| `Count` | int | Number of log entries for that date |

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

- The `logType` parameter is case-insensitive
- Only dates that have at least one log entry are returned
- The `Count` value represents the number of XML child elements in the log file for that date
- Use the returned `LogDate` values as the `logDate` parameter when calling `GetLogs` to retrieve the actual log entries
- If no log files exist for the specified log type, an empty `<Statistics>` element is returned
