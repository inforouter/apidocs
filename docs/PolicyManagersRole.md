# Policy Managers

Group id `102`, stored as `[Policy Managers]`, enum value `enum_IR.AdmistrativeRoles.PolicyManager`
(`IRBase\IRBaseEnum.cs`). The role is for the application-wide settings (general, authentication and password,
system behaviour, e-mail and notification, default folder columns) and for the policies of every library. It is a
system group: it belongs to no library (`DOMAINID` 0, `setup\PatchLibrary\...\Update_8_2_000_updater.cs`), and only
Administrators can add or remove its members. `IRSecurity.IsAllowed` gives `UpdateGroupMembers` no role and no
library-manager pass for a group id up to `IRConstants.LastSystemUserGroupId` (1000), so only the administrator
check at the top of `AccessAllowedforAdminFunctionsAsync` lets a member change.

## How the role is checked

Three entries of the `IRSecurity.IsAllowed` matrix name the role (`IRNET\IRSecurity.cs`):

| IrAdminAction | Required roles | Self | Library managers |
|---|---|---|---|
| `UpdateApplicationSettingsAndPolicies` | PolicyManager | no | no |
| `UpdateLibraryPolices` | PolicyManager | no | only when the system behaviour setting `AllowLibraryManagersToEditPolicy` is on |
| `ListLibrariesForAdministration` | UserManager, PolicyManager | no | yes |

Order of the decision (`IRSecurity.AccessAllowedforAdminFunctionsAsync`, then `IsAllowed`):

1. An administrator (`ThreadVariables.IsAdministrator()`: the `sysadmin` account or a member of `[Administrators]`) passes everything.
2. Self-service: none of the three actions allows it.
3. Membership of a required role group (`UsergroupMembersStore.IsMemberOfAnyGroupAsync`).
4. Library managers, only when the action allows them and a library id above 0 was passed (`SecurityFunctions.CheckDomainManagementAsync`, `IRNET\ModuleSecurityFunctions.cs`). The settings calls pass `localDomainId` 0, so no library manager ever passes them.

A refusal is `errorCode="4030"` with the message `Access denied. This action is restricted to the following roles:
The system administrator, Policy managers` (`Messages.AccessDenied`, `ActionRestrictedToFollowingRoles`,
`TheSystemAdministrator`, `PolicyManagers`). For a library policy change with the setting on, `Library manager(s)`
is listed as well.

Administrators always pass every check below; the tables do not repeat it.

## What the role can do

### Application settings

All of these call `AccessAllowedforAdminFunctionsAsync(UpdateApplicationSettingsAndPolicies, UNSPECIFIED, 0, 0)` first.

