---
search:
  exclude: true
---

# infoRouter UI internal API

!!! warning "Internal API"
    These operations are made for infoRouter's own user interface. They are not part of the public web
    API: there is no SOAP form and no promise of backward compatibility, and they may change or be removed
    in any release without notice. Do not use them in an integration.

They answer the same XML as the public operations, to GET (query string) and POST (form data), with the
same `authenticationTicket`, at:

```
/api/UIInternals/<OperationName>
```

Each operation keeps its own permission check. The public web API is documented at the [home page](../index.md).

## Settings

- [GetSmtpSettings](GetSmtpSettings.md) - Returns the SMTP settings in effect
- [SetSmtpSettings](SetSmtpSettings.md) - Replaces the SMTP settings and applies them at once, without restarting infoRouter
- [GetContentSearchSettings](GetContentSearchSettings.md) - Returns the content search settings in effect
- [SetContentSearchSettings](SetContentSearchSettings.md) - Replaces the content search settings and applies them at once, without restarting infoRouter
- [GetSignOnSettings](GetSignOnSettings.md) - Returns the sign-on settings in effect
- [GetConnectSettings](GetConnectSettings.md) - Returns what this infoRouter instance can ask the **infoRouter Connect** AI service for
- [GetGeneralAppSettings](GetGeneralAppSettings.md) - Returns the general application settings including upload limits, work days configuration, holidays, and system preferences
- [SetGeneralAppSettings](SetGeneralAppSettings.md) - Updates the global *General Application Settings* by sending a serialized `GeneralSettings` object
- [GetAuthenticationAndPasswordPolicy](GetAuthenticationAndPasswordPolicy.md) - Returns the authentication and password policy settings including password complexity requirements and password re-prompt actions
- [SetAuthenticationAndPasswordPolicy](SetAuthenticationAndPasswordPolicy.md) - Updates the authentication and password policy settings by sending a serialized `AuthenticationAndPasswordPolicy` object
- [GetSystemBehaviorSettings](GetSystemBehaviorSettings.md) - Returns the system behavior settings including login logging configuration, login delay (anti-brute-force) settings, and library manager policy editing permissions
- [SetSystemBehaviorSettings](SetSystemBehaviorSettings.md) - Updates the system behavior settings including login logging configuration and login delay (anti-brute-force) settings
- [GetEmailAndNotificationSettings](GetEmailAndNotificationSettings.md) - Returns all email and notification settings for the infoRouter system
- [SetEmailAndNotificationSettings](SetEmailAndNotificationSettings.md) - Updates the email and notification settings for the infoRouter system
- [FlushApplicationCache](FlushApplicationCache.md) - Flushes the in-memory application cache, forcing the system to reload configuration and cached data from the database and file system
- [GetLicenseInfo](GetLicenseInfo.md) - Retrieves the application license information including company details, licensed user counts, subscription dates, and feature flags

## Server health and maintenance

- [GetServerAlerts](GetServerAlerts.md) - Returns the server's current alerts
- [DismissServerAlert](DismissServerAlert.md) - Dismisses one server alert
- [GetWarehouseStatus](GetWarehouseStatus.md) - Returns warehouse storage status information including total document count, total warehouse size, per-warehouse path statistics, and disk drive information
- [GetMaintenanceJobsStatus](GetMaintenanceJobsStatus.md) - Returns the status of all system maintenance jobs including their last execution time, duration, success status, schedule type, and whether they are overdue
- [GetSystemStatistics](GetSystemStatistics.md) - Retrieves system-wide statistics including user counts, document counts, total document storage size, the number of checked-out documents, and the number of documents registered in the last 30, 60, and 90 days
