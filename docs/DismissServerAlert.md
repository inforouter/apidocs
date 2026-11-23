# DismissServerAlert API

Dismisses one server alert. The alert stays in the list of [GetServerAlerts](GetServerAlerts.md), marked dismissed, so the user interface can stop showing it. The mark is one for all administrators.

## Endpoint

```
/srv.asmx/DismissServerAlert
```

## Methods

- **GET** `/srv.asmx/DismissServerAlert?authenticationTicket=...&alertType=...&subject=...`
- **POST** `/srv.asmx/DismissServerAlert` (form data)
- **SOAP** Action: `http://tempuri.org/DismissServerAlert`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `alertType` | string | Yes | The `Type` of the alert as `GetServerAlerts` returns it, for example `WarehouseDiskSpaceLow`. Upper and lower case do not matter. |
| `subject` | string | No | The `Subject` of the alert as `GetServerAlerts` returns it. Empty for an alert that has none. |

## Response

### Success Response
```xml
<root success="true" />
```

### Error Response
```xml
<root success="false" error="[ErrorCode] Error message" />
```

| Situation | Answer |
|-----------|--------|
| `alertType` is empty or not an alert type | `4000`, with the list of types |
| There is no such alert (the server may have cleared it meanwhile) | `4040` |
| The caller is not a system administrator | `4030` |

## Required Permissions

System administrators only.

## Example

### Request (POST)
```
POST /srv.asmx/DismissServerAlert HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&alertType=WarehouseDiskSpaceLow&subject=D%3A%5C
```

## Notes

- Who dismissed the alert and when is kept on the alert (`DismissedBy`, `DismissedOn`) and written to the `Alerts` log.
- Dismissing an alert that is already dismissed succeeds and changes nothing: the first dismissal stands.
- A dismissed alert is shown again when its severity rises, and it is removed when its problem is gone. If the problem comes back later, that is a new alert and it is shown.
- Dismissing does not stop anything: the server keeps checking, and a `CustomerServicesUnreachable` alert still stops the application on the day it names.
