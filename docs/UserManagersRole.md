# User Managers

Group id `100`, stored as `[User Managers]`, enum value `enum_IR.AdmistrativeRoles.UserManager`. The role is for
the people who run the accounts: they create, change, delete and list users, manage user groups and their
members, add and remove library members and library managers, and move one user's work to another. It is a
system group (no library, fixed id). Its members can be changed by Administrators only: `IRSecurity.IsAllowed`
adds no role to `UpdateGroupMembers` for a group id up to `IRConstants.LastSystemUserGroupId` (1000), so only
the administrator check at the top of `AccessAllowedforAdminFunctionsAsync` passes.

## How the role is checked

The matrix in `IRSecurity.IsAllowed` (`IRNET/IRSecurity.cs`) names `UserManager` for these `IrAdminAction`
values: `ListingGroupMembershipOfUser`, `CreateUser`, `ListUsers`, `UpdateUserProfile`, `UpdateUserPreferences`,
`ListingAuditLogOfUser`, `ListingUserOwnerships`, `SetUserPassword`, `SetUserTaskRedirections`,
`RerouteUserTaskRedirection`, `ApplyRemoveCustomMetaData`, `DeleteUser`, `UpdateGroupMembers` (group ids above
1000 only), `ListGroups`, `CreateUserGroup`, `UpdateUserGroupProperties`, `DeleteUserGroup`,
`ListLibrariesForAdministration` (shared with Policy Managers), `AddRemoveLibraryMembers`,
`AddRemoveLibraryManagers` and `TransferUserOwnershipsAndTasks`. Two more, `DisplayUserProfile` and
`ListLibraryMembers`, name the role but nothing calls them (see Notes).

`IRSecurity.AccessAllowedforAdminFunctionsAsync` decides, in this order:

1. An administrator (`ThreadVariables.IsAdministrator()`: the `sysadmin` account, id 4, or a member of
   `[Administrators]`) passes everything.
2. The administrator's-account guard: for the actions that change an account (`UpdateUserProfile`,
   `UpdateUserPreferences`, `SetUserPassword`, `DeleteUser`, `SetUserTaskRedirections`,
   `ApplyRemoveCustomMetaData`; method `ChangesTheAccount`), a non-administrator acting on the `sysadmin`
   account or on a member of `[Administrators]` is refused before the matrix is asked: `4030`, "Access denied.
   Only administrators can change an administrator's account." Reads, transfers and rerouting are not in that
   list (transfers have their own guard, see the Transfers table).
3. `IsAllowed`: self first (only for the actions marked *self* below, and only when the object is a USER and is
   the caller), then membership of a required role group, then, when the action allows it and a library id was
   passed, the library managers of that library (`SecurityFunctions.CheckDomainManagementAsync`). A library id
   of 0 (a global user, a global group, an application-wide action) means the library-manager step can never
   pass.
4. For `RerouteUserTaskRedirection` only: after a refusal, the caller passes anyway when the user's current
   redirection points to the caller.

A refusal from the matrix is `errorCode="4030"` with "Access denied. This action is restricted to the
following roles: The system administrator, Library manager(s), User managers" (the library managers part only
when a library id was passed; the role list follows the action). The guard in step 2 answers `4030` with the
administrator's-account message above.

Every call that takes a user name first looks the user up. With the security check on
(`UserOperations.GetUserObjectAsync`, `checkSecurity` true), the caller may see the user when they are the user,
an administrator, a User Manager, a manager of the user's home library (local users only), or a co-worker
(`IsCoWorkerAsync`: a member of a library the caller is also a member of); otherwise `4030`, "Access denied. You
need to be a coworker, administrator, library manager, or user manager to access this information." An unknown
name answers `4041` to a caller who may list users (`ListUsers` with no library: administrators and User
Managers) and `4030` to anyone else. Calls that look the user up without the check (`checkSecurity` false)
answer `4041` for an unknown name to everyone and leave the decision to the action named in the tables.

## What the role can do

Administrators may do everything in these tables; the "Who else may do it" column lists the others. "Lib
managers" means the managers of the user's or group's home library, so only for users and groups local to a
library, never for global ones, unless the row says otherwise. An administrator's account (the `sysadmin`
account or a member of `[Administrators]`) can be read but not changed by a User Manager; the rows say where
that guard applies.

