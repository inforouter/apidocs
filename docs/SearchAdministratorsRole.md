# Search & Category Administrators

Group id `105`, stored as `[Search & Category Administrators]`, enum value `enum_IR.AdmistrativeRoles.SearchAdministrators`.
The role is for the **system-wide** saved searches and search pages: the SEARCHPAGES entries with no owner
(`ownerId="0"`), which can be shared with every signed-in user, with the anonymous user, or with user groups.
Personal entries (`ownerId` > 0) belong to their owner and need no role. The group is a system group with no
library (DOMAINID 0), created by the 8.6.105 update (`setup/PatchLibrary/Worker/Updates/Update_8_6_105.cs`,
CreateSearchAndCategoryAdministratorsGroup). Only Administrators can add or remove its members: for a group id up
to `IRConstants.LastSystemUserGroupId` (1000) the UpdateGroupMembers rule adds no role and no library-manager step,
so only the administrator check at the top of `AccessAllowedforAdminFunctionsAsync` passes (`IRSecurity.cs`, IsAllowed).

## How the role is checked

This role is **not** in the IRSecurity matrix: no `IrAdminAction` names it. The check is
`UserOperations.HasAdministrativeRoleAsync` (`IRNET/Operations/UserOperations.cs`), which passes when the caller is
the `sysadmin` account (user id 4) or a member of group `105` or of `[Administrators]` (`104`). It is called only
from `IRNET/SearchPages.cs`, which is reached only by the five saved-search operations below. There is no self step
and no library-manager step: the entries belong to no library.

Order of the checks in `SearchPages.cs`:

1. Signed in. A caller whose user id is 0 or below (the anonymous session has a negative id) gets `4010`
   "Access denied." from create, update and delete.
2. The entry exists, and for an update its `searchPageType` matches the stored type: otherwise `4041`
   "Search or category page cannot be found."
3. Ownership decides which rule applies, read from the **stored row**, never from the caller's `isPersonal`:
    - `ownerId` = 0 (system-wide): the role check. Refusal is `4030`
      "Access denied. Only search administrators can perform this operation."
    - `ownerId` > 0 (personal): the caller must be the owner. Refusal is `4030`
      "Access denied. Only the search page owner can perform this operation." The role does not help here, and
      neither does being an administrator.

Reading (`GetSavedSearch`) uses the same rule as the listing: a refusal is `4030` "Access denied."

## What the role can do

Administrators hold this role without being in the group (`HasAdministrativeRoleAsync`). On **personal** entries,
however, administrators are treated like everyone else: the owner check has no administrator bypass (see Notes).

### System-wide saved searches and search pages

| Action | Web service calls | Who else may do it | Conditions |
|---|---|---|---|
| Create a system-wide entry | [CreateSavedSearch](CreateSavedSearch.md) with `isPersonal=false` | nobody else | `searchPageType` is `savedSearch` or `searchPage` (`4000` otherwise); name 5 to 64 characters; a name already used for that type is `4090` |
| Change a system-wide entry: name, description, sharing (`anonymousAccess`, `publicAccess`, `userGroupNames`), search parameters | [UpdateSavedSearch](UpdateSavedSearch.md) | nobody else | the owner stays 0 whatever `isPersonal` says; `searchPageType` must match the stored type (`4041`); for page 1 (Advanced Search) only the sharing flags and groups are written and the name must stay "advanced search" (`4030` otherwise) |
| Delete a system-wide entry | [DeleteSavedSearch](DeleteSavedSearch.md) | nobody else | not page 1 (`4030` "Advanced search page cannot be renamed or deleted.") |
| Read any system-wide entry, whatever it is shared with | [GetSavedSearch](GetSavedSearch.md) | anyone signed in for a `publicAccess` entry; members of a group in its `userGroupNames`; the anonymous user for an `anonymousAccess` entry | |
| List every system-wide entry | [GetSavedSearches](GetSavedSearches.md) | anyone signed in gets the public entries and those shared with one of their groups; the anonymous user gets the `anonymousAccess` entries | the list also holds the caller's own personal entries, never anyone else's (`SearchPageStore.GetSearchPagesAsync`) |

