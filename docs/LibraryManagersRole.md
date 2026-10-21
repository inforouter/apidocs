# Library Managers

A library manager is not a role group: there is no group id and no `enum_IR.AdmistrativeRoles` value. A user
is a manager of one particular library, recorded as a row in `DOMAINMANAGERS`, and may manage several. A
manager is appointed with [AddManagerToDomain](AddManagerToDomain.md) and removed with
[RemoveManagerFromDomain](RemoveManagerFromDomain.md); both need `IrAdminAction.AddRemoveLibraryManagers`,
which administrators and User Managers hold and library managers do not (`IRSecurity.cs`, IsAllowed). The
user appointed must already be a member of the library (`DomainExtensions.cs`, SetDomainManagerAsync), and
a non-administrator cannot appoint themselves (4030, "Access denied. Only administrators can make themselves
a library manager."). The user who creates a library becomes its member and its first manager
(`DomainOperations.cs`, CreateAsync). Losing the membership loses the role: removing a user or a group from
the library's members, or removing a user from a member group, deletes the manager rows of whoever is no
longer a member (`DomainsStore.DeleteLibraryManagersWhoAreNotLibraryMemberAsync`).

## How the role is checked

Three different checks decide, and they do not agree with each other on what else counts.

1. **The administrative matrix** (`IRSecurity.cs`, IsAllowed). Each `IrAdminAction` sets `allowLibManagers`,
   and the call site passes a `localDomainId`. Order: administrators pass first; then the "an
   administrator's account is changed by administrators only" guard; then self-service (USER object and
   objectId is the caller); then membership of a required role group; then, only when `allowLibManagers`
   is true **and** `localDomainId > 0`, `SecurityFunctions.CheckDomainManagementAsync`, which is a lookup
   of the (library, caller) row in `DOMAINMANAGERS` (`UserOperations.IsDomainManagerAsync`). A global user
   or group has `DomainId` 0 and every application-wide action passes 0, so this step passes only for
   users and groups **local to a managed library** and for actions on the library itself. Refusal:
   `errorCode="4030"`, message "Access denied. This action is restricted to the following roles: The system
   administrator, Library manager(s), User managers" (the "Library manager(s)" part appears only when the
   step was reachable, so a refusal on a global user does not name library managers at all).
