# Administrative Roles

infoRouter has six built-in **administrative role groups**. A user gets a role by being a member of its
group. This page lists what each role allows, and which web service calls it unlocks, so the Control Panel
can show the actions a user may take and hide the rest.

The roles are the values of `enum_IR.AdmistrativeRoles` (`IRBase\IRBaseEnum.cs`). The server checks them;
this page describes those checks as the server makes them.

## The role groups

| Group id | Group name | Role | In short |
|---:|---|---|---|
| `104` | `[Administrators]` | Administrators | Everything. Passes every role check below. |
| `100` | `[User Managers]` | UserManager | Users, user groups, library membership and managers, user transfers. Sees every library. |
| `101` | `[Audit Managers]` | AuditManager | Audit logs, licence, server and warehouse status. |
| `102` | `[Policy Managers]` | PolicyManager | Application settings and library policies. Sees every library. |
| `103` | `[R&D Managers]` | RDManager | Retention and disposition schedules, disposition, freezing. |
| `105` | `[Search & Category Administrators]` | SearchAdministrators | System-wide saved searches and search pages. |

- These are system groups: they belong to no library, and their ids are fixed.
- **Only Administrators can add or remove members of these groups.** A user manager cannot make someone a user
  manager.
- The `sysadmin` account always counts as an administrator, and cannot be removed from `[Administrators]`.
- Holding several roles combines what they allow.
- The members of these groups are hidden: only Administrators and User Managers can list them.

## How the server decides

For an administrative action the server allows the call when **any** of these is true, in this order:

1. The caller is in `[Administrators]`.
2. The action allows **self-service** and the caller is acting on their own account (marked *self* below).
3. The caller is in one of the role groups the action requires.
4. The action allows **library managers** and the caller manages the library the action is about (marked
   *lib managers* below). A user or group belongs to a library only when it is local to that library: for a
   global user or group, and for application-wide actions, there is no library and this step never passes.

A refusal is `errorCode="4030"`, and the message names the roles that would have been allowed.

## Finding out which roles the signed-in user has

There is no single "my roles" call. Use these:

- [GetGroupMembershipsOfUser](GetGroupMembershipsOfUser.md) with the user's own name (always allowed for
  yourself): the `GroupID` values `100`–`105` in the answer are the roles held.
- [getApplicationParameters](getApplicationParameters.md) tells you whether the caller is an administrator:
  only administrators get the extended block (SMTP, password policy, authentication authorities, warehouse
  paths).
- Whether the caller manages a library: [GetManagedDomainsByUser](GetManagedDomainsByUser.md) with the caller's
  own name, or an empty name.
- Which libraries the caller may administer at all: [GetLibrariesForAdministration](GetLibrariesForAdministration.md),
  which answers every library for Administrators, User Managers and Policy Managers, the managed ones for a library
  manager, and nothing for anyone else. New in 9.0.

---

## Administrators (104)

Administrators pass **every** check on this page, plus the following,
which are **only** for administrators:

| Area | Web service calls |
|---|---|
| Libraries | [CreateDomain](CreateDomain.md), [DeleteDomain](DeleteDomain.md), [UpdateDomain](UpdateDomain.md), [ArchiveDomain](ArchiveDomain.md), [UnarchiveDomain](UnarchiveDomain.md) |
| Property sets | [CreatePropertySetDefinition](CreatePropertySetDefinition.md) / [1](CreatePropertySetDefinition1.md), [UpdatePropertySetDefinition](UpdatePropertySetDefinition.md) / 1, [DeletePropertySetDefinition](DeletePropertySetDefinition.md), [AddPropertySetField](AddPropertySetField.md), [DeletePropertySetField](DeletePropertySetField.md), [AddPropertySetFieldOption](AddPropertySetFieldOption.md), [DeletePropertySetFieldOption](DeletePropertySetFieldOption.md), SetPropertySetLookupFieldParametersFor… (SQL Server, Oracle, MySQL) |
| Document types | [CreateDocumentTypeDef](CreateDocumentTypeDef.md) / [1](CreateDocumentTypeDef1.md), UpdateDocumentTypeDef / 1, [DeleteDocumentTypeDef](DeleteDocumentTypeDef.md) |
| Recycle bin | [SearchRecycledItems](SearchRecycledItems.md) / [1](SearchRecycledItems1.md), [PurgeRecycleBinItem](PurgeRecycleBinItem.md); [RestoreRecycleBinItem](RestoreRecycleBinItem.md) for items in **another user's** recycle bin (anyone may restore from their own) |
| Settings | [FlushApplicationCache](FlushApplicationCache.md), [UpdateApplicationLicense](UpdateApplicationLicense.md) |
| Users | [GetManagedDomainsByUser](GetManagedDomainsByUser.md) for **another** user |
| Role groups | Adding and removing members of the six groups on this page ([AddUsergroupMember](AddUsergroupMember.md), [RemoveUsergroupMember](RemoveUsergroupMember.md)) |

