# GetServerAlerts API

**Available in:** infoRouter 9.0 and later

Returns the server's current alerts: the things an administrator should know about right now, such as a warehouse disk that is almost full or an internet outage. An alert is removed by the server when its problem is gone, so the list is always the present state. Call it every few minutes to show the alerts in the user interface.

## Endpoint

```
/srv.asmx/GetServerAlerts
```

## Methods

- **GET** `/srv.asmx/GetServerAlerts?authenticationTicket=...`
- **POST** `/srv.asmx/GetServerAlerts` (form data)
- **SOAP** Action: `http://tempuri.org/GetServerAlerts`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |

## Response

### Success Response
```xml
<response success="true" error="">
  <Alert Type="WarehouseDiskSpaceLow" Subject="D:\" Severity="Warning" SeverityValue="2"
         Description="The disk D:\ is almost full." Detail="18.2 GB free of 500 GB"
         FirstSeen="2026-11-19T09:10:00" LastSeen="2026-11-19T14:10:00"
         Dismissed="true" DismissedBy="jsmith" DismissedOn="2026-11-19T10:02:00" />
</response>
```

No alerts is `<response success="true" error="" />`. The most serious alerts come first, then the oldest.

| Attribute | Type | Description |
|-----------|------|-------------|
| `Type` | string | The kind of alert: `WarehouseDiskSpaceLow` or `CustomerServicesUnreachable`. More kinds may be added; show an alert of a kind you do not know by its `Description`. |
| `Subject` | string | What the alert is about when one kind can occur more than once: the disk. Empty otherwise. `Type` and `Subject` together identify the alert. |
| `Severity` | string | `Warning`, `Critical` or `Fatal`. |
| `SeverityValue` | int | The same as a number, for sorting and colouring: `2`, `3` or `4`. There is no `1`. |
| `Description` | string | One sentence in the language of the caller. |
| `Detail` | string | Free text for the administrator: sizes, or the error message. Not translated. May be empty. |
| `FirstSeen` | datetime | When the problem was first noticed (server time). |
| `LastSeen` | datetime | When the problem was last confirmed. |
| `Dismissed` | boolean | `true` when an administrator dismissed the alert. A dismissed alert stays in the list until the server clears it. |
| `DismissedBy` | string | The user name of the administrator who dismissed it. Only present when `Dismissed` is `true`. |
| `DismissedOn` | datetime | When it was dismissed. Only present when `Dismissed` is `true`. |

### Severities

| Value | Name | Means |
|-------|------|-------|
| 2 | Warning | Something is wrong; the application works. |
| 3 | Critical | The application will stop working, or lose a function, unless somebody acts. |
| 4 | Fatal | The application, or a part of it, has stopped. |

### Alert types

| Type | Subject | Raised when | Severity |
|------|---------|-------------|----------|
| `WarehouseDiskSpaceLow` | the disk | A disk that holds a warehouse path has less than 10 % free space. | Warning; Critical under 2 % |
| `CustomerServicesUnreachable` | empty | The license requires the server to be online and infoRouter customer services cannot be reached. The description names the day the application will stop: 30 days after the first failure. | Warning; Critical in the last 7 days; Fatal once the application has stopped |

### Error Response
```xml
<response success="false" error="[ErrorCode] Error message" errorCode="4030" />
```

| errorCode | When |
|-----------|------|
| 4010 | No authentication ticket, or an invalid or expired one |
| 4030 | The caller is not a system administrator |

## Required Permissions

System administrators only.

## Example

### Request (GET)
```
GET /srv.asmx/GetServerAlerts?authenticationTicket=abc123 HTTP/1.1
```

## Notes

- The server checks for the problems in its maintenance job, so an alert appears or disappears within a few minutes of the problem, not at once.
- An alert goes away by itself when the problem is gone; nobody has to dismiss it. To hide one meanwhile, use [DismissServerAlert](DismissServerAlert.md).
- A dismissed alert is shown again (`Dismissed="false"`) when its severity rises.
- Everything that happens to an alert - raised, severity changed, dismissed, cleared - is written to the `Alerts` log, readable with [GetLogs](GetLogs.md).
- When an alert is raised, and again when its severity rises, one email goes to the technical contact of the mail settings, or to the sysadmin account when there is none.
- While the application is stopped by a Fatal `CustomerServicesUnreachable` alert, every API answers with that alert's text as the error, this one included.
