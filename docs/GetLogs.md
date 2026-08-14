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

### Turning the `IRConnect` log on

It is off by default and is set with `IRConnect.CallLogging` in the application settings, to one of
three levels:

| Level | What each record holds |
|-------|------------------------|
| `Off` | Nothing is logged. The default. |
| `Simple` | Everything about a call except what the document says: which document and version, its path, the options the call was made with, how long it waited and how long it took, the size or count of each thing that came back, and the tokens it was charged. |
| `Full` | `Simple`, plus the text sent to Connect and the content it returned. |

> **`Full` writes document text to disk in clear**, into these daily log files, where the ordinary
> log retention and the ordinary backup will pick it up. It is for working out why a model answered
> the way it did — a developer's machine, or a customer's for a bounded period and with their
> agreement. It should not be the resting state of a production instance.

`IRConnect.KeepCallLogsFor` is how many days of these are kept; the daily maintenance deletes the
rest. It defaults to 30 and is separate from `KeepErrorLogsFor`, because this log is written once
per call rather than once per failure and fills far faster.

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

#### IRConnect

One `<ConnectCall>` per call made to the infoRouter Connect AI service, written when the call
finished. `<ReturnedContent>` holds one element per thing the call produced, with its `length` —
characters for text, a count for a list. At the `Simple` level those elements are empty; at `Full`
each holds what came back.

```xml
<root success="true">
  <Value>
    <ConnectCall>
      <LogDate>2026-08-14T10:55:12.870Z</LogDate>
      <Server>YODA</Server>
      <Operation>profile</Operation>
      <DocumentId>1491</DocumentId>
      <VersionNumber>1000000</VersionNumber>
      <Path>/Public/Configuring-InfoRouter-Content-Search.pdf</Path>
      <RequestedBy>System Administrator</RequestedBy>
      <Priority>UserRequested</Priority>
      <Options ScrubPii="true" ProviderId="" MaxTags="10" SentAs="file" />
      <Timing QueuedSeconds="3.56" ElapsedSeconds="8.91" />
      <Status>Success</Status>
      <Model>claude-sonnet-4-5</Model>
      <Provider>anthropic</Provider>
      <Usage PromptTokens="1638" CompletionTokens="300" />
      <ReturnedContent>
        <Summary length="655" />
        <Description length="141" />
        <Abstract length="286" />
        <Tags length="10" />
        <Types length="0" version="393781196" />
        <ExtractedFields length="0" />
      </ReturnedContent>
    </ConnectCall>
    <!-- Additional ConnectCall entries -->
  </Value>
</root>
```

| Element | Description |
|---------|-------------|
| `Operation` | `summarize`, `keywords`, `ocr`, `profile`, or `status` / `document-types` for the two calls that keep the document type list in step |
| `Path` | The document's full path, in the form the APIs take |
| `RequestedBy` / `Priority` | Who the work was queued for, and whether anyone was waiting: `UserRequested` or `Automatic` |
| `Timing` | Seconds the job waited in the queue, and seconds the call itself took |
| `Status` | `Success`, `NoText` (Connect read the document and found nothing to work with) or `Failed`, which adds an `<Error>` element |
| `Usage` | The tokens the call was charged. Absent on `ocr`, `status` and `document-types`, which call no model |
| `ReturnedContent` | One element per thing produced; absent entirely for a call that produced nothing |
| `SentText` | At `Full` only: the text Connect was given, or a note that the document file itself was uploaded |

A document with no matching type reads as `<Types length="0" />`. The `version` attribute is the
document type list version the match was made against.

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
