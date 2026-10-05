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
| `100` | `[User Managers]` | UserManager | Users, user groups, library membership and managers, user transfers. |
| `101` | `[Audit Managers]` | AuditManager | Audit logs, licence, server and warehouse status. |
| `102` | `[Policy Managers]` | PolicyManager | Application settings and library policies. |
| `103` | `[R&D Managers]` | RDManager | Retention and disposition schedules, disposition, freezing. |
| `105` | `[Search & Category Administrators]` | SearchAdministrators | System-wide saved searches and search pages. |

- These are system groups: they belong to no library, and their ids are fixed.
- **Only Administrators can add or remove members of these groups.** A user manager cannot make someone a user
  manager.
- The `sysadmin` account is always a member of `[Administrators]` and cannot be removed from it.
- Holding several roles combines what they allow.

## How the server decides

For an administrative action the server allows the call when **any** of these is true, in this order:

1. The caller is in `[Administrators]`.
2. The action allows **self-service** and the caller is acting on their own account (marked *self* below).
3. The caller is in one of the role groups the action requires.
4. The action allows **library managers** and the caller manages the library the action is about (marked
   *lib managers* below). For a global user or group, there is no library and this does not apply.

A refusal is `errorCode="4030"`, and the message names the roles that would have been allowed.

> **Search & Category Administrators is the exception.** That role is checked on its own, and membership of
> `[Administrators]` does **not** grant it. To manage system-wide saved searches, an administrator must also be
> a member of `[Search & Category Administrators]`.

## Finding out which roles the signed-in user has

There is no single "my roles" call. Use these:

- [GetGroupMembershipsOfUser](GetGroupMembershipsOfUser.md) with the user's own name (always allowed for
  yourself): the `GroupID` values `100`–`105` in the answer are the roles held.
- `getApplicationParameters` answers whether the caller is an administrator.
- Whether the caller manages a library: [GetManagedDomainsByUser](GetManagedDomainsByUser.md) with the caller's
  own name, or an empty name.

---

## Administrators (104)

Administrators pass **every** check on this page, plus the following, which are **only** for administrators:

| Area | Web service calls |
|---|---|
| Libraries | [CreateDomain](CreateDomain.md), [DeleteDomain](DeleteDomain.md), [UpdateDomain](UpdateDomain.md), [ArchiveDomain](ArchiveDomain.md), [UnarchiveDomain](UnarchiveDomain.md) |
| Property sets | [CreatePropertySetDefinition](CreatePropertySetDefinition.md) / [1](CreatePropertySetDefinition1.md), [UpdatePropertySetDefinition](UpdatePropertySetDefinition.md) / 1, [DeletePropertySetDefinition](DeletePropertySetDefinition.md), [AddPropertySetField](AddPropertySetField.md), [DeletePropertySetField](DeletePropertySetField.md), [AddPropertySetFieldOption](AddPropertySetFieldOption.md), [DeletePropertySetFieldOption](DeletePropertySetFieldOption.md), SetPropertySetLookupFieldParametersFor… (SQL Server, Oracle, MySQL) |
| Document types | [CreateDocumentTypeDef](CreateDocumentTypeDef.md) / [1](CreateDocumentTypeDef1.md), UpdateDocumentTypeDef / 1, [DeleteDocumentTypeDef](DeleteDocumentTypeDef.md) |
| Recycle bin | [SearchRecycledItems](SearchRecycledItems.md), [PurgeRecycleBinItem](PurgeRecycleBinItem.md), [RestoreRecycleBinItem](RestoreRecycleBinItem.md) for items in **another user's** recycle bin (anyone may restore their own) |
| Settings and logs | [GetEmailAndNotificationSettings](GetEmailAndNotificationSettings.md), [UpdateApplicationLicense](UpdateApplicationLicense.md), [GetLogStatistics](GetLogStatistics.md) / [1](GetLogStatistics1.md), [GetLogs](GetLogs.md) |
| Users | [SendWelcomeEmailForUser](SendWelcomeEmailForUser.md); [GetManagedDomainsByUser](GetManagedDomainsByUser.md) for **another** user |
| Role groups | Adding and removing members of the six groups on this page ([AddUsergroupMember](AddUsergroupMember.md), [RemoveUsergroupMember](RemoveUsergroupMember.md)) |