Administrators also:

- see the database connection details of database lookup fields in [GetPropertySetDefinition](GetPropertySetDefinition.md)
  (others get the definition without them);
- see every property set in [GetPropertySetDefinitions](GetPropertySetDefinitions.md) (others see public sets and
  the sets of their libraries);
- may use [GetMembersWithoutAccess](GetMembersWithoutAccess.md) on any library (others only on the libraries they
  manage);
- pass every library-manager and workflow-management check, and see every workflow task in
  [getTasks](getTasks.md) / [GetTasks1](GetTasks1.md) (library managers see those of their libraries; User and Policy
  Managers only their own);
- are not limited by the maximum document size setting when uploading, WebDAV included.

---

## User Managers (100)

Library managers pass these checks only for users and groups **local to their library**, never for global ones.

**An administrator's account** - the `sysadmin` account or any member of `[Administrators]` - is changed by
administrators only. User Managers and library managers can read it, but cannot change its profile, status,
type, password, e-mail, preferences, task redirections or property set rows, delete it, or transfer its work to
someone else (`4030`, "Only administrators can change an administrator's account"). Up to 8.7 only the `sysadmin`
account was protected, so a User Manager could reset another administrator's password and sign in as them.

| Action | Web service calls | Also allowed for |
|---|---|---|
| Create a user, send them the welcome e-mail | [CreateUser](CreateUser.md), [SendWelcomeEmailForUser](SendWelcomeEmailForUser.md) | lib managers, for users of their library |
| List users | [GetAllUsers](GetAllUsers.md), [GetAllUsers1](GetAllUsers1.md), [GetAllUsers2](GetAllUsers2.md), [GetAllUsers3](GetAllUsers3.md), [GetAllUsersWithoutDetails](GetAllUsersWithoutDetails.md) | lib managers, when the library filter names their own library. GetAllUsers (no filter) is User Managers only. |
| Look up another user | [GetUser](GetUser.md), [GetUserStatistics](GetUserStatistics.md), [GetDomainMembershipsOfUser](GetDomainMembershipsOfUser.md), [GetManagedDomainsByUser](GetManagedDomainsByUser.md), [GetUserTaskRedirectionTo](GetUserTaskRedirectionTo.md), and every call that names a user other than the caller (see note) | self; lib managers; **co-workers** of that user (members of a library the caller is also a member of) |
| Change a user's profile, status or type | [UpdateUserProfile](UpdateUserProfile.md), [ChangeUserStatus](ChangeUserStatus.md), [ChangeUserType](ChangeUserType.md) | lib managers. **Not** self. |
| Change a user's preferences, contact details, e-mail | [UpdateUserPreferences](UpdateUserPreferences.md), [UpdateUserContactInfo](UpdateUserContactInfo.md), [UpdateUserEmail](UpdateUserEmail.md) | self, lib managers |
| Set a user's password | [ChangeUserPassword](ChangeUserPassword.md), [ChangeUserPassword1](ChangeUserPassword1.md) | lib managers; self through ChangeUserPassword1 only, with the current password |
| Delete a user | [DeleteUser](DeleteUser.md), [DeleteUser1](DeleteUser1.md) | lib managers |
| See a user's activity lists | GetUserViewLog / 1 / Lite, [GetAuthoredDocuments](GetAuthoredDocuments.md), [GetCheckedoutDocumentsByUser](GetCheckedoutDocumentsByUser.md), [GetDocumentsOwnedByUser](GetDocumentsOwnedByUser.md), [GetFavoriteDocumentsOfUser](GetFavoriteDocumentsOfUser.md), [GetISOReviewAssignmentsOfUser](GetISOReviewAssignmentsOfUser.md), [GetSubscribedDocumentsByUser](GetSubscribedDocumentsByUser.md), [GetFavoriteFoldersOfUser](GetFavoriteFoldersOfUser.md), [GetFoldersOwnedByUser](GetFoldersOwnedByUser.md), [GetSubscribedFoldersByUser](GetSubscribedFoldersByUser.md) | self, lib managers |
| See a user's group memberships | [GetGroupMembershipsOfUser](GetGroupMembershipsOfUser.md) | self, lib managers |
| See a user's workflow roles | [GetUsersWorkflowRoles](GetUsersWorkflowRoles.md) | self, lib managers |
| Manage task redirections | [SetUserTaskRedirection](SetUserTaskRedirection.md), [RemoveUserTaskRedirection](RemoveUserTaskRedirection.md), [RerouteUserTaskRedirection](RerouteUserTaskRedirection.md), [GetUserTaskRedirectionsFrom](GetUserTaskRedirectionsFrom.md) | self, lib managers; for rerouting, also the user the redirection points to. Rerouting also needs the `RerouteRedirections` setting on. |
| Transfer one user's work to another | all 13 Transfer… calls: [TransferUserTasks](TransferUserTasks.md), [TransferUserDocumentOwnerships](TransferUserDocumentOwnerships.md), [TransferUserFolderOwnerships](TransferUserFolderOwnerships.md), [TransferUserGroupMemberships](TransferUserGroupMemberships.md), [TransferUserDomainMemberships](TransferUserDomainMemberships.md), [TransferUserDomainManagerRoles](TransferUserDomainManagerRoles.md), [TransferUserSecurityPermissions](TransferUserSecurityPermissions.md), and the rest | lib managers, when **both** users are local to libraries they manage. TransferUserGroupMemberships moves the role groups only for administrators; for anyone else they stay behind, with a `warnings` attribute. |
| Property set rows on a user | [AddPropertySetRowForUser](AddPropertySetRowForUser.md), UpdatePropertySetRowForUser, [DeletePropertySetRowForUser](DeletePropertySetRowForUser.md) | lib managers. **Not** self. |
| Create a user group | [CreateUserGroup](CreateUserGroup.md), [CreateUserGroup1](CreateUserGroup1.md) | lib managers, for local groups of their library |
| Rename a user group | UpdateUserGroupName / 1 | lib managers, for groups of their library. Not the role groups. |
| Delete a user group | [DeleteUsergroup](DeleteUsergroup.md) | lib managers, for groups of their library. Not the role groups. |
| Add or remove group members | [AddUsergroupMember](AddUsergroupMember.md), [RemoveUsergroupMember](RemoveUsergroupMember.md) | lib managers. **Not** for the role groups on this page: those are administrators only. |
| See members of a group that hides them | [GetUserGroupMembers](GetUserGroupMembers.md), [GetUserGroupMembers1](GetUserGroupMembers1.md) | lib managers, for local groups. Groups that show their members can be read by anyone. |
| Add or remove library members | [AddUserAsDomainMember](AddUserAsDomainMember.md), [AddUserGroupAsDomainMember](AddUserGroupAsDomainMember.md), [RemoveUserFromDomainMembership](RemoveUserFromDomainMembership.md), [RemoveUserGroupFromDomainMembership](RemoveUserGroupFromDomainMembership.md) | lib managers of that library |
| Add or remove library managers | [AddManagerToDomain](AddManagerToDomain.md), [RemoveManagerFromDomain](RemoveManagerFromDomain.md) | nobody else - **not** library managers. A User Manager cannot appoint themselves. |
| List every library, membership aside | [GetLibrariesForAdministration](GetLibrariesForAdministration.md) | Policy Managers; lib managers get the libraries they manage. [GetDomains](GetDomains.md) answers everyone, but only with the libraries they belong to. New in 9.0. |

