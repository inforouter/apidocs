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

## User interface configuration

- [GetCustomMenus](GetCustomMenus.md) - Returns the custom menus this infoRouter installation adds to the document list, as an administrator set them with [SetCustomMenus](SetCustomMenus.md)
- [SetCustomMenus](SetCustomMenus.md) - Replaces every custom menu the document list draws, and their entries, in the order given
- [GetAllFolderColumns](GetAllFolderColumns.md) - Returns all available folder column definitions that can be used for configuring folder display views
- [GetDefaultFolderColumns](GetDefaultFolderColumns.md) - Returns the system default folder column configuration
- [SetDefaultFolderColumns](SetDefaultFolderColumns.md) - Sets the system default folder columns using a comma-separated list of column names
- [GetUserFolderColumns](GetUserFolderColumns.md) - Returns the effective column layout and custom property set preference saved for the authenticated user on the specified folder
- [SetUserFolderColumns](SetUserFolderColumns.md) - Saves the column layout and custom property set preference for the authenticated user on the specified folder
- [SetTagDefinitions](SetTagDefinitions.md) - Replaces the whole list of tag definitions
- [GetAddIns](GetAddIns.md) - Returns a list of all infoRouter client add-ins available on the server, including name, setup version, DLL version, and description
- [GetSignInOptions](GetSignInOptions.md) - Returns what a user can sign in with on this server

## Dashboard statistics

- [GetRecycleBinStatistics](GetRecycleBinStatistics.md) - Answers what the recycle bins of the whole instance hold, by where it is
- [GetAllDomainStatistics](GetAllDomainStatistics.md) - Returns the statistics of every domain/library in the caller's library list, in one call
- [GetUserStatistics](GetUserStatistics.md) - Returns activity and membership statistics for a specified user, including document counts, folder counts, task counts, workflow roles, and library memberships
- [GetFolderAccessListStatistics](GetFolderAccessListStatistics.md) - Counts the subfolders and documents under a folder whose access list is not the folder's own
- [GetFolderAccessListCatalog](GetFolderAccessListCatalog.md) - Lists the subfolders and documents under a folder that hold an access list of their own, each with counts of what inherits from it
- [GetLibrariesForAdministration](GetLibrariesForAdministration.md) - Returns the domains/libraries the calling user may administer, whether or not they belong to them
- [GetMembersWithoutAccess](GetMembersWithoutAccess.md) - Returns the members of a domain/library whose right on the library is below a minimum

## WebDAV sessions

- [CreateWebDavSession](CreateWebDavSession.md) - Creates a WebDAV session ticket for the signed-in user, to map infoRouter as a drive in Windows File Explorer or any WebDAV client
- [GetWebDavSessions](GetWebDavSessions.md) - Lists the WebDAV session tickets of the signed-in user
- [RemoveWebDavSession](RemoveWebDavSession.md) - Removes one of the signed-in user's WebDAV session tickets

## Libraries and Connect

- [SetDomainPolicies](SetDomainPolicies.md) - Sets the policies for a domain/library
- [GetConnectProfile](GetConnectProfile.md) - Has the local **infoRouter Connect** service profile a document version — a summary, a description, an abstract, keywords, the document type, the text of a scan, the values of a property set — and reports where each of the things you asked for has got to

## Recycle bin

- [EmptyAllUserRecycleBins](EmptyAllUserRecycleBins.md) - Empties every user's Recycle Bin into the system recycle bin, one user at a time

## User offboarding

- [TransferUserTasks](TransferUserTasks.md) - Transfers all open workflow tasks from one user to another
- [TransferUserDomainMemberships](TransferUserDomainMemberships.md) - Transfers domain/library memberships from one user to another
- [TransferUserGroupMemberships](TransferUserGroupMemberships.md) - Transfers user group memberships from one user to another
- [TransferUserDomainManagerRoles](TransferUserDomainManagerRoles.md) - Transfers domain/library manager roles from one user to another
- [TransferUserSecurityPermissions](TransferUserSecurityPermissions.md) - Transfers security permissions (ACL entries) from one user to another
- [TransferUserWorkflowDefinitions](TransferUserWorkflowDefinitions.md) - Transfers workflow definition roles (assignees and supervisors) from one user to another
- [TransferUserISOTasks](TransferUserISOTasks.md) - Transfers ISO review tasks from one user to another
- [TransferUserCheckedOutDocuments](TransferUserCheckedOutDocuments.md) - Transfers checked-out documents from one user to another
- [TransferUserFolderOwnerships](TransferUserFolderOwnerships.md) - Transfers folder ownerships from one user to another
- [TransferUserDocumentOwnerships](TransferUserDocumentOwnerships.md) - Transfers document ownerships from one user to another
- [TransferUserDocumentSubscriptions](TransferUserDocumentSubscriptions.md) - Transfers document subscriptions from one user to another
- [TransferUserFolderSubscriptions](TransferUserFolderSubscriptions.md) - Transfers folder subscriptions from one user to another
- [TransferUserExpirationNotices](TransferUserExpirationNotices.md) - Transfers document expiration notices from one user to another