### Personal saved searches (no role needed)

| Action | Web service calls | Who may do it | Conditions |
|---|---|---|---|
| Create a personal entry | [CreateSavedSearch](CreateSavedSearch.md) with `isPersonal=true` | anyone signed in | the entry is stored under the caller's id; same name rules as above |
| Read, change or delete your own personal entry | [GetSavedSearch](GetSavedSearch.md), [UpdateSavedSearch](UpdateSavedSearch.md), [DeleteSavedSearch](DeleteSavedSearch.md) | the owner only | `isPersonal` is ignored on update: an entry never changes owner |

## What the role cannot do

| Action | Web service calls | Who can | Error returned |
|---|---|---|---|
| Read, change or delete another user's personal entry | [GetSavedSearch](GetSavedSearch.md), [UpdateSavedSearch](UpdateSavedSearch.md), [DeleteSavedSearch](DeleteSavedSearch.md) | the owner only; not Administrators, not the `sysadmin` account | `4030` "Access denied." for a read; `4030` "Access denied. Only the search page owner can perform this operation." for a change or delete |
| See other users' personal entries | [GetSavedSearches](GetSavedSearches.md) | nobody: every caller gets only their own | no error; the entries are left out |
| Turn a personal entry into a system-wide one, or back; change an entry's type | [UpdateSavedSearch](UpdateSavedSearch.md) | nobody; create a new entry and delete the old one | `isPersonal` is ignored; a different `searchPageType` is `4041` |
| Delete or rename the Advanced Search page (id 1) | [DeleteSavedSearch](DeleteSavedSearch.md), [UpdateSavedSearch](UpdateSavedSearch.md) | nobody | `4030` "Advanced search page cannot be renamed or deleted." |
| Change the search results page size (`SearchPageSize`) and the other application settings | [SetGeneralAppSettings](SetGeneralAppSettings.md), [SetSystemBehaviorSettings](SetSystemBehaviorSettings.md), [SetAuthenticationAndPasswordPolicy](SetAuthenticationAndPasswordPolicy.md), [SetEmailAndNotificationSettings](SetEmailAndNotificationSettings.md), [SetDefaultFolderColumns](SetDefaultFolderColumns.md) | Policy Managers (`UpdateApplicationSettingsAndPolicies`, `SettingServices.cs`) | `4030` "Access denied. This action is restricted to the following roles: ..." naming the system administrator and Policy Managers |
| Administer the content search index: re-index, rebuild, index server settings | none exists: `ISrv.cs` has no operation for it | n/a | n/a |
| Flush the application cache | [FlushApplicationCache](FlushApplicationCache.md) | Administrators only (`IRSecurity.cs`, IsAllowed adds no role) | `4030` |
| Make someone a search administrator | [AddUsergroupMember](AddUsergroupMember.md), [RemoveUsergroupMember](RemoveUsergroupMember.md) on group 105 | Administrators only (UpdateGroupMembers, ids up to 1000) | `4030` |
| List the members of group 105 | [GetUserGroupMembers](GetUserGroupMembers.md), [GetUserGroupMembers1](GetUserGroupMembers1.md) | Administrators and User Managers (`ListGroups`); the 8.6.105 insert sets no SHOWMEMBERS, so the group hides its members (`UsergroupExtensions.GetMembersForPublic`) | `4000` "Cannot access user group members. The user group is marked as a public user group." followed by the roles text |

Running a search ([Search](Search.md), [GetNextSearchPage](GetNextSearchPage.md) and the rest) needs no role:
`SearchServices.ExecuteSearchAsync` makes no administrative check.

## Finding out whether the signed-in user has this role

