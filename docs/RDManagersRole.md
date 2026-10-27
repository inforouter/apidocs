# R&D Managers

Group `103`, stored as `[R&D Managers]` (a global group, library id 0), enum value
`enum_IR.AdmistrativeRoles.RDManager`. The role is for records management: defining retention and
disposition schedules and their source authorities, applying schedules to items, freezing them, and
disposing of items whose disposition date has come. It is a system group: `IRSecurity.IsAllowed` adds no
role and no library-manager step to `UpdateGroupMembers` for a group id up to
`IRConstants.LastSystemUserGroupId` (1000), so only the administrator check at the top of
`AccessAllowedforAdminFunctionsAsync` can add or remove its members.

## How the role is checked

The `IRSecurity.IsAllowed` matrix names `RDManager` for seven actions: `AddRDDef`, `UpdateRDDef`,
`DeleteRDDef`, `DisposeDocument`, `SetDifferentRetentionDispostion`,
`AddRemoveRetentionSourceAuthorities` and `TransferToExternalAgency`. Every call site passes
`objectType UNSPECIFIED, objectId 0, localDomainId 0`, and none of the seven sets `allowSelfAction` or
`allowLibManagers`. So the check is, in order: administrators (`threadInfo.IsAdministrator()`: the
`sysadmin` account or a member of `[Administrators]`) pass; the administrator-account guard does not
apply (the object is never a user); then membership of group 103; library managers never pass.

A refusal is `errorCode="4030"` with the message *"Access denied. This action is restricted to the
following roles: The system administrator, R&D managers"* (`Messages.AccessDenied`,
`ActionRestrictedToFollowingRoles`, `TheSystemAdministrator`, `RdManagers`).

The role is used in two ways:

- **Defining** (schedules, source authorities) and **disposing**: the role is asked directly
  (`RetentionAndDispositionOperations.AddNewAsync`, `UpdateAsync`, `DeleteAsync`,
  `RetentionSourceAuthoritiesOperations`, `DocumentRecycleOperation.DocumentDeleteCheckAsync`,
  `FolderRecycleOperation.FolderDeleteCheck`).
- **Applying, removing, freezing, unfreezing** a schedule on an item: the `RetentionPeriodChange` right on
  the item is asked first; only when that answer is a `4030` does
  `RetentionAndDispositionOperations.MayChangeRetentionAsync` ask the role (as
  `SetDifferentRetentionDispostion`) and let it stand in. Any other failure of the right check (item not
  found `4041`, anonymous caller `4010`) is returned as it is.

The `RetentionPeriodChange` right is a library policy (`IRBase/Models/DomainPolicies.cs`): by default it
goes to the item's owner, the library's managers, and anyone with CHANGE or Full Control on the item;
anonymous never. `IRSecurity.AccessAllowedAsync` has no administrator bypass of its own, so an
administrator without the right is let through by the role step too.

## What the role can do

Administrators always pass every row below.

**Reaching the item comes first.** Every call that takes a path looks the document or folder up before
any right or role is asked (`InfoRouter.GetDocumentByPathAsync`, `GetFolderByPathAsync`,
`DocumentLoadOperation.GetDocumentAsync`, `FolderOperations.GetFolderAsync`). The lookup refuses with
`4041` ("Document not found." / "The folder has either been deleted or is not accessible.") unless the
item's library is in `DomainsStore.GetViewableLibraryListAsync` for the caller: a library the caller is a
member of (directly or through a group), or one that allows anonymous access. The R&D Manager role is not
in that list, so **the role alone does not reach an item in a library the manager is not a member of**.
That is by design: a library that keeps no records under retention has nothing for the role to see, and a
library that does is opened to the role by its manager, who adds the `[R&D Managers]` group to the
library's members with [AddUserGroupAsDomainMember](AddUserGroupAsDomainMember.md). Inside a library the
manager or the group is a member of, the role stands in for the missing right on any item, whatever the
item's own access list says.

### Defining schedules and source authorities (role only)

| Action | Web service calls | Who else may do it | Conditions |
|---|---|---|---|
| Create a schedule | [CreateRandDSchedule](CreateRandDSchedule.md) | nobody else | `AddRDDef`. The schedule XML is validated (`4000`) before the role is asked. A duplicate name is refused. |
| Change a schedule | [UpdateRandDSchedule](UpdateRandDSchedule.md) | nobody else | `UpdateRDDef`, asked before the schedule is looked up (`4041` after). With `ApplyToExistingDocumentFolders` the dates of every item using the schedule are recalculated and its open disposition tasks dropped. |
| Delete a schedule | [DeleteRandDSchedule](DeleteRandDSchedule.md), [DeleteRandDSchedule1](DeleteRandDSchedule1.md) | nobody else | `DeleteRDDef`, asked first. Id 0 is `4000`, an unknown id `4041`. A schedule still applied to items is refused with the counts unless `forceDelete` (DeleteRandDSchedule sends false); forced, the schedule is cleared from every item and their disposition tasks dropped. |
| Create, rename, delete a source authority | [CreateRetentionSourceAuthority](CreateRetentionSourceAuthority.md), [UpdateRetentionSourceAuthority](UpdateRetentionSourceAuthority.md), [DeleteRetentionSourceAuthority](DeleteRetentionSourceAuthority.md) | nobody else | `AddRemoveRetentionSourceAuthorities`. Empty or over-long names are `4000` before the role is asked. Delete is refused while a schedule quotes the authority; rename follows onto the schedules that quote it. |

