# Audit Managers

Group id `101`, stored as `[Audit Managers]`, enum value `enum_IR.AdmistrativeRoles.AuditManager`. The role reads: the audit logs of every library, the licence, the server and warehouse status, and the server log files. It changes nothing. It is a system group with no library (the group is created with library id 0), and its members are changed by Administrators only: `UpdateGroupMembers` adds no role for a group id up to `IRConstants.LastSystemUserGroupId` (1000), so only the administrator check at the top of `AccessAllowedforAdminFunctionsAsync` passes (`IRSecurity.cs`, IsAllowed; `UsergroupOperations.cs`, `UsergroupExtensions.cs`).

## How the role is checked

Four entries of the `IRSecurity.IsAllowed` matrix name the role:

| IrAdminAction | Required role | Library managers | Self |
|---|---|---|---|
| `ViewAuditLogs` | AuditManager | yes, when the call passes a library id (`localDomainId > 0`) | no |
| `ViewLicenseInformation` | AuditManager | no | no |
| `ViewServerStatus` | AuditManager | no | no |
| `ViewWarehouseStatus` | AuditManager | no | no |

Order in `AccessAllowedforAdminFunctionsAsync`: an administrator (the `sysadmin` account or a member of `[Administrators]`) passes first; then membership of `[Audit Managers]`; then, for `ViewAuditLogs` only and only when a library id was passed, `SecurityFunctions.CheckDomainManagementAsync` (a row in DOMAINMANAGERS for that library). None of the four is a self action.

Several audit calls ask for a right on the item first and fall back to `ViewAuditLogs` only when that right is missing; the tables below say which. A refusal from the matrix is `errorCode="4030"` with the message `Access denied. This action is restricted to the following roles: The system administrator, Audit managers`; when the call passed a library id the list also names `Library manager(s)`. One exception is noted under "Rules that look wrong": a refused `GetSoxLogs` answers `4000`.

## What the role can do

Administrators may do everything below. Every audit-log call also keeps a row limit: more than 10,000 matching rows is `4000` `Maximum log display count exceeded (10000). Please narrow down your query.` (`AuditLogFilter.DefaultMaxRecordCount`); the security change log uses the `MaxDisplayAccessListHistoryCount` UI setting instead.

### Audit logs by date range and path filter

These eight calls take `startDate`, `endDate` and `pathFilter` and go through `LogOperations.IsLogAccessAllowed`, which checks `ViewAuditLogs` and nothing else: no right on any item is asked.

| Action | Web service calls | Who else may do it | Conditions |
|---|---|---|---|
| Read the checkout and check-in logs | [GetCheckoutLog](GetCheckoutLog.md), [GetCheckInLog](GetCheckInLog.md) | library managers, when `pathFilter` starts with the name of a library they manage | see below |
| Read the version logs | [GetVersionCreateLog](GetVersionCreateLog.md), [GetVersionDeleteLog](GetVersionDeleteLog.md) | same | see below |
| Read the creation and deletion logs | [GetNewDocumentsAndFoldersLog](GetNewDocumentsAndFoldersLog.md), [GetDeleteLog](GetDeleteLog.md) | same | see below |
| Read the disposition and ownership logs | [GetDispositionLog](GetDispositionLog.md), [GetOwnershipChangeLog](GetOwnershipChangeLog.md) | same | see below |

Conditions, from `LogOperations.IsLogAccessAllowed` and `DocumentsAndFoldersWs.BuildAuditFilter`:

- With no `pathFilter`, the library id passed to the matrix is 0: only Audit Managers (and administrators) pass, and the log spans every library.
- With a `pathFilter`, its first segment is looked up as a library name through `DomainOperations.GetLibraryByNameAsync`, and that library's id is passed to the matrix, which is why a library manager passes for their own library. The lookup itself answers `4041` `Library not found` unless the caller can reach the library (see the first warning below).
- A `pathFilter` that is only a library name is cleared to "the whole library"; a longer one filters rows by path. `BuildAuditFilter` sets only the two dates and the path, so the folder-id and document-id branches of `IsLogAccessAllowed` are never reached from the API.