### Users

| Action | Web service calls | Who else may do it | Conditions |
|---|---|---|---|
| Create a user | [CreateUser](CreateUser.md) | lib managers, for a user local to their library (the call names the library) | A global user (no library name) is User Managers only. The library name must be reachable (see Libraries list), else `4041`. Anonymous callers get `4010`. |
| Send a user the welcome e-mail | [SendWelcomeEmailForUser](SendWelcomeEmailForUser.md) | lib managers, for a user local to their library | Checks `CreateUser` on the looked-up user (`UserServices.cs`, SendWelcomeEmailForUserAsync). Not self. The user must have an e-mail address (`4000`). Not blocked by the administrator's-account guard. |
| List users | [GetAllUsers](GetAllUsers.md), [GetAllUsers1](GetAllUsers1.md), [GetAllUsers2](GetAllUsers2.md), [GetAllUsers3](GetAllUsers3.md), [GetAllUsersWithoutDetails](GetAllUsersWithoutDetails.md) | lib managers, only when the filter's library name (or `~L<id>`) is a library they manage | `ListUsers` with the library id from the filter (`InfoRouter.cs`, GetAllUsers). With no library filter only User Managers pass. A library filter selects the users local to that library (`PLAYER.DOMAINID`), not its members. An unknown library name is `4000` "Library not found". |
| Look up a user | [GetUser](GetUser.md), [GetUserStatistics](GetUserStatistics.md), [GetDomainMembershipsOfUser](GetDomainMembershipsOfUser.md), [GetManagedDomainsByUser](GetManagedDomainsByUser.md), [GetUserTaskRedirectionTo](GetUserTaskRedirectionTo.md) | self, lib managers, co-workers | Only the visibility check above; no further role check (see the first warning). GetUser and GetManagedDomainsByUser with an empty name answer for the caller. |
| Change a user's name or authentication source | [UpdateUserProfile](UpdateUserProfile.md) | lib managers | `UpdateUserProfile`. Not self. Administrator's-account guard. For the `sysadmin` account the status and type are forced to enabled and author. |
| Enable or disable a user | [ChangeUserStatus](ChangeUserStatus.md) | lib managers | `UpdateUserProfile`. Not self. Administrator's-account guard. The `sysadmin` account is refused for everyone (`4030`, "This is a system account and cannot be changed."). A licence check may refuse enabling (`UserOperations.CheckLicenseChangingUserStatusAsync`). |
| Change a user's type (author or reader) | [ChangeUserType](ChangeUserType.md) | lib managers | As ChangeUserStatus. |
| Change a user's e-mail, mobile number or preferences | [UpdateUserContactInfo](UpdateUserContactInfo.md), [UpdateUserEmail](UpdateUserEmail.md), [UpdateUserPreferences](UpdateUserPreferences.md) | self, lib managers | `UpdateUserPreferences`. Administrator's-account guard. |
| Set a user's password | [ChangeUserPassword](ChangeUserPassword.md), [ChangeUserPassword1](ChangeUserPassword1.md) | lib managers; self through ChangeUserPassword1 only, with the current password | `SetUserPassword`. Administrator's-account guard. ChangeUserPassword on your own account is `4000` naming ChangeUserPassword1. Only infoRouter-authenticated accounts (`4000` otherwise). A wrong current password is `4030`, not `4010`. |
| Delete a user | [DeleteUser](DeleteUser.md), [DeleteUser1](DeleteUser1.md) | lib managers | `DeleteUser`. Not self. Administrator's-account guard. DeleteUser is `4000` naming DeleteUser1 when the password policy re-prompts for user deletion (`PasswordRePromptActions.UserDelete`) and Windows authentication is off. The `sysadmin` account cannot be deleted by anyone (`4000`). A user with open tasks, workflow roles or ISO reviewer roles is refused with the counts. |
| Read a user's activity lists | [GetUserViewLog](GetUserViewLog.md), [GetUserViewLog1](GetUserViewLog1.md), [GetUserViewLogLite](GetUserViewLogLite.md), [GetAuthoredDocuments](GetAuthoredDocuments.md), [GetCheckedoutDocumentsByUser](GetCheckedoutDocumentsByUser.md), [GetDocumentsOwnedByUser](GetDocumentsOwnedByUser.md), [GetFavoriteDocumentsOfUser](GetFavoriteDocumentsOfUser.md), [GetISOReviewAssignmentsOfUser](GetISOReviewAssignmentsOfUser.md), [GetSubscribedDocumentsByUser](GetSubscribedDocumentsByUser.md), [GetFavoriteFoldersOfUser](GetFavoriteFoldersOfUser.md), [GetFoldersOwnedByUser](GetFoldersOwnedByUser.md), [GetSubscribedFoldersByUser](GetSubscribedFoldersByUser.md) | self, lib managers | `ListingAuditLogOfUser` when the user is not the caller (`UserExtensions.cs`, GetReadLogAsync, GetRelatedDocumentsAsync, GetUserRelatedFoldersAsync and their count twins). A co-worker passes the lookup and is refused here with `4030`. |
| Search another user's lists | [Search](Search.md), [GetFoldersAndDocumentsByPage2](GetFoldersAndDocumentsByPage2.md) with `SUBSCRIPTIONSOF`, `FAVORITESOF`, `DOWNLOADQUEOF`, or `VIEWCRITERIA` with `USERNAME` | self, lib managers | `ListingAuditLogOfUser` on the named user (`SearchServices.cs`, GetUserWithError; both operations parse the criteria with ParseSearchParameters). `CHECKEDOUTBYUSER` needs only the visibility check; the `USERNAME` (author) criterion needs none. |
| Read a user's group memberships | [GetGroupMembershipsOfUser](GetGroupMembershipsOfUser.md) | self, lib managers | `ListingGroupMembershipOfUser` (`UserServices.cs`, GetGroupMembershipsOfUserAsync). A co-worker passes the lookup and is refused here. |
| Read a user's workflow roles | [GetUsersWorkflowRoles](GetUsersWorkflowRoles.md) | self, lib managers | `ListingUserOwnerships` (`WorkflowDefinitionServices.cs`). The lookup is made without the visibility check, so an unknown name is `4041` for everyone. |
| Set or remove a user's task redirection | [SetUserTaskRedirection](SetUserTaskRedirection.md), [RemoveUserTaskRedirection](RemoveUserTaskRedirection.md) | self, lib managers | `SetUserTaskRedirections`. Administrator's-account guard. The target user must exist and be enabled. |
| Read the redirections that point to a user | [GetUserTaskRedirectionsFrom](GetUserTaskRedirectionsFrom.md) | self, lib managers | `RerouteUserTaskRedirection` and then `SetUserTaskRedirections`, so the second one decides. The administrator's-account guard applies to this read (see warnings). |
| Reroute a user's existing redirection | [RerouteUserTaskRedirection](RerouteUserTaskRedirection.md) | self, lib managers, and the user the redirection currently points to | `RerouteUserTaskRedirection`. The general setting `RerouteRedirections` must be on (`4030`, "Rerouting of redirected tasks is not allowed by the application settings."). No redirection is `4041`. Not blocked by the administrator's-account guard (see warnings). |
| Add, update or delete property set rows on a user | [AddPropertySetRowForUser](AddPropertySetRowForUser.md), [UpdatePropertySetRowForUser](UpdatePropertySetRowForUser.md), [DeletePropertySetRowForUser](DeletePropertySetRowForUser.md) | lib managers | `ApplyRemoveCustomMetaData` per row (`PropertySetOperations.cs`, PsetApplySecurityCheck). Not self. Administrator's-account guard. The user is looked up with the visibility check, so a co-worker reaches the row check and is refused there; a single refusal is answered with the code the check gave. |