### Applying schedules to items (right on the item or the role)

"Who else" in this table means: anyone who holds `RetentionPeriodChange` on the item, which by default is
its owner, the managers of its library, and users with CHANGE or Full Control on it.

| Action | Web service calls | Who else may do it | Conditions |
|---|---|---|---|
| Set or remove a document's schedule | [SetDocumentRandDSchedule](SetDocumentRandDSchedule.md), [RemoveDocumentRandDSchedule](RemoveDocumentRandDSchedule.md) | holders of the right on the document | Member of the library (see above). Shortcuts (`.lnk`) take no schedule (`4000`). An unknown schedule id is `4041`. Removing clears the freeze with it. |
| Set or remove a folder's schedule | [SetFolderRandDSchedule](SetFolderRandDSchedule.md), [RemoveFolderRandDSchedule](RemoveFolderRandDSchedule.md) | holders of the right on the folder | Checked once on the top folder (`FolderExtensions.SetRetentionAndDispositionAsync`). With `includeFolders` the subfolders are written with no further check; with `includeDocuments` each document goes through the document rule again and a refused document is listed in the answer, not returned as an error. Removing a folder's schedule clears its freeze. |
| Freeze or unfreeze | [SetRdFreezeFlag](SetRdFreezeFlag.md) | holders of the right on the document or folder | The item must carry a schedule (`4000`). A freeze cannot be lifted while the parent folder is frozen. On a folder the check runs on the folder, then on every subfolder and document below it; freezing a folder needs every item below it frozen; per-item refusals come back in the answer with `errorCode="2070"` (multi-status). |
| Change a document's type when the type carries a default schedule | [UpdateDocumentType](UpdateDocumentType.md) | holders of the right on the document | The type change itself needs `ChangeDocumentType` (set) or `SetDocumentType` (remove) on the document, with no role fallback. Setting a type onto a document with no schedule applies the type's default schedule through the document rule above; removing a type whose default schedule is the one on the document clears it through the same rule, and a refusal stops the removal (`DocumentExtensions.RemoveDocumentTypeAsync`). |

### Disposing of items (role and the delete right)

| Action | Web service calls | Who else may do it | Conditions |
|---|---|---|---|
| Dispose of a document | [DisposeItem](DisposeItem.md) | nobody else | `DocumentDeleteCheckAsync` with the dispose flag: frozen, under permanent retention or retention not yet expired are `4000` before the role; a document with no disposition date is `4000` ("A disposition date has not been assigned to this document.") and the role is never asked; with one, the role (`DisposeDocument`, `4030`), then a Transfer-to-agency schedule (`4000`), then a date still in the future (`4000`). After that: form templates with rendered copies, checked out or in a workflow are refused; folder rules that disallow deletion are `4030`; and the caller needs the `DocumentDelete` right on the document (`4030`). The document goes to the caller's recycle bin. |
| Record a transfer to an external agency | [TransferToExternalAgency](TransferToExternalAgency.md) | nobody else | The role is asked first, before the path is looked up (`DocumentServices.TransferToExternalAgencyAsync`, `IrAdminAction.TransferToExternalAgency`, `4030`), then the `RetentionPeriodChange` right on the item (`4030`). The item must carry an unfrozen schedule whose disposition type is Transfer, with a disposition date that has arrived and a status row from the daily job; each failing condition is `4000`. For a folder, `includeSubFolders` and `includeDocuments` walk the tree and every refusal is one entry in the answer, which is `2070` when there is at least one. Recording the transfer is what lets the document's Transfer task be completed. |
| Dispose of a folder | [DisposeItem](DisposeItem.md) | nobody else | `FolderOperations.DisposeDocumentsRecursivelyAsync`: the folder's documents are listed with the `FolderList` right (a folder the caller cannot list is logged and skipped), each document goes through the document rule above, subfolders are walked without a list check, then the folder itself through `FolderDeleteCheck`: root folders, folder rules, workflow folders, freeze, retention, the role (`DisposeDocument`), Transfer type, future date, the tree checks (checked-out, workflow, retention and future dispositions below), then the `FolderDelete` right. Every refusal is one entry in the answer; the answer is `2070` when some item was refused. |