**Looking up another user.** Any call that names a user other than the caller first checks that the caller may
see that user: self, administrators, User Managers, the managers of that user's library, and co-workers pass.
This covers the user calls above, the Transfer… calls, the property-set-row-for-user calls, and [Search](Search.md)
or GetFoldersAndDocumentsByPage2 when the criteria name a user. Search criteria that read a user's own lists (`SUBSCRIPTIONSOF`,
`FAVORITESOF`, `DOWNLOADQUEOF`, `VIEWCRITERIA` with `USERNAME`) then need the *activity lists* right above. Most of these calls then make their own check
from the table; GetUser, GetUserStatistics, GetDomainMembershipsOfUser, GetManagedDomainsByUser and GetUserTaskRedirectionTo make no further check, so a co-worker
can read them. GetManagedDomainsByUser was administrators only up to 9.0.

---

## Audit Managers (101)

| Action | Web service calls | Also allowed for |
|---|---|---|
| Read audit logs | [GetCheckoutLog](GetCheckoutLog.md), [GetCheckInLog](GetCheckInLog.md), GetVersionCreateLog, GetVersionDeleteLog, [GetNewDocumentsAndFoldersLog](GetNewDocumentsAndFoldersLog.md), [GetDeleteLog](GetDeleteLog.md), [GetDispositionLog](GetDispositionLog.md), [GetOwnershipChangeLog](GetOwnershipChangeLog.md) | lib managers, when the path filter or object is in their library. With no path filter, only Audit Managers. |
| Read the security change log | [GetSecurityChangeLog](GetSecurityChangeLog.md) | anyone with the right to read the access list of the document or folder; lib managers, the library's root folder included |
| Read SOX, ISO, classification and access-list history | [GetSoxLogs](GetSoxLogs.md), [GetISOLogs](GetISOLogs.md), [GetClassificationLogs](GetClassificationLogs.md), [GetAccessListHistory](GetAccessListHistory.md) | anyone with the right to read that log on the document; the role is the fallback for callers without it; lib managers |
| See the licence | [GetLicenseInfo](GetLicenseInfo.md) | nobody else |
| See server status | [GetSystemStatistics](GetSystemStatistics.md), [GetMaintenanceJobsStatus](GetMaintenanceJobsStatus.md) | nobody else |
| See warehouse status | [GetWarehouseStatus](GetWarehouseStatus.md) | nobody else |
| Read the server logs | [GetLogStatistics](GetLogStatistics.md) / [1](GetLogStatistics1.md), [GetLogs](GetLogs.md) | nobody else |