2. **`SecurityFunctions.CheckDomainManagementAsync`** (`ModuleSecurityFunctions.cs`) called on its own, for the
   library operations outside the matrix: administrators pass, then the manager row of the library. Refusal
   4030 "Access denied. Only library managers can perform this operation." (or "Only the system
   administrator can perform this operation" when no library is involved).
3. **The library's policies** (`IRSecurity.cs`, AccessAllowedAsync, and `DomainPolicies`). Each of the 46
   library policies has a "library manager" flag (`RightDomainManager`); 45 default to true, `DocumentCheckIn`
   has no such flag. For a document or folder action with the flag on, a manager of the item's library gets
   the action without any access-list right. This applies only when the manager is a **member** of the
   library (a non-member gets 4030 "Insufficient rights. This action can only be performed by library members
   with appropriate rights.") and is an **Author**-type user; a Reader-type manager gets it only for actions
   whose required right is List or Read.

Administrators pass all three. Note that `ThreadVariables.IsAdministrator()` is the `sysadmin` account
(id 4) or membership of `[Administrators]` (104).

## What the role can do

Administrators may do everything below; the tables name who else may.

### Users and groups local to the managed library

Each row is a matrix action with `allowLibManagers`; `localDomainId` is the `DomainId` of the user or group
acted on, so the row holds only for users and groups whose home library the caller manages. User Managers
hold every row for every user and group. An administrator's account (sysadmin or any member of
`[Administrators]`) cannot be changed by a library manager even when local (4030, "Access denied. Only
administrators can change an administrator's account."); local users cannot join global groups, so this
case does not arise in practice.

| Action | Web service calls | Who else may do it | Conditions |
|---|---|---|---|
| Create a local user in the library, send the welcome mail | [CreateUser](CreateUser.md) with `DomainName` = the managed library, [SendWelcomeEmailForUser](SendWelcomeEmailForUser.md) | User Managers | `CreateUser`; CreateUser passes the new user's library (`InfoRouter.cs`, CreateUser), SendWelcomeEmailForUser the user's `DomainId` |
| List the users of the library | [GetAllUsers1](GetAllUsers1.md), [GetAllUsers2](GetAllUsers2.md), [GetAllUsers3](GetAllUsers3.md), [GetAllUsersWithoutDetails](GetAllUsersWithoutDetails.md) with a library filter naming the managed library (`~L<id>` works too) | User Managers | `ListUsers`; with no library filter `localDomainId` is 0 and the manager is refused (`InfoRouter.cs`, GetAllUsers) |
| Look up a local user | [GetUser](GetUser.md), [GetUserStatistics](GetUserStatistics.md), [GetDomainMembershipsOfUser](GetDomainMembershipsOfUser.md), [GetManagedDomainsByUser](GetManagedDomainsByUser.md), [GetUserTaskRedirectionTo](GetUserTaskRedirectionTo.md), and every call that names a user | self, User Managers, co-workers (members of a library the caller is also a member of) | `ListUsers` with the user's `DomainId` (`UserOperations.cs`, GetUserObjectAsync); these five make no further check |
| Change a local user's profile, status, type | [UpdateUserProfile](UpdateUserProfile.md), [ChangeUserStatus](ChangeUserStatus.md), [ChangeUserType](ChangeUserType.md) | User Managers; not self | `UpdateUserProfile` |
| Change a local user's preferences, contact details, e-mail | [UpdateUserPreferences](UpdateUserPreferences.md), [UpdateUserContactInfo](UpdateUserContactInfo.md), [UpdateUserEmail](UpdateUserEmail.md) | self, User Managers | `UpdateUserPreferences` |
| Set a local user's password | [ChangeUserPassword](ChangeUserPassword.md) | User Managers; self only through [ChangeUserPassword1](ChangeUserPassword1.md) with the current password | `SetUserPassword` |
| Delete a local user | [DeleteUser](DeleteUser.md), [DeleteUser1](DeleteUser1.md) | User Managers | `DeleteUser` (`UserOperations.cs`, DeleteUserAsync) |
| Read a local user's activity lists | [GetUserViewLog](GetUserViewLog.md), [GetUserViewLog1](GetUserViewLog1.md), [GetUserViewLogLite](GetUserViewLogLite.md), [GetAuthoredDocuments](GetAuthoredDocuments.md), [GetCheckedoutDocumentsByUser](GetCheckedoutDocumentsByUser.md), [GetDocumentsOwnedByUser](GetDocumentsOwnedByUser.md), [GetFavoriteDocumentsOfUser](GetFavoriteDocumentsOfUser.md), [GetISOReviewAssignmentsOfUser](GetISOReviewAssignmentsOfUser.md), [GetSubscribedDocumentsByUser](GetSubscribedDocumentsByUser.md), [GetFavoriteFoldersOfUser](GetFavoriteFoldersOfUser.md), [GetFoldersOwnedByUser](GetFoldersOwnedByUser.md), [GetSubscribedFoldersByUser](GetSubscribedFoldersByUser.md), [Search](Search.md) with `SUBSCRIPTIONSOF`, `FAVORITESOF`, `DOWNLOADQUEOF` or `VIEWCRITERIA` + `USERNAME` | self, User Managers | `ListingAuditLogOfUser` (`UserExtensions.cs`; `SearchServices.cs`) |
| Read a local user's group memberships | [GetGroupMembershipsOfUser](GetGroupMembershipsOfUser.md) | self, User Managers | `ListingGroupMembershipOfUser` |
| Read a local user's workflow roles | [GetUsersWorkflowRoles](GetUsersWorkflowRoles.md) | self, User Managers | `ListingUserOwnerships` |
| Manage a local user's task redirections | [SetUserTaskRedirection](SetUserTaskRedirection.md), [RemoveUserTaskRedirection](RemoveUserTaskRedirection.md), [RerouteUserTaskRedirection](RerouteUserTaskRedirection.md), [GetUserTaskRedirectionsFrom](GetUserTaskRedirectionsFrom.md) | self, User Managers; for rerouting also the user the redirection points to | `SetUserTaskRedirections` / `RerouteUserTaskRedirection` (`UserExtensions.cs`) |
| Property set rows on a local user | [AddPropertySetRowForUser](AddPropertySetRowForUser.md), [UpdatePropertySetRowForUser](UpdatePropertySetRowForUser.md), [DeletePropertySetRowForUser](DeletePropertySetRowForUser.md) | User Managers; not self | `ApplyRemoveCustomMetaData` (`PropertySetOperations.cs`) |
| Transfer one local user's work to another local user | all Transfer calls: [TransferUserTasks](TransferUserTasks.md), [TransferUserDocumentOwnerships](TransferUserDocumentOwnerships.md), [TransferUserFolderOwnerships](TransferUserFolderOwnerships.md), [TransferUserGroupMemberships](TransferUserGroupMemberships.md), [TransferUserDomainMemberships](TransferUserDomainMemberships.md), [TransferUserDomainManagerRoles](TransferUserDomainManagerRoles.md), [TransferUserSecurityPermissions](TransferUserSecurityPermissions.md), [TransferUserCheckedOutDocuments](TransferUserCheckedOutDocuments.md), [TransferUserDocumentSubscriptions](TransferUserDocumentSubscriptions.md), [TransferUserFolderSubscriptions](TransferUserFolderSubscriptions.md), [TransferUserWorkflowDefinitions](TransferUserWorkflowDefinitions.md), [TransferUserExpirationNotices](TransferUserExpirationNotices.md), [TransferUserISOTasks](TransferUserISOTasks.md) | User Managers | `TransferUserOwnershipsAndTasks` is checked on **both** users with each one's `DomainId` (`UserTakeOverOperations.cs`, RunAsync); the from-user must not be an administrator; role groups never move for a non-administrator |
| Remove every subscription of a local user | [RemoveAllSubscriptions](RemoveAllSubscriptions.md) | self; **not** User Managers | `CheckDomainManagementAsync` on the user's `DomainId`, outside the matrix (`UserExtensions.cs`, UnSubscribeAllAsync) |
| Create a group in the library | [CreateUserGroup](CreateUserGroup.md), [CreateUserGroup1](CreateUserGroup1.md) with `DomainName` = the managed library | User Managers | `CreateUserGroup` with the library (`IRGeneral.cs`) |
| Rename or delete a local group | [UpdateUserGroupName](UpdateUserGroupName.md), [UpdateUserGroupName1](UpdateUserGroupName1.md), [DeleteUsergroup](DeleteUsergroup.md) | User Managers | `UpdateUserGroupProperties` / `DeleteUserGroup` with the group's `DomainId` (`UsergroupOperations.cs`) |
| Add or remove members of a local group | [AddUsergroupMember](AddUsergroupMember.md), [RemoveUsergroupMember](RemoveUsergroupMember.md) | User Managers | `UpdateGroupMembers` with the group's `DomainId`; the member must be a member of the library |
| See the members of a local group that hides them | [GetUserGroupMembers](GetUserGroupMembers.md), [GetUserGroupMembers1](GetUserGroupMembers1.md) | User Managers; anyone for a group that shows its members | `ListGroups` with the group's `DomainId` (`UsergroupExtensions.cs`, GetMembersForPublic) |

### The library itself

| Action | Web service calls | Who else may do it | Conditions |
|---|---|---|---|
| Add or remove library members | [AddUserAsDomainMember](AddUserAsDomainMember.md), [RemoveUserFromDomainMembership](RemoveUserFromDomainMembership.md), [AddUserGroupAsDomainMember](AddUserGroupAsDomainMember.md), [RemoveUserGroupFromDomainMembership](RemoveUserGroupFromDomainMembership.md) | User Managers | `AddRemoveLibraryMembers` with the library's id (`DomainExtensions.cs`, `DomainOperations.cs`); only global users and global groups can be added; the last member cannot be removed |
| Reach the library by name | every call with a `DomainName`, e.g. [GetDomain](GetDomain.md), [GetManagers](GetManagers.md), [GetDomainMembers](GetDomainMembers.md), [GetDomainMembers1](GetDomainMembers1.md), [GetDomainUsers](GetDomainUsers.md), [GetDomainUsers1](GetDomainUsers1.md), [GetDomainGroups](GetDomainGroups.md), [GetLocalUsers](GetLocalUsers.md), [GetDomainStatistics](GetDomainStatistics.md) | members of the library, anyone where it allows anonymous access, User Managers and Policy Managers for every library | `DomainOperations.GetLibraryByNameAsync` and `GetLibraryByIdAsync` share `MayReachAsync`: membership, or `ListLibrariesForAdministration` with the library's id, which a manager passes. An unreachable library is 4041 "Library not found". These listing calls make no further check: any signed-in user who reaches the library gets them |
| List the libraries to administer | [GetLibrariesForAdministration](GetLibrariesForAdministration.md) | User Managers and Policy Managers, who get every library | A manager gets the libraries they manage (`UserOperations.cs`, GetLibraryListForAdministrationAsync, `localDomainId` 0 so the role step fails and the managed list is read instead); anyone else gets an empty list |
| See which members cannot open the library | [GetMembersWithoutAccess](GetMembersWithoutAccess.md) | nobody else: User and Policy Managers are refused | With no `domainName`, every managed library; with one, it must be managed (4030 "Access denied. Only library managers can perform this operation.") (`LibraryServices.cs`, GetMembersWithoutAccessAsync) |
| Read the library's policies | [GetDomainPolicies](GetDomainPolicies.md) | Policy Managers | `Domain.AccessAllowedToReadPoliciesAsync`: `UpdateLibraryPolices`, or `CheckDomainManagementAsync` (task #19) |
| Change the library's policies | [SetDomainPolicies](SetDomainPolicies.md) | Policy Managers | `UpdateLibraryPolices`; `allowLibManagers` is set only when the system behaviour setting `AllowLibraryManagersToEditPolicy` is on (`IRSecurity.cs`, IsAllowed; stored as `LIBMANAGERS_EDITPOLICY`) |

### Audit logs of the library

`ViewAuditLogs` has `allowLibManagers`; what is passed as `localDomainId` is the library the log is read for.

| Action | Web service calls | Who else may do it | Conditions |
|---|---|---|---|
| Read the library's operation logs | [GetCheckoutLog](GetCheckoutLog.md), [GetCheckInLog](GetCheckInLog.md), [GetVersionCreateLog](GetVersionCreateLog.md), [GetVersionDeleteLog](GetVersionDeleteLog.md), [GetNewDocumentsAndFoldersLog](GetNewDocumentsAndFoldersLog.md), [GetDeleteLog](GetDeleteLog.md), [GetDispositionLog](GetDispositionLog.md), [GetOwnershipChangeLog](GetOwnershipChangeLog.md) | Audit Managers | The path filter's first part is the library (`LogOperations.cs`, IsLogAccessAllowed); with no path filter the library is 0 and only Audit Managers pass |
| Read the security change log | [GetSecurityChangeLog](GetSecurityChangeLog.md) | Audit Managers; anyone with `ReadSecurityAccessList` on the document or folder | The right on the item first (`FolderServices.cs`, GetSecurityChangeLogAsync); otherwise `ViewAuditLogs` with the item's library, the library root included (task #13, `LogOperations.cs`, GetAccessListHistoryAsync) |
| Read SOX, ISO and classification logs | [GetSoxLogs](GetSoxLogs.md), [GetISOLogs](GetISOLogs.md), [GetClassificationLogs](GetClassificationLogs.md) | Audit Managers; anyone the library policy gives the read right | The policy on the item first (`DocumentReadSoxLog`, `DocumentReadIsoLog`, `DocumentReadClassificationLog`; all three default the library-manager flag to true, so a member manager passes there already); otherwise `ViewAuditLogs` with the item's library |
| Read an item's access list history | [GetAccessListHistory](GetAccessListHistory.md) | Audit Managers; anyone with `ReadSecurityAccessList` on the item | The right first, otherwise `ViewAuditLogs` with the item's library; the current list is read with the same fallback (task #14, `DocumentExtensions.cs`, `FolderExtensions.cs`) |

### Workflow in the library

These are outside the matrix.

| Action | Web service calls | Who else may do it | Conditions |
|---|---|---|---|
| Create a workflow definition | [CreateFlowDef](CreateFlowDef.md), [CreateFlowDef1](CreateFlowDef1.md), [CreateFlowDef2](CreateFlowDef2.md), [CreateFlowDef3](CreateFlowDef3.md) | nobody else | `CheckDomainManagementAsync` on the library (`WorkflowOperations.cs`, CreateWorkflowAsync); the licence must allow workflows; the active folder must be in the library |
| Delete a workflow definition | [DeleteWorkflow](DeleteWorkflow.md) | nobody else | `CheckDomainManagementAsync` (`DomainExtensions.cs`, DeleteWorkflowAsync); the definition must be inactive |
| Change a definition: activate, deactivate, update, steps, task definitions | [ActivateFlowDef](ActivateFlowDef.md), [DeactivateFlowDef](DeactivateFlowDef.md), [UpdateWorkflowDefinition](UpdateWorkflowDefinition.md), [AddFlowStepDef](AddFlowStepDef.md), [AddFlowStepDef1](AddFlowStepDef1.md), [DeleteFlowStepDef](DeleteFlowStepDef.md), [UpdateWorkflowStepDef](UpdateWorkflowStepDef.md), [AddFlowTaskDef](AddFlowTaskDef.md), [DeleteFlowTaskDef](DeleteFlowTaskDef.md), [UpdateWorkflowTaskDef](UpdateWorkflowTaskDef.md) | members of the definition's supervisor list | `SecurityFunctions.CheckWorkflowManagementAsync`: administrator, manager of the definition's library, or supervisor; refusal 4030 "Access denied. Only administrators, library managers, or workflow supervisors can perform this operation." |
| See every task in the library | [getTasks](getTasks.md), [GetTasks1](GetTasks1.md) | nobody else: User and Policy Managers see only their own | With no document or workflow filter and no own-user filter, the caller's own tasks plus every task of the managed libraries (`WorkflowOperations.cs`, GetTasksAsync, task #16) |
| Supervise a running task in the library | [ReassignTask](ReassignTask.md), [ChangeTaskDueDate](ChangeTaskDueDate.md), [UpdateTaskFinishDate](UpdateTaskFinishDate.md), [SetTaskPriority](SetTaskPriority.md), [CreateRelatedTask](CreateRelatedTask.md) | the task's supervisor, the user who assigned it; the assignee for some of them | `WorkflowExecutingTaskExtensions.CheckAllowSupervisionAsync`: a `DOMAINMANAGERS` row for the task's library, read directly, membership not asked; refusal 4030 "Access denied." |
| Edit a later step of a running workflow | [UpdateRunningWorkflowTaskDef](UpdateRunningWorkflowTaskDef.md) | the step's supervisor; an assignee of an earlier step with the edit-next-step or edit-all-steps permission | `WorkflowExecutingTaskDefExtensions.CheckAllowEditStepAsync`: a `DOMAINMANAGERS` row for the document's library |

### Documents and folders in the library

| Action | Web service calls | Who else may do it | Conditions |
|---|---|---|---|
| Any document or folder action whose library policy has the library-manager flag on | every document and folder call | whoever the access list or the other policy flags admit | Default on for 45 of 46 policies (delete, check out, move, security change, ownership change, read logs, read unpublished versions, and the rest; not `DocumentCheckIn`). Needs library membership and an Author-type account; a Reader-type manager only for List/Read-level actions (`IRSecurity.cs`, AccessAllowedAsync). Changed per library with [SetDomainPolicies](SetDomainPolicies.md) |
| Read an unpublished document, or a version other than the published one | document reads | the owner, an author of any version, an assignee with an active task | A manager is in the exception list (`ModuleSecurityFunctions.cs`, IsUserInExceptionListForReadAsync); otherwise the `AccessToDocumentVersions` policy decides |
| Publish, unpublish, set the publishing rule without having authored a version | [PublishDocument](PublishDocument.md), [UnpublishDocument](UnpublishDocument.md), [SetDocumentPublishingRule](SetDocumentPublishingRule.md) | the owner | The `SetPublishingRules` policy first; then the "author of at least one version" requirement is waived for the owner and the library's managers (`SetPublishingRulesOperation.cs`) |

## What the role cannot do

| Action | Web service calls | Who can | Error returned |
|---|---|---|---|
| Appoint or remove a library manager, even for their own library | [AddManagerToDomain](AddManagerToDomain.md), [RemoveManagerFromDomain](RemoveManagerFromDomain.md) | Administrators, User Managers (not on themselves) | 4030 "Access denied. This action is restricted to the following roles: The system administrator, User managers" |
| Create or change a global user; change a local user of another library | [CreateUser](CreateUser.md) with an empty `DomainName`, and every user call above on such a user | Administrators, User Managers | 4030, the same message without "Library manager(s)" (the step is unreachable at `localDomainId` 0) |
| List all users | [GetAllUsers](GetAllUsers.md), the other overloads without a library filter | Administrators, User Managers | 4030 as above |
| Create a global group, change its name or members | [CreateUserGroup](CreateUserGroup.md) with an empty `DomainName`, [UpdateUserGroupName](UpdateUserGroupName.md), [DeleteUsergroup](DeleteUsergroup.md), [AddUsergroupMember](AddUsergroupMember.md), [RemoveUsergroupMember](RemoveUsergroupMember.md) on a global group | Administrators, User Managers | 4030 as above |
| Change the members of a role group (ids up to 1000) | [AddUsergroupMember](AddUsergroupMember.md), [RemoveUsergroupMember](RemoveUsergroupMember.md) on `[Administrators]`, `[User Managers]` and the rest | Administrators only | 4030 "... restricted to the following roles: The system administrator" |
| Transfer work from or to a user outside their libraries, or from an administrator | the Transfer calls | Administrators; User Managers for any two non-administrator users | 4030 (both users are checked); "Access denied. Only administrators can change an administrator's account." |
| Create, rename, delete, archive the library | [CreateDomain](CreateDomain.md), [UpdateDomain](UpdateDomain.md), [DeleteDomain](DeleteDomain.md), [ArchiveDomain](ArchiveDomain.md), [UnarchiveDomain](UnarchiveDomain.md) | Administrators only (`IsAdministrator()`) | 4030 "Only the system administrator can perform this operation" |
| Change the library's policies while the setting is off | [SetDomainPolicies](SetDomainPolicies.md) | Administrators, Policy Managers | 4030 "... restricted to the following roles: The system administrator, Policy managers" |
| Read or change application settings, the setting that would let them edit policies included | [GetSystemBehaviorSettings](GetSystemBehaviorSettings.md), [SetSystemBehaviorSettings](SetSystemBehaviorSettings.md) and the other settings calls | Administrators, Policy Managers (`UpdateApplicationSettingsAndPolicies`, `localDomainId` 0) | 4030 "... The system administrator, Policy managers" |
| Read audit logs across all libraries | the log calls above with no path filter | Administrators, Audit Managers | 4030 "... The system administrator, Audit managers" |
| See the licence, server, warehouse and server logs | [GetLicenseInfo](GetLicenseInfo.md), [GetSystemStatistics](GetSystemStatistics.md), [GetWarehouseStatus](GetWarehouseStatus.md), [GetLogs](GetLogs.md) | Administrators, Audit Managers | 4030 |
| Define retention schedules, dispose of documents | [CreateRandDSchedule](CreateRandDSchedule.md), [DisposeItem](DisposeItem.md) and the other R&D calls | Administrators, R&D Managers | 4030 |
| Flush the cache | [FlushApplicationCache](FlushApplicationCache.md) | Administrators only | 4030 |
| See a library they do not manage and do not belong to | any call with that `DomainName` | members, Administrators, User Managers, Policy Managers | 4041 "Library not found" |
| See the members without access of a library they do not manage | [GetMembersWithoutAccess](GetMembersWithoutAccess.md) | Administrators | 4030 "Access denied. Only library managers can perform this operation." |

## Rules that look wrong

!!! warning "TransferUserDomainManagerRoles lets a library manager hand their library's manager role to another local user"
    `UserTakeOverOperations.RunAsync` checks `TransferUserOwnershipsAndTasks` on both users, which admits
    the manager of their library, and the only extra guard on manager roles is "not to yourself" (:59).
    `TransferDomainManagerRolesAsync` then moves every manager role of the from-user. When the from-user is
    a local user who manages the library, a library manager appoints a new manager, which
    `AddRemoveLibraryManagers` says only administrators and User Managers may do. A local user can be a
    member, and so a manager, of their home library only, so the reach is that one library. The UI should
    not offer the manager-role transfer to library managers; expect it to succeed if called.

!!! warning "RemoveAllSubscriptions admits library managers but not User Managers"
    `UserExtensions.UnSubscribeAllAsync` grants self, administrators and, for a local user, the managers of
    their library through `CheckDomainManagementAsync`; it never consults the matrix, so a User Manager, who
    may read and change the same user's subscriptions through every other user call, is refused with 4030
    "Access denied.". Show the action to library managers for local users; hide it for User Managers until
    the rule is aligned.

!!! warning "The setting that lets managers edit policies cannot be read by managers"
    `SetDomainPolicies` passes for a library manager only when `AllowLibraryManagersToEditPolicy` is on, but
    the only call that returns it, [GetSystemBehaviorSettings](GetSystemBehaviorSettings.md), needs
    `UpdateApplicationSettingsAndPolicies` (Policy Managers). The 4030 message a manager gets when the
    setting is off names only the system administrator and Policy Managers. The UI cannot tell in advance:
    either show the policy editor to managers and handle the 4030, or expose the flag through a call any
    signed-in user may make.

!!! warning "Dead matrix entries name library managers (task #31, deferred)"
    `IrAdminAction.ListLibraryMembers` and `DisplayUserProfile` set `allowLibManagers` in `IRSecurity.IsAllowed`
    but no code checks them. Listing a library's members ([GetDomainMembers](GetDomainMembers.md) and the
    rest) is open to any signed-in user who reaches the library; do not gate it on a manager check.
    `UserOperations.GetLibraryListForAdministrationAsync` has a branch for listing another user's libraries
    that nothing calls.

!!! warning "Co-workers read what the manager gate protects (task #17, deferred)"
    [GetUserStatistics](GetUserStatistics.md), [GetDomainMembershipsOfUser](GetDomainMembershipsOfUser.md)
    and [GetManagedDomainsByUser](GetManagedDomainsByUser.md) check only that the caller may see the user,
    and every member of the user's library is a co-worker of a local user. For local users the library
    manager condition on these three calls adds nothing: any member of the library reads them.

!!! warning "AddUsergroupMember tells a caller with no right whether the user and group exist"
    `UsergroupOperations.AddMemberTransactionAsync` answers "User group not found", "User not found" and
    "User is not a member of the library." before it checks `UpdateGroupMembers` (:200-229). Task #26 fixed
    the same order in five other operations but not here. A caller who may add nobody to the group learns
    which names exist. The UI is not affected; noted for the server.

## Finding out whether the signed-in user has this role

- [GetManagedDomainsByUser](GetManagedDomainsByUser.md) with the caller's own name, or an empty name:
  the libraries the caller manages (`UserServices.cs`, GetManagedDomainsByUserAsync; the list is
  `DOMAINMANAGERS` rows). An empty list means the caller manages nothing.
- [GetLibrariesForAdministration](GetLibrariesForAdministration.md): for a pure library manager, the managed
  libraries; but a User Manager or Policy Manager gets every library from the same call, so use
  GetManagedDomainsByUser to tell the two apart, or [GetGroupMembershipsOfUser](GetGroupMembershipsOfUser.md)
  with the caller's own name for the role groups (`GroupID` 100 to 105).
- [GetManagers](GetManagers.md) with a library name answers any signed-in user who reaches the library;
  [GetDomains1](GetDomains1.md) can return the managers of every library the caller belongs to in one call.
- [GetUserStatistics](GetUserStatistics.md) carries a count of managed libraries
  (`UserStatistics.DomainManagerRoles`; the attribute name in the answer was not verified here).

## Notes

- Library reachability by name changed in commit 61e1fb36 (dated 2026-10-21 in git): `GetLibraryByNameAsync`
  and `GetLibraryByIdAsync` share `MayReachAsync`, which is membership, or anonymous access, or
  `ListLibrariesForAdministration` with the library's id. Administrators, User Managers and Policy
  Managers reach every library; a library's manager reaches it whether or not they are still a member. Task
  #20 ("library lookup by name has no administrator bypass") is closed by this commit for administrators and
  library managers, though the task list still marks it deferred; Audit Managers still reach by name only
  what they belong to.
- Can a manager be a non-member? Appointment requires membership, and `DeleteLibraryManagersWhoAreNotLibraryMemberAsync`
  runs on every path that takes a membership away (user removed, group removed, user removed from a member
  group), so by the code read here a manager is always a member. If a non-member manager row exists from
  older data, the matrix and the workflow checks still pass for it (they read `DOMAINMANAGERS` only), but
  every document and folder action fails with "library members only".
- Workflow: creating and deleting definitions is managers and administrators only; everything in between
  (activate, steps, task definitions) is also open to the definition's supervisors. Supervising a running
  task is open to the task's supervisor and assigner as well. [GetWorkflowDefinitions](GetWorkflowDefinitions.md)
  with no library lists the caller's member libraries; with a library name any reachable library.
- [TransferUserDomainMemberships](TransferUserDomainMemberships.md) between two local users moves nothing:
  memberships are transferred only when the to-user is global (`UserTakeOverOperations.cs`, RunAsync), and a
  local user holds only their home membership anyway. The call still answers success.
- [TransferUserGroupMemberships](TransferUserGroupMemberships.md) by a library manager leaves the role
  groups (ids up to 1000) with the from-user and says so in `warnings` (task #32).
- The matrix message lists "Library manager(s)" only when the library step was reachable. A manager refused
  on a global user sees a message that does not mention library managers; that is the message, not a sign
  that the role never applies.
- [GetMembersWithoutAccess](GetMembersWithoutAccess.md) is the one library-management call that admits
  library managers and administrators but refuses User Managers and Policy Managers, who otherwise
  administer every library; the refusal says "Only library managers can perform this operation".
- `UserOperations.IsDomainManagerAsync` is a plain row lookup with no caching; manager changes take effect
  on the next call.

## Related

- [AdministrativeRoles](AdministrativeRoles.md), all roles at a glance
- the other role pages: [Administrators](AdministratorsRole.md), [User Managers](UserManagersRole.md),
  [Audit Managers](AuditManagersRole.md), [Policy Managers](PolicyManagersRole.md),
  [R&D Managers](RDManagersRole.md), [Search & Category Administrators](SearchAdministratorsRole.md)
