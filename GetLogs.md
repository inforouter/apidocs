# GetLogs API

Returns the server log entries for a specified log type and date.

## Endpoint

```
/srv.asmx/GetLogs
```

## Methods

- **GET** `/srv.asmx/GetLogs?authenticationTicket=...&logType=...&logDate=...`
- **POST** `/srv.asmx/GetLogs` (form data)
- **SOAP** Action: `http://tempuri.org/GetLogs`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `logType` | string | Yes | The type of log to retrieve (see valid values below) |
| `logDate` | string | Yes | The date of the log in `yyyy-MM-dd` format (e.g., `2021-05-27`) |

## Valid logType Values

| Value | Description |
|-------|-------------|
| `Errors` | Application error logs |
| `LoginAttempts` | Failed login attempt logs |
| `Logins` | Successful login logs |
| `Notifications` | Email notification logs |

## Response

### Success Response

The response XML varies depending on the `logType` requested. The log entries are wrapped inside a `<Value>` element.

#### Errors

```xml
<root success="true">
  <Value>
    <Error>
      <LogDate>2025-01-15T10:30:00Z</LogDate>
      <ExceptionNumber>-2146233088</ExceptionNumber>
      <Message>Error description</Message>
      <Source>ErrorSource</Source>
      <StackTrace>Stack trace details...</StackTrace>
      <Platform>
        <AppVersion>8.7.100</AppVersion>
        <DbType>SqlServer</DbType>
        <OS>Win32NT</OS>
        <OSVersion>10.0.26200</OSVersion>
        <Language>English (United States)</Language>
      </Platform>
    </Error>
    <!-- Additional Error entries -->
  </Value>
</root>
```

#### Logins

```xml
<root success="true">
  <Value>
    <Login>
      <LogDate>2025-01-15T09:00:00Z</LogDate>
      <UserName>jsmith</UserName>
      <UserId>42</UserId>
      <FirstName>John</FirstName>
      <LastName>Smith</LastName>
      <Email>jsmith@example.com</Email>
    </Login>
    <!-- Additional Login entries -->
  </Value>
</root>
```

#### LoginAttempts

```xml
<root success="true">
  <Value>
    <LoginAttempt>
      <LogDate>2025-01-15T09:05:00Z</LogDate>
      <UserName>unknownuser</UserName>
      <IpAddress>192.168.1.100</IpAddress>
      <HostName>workstation1</HostName>
      <Platform>Windows</Platform>
      <Browser>Chrome</Browser>
    </LoginAttempt>
    <!-- Additional LoginAttempt entries -->
  </Value>
</root>
```

#### Notifications

```xml
<root success="true">
  <Value>
    <Notification>
      <LogDate>2025-01-15T11:00:00Z</LogDate>
      <UserId>42</UserId>
      <UserName>jsmith</UserName>
      <email>jsmith@example.com</email>
      <Path>/MyLibrary/Documents/report.pdf</Path>
      <EventType>DocumentCreated</EventType>
      <DeliveryType>Email</DeliveryType>
      <Problem></Problem>
    </Notification>
    <!-- Additional Notification entries -->
  </Value>
</root>
```

### Error Response

```xml
<root success="false" error="[ErrorCode] Error message" />
```

## Required Permissions

The caller must be a **System Administrator**.

## Example

### Request (GET)

```
GET /srv.asmx/GetLogs?authenticationTicket=abc123-def456&logType=Errors&logDate=2025-01-15 HTTP/1.1
```

### Request (POST)

```
POST /srv.asmx/GetLogs HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&logType=Logins&logDate=2025-01-15
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetLogs"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetLogs xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
      <logType>Errors</logType>
      <logDate>2025-01-15</logDate>
    </GetLogs>
  </soap:Body>
</soap:Envelope>
```

## Notes

- The `logType` parameter is case-insensitive
- If no log file exists for the specified date, an empty `<Value>` element is returned
- Log dates correspond to files stored on disk; use `GetLogStatistics` to discover which dates have log entries and how many entries each date contains
- The `logDate` parameter must be parseable as a date; invalid formats will return an error