### User groups

| Action | Web service calls | Who else may do it | Conditions |
|---|---|---|---|
| Create a group | [CreateUserGroup](CreateUserGroup.md), [CreateUserGroup1](CreateUserGroup1.md) | lib managers, for a group of their library | `CreateUserGroup` with the library id (`IRGeneral.cs`, Internal_CreateUserGroup). A global group (no library name) is User Managers only. |
| Rename a group or change whether it shows its members | [UpdateUserGroupName](UpdateUserGroupName.md), [UpdateUserGroupName1](UpdateUserGroupName1.md) | lib managers, for a group of their library | `UpdateUserGroupProperties`. A system group (id up to 1000, the six role groups included) is refused after the check with `4000`, "System user groups cannot be renamed.", administrators included. |
| Delete a group | [DeleteUsergroup](DeleteUsergroup.md) | lib managers, for a group of their library | `DeleteUserGroup`. A system group is `4000`, "System user groups cannot be deleted.", administrators included. A group with tasks or workflow roles is refused with the count. |
| Add or remove a member of an ordinary group | [AddUsergroupMember](AddUsergroupMember.md), [RemoveUsergroupMember](RemoveUsergroupMember.md) | lib managers, for a group of their library | `UpdateGroupMembers`, which names the role only for group ids above 1000. Adding to a library group needs the user to be a member of that library (`4000`); a local user can only join the groups of their own library (`4000`). |
| Read the members of a group that hides them | [GetUserGroupMembers](GetUserGroupMembers.md), [GetUserGroupMembers1](GetUserGroupMembers1.md) | lib managers, for a group of their library | `ListGroups`, asked only when the group's `ShowMembers` is false (`UsergroupExtensions.cs`, GetMembersForPublic). The refusal is `4000`, not `4030` (see warnings). A group that shows its members answers any signed-in user. For a role group (global, so no library) a hidden membership is read by administrators and User Managers only. |
| List groups, read a group | [GetGlobalGroups](GetGlobalGroups.md), [GetDomainGroups](GetDomainGroups.md), [GetLocalGroups](GetLocalGroups.md), [GetUserGroup](GetUserGroup.md) | anyone signed in; GetDomainGroups and GetLocalGroups need the library to be reachable | No role check. GetUserGroup resolves the library name without the reach check (`InfoRouter.cs`, GetUserGroupByNameAsync). |