Administrators also:

- see the database connection details of database lookup fields in [GetPropertySetDefinition](GetPropertySetDefinition.md)
  (others get the definition without them);
- see every property set in [GetPropertySetDefinitions](GetPropertySetDefinitions.md) (others see public sets and
  the sets of their libraries);
- can open any library, and pass every library-manager and workflow-management check;
- are not limited by the maximum document size setting when uploading.

---

## User Managers (100)

| Action | Web service calls | Also allowed for |
|---|---|---|
| Create a user | [CreateUser](CreateUser.md) | lib managers, for users of their library |
| List users | [GetAllUsers](GetAllUsers.md), [GetAllUsers1](GetAllUsers1.md), [GetAllUsers2](GetAllUsers2.md), [GetAllUsersWithoutDetails](GetAllUsersWithoutDetails.md) | lib managers, when listing their own library |
| Look up another user | [GetUser](GetUser.md), [GetUserStatistics](GetUserStatistics.md), [GetDomainMembershipsOfUser](GetDomainMembershipsOfUser.md), and every call that names a user other than the caller (see note) | lib managers; co-workers of that user |
| Change a user's profile, status or type | [UpdateUserProfile](UpdateUserProfile.md), [ChangeUserStatus](ChangeUserStatus.md), [ChangeUserType](ChangeUserType.md) | lib managers. **Not** self. |
| Change a user's preferences, contact details, e-mail | [UpdateUserPreferences](UpdateUserPreferences.md), [UpdateUserContactInfo](UpdateUserContactInfo.md), [UpdateUserEmail](UpdateUserEmail.md) | self, lib managers |
| Set a user's password | [ChangeUserPassword](ChangeUserPassword.md) | self, lib managers |
| Delete a user | [DeleteUser](DeleteUser.md), [DeleteUser1](DeleteUser1.md) | lib managers |
| See a user's activity lists | GetUserViewLog / 1 / Lite, [GetAuthoredDocuments](GetAuthoredDocuments.md), [GetCheckedoutDocumentsByUser](GetCheckedoutDocumentsByUser.md), [GetDocumentsOwnedByUser](GetDocumentsOwnedByUser.md), [GetFavoriteDocumentsOfUser](GetFavoriteDocumentsOfUser.md), [GetISOReviewAssignmentsOfUser](GetISOReviewAssignmentsOfUser.md), [GetSubscribedDocumentsByUser](GetSubscribedDocumentsByUser.md), [GetFavoriteFoldersOfUser](GetFavoriteFoldersOfUser.md), [GetFoldersOwnedByUser](GetFoldersOwnedByUser.md), [GetSubscribedFoldersByUser](GetSubscribedFoldersByUser.md) | self, lib managers |
| See a user's group memberships | [GetGroupMembershipsOfUser](GetGroupMembershipsOfUser.md) | self, lib managers |
| See a user's workflow roles | [GetUsersWorkflowRoles](GetUsersWorkflowRoles.md) | self, lib managers |
| Manage task redirections | [SetUserTaskRedirection](SetUserTaskRedirection.md), [RemoveUserTaskRedirection](RemoveUserTaskRedirection.md), [RerouteUserTaskRedirection](RerouteUserTaskRedirection.md), [GetUserTaskRedirectionsFrom](GetUserTaskRedirectionsFrom.md) | self, lib managers; for rerouting, also the user the redirection points to |
| Transfer one user's work to another | all 13 Transfer… calls: [TransferUserTasks](TransferUserTasks.md), [TransferUserDocumentOwnerships](TransferUserDocumentOwnerships.md), [TransferUserFolderOwnerships](TransferUserFolderOwnerships.md), [TransferUserGroupMemberships](TransferUserGroupMemberships.md), [TransferUserDomainMemberships](TransferUserDomainMemberships.md), [TransferUserDomainManagerRoles](TransferUserDomainManagerRoles.md), [TransferUserSecurityPermissions](TransferUserSecurityPermissions.md), and the rest | lib managers of **both** users' libraries |
| Property set rows on a user | [AddPropertySetRowForUser](AddPropertySetRowForUser.md), UpdatePropertySetRowForUser, [DeletePropertySetRowForUser](DeletePropertySetRowForUser.md) | lib managers |
| Create a user group | [CreateUserGroup](CreateUserGroup.md), [CreateUserGroup1](CreateUserGroup1.md) | lib managers, for local groups of their library |
| Rename a user group | UpdateUserGroupName / 1 | lib managers, for groups of their library |
| Delete a user group | [DeleteUsergroup](DeleteUsergroup.md) | lib managers, for groups of their library |
| Add or remove group members | [AddUsergroupMember](AddUsergroupMember.md), [RemoveUsergroupMember](RemoveUsergroupMember.md) | lib managers. **Not** for the role groups on this page: those are administrators only. |
| See members of a group that hides them | [GetUserGroupMembers](GetUserGroupMembers.md), [GetUserGroupMembers1](GetUserGroupMembers1.md) | lib managers. Groups that show their members can be read by anyone. |
| Add or remove library members | [AddUserAsDomainMember](AddUserAsDomainMember.md), [AddUserGroupAsDomainMember](AddUserGroupAsDomainMember.md), [RemoveUserFromDomainMembership](RemoveUserFromDomainMembership.md), [RemoveUserGroupFromDomainMembership](RemoveUserGroupFromDomainMembership.md) | lib managers of that library |
| Add or remove library managers | [AddManagerToDomain](AddManagerToDomain.md), [RemoveManagerFromDomain](RemoveManagerFromDomain.md) | nobody else - **not** library managers |
| Flush the application cache | [FlushApplicationCache](FlushApplicationCache.md) | nobody else |
| See tasks across libraries | [getTasks](getTasks.md), [GetTasks1](GetTasks1.md) | never refused: without the role, the list covers the caller's own tasks and the libraries they manage (also widened by Policy Managers) |