### Logs of one document or folder

These calls name an item by path. The item is first loaded by `GetDocumentByPathAsync` / `GetFolderByPathAsync`, which is `4041` when the item is not in a library the caller is a member of or that allows anonymous access (see the second warning). Then, for each, a right on the item is tried first and `ViewAuditLogs` for the item's library is the fallback, so library managers of that library pass as well.

| Action | Web service calls | Who else may do it | Conditions |
|---|---|---|---|
| Read a document's SOX log | [GetSoxLogs](GetSoxLogs.md) | anyone with `DocumentReadSoxLog` on the document; the item's library managers | `4230` while the document is offline, checked before the role (`DocumentExtensions.GetSoxLogsAsync`) |
| Read a document's ISO log | [GetISOLogs](GetISOLogs.md) | anyone with `DocumentReadIsoLog` on the document; the item's library managers | `4230` while the document is offline, checked before the role (`DocumentExtensions.GetIsoLogsAsync`) |
| Read the classification log of a document or folder | [GetClassificationLogs](GetClassificationLogs.md) | anyone with `DocumentReadClassificationLog` on the document or folder (a library policy); the item's library managers | `LogOperations.GetClassificationLogsAsync` |
| Read the access list and its history | [GetAccessListHistory](GetAccessListHistory.md) | anyone with `ReadSecurityAccessList` on the item; the item's library managers | The call reads the current list with `orAuditLogReader` set and then the history; both accept `ViewAuditLogs` for the item's library when the right is missing (`Document/Folder.GetAccessListAsync`, `GetAccessListHistoryAsync`) |
| Read the security change log of a document, a folder or a library | [GetSecurityChangeLog](GetSecurityChangeLog.md) | anyone with `ReadSecurityAccessList` on the document or folder; the library's managers, the library root included | A document: `Document.GetAccessListHistoryAsync`. A subfolder: `LogOperations.GetAccessListHistoryAsync` with `FolderId` set, right on the folder first, then `ViewAuditLogs` with `LibraryId`. The library root: `FolderId` 0, so the right is not tried and `ViewAuditLogs` with `LibraryId` decides, which a library manager passes (`FolderServices.GetSecurityChangeLogAsync`). An unknown `userName` filter is `4041` before any of this |

### Licence, server and warehouse

All four actions are checked with library id 0, so library managers never pass; nobody but Audit Managers and administrators may call these.

| Action | Web service calls | Who else may do it | Conditions |
|---|---|---|---|
| See the licence and the licensed-user counts | [GetLicenseInfo](GetLicenseInfo.md) | nobody else | `ViewLicenseInformation` (`MiscServices.GetLicenseInfoAsync`) |
| See the system statistics | [GetSystemStatistics](GetSystemStatistics.md) | nobody else | `ViewServerStatus` (`MiscServices.GetSystemStatisticsAsync`) |
| See the maintenance jobs' last runs | [GetMaintenanceJobsStatus](GetMaintenanceJobsStatus.md) | nobody else | `ViewServerStatus` (`MiscServices.GetMaintenanceJobsStatusAsync`) |
| See the warehouse paths and totals | [GetWarehouseStatus](GetWarehouseStatus.md) | nobody else | `ViewWarehouseStatus` (`InfoRouter.WarehouseInfoAsync`) |
| Read the server log files | [GetLogStatistics](GetLogStatistics.md), [GetLogStatistics1](GetLogStatistics1.md), [GetLogs](GetLogs.md) | nobody else | `ViewServerStatus` (`ServerLogs.CanReadLogsAsync`). An unknown `logType` is `4000` before the role check; `lastNDays` over 365 is `4000` |

## What the role cannot do