### Library membership and managers

| Action | Web service calls | Who else may do it | Conditions |
|---|---|---|---|
| Add or remove a library member | [AddUserAsDomainMember](AddUserAsDomainMember.md), [RemoveUserFromDomainMembership](RemoveUserFromDomainMembership.md), [AddUserGroupAsDomainMember](AddUserGroupAsDomainMember.md), [RemoveUserGroupFromDomainMembership](RemoveUserGroupFromDomainMembership.md) | the managers of that library | `AddRemoveLibraryMembers` with the library's id, checked before the user or group is looked up (`DomainExtensions.cs`, `DomainOperations.cs`). Only global users and groups can be added (`4000`). A User Manager may add themselves. |
| Appoint a library manager | [AddManagerToDomain](AddManagerToDomain.md) | nobody else: library managers are not allowed | `AddRemoveLibraryManagers` (no library-manager step). The user must already be a member of the library (`4000`). A non-administrator naming themselves is refused: `4030`, "Access denied. Only administrators can make themselves a library manager." (`DomainExtensions.cs`, SetDomainManagerAsync). |
| Remove a library manager | [RemoveManagerFromDomain](RemoveManagerFromDomain.md) | nobody else | `AddRemoveLibraryManagers`. No self guard: a User Manager may remove anyone, themselves included. |
| Read a library's members, users and managers | [GetDomainMembers](GetDomainMembers.md), [GetDomainMembers1](GetDomainMembers1.md), [GetDomainUsers](GetDomainUsers.md), [GetDomainUsers1](GetDomainUsers1.md), [GetLocalUsers](GetLocalUsers.md), [GetManagers](GetManagers.md) | anyone signed in who can reach the library | No role check beyond reaching the library (`LibraryServices.cs`). The `ListLibraryMembers` action exists for this but is never asked. |

### Transfers

All thirteen calls go through `UserExtensions.TakeOverAsync` and `UserTakeOverOperations.RunAsync`, with
`TransferUserOwnershipsAndTasks` checked on the from-user and then on the to-user, each with that user's own
home library.