**Looking up another user.** Any call that names a user other than the caller checks this role first:
the user lists above, the Transfer… calls, the property-set-row-for-user calls, and [Search](Search.md) or
GetFoldersAndDocumentsByPage2 when the criteria name a user. A library manager of that user's library, or a
co-worker of that user, passes as well.

---

## Audit Managers (101)

| Action | Web service calls | Also allowed for |
|---|---|---|
| Read audit logs | [GetCheckoutLog](GetCheckoutLog.md), [GetCheckInLog](GetCheckInLog.md), GetVersionCreateLog, GetVersionDeleteLog, [GetNewDocumentsAndFoldersLog](GetNewDocumentsAndFoldersLog.md), [GetDeleteLog](GetDeleteLog.md), [GetDispositionLog](GetDispositionLog.md), [GetOwnershipChangeLog](GetOwnershipChangeLog.md), [GetClassificationLogs](GetClassificationLogs.md), [GetSecurityChangeLog](GetSecurityChangeLog.md) | lib managers of the library the log is about (not for a library's root security log) |
| Read SOX, ISO and access-list history | [GetSoxLogs](GetSoxLogs.md), [GetISOLogs](GetISOLogs.md), [GetAccessListHistory](GetAccessListHistory.md) | anyone with the right on the document or folder; the role is the fallback for callers without it; lib managers |
| See the licence | [GetLicenseInfo](GetLicenseInfo.md) | nobody else |
| See server status | [GetSystemStatistics](GetSystemStatistics.md), [GetMaintenanceJobsStatus](GetMaintenanceJobsStatus.md) | nobody else |
| See warehouse status | [GetWarehouseStatus](GetWarehouseStatus.md) | nobody else |

---

## Policy Managers (102)

| Action | Web service calls | Also allowed for |
|---|---|---|
| Change application settings | [SetGeneralAppSettings](SetGeneralAppSettings.md), [SetAuthenticationAndPasswordPolicy](SetAuthenticationAndPasswordPolicy.md), [SetSystemBehaviorSettings](SetSystemBehaviorSettings.md), [SetEmailAndNotificationSettings](SetEmailAndNotificationSettings.md), [SetDefaultFolderColumns](SetDefaultFolderColumns.md) | nobody else |
| Read system behaviour settings | [GetSystemBehaviorSettings](GetSystemBehaviorSettings.md) | nobody else. The other Get…Settings calls need no role, except GetEmailAndNotificationSettings (administrators only). |
| Read and change library policies | [GetDomainPolicies](GetDomainPolicies.md), [SetDomainPolicies](SetDomainPolicies.md) | managers of that library, **only** when the system behaviour setting *Allow library managers to edit policies* is on |
| See tasks across libraries | [getTasks](getTasks.md), [GetTasks1](GetTasks1.md) | as for User Managers |

---

## R&D Managers (103)

Retention and disposition. Library managers are **never** allowed these.

| Action | Web service calls | Notes |
|---|---|---|
| Create a schedule | [CreateRandDSchedule](CreateRandDSchedule.md) | |
| Change or delete a schedule | [UpdateRandDSchedule](UpdateRandDSchedule.md), [DeleteRandDSchedule](DeleteRandDSchedule.md), [DeleteRandDSchedule1](DeleteRandDSchedule1.md) | |
| Manage retention source authorities | [CreateRetentionSourceAuthority](CreateRetentionSourceAuthority.md), [UpdateRetentionSourceAuthority](UpdateRetentionSourceAuthority.md), [DeleteRetentionSourceAuthority](DeleteRetentionSourceAuthority.md) | |
| Dispose of documents | [DisposeItem](DisposeItem.md) | For items that have a disposition date. A folder is checked document by document. |
| Freeze or unfreeze | [SetRdFreezeFlag](SetRdFreezeFlag.md) | Documents and folders. |
| Give a document a schedule other than its folder's | [SetDocumentRandDSchedule](SetDocumentRandDSchedule.md), [RemoveDocumentRandDSchedule](RemoveDocumentRandDSchedule.md), UpdateDocumentType | Only when the folder has a schedule and the new one differs from it (or is none). Following the folder's schedule needs no role. |

R&D Managers also **receive the disposition tasks** the daily disposition job creates: each goes to one active
member of `[R&D Managers]`, or to `sysadmin` when the group has none.

---

## Search & Category Administrators (105)

System-wide saved searches and search pages are the ones with no owner. Personal ones belong to their
owner and need no role.

| Action | Web service calls |
|---|---|
| Create a system-wide saved search or search page | [CreateSavedSearch](CreateSavedSearch.md) without `isPersonal` |
| Change one | [UpdateSavedSearch](UpdateSavedSearch.md) |
| Delete one, or anyone's personal one | [DeleteSavedSearch](DeleteSavedSearch.md) |
| See every saved search, whatever groups it is shared with | [GetSavedSearches](GetSavedSearches.md), [GetSavedSearch](GetSavedSearch.md) |

As noted above, `[Administrators]` membership does not include this role.

---

## Notes for the Control Panel

- **Show or hide by role, then let the server decide.** A library manager's rights depend on the library: the
  same call can succeed for one library and return `4030` for another. Read `errorCode` rather than assuming.
- **Library managers** are not one of these groups: a user is a library manager of a particular library
  ([AddManagerToDomain](AddManagerToDomain.md)). Only Administrators and User Managers can make someone one.
- **Self-service** calls (marked *self*) work for every signed-in user on their own account, with no role.
- [UpdateRandDSchedule](UpdateRandDSchedule.md) is checked internally as "delete a schedule". Both are R&D Managers
  only, so the outcome is the same.