| Action | Web service calls | Who can | Error returned |
|---|---|---|---|
| Replace the licence | [UpdateApplicationLicense](UpdateApplicationLicense.md) | administrators only (`IsAdministrator()` in `InfoRouterExtensions.UpdateLicenseInformation`) | `4030` `Access denied.` |
| Flush the application cache | [FlushApplicationCache](FlushApplicationCache.md) | administrators only (no role in the matrix) | `4030` `Access denied. This action is restricted to the following roles: The system administrator` |
| Read what a user has viewed | [GetUserViewLog](GetUserViewLog.md), [GetUserViewLog1](GetUserViewLog1.md), [GetUserViewLogLite](GetUserViewLogLite.md) | the user themselves, User Managers, the managers of the user's own library (local users only); `ListingAuditLogOfUser` in `User.GetReadLogAsync` | `4030` `Access denied. This action is restricted to the following roles: The system administrator, User managers` (plus `Library manager(s)` for a local user) |
| Read who viewed a document | [GetDocumentReadLogHistory](GetDocumentReadLogHistory.md) | anyone with `DocumentReadViewLog` on the document; there is no role fallback (`Document.GetAllViewLogsAsync`) | `4030` from the item permission check |
| Read an item's current access list without the history | [GetAccessList](GetAccessList.md) | anyone with `ReadSecurityAccessList` on the item; `orAuditLogReader` is false here | `4030` from the item permission check |
| Add or remove members of `[Audit Managers]` or any role group | [AddUsergroupMember](AddUsergroupMember.md), [RemoveUsergroupMember](RemoveUsergroupMember.md) | administrators only | `4030` `Access denied. This action is restricted to the following roles: The system administrator` |
| Read or change application settings | [GetSystemBehaviorSettings](GetSystemBehaviorSettings.md), [GetEmailAndNotificationSettings](GetEmailAndNotificationSettings.md) and the `Set…` settings calls | Policy Managers (`UpdateApplicationSettingsAndPolicies`, `SettingServices.cs`) | `4030` naming Policy managers |

The weekly technical status report (`SendTechnicalStatusReport`) is a maintenance job in `IRDiagnostics.JobTypes()`, not a web service call; no role triggers it.

## Rules that look wrong

!!! warning "A path filter names a library the Audit Manager must belong to"
    `LogOperations.IsLogAccessAllowed` resolves the first segment of `pathFilter` with `DomainOperations.GetLibraryByNameAsync`, whose `MayReachAsync` admits a member of the library, anyone where it allows anonymous access, and whoever passes `ListLibrariesForAdministration`: administrators, User Managers, Policy Managers and the library's own managers. `AuditManager` is not in that action, so an Audit Manager who is not a member of the library gets `4041` `Library not found` from the eight date-range logs when filtering by that library, while the same call with no filter answers them with every library's rows, that library included. Task #20 of the fix list is still open for this role (commit 61e1fb36 fixed it for administrators, User and Policy Managers). Meanwhile the UI should offer an Audit Manager only the libraries [GetDomains](GetDomains.md) returns for them as filter values, or treat `4041` on a filtered query as "not reachable" rather than "no such library".

!!! warning "The per-item logs are reachable only inside the caller's own libraries"
    `GetSoxLogs`, `GetISOLogs`, `GetClassificationLogs`, `GetAccessListHistory` and `GetSecurityChangeLog` load the item by path first. `DocumentLoadOperation.GetDocumentAsync` and `FolderOperations.GetFolderAsync` answer `4041` (`Document not found.` / `The folder has either been deleted or is not accessible.`) unless the item's library is in `DomainsStore.GetViewableLibraryListAsync` for the caller, which is the libraries the caller is a member of plus those allowing anonymous access. That lookup has no role or administrator bypass (only the internal system account, id 3, is exempt), so the `ViewAuditLogs` fallback in these calls is reached only for items in libraries the Audit Manager already belongs to. The UI should not offer these five calls for a path outside the caller's libraries, and should read `4041` on them as "not reachable", not as "the role is missing".

!!! warning "A refused GetSoxLogs answers 4000, its siblings 4030"
    `DocumentExtensions.GetSoxLogsAsync` keeps the refusal text in a string and returns `Result.BadRequest(responseStr)`, so a caller without `DocumentReadSoxLog` and without the audit role gets `errorCode="4000"` with the access-denied message. `GetIsoLogsAsync`, `GetClassificationLogsAsync` and the security logs return the matrix result unchanged, `4030`. A UI that hides on `4030` will not recognise this refusal; check the message, or treat `4000` from `GetSoxLogs` as a refusal too, until the code returns `AccessDenied`.