| Action | Web service calls | Who else may do it | Conditions |
|---|---|---|---|
| Move one user's work to another | [TransferUserTasks](TransferUserTasks.md), [TransferUserCheckedOutDocuments](TransferUserCheckedOutDocuments.md), [TransferUserDocumentOwnerships](TransferUserDocumentOwnerships.md), [TransferUserFolderOwnerships](TransferUserFolderOwnerships.md), [TransferUserDocumentSubscriptions](TransferUserDocumentSubscriptions.md), [TransferUserFolderSubscriptions](TransferUserFolderSubscriptions.md), [TransferUserExpirationNotices](TransferUserExpirationNotices.md), [TransferUserISOTasks](TransferUserISOTasks.md), [TransferUserWorkflowDefinitions](TransferUserWorkflowDefinitions.md), [TransferUserSecurityPermissions](TransferUserSecurityPermissions.md), [TransferUserDomainMemberships](TransferUserDomainMemberships.md) | lib managers, only when both users are local to libraries they manage | Not self. Both users must be visible to the caller (lookup with the check). The same user as source and target is `4000`. A from-user who is an administrator is refused for non-administrators: `4030`, "Only administrators can change an administrator's account."; giving work to an administrator is not guarded. Library memberships are not moved to a local to-user. |
| Move a user's group memberships | [TransferUserGroupMemberships](TransferUserGroupMemberships.md) | as above | As above, and the role groups (ids up to 1000) are skipped for a non-administrator: they stay with the from-user and the answer carries `warnings="Administrative role memberships were not transferred: only administrators can transfer them."` (`UserTakeOverOperations.cs`, TransferUsergroupMembershipsAsync). |
| Move a user's library manager roles | [TransferUserDomainManagerRoles](TransferUserDomainManagerRoles.md) | as above | As above, and a non-administrator naming themselves as the to-user is refused before anything moves: `4030`, "Only administrators can make themselves a library manager." |

### Libraries list

| Action | Web service calls | Who else may do it | Conditions |
|---|---|---|---|
| List every library, membership aside | [GetLibrariesForAdministration](GetLibrariesForAdministration.md) | Policy Managers get every library too; library managers get the libraries they manage; anyone else signed in gets their (empty) managed list | `ListLibrariesForAdministration` with no library id (`UserOperations.cs`, GetLibraryListForAdministrationAsync), so the library-manager step never passes and they fall to the managed list. Anonymous callers get `4010`. |
| Reach a library by name | every call that takes a `DomainName` ([GetManagers](GetManagers.md), [AddUserAsDomainMember](AddUserAsDomainMember.md), [CreateUser](CreateUser.md) with a library, [GetDomainGroups](GetDomainGroups.md), ...) | its members, anyone where it allows anonymous access, Policy Managers, its managers | `DomainOperations.MayReachAsync`: the viewable-library list, then `ListLibrariesForAdministration` with the library's id. A library the caller cannot reach is `4041` "Library not found". [GetDomains](GetDomains.md) still lists only the libraries the caller belongs to. |

## What the role cannot do

| Action | Web service calls | Who can | Error returned |
|---|---|---|---|
| Change an administrator's account: name, status, type, password, e-mail, preferences, task redirection, property set rows; delete it; take its work | the calls marked with the administrator's-account guard above, and the Transfer calls with an administrator as from-user | Administrators | `4030` "Access denied. Only administrators can change an administrator's account." |
| Change their own name or authentication source | [UpdateUserProfile](UpdateUserProfile.md) on their own account | Administrators; another User Manager; the managers of their home library | `4030`, the role list |
| Add or remove members of the six role groups (ids 100 to 105), or of any group with an id up to 1000 | [AddUsergroupMember](AddUsergroupMember.md), [RemoveUsergroupMember](RemoveUsergroupMember.md) | Administrators | `4030` "Access denied. This action is restricted to the following roles: The system administrator" |
| Rename or delete a role group | [UpdateUserGroupName](UpdateUserGroupName.md), [DeleteUsergroup](DeleteUsergroup.md) | nobody | `4000` "System user groups cannot be renamed." / "System user groups cannot be deleted." |
| Appoint themselves a library manager | [AddManagerToDomain](AddManagerToDomain.md), [TransferUserDomainManagerRoles](TransferUserDomainManagerRoles.md) to themselves | Administrators | `4030` "Access denied. Only administrators can make themselves a library manager." |
| Create, rename, delete, archive or unarchive a library | [CreateDomain](CreateDomain.md), [UpdateDomain](UpdateDomain.md), [DeleteDomain](DeleteDomain.md), [ArchiveDomain](ArchiveDomain.md), [UnarchiveDomain](UnarchiveDomain.md) | Administrators (`IsAdministrator()` in `DomainOperations.cs` and `DomainExtensions.cs`) | `4030` "Only the system administrator can perform this operation" |
| Read or change library policies | [GetDomainPolicies](GetDomainPolicies.md), [SetDomainPolicies](SetDomainPolicies.md) | Policy Managers; the library's managers (reading always, changing only when *Allow library managers to edit policies* is on) | `4030`, the role list naming Policy Managers |
| List a library's members below a given right | [GetMembersWithoutAccess](GetMembersWithoutAccess.md) | Administrators for any library; the library's managers for it | `4030` "Access denied. Only library managers can perform this operation." |
| Remove all of another user's subscriptions | [RemoveAllSubscriptions](RemoveAllSubscriptions.md) | self; the managers of the user's home library (`UserExtensions.cs`, UnSubscribeAllAsync) | `4030` "Access denied." |
| See other users' workflow tasks | [getTasks](getTasks.md), [GetTasks1](GetTasks1.md) with no document or flow | Administrators for every library; library managers for theirs (`WorkflowOperations.cs`) | not an error: the list holds only the caller's own tasks |
| Create or delete property set definitions | [CreatePropertySetDefinition](CreatePropertySetDefinition.md), [DeletePropertySetDefinition](DeletePropertySetDefinition.md) | Administrators (`PropertySetOperations.cs`, CreatePropertySet; `InfoRouter.cs`, DeletePropertySetAsync) | `4030` "Only the system administrator can perform this operation" |
| Flush the application cache | [FlushApplicationCache](FlushApplicationCache.md) | Administrators | `4030`, the role list naming the system administrator only |