---

## Policy Managers (102)

| Action | Web service calls | Also allowed for |
|---|---|---|
| Change application settings | [SetGeneralAppSettings](SetGeneralAppSettings.md), [SetAuthenticationAndPasswordPolicy](SetAuthenticationAndPasswordPolicy.md), [SetSystemBehaviorSettings](SetSystemBehaviorSettings.md), [SetEmailAndNotificationSettings](SetEmailAndNotificationSettings.md), [SetDefaultFolderColumns](SetDefaultFolderColumns.md) | nobody else |
| Read system behaviour and e-mail settings | [GetSystemBehaviorSettings](GetSystemBehaviorSettings.md), [GetEmailAndNotificationSettings](GetEmailAndNotificationSettings.md) | nobody else |
| Read and change library policies | [GetDomainPolicies](GetDomainPolicies.md), [SetDomainPolicies](SetDomainPolicies.md) | managers of that library: reading always, changing **only** when the system behaviour setting *Allow library managers to edit policies* is on |
| List every library, membership aside | [GetLibrariesForAdministration](GetLibrariesForAdministration.md) | User Managers; lib managers get the libraries they manage. New in 9.0. |

The other settings calls need no role: [GetGeneralAppSettings](GetGeneralAppSettings.md) and
[GetAuthenticationAndPasswordPolicy](GetAuthenticationAndPasswordPolicy.md) answer any signed-in user, and
[GetDefaultFolderColumns](GetDefaultFolderColumns.md) answers anyone.