| Action | Web service calls | Who else may do it | Conditions |
|---|---|---|---|
| Change the general settings | [SetGeneralAppSettings](SetGeneralAppSettings.md) | nobody else | `InfoRouterExtensions.UpdateGeneralApplicationSettings` after `SettingServices.SetGeneralAppSettingsAsync`; both check. Recycle bin months 0 to 36, holiday description length checked after the role. |
| Change the authentication and password policy | [SetAuthenticationAndPasswordPolicy](SetAuthenticationAndPasswordPolicy.md) | nobody else | `SettingServices.SetAuthenticationAndPasswordPolicyAsync` and `InfoRouterExtensions.UpdateAuthenticationAndPasswordPolicySettings` both check. |
| Change the system behaviour settings | [SetSystemBehaviorSettings](SetSystemBehaviorSettings.md) | nobody else | Includes `AllowLibraryManagersToEditPolicy` (stored as `LIBMANAGERS_EDITPOLICY`), the flag that decides whether library managers may change library policies. |
| Read the system behaviour settings | [GetSystemBehaviorSettings](GetSystemBehaviorSettings.md) | nobody else | `SettingServices.GetSystemBehaviorSettingsAsync`. |
| Change the e-mail and notification settings | [SetEmailAndNotificationSettings](SetEmailAndNotificationSettings.md) | nobody else | Role checked before the XML is parsed; a refused caller gets 4030, not 4000. |
| Read the e-mail and notification settings | [GetEmailAndNotificationSettings](GetEmailAndNotificationSettings.md) | nobody else | `SettingServices.GetEmailAndNotificationSettingsAsync` checks the same action as the writer (task #10 confirmed). No SMTP server or credentials are in it. |
| Set the system default folder columns | [SetDefaultFolderColumns](SetDefaultFolderColumns.md) | nobody else | Anonymous callers get 4010 first; then the role (`SettingServices.SetDefaultFolderColumnsAsync`), then `InfoRouter.SaveSystemDefaultColumnSettings` checks it again. No administrators-only check remains (task #11 confirmed). |

### Library policies

| Action | Web service calls | Who else may do it | Conditions |
|---|---|---|---|
| Read a library's policies | [GetDomainPolicies](GetDomainPolicies.md) | the library's managers, always | `Domain.AccessAllowedToReadPoliciesAsync` (`DomainExtensions.cs`): `UpdateLibraryPolices` first, then `CheckDomainManagementAsync` for the library's managers (task #19 confirmed). The library is looked up by name first; one the caller cannot reach is 4041 `Library not found`. |
| Change a library's policies | [SetDomainPolicies](SetDomainPolicies.md) | the library's managers, only when `AllowLibraryManagersToEditPolicy` is on | `LibraryServices.SetDomainPoliciesAsync` checks `UpdateLibraryPolices` with the library id, and `DomainPolicyOperations.UpdatePoliciesAsync` checks it again. System policies in the XML are skipped. The change is logged to `Logs\PolicyUpdates`. |
| Reach any library by name, member or not | every call that takes a `DomainName` | User Managers for every library; a library's own managers for it; members; anyone, for a library that allows anonymous access | `DomainOperations.MayReachAsync`: membership or anonymous access (`DomainsStore.GetViewableLibraryListAsync`), else `ListLibrariesForAdministration` with the library's id. Reaching is only the lookup; each call then makes its own check. |
| List every library, membership aside | [GetLibrariesForAdministration](GetLibrariesForAdministration.md) | User Managers; library managers get the libraries they manage; anyone else gets an empty list | `UserOperations.GetLibraryListForAdministrationAsync`: `ListLibrariesForAdministration` with library id 0 passes the role, then `DomainsStore.GetAllLibrariesAsync` (hidden and archived included). Anonymous callers get 4010. |

### Settings reads that need no role

These are listed so the UI does not hide them from anyone; they are not what the role unlocks.

| Action | Web service calls | Who may do it | Conditions |
|---|---|---|---|
| Read the general settings | [GetGeneralAppSettings](GetGeneralAppSettings.md) | anyone signed in | Anonymous callers get 4010 (`IsAuthenticatedUser()`). |
| Read the authentication and password policy | [GetAuthenticationAndPasswordPolicy](GetAuthenticationAndPasswordPolicy.md) | anyone signed in | Same check. |
| Read the default and available folder columns | [GetDefaultFolderColumns](GetDefaultFolderColumns.md), [GetAllFolderColumns](GetAllFolderColumns.md) | anyone, the anonymous user included | No check in `SettingServices`; a call with no ticket runs as the anonymous user (`GetUserInfoFromInfoRouterAsync.IRServiceLogin`). |
| Read the public application parameters | [getApplicationParameters](getApplicationParameters.md) | anyone signed in | `SettingsWebServices.GetApplicationParametersAsync`. The block after `ALLOWPARTIALEMAILUPLOADS` (`INDEXCATALOG`, `LOGLOGINS`, `FILEUPLOADTIMEOUT`, `ALLOWOWNERSHIPTRANSFER`, `SUBSCRIPTIONNOTIFICATIONS`, `SENDEMAIL`, `SENDTO_DISPLAYUSERLIST`, `SMTPSERVER`, `SMTPSERVERPORT`, `SMTPCONNECTIONTIMEOUT`, `SMTPSENDUSERNAME`, `SMTPSENDPASSWORD` masked, `PWD*`, `AuthenticationAuthorities`, `ServerName`, `IPAddressList`, `WarehousePaths`) is written only when `IsAdministrator()` is true. A Policy Manager gets the public block only. |
| Read the Connect settings report | [GetConnectSettings](GetConnectSettings.md) | anyone signed in | `ConnectServices.GetConnectSettingsAsync`: 4010 for anonymous, no role. |

## What the role cannot do

| Action | Web service calls | Who can | Error returned |
|---|---|---|---|
| Flush the application cache | [FlushApplicationCache](FlushApplicationCache.md) | Administrators only: `IsAllowed` adds no role for `FlushApplicationCache` (task #1) | 4030 `Access denied. This action is restricted to the following roles: The system administrator` |
| Update the licence | [UpdateApplicationLicense](UpdateApplicationLicense.md) | Administrators only (`InfoRouterExtensions.UpdateLicenseInformation`, `IsAdministrator()`) | 4030 `Access denied.` |
| See the licence, server status, maintenance jobs, warehouse status | [GetLicenseInfo](GetLicenseInfo.md), [GetSystemStatistics](GetSystemStatistics.md), [GetMaintenanceJobsStatus](GetMaintenanceJobsStatus.md), [GetWarehouseStatus](GetWarehouseStatus.md) | Audit Managers (`ViewLicenseInformation`, `ViewServerStatus`, `ViewWarehouseStatus`; `MiscServices.cs`, `InfoRouter.cs:1235`) | 4030, roles listed: the system administrator, Audit managers |
| See the extended block of `getApplicationParameters` | [getApplicationParameters](getApplicationParameters.md) | Administrators only (`IsAdministrator()`) | No error: the call succeeds with the public block only |
| Create, rename, delete, archive or unarchive a library | [CreateDomain](CreateDomain.md), [UpdateDomain](UpdateDomain.md), [DeleteDomain](DeleteDomain.md), [ArchiveDomain](ArchiveDomain.md), [UnarchiveDomain](UnarchiveDomain.md) | Administrators only (`DomainOperations.CreateAsync`, `DeleteAsync`; `DomainExtensions.UpdateAsync`, `ArchiveAsync`, `UnArchiveAsync`: `IsAdministrator()`) | 4030 `Only the system administrator can perform this operation` |
| Add or remove library members | [AddUserAsDomainMember](AddUserAsDomainMember.md), [AddUserGroupAsDomainMember](AddUserGroupAsDomainMember.md), [RemoveUserFromDomainMembership](RemoveUserFromDomainMembership.md), [RemoveUserGroupFromDomainMembership](RemoveUserGroupFromDomainMembership.md) | User Managers; the library's managers (`AddRemoveLibraryMembers`; `DomainExtensions.cs`, `DomainOperations.cs:44`) | 4030, roles listed: the system administrator, Library manager(s), User managers |
| Appoint or remove library managers | [AddManagerToDomain](AddManagerToDomain.md), [RemoveManagerFromDomain](RemoveManagerFromDomain.md) | User Managers only (`AddRemoveLibraryManagers`, no library-manager pass; `DomainExtensions.SetDomainManagerAsync`, `RemoveDomainManagerAsync`) | 4030, roles listed: the system administrator, User managers |
| Add or remove members of `[Policy Managers]` or any role group | [AddUsergroupMember](AddUsergroupMember.md), [RemoveUsergroupMember](RemoveUsergroupMember.md) | Administrators only (`UpdateGroupMembers` for group ids up to 1000; `UsergroupExtensions.cs:64`, `UsergroupOperations.cs:229`) | 4030, roles listed: the system administrator |
| Create, change or delete document types | [CreateDocumentTypeDef](CreateDocumentTypeDef.md), [CreateDocumentTypeDef1](CreateDocumentTypeDef1.md), [UpdateDocumentTypeDef](UpdateDocumentTypeDef.md), [UpdateDocumentTypeDef1](UpdateDocumentTypeDef1.md), [DeleteDocumentTypeDef](DeleteDocumentTypeDef.md) | Administrators only (`DocumentTypeOperations.CreateDocumentTypeAsync`, `UpdateAsync`, `DeleteAsync`: `IsAdministrator()`) | 4030 `Only the system administrator can perform this operation` |
| Create, change or delete property sets and their fields | [CreatePropertySetDefinition](CreatePropertySetDefinition.md), [CreatePropertySetDefinition1](CreatePropertySetDefinition1.md), [UpdatePropertySetDefinition](UpdatePropertySetDefinition.md), [UpdatePropertySetDefinition1](UpdatePropertySetDefinition1.md), [DeletePropertySetDefinition](DeletePropertySetDefinition.md), [AddPropertySetField](AddPropertySetField.md), [DeletePropertySetField](DeletePropertySetField.md) | Administrators only (`PropertySetOperations.CreatePropertySet`, `PropertySetExtensions.UpdateAsync`, `AddFieldAsync`, `RemoveField`, `InfoRouter.DeletePropertySetAsync`: `IsAdministrator()`) | 4030 `Only the system administrator can perform this operation` |
| Define retention and disposition schedules | [CreateRandDSchedule](CreateRandDSchedule.md), [UpdateRandDSchedule](UpdateRandDSchedule.md), [DeleteRandDSchedule](DeleteRandDSchedule.md), [DeleteRandDSchedule1](DeleteRandDSchedule1.md) | R&D Managers (`AddRDDef`, `UpdateRDDef`, `DeleteRDDef`; `RetentionAndDispositionOperations.cs`) | 4030, roles listed: the system administrator, R&D managers |
| See other users' workflow tasks | [getTasks](getTasks.md), [GetTasks1](GetTasks1.md) when the criteria name no document or flow and do not name the caller as assignee, assigner or supervisor | Administrators see every task; library managers those of the libraries they manage (`WorkflowOperations.GetTasksAsync`, `DomainsStore.GetLibraryListForAdministrationAsync`) | No error: a Policy Manager gets their own tasks only (task #16 confirmed) |

## Rules that look wrong

!!! warning "Dead code: SetDomainPolicyTemplate (task #31, open)"
    `DomainExtensions.SetDomainPolicyTemplate` checks `UpdateLibraryPolices` and resets a library's rules and
    policies to the defaults, but nothing calls it: no WebServices method, no `ISrv` operation. There is no
    "reset policies to default" API for a Policy Manager; the UI must not offer one until it exists. Its only
    accepted template name is `default`.

!!! warning "Dead branch: GetLibraryListForAdministrationAsync for another user (task #31, open)"
    `UserOperations.GetLibraryListForAdministrationAsync(cn, threadInfo, userId)` has a branch for a `userId` other
    than the caller that checks `ListLibrariesForAdministration` and returns the libraries that user manages. Its
    only caller, `InfoRouter.GetLibrariesForAdministrationAsync`, passes the caller's own id, so the branch never
    runs. [GetManagedDomainsByUser](GetManagedDomainsByUser.md) lists the libraries another user manages through
    its own rule (`UserServices.GetManagedDomainsByUserAsync`) and does not use this branch; nothing for the UI to show.

## Finding out whether the signed-in user has this role

- [GetGroupMembershipsOfUser](GetGroupMembershipsOfUser.md) with the caller's own name: `ListingGroupMembershipOfUser` allows self (`UserServices.cs:992`, `User.AccessAllowedForUserAsync` passes `USER` and the user's id). A `GroupID` of `102` in the answer is this role; `104` is an administrator, who passes every check on this page without being in group 102.
- [GetLibrariesForAdministration](GetLibrariesForAdministration.md): every library for a Policy Manager, User Manager or administrator; only the managed ones for a library manager; empty for anyone else. It does not say which of the three the caller is.
- [GetSystemBehaviorSettings](GetSystemBehaviorSettings.md) succeeds only for a Policy Manager or an administrator, so a 4030 from it means the caller is neither.
- [getApplicationParameters](getApplicationParameters.md): the `SMTPSERVER` or `WarehousePaths` element is present only for an administrator; it says nothing about this role.

## Notes

- **The flag that lets library managers edit policies is itself a Policy Manager setting.** `AllowLibraryManagersToEditPolicy` is part of the system behaviour settings (`SetSystemBehaviorSettings`), so a Policy Manager decides whether library managers may change their libraries' policies. Reading policies does not depend on it (`Domain.AccessAllowedToReadPoliciesAsync`).
- **Reading a library's policies, by whom.** A Policy Manager and a library's managers read them; a plain member of the library gets 4030; a non-member who is not a Policy Manager, User Manager or manager of that library gets 4041 `Library not found` from the lookup, before the policy check. The 4030 message for a member names `Library manager(s)` only when the edit flag is on, because `IsAllowed` lists library managers only when it would have let them pass.
- **Library lookup by name (task #20).** The task list still marks #20 as deferred, but commit 61e1fb36 (2026-10-21) gave `DomainOperations.GetLibraryByNameAsync` and `GetLibraryByIdAsync` the same `MayReachAsync` rule: members, anonymous-access libraries, then `ListLibrariesForAdministration` with the library's id. A Policy Manager therefore reaches any library by name, member or not. `GetLibrariesForAdministration` itself was added by commit fdd53cf9 (2026-10-21); the test `GetLibrariesForAdministrationApiTests.APolicyManager_GetsEveryLibraryToo` covers the role.
- **Refusals of the anonymous user differ by code.** With no ticket, `GetGeneralAppSettings` and `GetAuthenticationAndPasswordPolicy` answer 4010 (explicit `IsAuthenticatedUser()` check), while `GetSystemBehaviorSettings`, `GetEmailAndNotificationSettings`, the four `Set*` settings calls and `FlushApplicationCache` answer 4030 (the matrix refuses the anonymous user like any non-member). The test `AppSettingsBatchApiTests.WithoutATicket_EachOneIsRefused_ButNotAllTheSameWay` records this. A UI should treat 4010 and 4030 alike for these.
- **Every settings writer checks twice.** The `SettingServices` method checks `UpdateApplicationSettingsAndPolicies`, and the `InfoRouterExtensions` method it calls (or `InfoRouter.SaveSystemDefaultColumnSettings` for the columns) checks it again. Same action, same answer; the second check is for callers inside IRNET.
- **`getApplicationParameters` and the settings readers overlap.** The extended block shows `LOGLOGINS` and the `PWD*` values to administrators only, yet a Policy Manager reads the same values through `GetSystemBehaviorSettings`, and any signed-in user through `GetAuthenticationAndPasswordPolicy`. Nothing is hidden by it that a dedicated reader does not give, except the SMTP server details, server name, IP addresses and warehouse paths, which no settings call exposes. Defensible: the block is infrastructure, not policy.
- **`ListLibrariesForAdministration` is shared with User Managers** and is what `MayReachAsync` and `GetLibrariesForAdministration` use. It no longer widens `getTasks`: `WorkflowOperations.GetTasksAsync` reads the administrator flag and `DomainsStore.GetLibraryListForAdministrationAsync` (managed libraries) directly, so User and Policy Managers see only their own tasks.
- The XML comment on `SystemBehaviorSettings.AllowLibraryManagersToEditPolicy` (`IRBase\Models\SystemBehaviorSettings.cs`) says "password policy"; the code uses it for library policies (`IRSecurity.IsAllowed`, `UpdateLibraryPolices`). The comment is wrong, the behaviour is as described here.

## Related

- [AdministrativeRoles](AdministrativeRoles.md), all roles at a glance
- the other role pages: [Administrators](AdministratorsRole.md), [User Managers](UserManagersRole.md),
  [Audit Managers](AuditManagersRole.md), [R&D Managers](RDManagersRole.md),
  [Search & Category Administrators](SearchAdministratorsRole.md), [Library Managers](LibraryManagersRole.md)