!!! warning "View logs are not audit logs"
    Who viewed what is held under `ListingAuditLogOfUser` for the user calls (`GetUserViewLog`, `GetUserViewLog1`, `GetUserViewLogLite`: self, User Managers, the user's library managers) and under the item right `DocumentReadViewLog` for `GetDocumentReadLogHistory`, with no `ViewAuditLogs` fallback in either (`UserExtensions.GetReadLogAsync`, `DocumentExtensions.GetAllViewLogsAsync`). An Audit Manager who reads every checkout, check-in, delete and security change in the system is refused a user's view log with a message naming User Managers. Whether the rule is wrong is for the product to decide; the UI should put the view logs under the User Managers role, not under this one, and expect `4030` here.

## Finding out whether the signed-in user has this role

- [GetGroupMembershipsOfUser](GetGroupMembershipsOfUser.md) with the caller's own user name: the check is `ListingGroupMembershipOfUser`, which allows a self action, so it always answers for yourself (`UserServices.GetGroupMembershipsOfUserAsync`, `UserExtensions.AccessAllowedForUserAsync`). A group with `GroupID` `101` in the answer is this role; `104` means the caller is an administrator and passes every check on this page.
- [GetLicenseInfo](GetLicenseInfo.md) is a cheap probe for the server area as a whole: it has no fallback, so `success="true"` means the caller is an Audit Manager or an administrator, and `4030` means neither.
- For the audit-log area a library manager passes too, so a `4030` on a filtered log does not mean the caller lacks the role for every library; the Library Managers page says how to list the libraries someone manages.

## Notes

- `ViewAuditLogs` is the only one of the four actions that admits library managers, and only through the library id the call passes. The date-range logs pass the id resolved from `pathFilter` (0 without one); the item logs pass the item's `DomainId`; `GetSecurityChangeLog` passes the folder's library, at the root included, which closed task #13 (`LogOperations.GetAccessListHistoryAsync`). Test: `AuditLogBatchApiTests.GetSecurityChangeLog_AtTheLibraryRoot_AnswersItsManager_ButNotAPlainMember`.
- `GetAccessListHistory` passes `WithHistory=true` from `Srv.cs`, which sets `orAuditLogReader` on the current-list read; without it (`GetAccessList`) the item right alone decides. That closed task #14. Test: `AuditLogBatchApiTests.GetAccessListHistory_AnswersAnAuditManager_WithoutTheRightOnTheFolder`.
- `GetClassificationLogs` tries the library's `DocumentReadClassificationLog` policy on the item before the role (task #15). Test: `AuditLogBatchApiTests.GetClassificationLogs_FollowsTheLibrarysPolicy_SoTheOwnerMayReadThem`.
- The server log files were administrators only until `ServerLogs.CanReadLogsAsync` was changed to `ViewServerStatus` (task #12). Test: `ServerAndLicenseBatchApiTests.ServerLogs_ByAnAuditManager_Answer_ButNotForAUserManager`.
- `GetLogStatistics` and `GetLogs` validate `logType` in `MiscServices` before `ServerLogs` checks the role, so a caller without the role sees `4000` for a bad type and `4030` for a good one.
- The SOX and ISO logs refuse an offline document with `4230` before any permission check, for everyone.
- The user named in `GetSecurityChangeLog`'s `userName` filter is looked up with `GetUserAsync(name, false)`, that is without the user-visibility check; an unknown name is `4041`.
- Tasks #17 and #31 of the fix list do not touch this role.

## Related

- [AdministrativeRoles](AdministrativeRoles.md), all roles at a glance
- the other role pages: [Administrators](AdministratorsRole.md), [User Managers](UserManagersRole.md), [Policy Managers](PolicyManagersRole.md), [R&D Managers](RDManagersRole.md), [Search & Category Administrators](SearchAdministratorsRole.md), [Library Managers](LibraryManagersRole.md)