---

## R&D Managers (103)

Retention and disposition. The role is not limited to a library: an R&D Manager acts on every library.

**Defining** schedules is for R&D Managers only:

| Action | Web service calls | Notes |
|---|---|---|
| Create a schedule | [CreateRandDSchedule](CreateRandDSchedule.md) | |
| Change or delete a schedule | [UpdateRandDSchedule](UpdateRandDSchedule.md), [DeleteRandDSchedule](DeleteRandDSchedule.md), [DeleteRandDSchedule1](DeleteRandDSchedule1.md) | |
| Manage retention source authorities | [CreateRetentionSourceAuthority](CreateRetentionSourceAuthority.md), [UpdateRetentionSourceAuthority](UpdateRetentionSourceAuthority.md), [DeleteRetentionSourceAuthority](DeleteRetentionSourceAuthority.md) | |
| Dispose of documents | [DisposeItem](DisposeItem.md) | For items that have a disposition date. Also needs the right to delete the item. A folder is checked document by document. |

**Applying** schedules to items takes the *change retention period* right on the item **or** the R&D Manager
role: either one is enough, so library managers and other users with the right may do these too.

| Action | Web service calls |
|---|---|
| Freeze or unfreeze | [SetRdFreezeFlag](SetRdFreezeFlag.md) (documents and folders) |
| Set or remove a document's schedule | [SetDocumentRandDSchedule](SetDocumentRandDSchedule.md), [RemoveDocumentRandDSchedule](RemoveDocumentRandDSchedule.md), UpdateDocumentType |
| Set or remove a folder's schedule | [SetFolderRandDSchedule](SetFolderRandDSchedule.md), [RemoveFolderRandDSchedule](RemoveFolderRandDSchedule.md). Removing one also lifts the freezes it covers. |

Up to 8.7 a freeze, and a document schedule other than its folder's, needed the right **and** the role, while a
folder's schedule needed the right alone.

R&D Managers also **receive the disposition tasks** the daily disposition job creates: each goes to one active
member of `[R&D Managers]`, or to the `sysadmin` account when the group has none.

---

## Search & Category Administrators (105)

System-wide saved searches and search pages are the ones with no owner. Personal ones belong to their
owner and need no role.

| Action | Web service calls |
|---|---|
| Create a system-wide saved search or search page | [CreateSavedSearch](CreateSavedSearch.md) without `isPersonal` |
| Change a system-wide one | [UpdateSavedSearch](UpdateSavedSearch.md). A personal one can be changed only by its owner, even by a search administrator. |
| Delete a system-wide one | [DeleteSavedSearch](DeleteSavedSearch.md). A personal one can be deleted only by its owner. |
| See every system-wide saved search, whatever groups it is shared with | [GetSavedSearches](GetSavedSearches.md), [GetSavedSearch](GetSavedSearch.md) |

Administrators hold this role too, without being members of the group. Up to 8.7 they had to be added to it.

---

## Notes for the Control Panel

- **Show or hide by role, then let the server decide.** A library manager's rights depend on the library: the
  same call can succeed for one library and return `4030` for another. Read `errorCode` rather than assuming.
- **Library managers** are not one of these groups: a user is a library manager of a particular library
  ([AddManagerToDomain](AddManagerToDomain.md)). Only Administrators and User Managers can make someone one.
- **Self-service** calls (marked *self*) work for every signed-in user on their own account, with no role.
- **Which libraries to offer.** [GetDomains](GetDomains.md) lists only the libraries the caller belongs to, whatever
  their role. A page that manages users, memberships, managers or policies should list
  [GetLibrariesForAdministration](GetLibrariesForAdministration.md) instead: every library for Administrators, User
  Managers and Policy Managers, the managed ones for a library manager, nothing for anyone else.
- [UpdateRandDSchedule](UpdateRandDSchedule.md) is checked internally as "delete a schedule". Both are R&D Managers
  only, so the outcome is the same.