### Reading (any signed-in user)

| Action | Web service calls | Who else may do it | Conditions |
|---|---|---|---|
| List and read schedules | [GetRandDSchedules](GetRandDSchedules.md), [GetRandDScheduleInfo](GetRandDScheduleInfo.md) | anyone signed in | Only `IsAuthenticatedUser()` (`RetentionServices`); anonymous is `4010`. No role. |
| List source authorities | [GetRetentionSourceAuthorities](GetRetentionSourceAuthorities.md) | anyone signed in | Same. |
| Read an item's schedule, freeze log, applied-schedule log | [GetDocumentRandDSchedule](GetDocumentRandDSchedule.md), [GetFolderRandDSchedule](GetFolderRandDSchedule.md), [GetRdFreezeLogs](GetRdFreezeLogs.md), [GetAppliedRDScheduleLogs](GetAppliedRDScheduleLogs.md) | anyone who can reach the item | Only the path lookup (library membership or anonymous library); no right on the item is asked. |

## What the role cannot do

| Action | Web service calls | Who can | Error returned |
|---|---|---|---|
| Set or clear a cut-off date | [SetDocumentCutoffDate](SetDocumentCutoffDate.md), [RemoveDocumentCutoffDate](RemoveDocumentCutoffDate.md), [SetFolderCutoffDate](SetFolderCutoffDate.md), [RemoveFolderCutoffDate](RemoveFolderCutoffDate.md) | holders of `RetentionPeriodChange` on the item only; the role does not stand in (`DocumentSetCutOffDateOperation`, `FolderSetCutOffDateOPeration`) | `4030`, the library-policy message, e.g. "Insufficient rights. This action can only be performed by library members with appropriate rights." |
| Delete a document or folder | [DeleteDocument](DeleteDocument.md), [DeleteFolder](DeleteFolder.md) | holders of `DocumentDelete` / `FolderDelete` on the item | `4030` from the right check. An item with a disposition date is `4000` for everyone: "This document is marked for disposition. Please use the dispose function instead." |
| Dispose without the delete right | [DisposeItem](DisposeItem.md) | nobody: the role and the delete right are both needed | `4030` from the `DocumentDelete` / `FolderDelete` check, after the role passed |
| Dispose an item with no disposition date | [DisposeItem](DisposeItem.md) | nobody, administrators included | `4000` "A disposition date has not been assigned to this document." |
| Read the disposition log | [GetDispositionLog](GetDispositionLog.md) | Audit Managers; a library's managers when the filter names that library (`LogOperations.IsLogAccessAllowed`, `ViewAuditLogs`) | `4030` naming the system administrator, library managers and Audit Managers |
| Purge disposed items from the recycle bin, or restore items from another user's bin | [PurgeRecycleBinItem](PurgeRecycleBinItem.md), [RestoreRecycleBinItem](RestoreRecycleBinItem.md) | Administrators (`RecycleBinOperations`, `IsAdministrator()`) | `4030` "Only the system administrator can perform this operation" |
| Define document types and their default schedules | [CreateDocumentTypeDef](CreateDocumentTypeDef.md), [CreateDocumentTypeDef1](CreateDocumentTypeDef1.md), [UpdateDocumentTypeDef](UpdateDocumentTypeDef.md), [UpdateDocumentTypeDef1](UpdateDocumentTypeDef1.md), [DeleteDocumentTypeDef](DeleteDocumentTypeDef.md) | Administrators (`DocumentTypeOperations`, `IsAdministrator()`) | `4030` "Only the system administrator can perform this operation" |
| Change the `RetentionPeriodChange` policy of a library | [SetDomainPolicies](SetDomainPolicies.md) | Policy Managers; the library's managers when *Allow library managers to edit policies* is on | `4030` |
| List libraries they are not a member of | [GetLibrariesForAdministration](GetLibrariesForAdministration.md) | User Managers, Policy Managers (every library); library managers (theirs) | Not an error: the answer holds only the libraries the caller manages, usually none (`UserOperations.GetLibraryListForAdministrationAsync`). [GetDomains](GetDomains.md) lists the member libraries. |
| Add or remove members of `[R&D Managers]` | [AddUsergroupMember](AddUsergroupMember.md), [RemoveUsergroupMember](RemoveUsergroupMember.md) | Administrators | `4030` "Access denied. This action is restricted to the following roles: The system administrator" |

## Finding out whether the signed-in user has this role

- [GetGroupMembershipsOfUser](GetGroupMembershipsOfUser.md) with the caller's own user name: the check is
  `ListingGroupMembershipOfUser`, which allows self (`IRSecurity.IsAllowed`, `allowSelfAction`), so it
  always answers for yourself. A `GroupID` of `103` in the answer is this role; `104` is Administrators,
  who pass every R&D check without being in group 103.