- [GetGroupMembershipsOfUser](GetGroupMembershipsOfUser.md) with the caller's own user name: the
  `ListingGroupMembershipOfUser` rule allows self (`IRSecurity.cs`, IsAllowed), so this works for every user. A
  `GroupID` of `105` is the role; `104` ([Administrators]) holds it as well.
- [getApplicationParameters](getApplicationParameters.md) answers an administrator with the extended block
  (`WebAPI/SettingsWebServices.cs`, GetApplicationParametersAsync branches on the administrator flag), which covers
  the administrator case without a group lookup.
- No call reports the role itself, and [GetSavedSearches](GetSavedSearches.md) does not reveal it: a public
  system-wide entry is listed for everyone.

## Notes

- **Administrators and personal entries.** Every rule in the IRSecurity matrix lets administrators through first,
  and `HasAdministrativeRoleAsync` gives them this role. The owner check in `SearchPages.UpdateSearchPageAsync`,
  `DeleteSearchPageAsync` and `CanReadSearchPageAsync` has no such bypass, on purpose
  (commit 0f6cb155): nobody reads, changes or deletes another user's personal entry, and nobody sees it in a list.
  A personal entry disappears with its owner: deleting the user deletes their entries
  (`UserOperations.cs`, `SearchPageStore.DeleteAllByOwnerAsync`). Deleting a user group removes it from every
  entry's sharing list (`UsergroupOperations.cs`, `DeleteSearchGroupsByGroupAsync`).
- **Who is in the group.** The 8.6.105 update created group 105 with the `sysadmin` account and the users named in
  `config/searchadmins.xml` of that day, then deleted the file. Those members stay. Administrators added since are
  not in the group and do not need to be (commit 0f6cb155, 2026-10-14; `HasAdministrativeRoleAsync` was
  a plain membership test before that).
- **The anonymous user** (a session with a negative user id, issued when a call carries no ticket and no ticket
  cookie) can list and read the system-wide entries with `anonymousAccess=true` and nothing else; create, update
  and delete answer `4010`. One exception in order: `DeleteSavedSearch` with id 1 checks the page before the
  session, so an anonymous caller gets `4030` "Advanced search page cannot be renamed or deleted." there.
- **Stored names.** A personal entry is stored under its owner's id followed by the name (`4My searches`), so two
  users can use the same name; `SearchPageDbModel.DisplayName` strips the id again for the answers. Uniqueness is
  per type on the stored name.
- **Page 1, Advanced Search,** is a system-wide `searchPage`. Its update writes only the sharing flags and groups
  (`SearchPageStore.UpdateSearchPageAsync`, the id 1 branch); the name and description sent are ignored, and a
  name other than "advanced search" (case-insensitive) is refused.
- **Existence of an entry is not hidden.** `GetSavedSearch` answers `4041` for an id that does not exist and
  `4030` for one the caller may not see; `UpdateSavedSearch` and `DeleteSavedSearch` likewise tell a personal
  entry ("only the search page owner") from a system-wide one ("only search administrators").
- **The name.** The group is `[Search & Category Administrators]`, and the role covers the system-wide saved
  searches and search pages. No operation checks it for anything else; "Categories" is only the directory
  under the application directory where the XML of `savedSearch` entries is kept (`SearchPages.cs`).
- **Tests:** `TestProjects/WebApiTests/Tests/SavedSearchRoleApiTests.cs` covers the two rules above
  (a search administrator refused on another user's personal entry; an administrator outside group 105 creating a
  system-wide entry).

## Related

- [AdministrativeRoles](AdministrativeRoles.md), all roles at a glance
- the other role pages: [Administrators](AdministratorsRole.md), [User Managers](UserManagersRole.md),
  [Audit Managers](AuditManagersRole.md), [Policy Managers](PolicyManagersRole.md),
  [R&D Managers](RDManagersRole.md), [Library Managers](LibraryManagersRole.md)
- [SavedSearchXmlReference](SavedSearchXmlReference.md), the search parameters XML the entries store