## Finding out whether the signed-in user has this role

- [GetGroupMembershipsOfUser](GetGroupMembershipsOfUser.md) with the caller's own name: `ListingGroupMembershipOfUser`
  allows self, so it always answers for yourself; a group with `GroupID` `100` in the answer is this role
  (`104` is Administrators, who pass every check on this page without holding the role).
- [GetLibrariesForAdministration](GetLibrariesForAdministration.md) answers every library for a User Manager,
  Policy Manager or administrator and only the managed ones for a library manager, so it does not tell the
  roles apart; use it for the list of libraries to offer, not for the role.
- [getApplicationParameters](getApplicationParameters.md) tells whether the caller is an administrator
  (`LibraryServices.GetApplicationParametersAsync` returns `IsAdministrator()`); it says nothing about this role.

## Notes

- The user profile is read through the visibility check and library members through reaching the library;
  the two rows above describe what actually runs.
- The administrator's-account guard reads: a User Manager can list, look up and read the activity lists,
  group memberships and workflow roles of an administrator, and send the welcome e-mail (the reset link goes
  to the administrator's own address, which the User Manager cannot change). Up to 8.7 only the `sysadmin`
  account was guarded.
- A library manager's rights on this page are per user and per group: they pass only for users and groups
  whose home library they manage. For a global user or group there is no library and the library-manager
  step never passes, whatever library the manager runs. The exceptions are the library-scoped actions
  (members of a library, local users and groups created in it, the users listed with a library filter), where
  the library in the call is the one checked.
- `UpdateUserProfile` allows no self action: a user cannot change their own user name, first or last name or
  authentication source through the API. Contact details and preferences are the self-service calls.
- Library managers are not a role group: a user manages a particular library (`DataLayer.DomainManagersStore`), and only
  Administrators and User Managers may make someone one. Two User Managers may appoint each other.
- GetAllUsers answers users by home library, so a library manager filtering by their library sees that
  library's local users, not the global users who are its members; the members are read with GetDomainMembers.
- Library lookup by name (`DomainOperations.GetLibraryByNameAsync`) goes through `MayReachAsync`, whose
  second step is `ListLibrariesForAdministration`, which administrators pass first.
- A User Manager's own workflow task list is theirs alone: `getTasks` widens to every library only for
  administrators and to the managed libraries for library managers (`WorkflowOperations.cs`).

## Related

- [AdministrativeRoles](AdministrativeRoles.md), all roles at a glance
- the other role pages: [Administrators](AdministratorsRole.md), [Audit Managers](AuditManagersRole.md),
  [Policy Managers](PolicyManagersRole.md), [R&D Managers](RDManagersRole.md),
  [Search & Category Administrators](SearchAdministratorsRole.md), [Library Managers](LibraryManagersRole.md)