- There is no R&D-specific call that reveals the role. [GetRandDSchedules](GetRandDSchedules.md) answers
  every signed-in user, so a successful answer does not mean the caller holds the role.
- [GetLibrariesForAdministration](GetLibrariesForAdministration.md) says nothing about this role: it answers
  an R&D Manager with the libraries they manage, like any other user.

## Notes

- **Which items the role reaches, and why.** The role is defined system-wide (every call site passes
  `localDomainId 0`), but every item call looks the item up first, and the lookup admits only libraries the
  caller is a member of or that allow anonymous access. This is intended (confirmed 2026-10-22): a library
  whose content needs no records management has no reason to show its documents and folders to R&D
  Managers, and a library that does is opened by its manager adding the `[R&D Managers]` group as a member
  ([AddUserGroupAsDomainMember](AddUserGroupAsDomainMember.md)); from then on every member of the group
  reaches its items and the role supplies the rights. In a library that allows anonymous access an R&D
  Manager who is not a member reaches the item anyway: the right check then fails with `4030` ("library
  members with appropriate rights"), and `MayChangeRetentionAsync` lets the role replace that `4030`. In a
  members-only library the same manager gets `4041` from the lookup. Control Panel pages that offer R&D
  actions per item should list the libraries from [GetDomains](GetDomains.md) (member libraries, which
  include the ones the group was added to), not assume every library; "document not found" for an R&D
  Manager in a library they expect to work in means the library's manager has not added the group.
- **`SetDifferentRetentionDispostion` is live.** It is the action `MayChangeRetentionAsync`
  (`RetentionAndDispositionOperations.cs`) asks for whenever the role stands in for the missing right:
  document and folder schedule, document and folder freeze, and the schedule side of `UpdateDocumentType`.
  Its name is from the old rule (a document schedule other than its folder's); that rule was replaced
  on 2026-10-14 with "the right on the item or the role" for every apply, remove, freeze and unfreeze,
  checked in `RetentionBatch2ApiTests.ApplyingAndFreezing_TakeTheRightOnTheItem_OrTheRdManagerRole`.
- **Disposition tasks and e-mails from the daily job.** `DispositionCheck.GetRdTaskOwner` reads the
  members of group 103 (`PlayerStore.GetUsergroupMembersAsync`, ordered by first name, then last name),
  passes them to `TaskOperations.AutomaticallyChooseTaskUsersAsync` with a required count of 100, and takes
  the first user in the result whose status is not Disabled. With 100 members or fewer the chooser returns
  the list as it is, so the same member (the first by name who is not disabled) receives every task and
  every notice; only with more than 100 members are they shuffled and ranked by open-task count. When the
  group has no usable member the `sysadmin` account is used. The job does not check that the chosen
  member reaches the document's library: a schedule applied in a library the `[R&D Managers]` group is not
  a member of yields a task its assignee cannot complete, so the group is added before schedules are
  applied there. For a document the job creates the task
  (requirement Dispose or Transfer, due in three days, assigned by SYSTEM, failing over to `sysadmin` if the
  assignee cannot be resolved) when the schedule has `CreateTask`, and sends the DOCUMENT_DISPOSE notice to
  the same user when it has `SendEmail`; for a folder no task is created, only the FOLDERDISPOSE notice when
  `SendEmail` is on.
- **Order of checks when creating.** `CreateRandDSchedule` validates the schedule XML before asking the role,
  and the source-authority calls validate the name first, so a caller without the role sees `4000` for bad
  input and `4030` for good input. Nothing about existing schedules or authorities is revealed before the
  role check (`UpdateRandDSchedule` and `DeleteRandDSchedule` ask the role first; the authority existence
  checks come after it).
- **Library managers** hold no R&D right as such: they pass the item calls only because the default
  `RetentionPeriodChange` policy gives them the right on items of their library, and they are refused by
  every define and dispose call.
- **The disposition log is an audit log.** An R&D Manager who disposes of items cannot read
  `GetDispositionLog` afterwards unless they are also an Audit Manager or a manager of the library named in
  the filter. The per-item logs they can read are [GetRdFreezeLogs](GetRdFreezeLogs.md) and
  [GetAppliedRDScheduleLogs](GetAppliedRDScheduleLogs.md).

## Related

- [AdministrativeRoles](AdministrativeRoles.md), all roles at a glance
- the other role pages: [Administrators](AdministratorsRole.md), [User Managers](UserManagersRole.md),
  [Audit Managers](AuditManagersRole.md), [Policy Managers](PolicyManagersRole.md),
  [Search & Category Administrators](SearchAdministratorsRole.md), [Library Managers](LibraryManagersRole.md)
