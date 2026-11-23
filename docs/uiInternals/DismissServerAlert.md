---
search:
  exclude: true
---

# DismissServerAlert API

**Available in:** infoRouter 9.0 and later

!!! warning "Internal API"
    Made for infoRouter's own user interface. It is not part of the public web API: there is no SOAP
    form and no promise of backward compatibility, and it may change or be removed in any release
    without notice. Do not use it in an integration.

Dismisses one server alert. The alert stays in the list of [GetServerAlerts](GetServerAlerts.md), marked dismissed, so the user interface can stop showing it. The mark is one for all administrators.

## Endpoint

```
/api/UIInternals/DismissServerAlert
```

## Methods

- **GET** `/api/UIInternals/DismissServerAlert?authenticationTicket=...&alertType=...&subject=...`
- **POST** `/api/UIInternals/DismissServerAlert` (form data)

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `alertType` | string | Yes | The `Type` of the alert as `GetServerAlerts` returns it, for example `WarehouseDiskSpaceLow`. Upper and lower case do not matter. |
| `subject` | string | No | The `Subject` of the alert as `GetServerAlerts` returns it. Empty for an alert that has none. |

## Response

### Success Response
```xml
<response success="true" error="" />
```

### Error Response
```xml
<response success="false" error="[ErrorCode] Error message" errorCode="4030" />
```

| errorCode | When |
|-----------|------|
| 4000 | `alertType` is empty or not an alert type; the error lists the types |
| 4010 | No authentication ticket, or an invalid or expired one |
| 4030 | The caller is not a system administrator |
| 4041 | There is no such alert (the server may have cleared it meanwhile) |

## Required Permissions

System administrators only.

## Example

### Request (POST)
```
POST /api/UIInternals/DismissServerAlert HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&alertType=WarehouseDiskSpaceLow&subject=D%3A%5C
```

## Notes

- Who dismissed the alert and when is kept on the alert (`DismissedBy`, `DismissedOn`) and written to the `Alerts` log.
- Dismissing an alert that is already dismissed succeeds and changes nothing: the first dismissal stands.
- A dismissed alert is shown again when its severity rises, and it is removed when its problem is gone. If the problem comes back later, that is a new alert and it is shown.
- Dismissing does not stop anything: the server keeps checking, and a `CustomerServicesUnreachable` alert still stops the application on the day it names.
