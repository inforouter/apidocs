# Administrative Roles

infoRouter has six built-in **administrative role groups**. A user holds a role by being a member of its
group. Each role has its own page with the web service calls it unlocks, the related calls it does **not**
unlock, and notes on how the checks run. This page is the overview.

The roles are the values of `enum_IR.AdmistrativeRoles` (`IRBase\IRBaseEnum.cs`). The server checks them in
`IRNET\IRSecurity.cs`; the pages describe those checks as the server makes them, read from the code.

## The roles

| Group id | Group name | Page | In short |
|---:|---|---|---|
| `104` | `[Administrators]` | [Administrators](AdministratorsRole.md) | Everything. Passes every role check, plus the actions that are administrators only. |
| `100` | `[User Managers]` | [User Managers](UserManagersRole.md) | Users, user groups, library membership and managers, user transfers. Sees every library. |
| `101` | `[Audit Managers]` | [Audit Managers](AuditManagersRole.md) | Audit logs, licence, server, warehouse and server-log status. |
| `102` | `[Policy Managers]` | [Policy Managers](PolicyManagersRole.md) | Application settings and library policies. Sees every library. |
| `103` | `[R&D Managers]` | [R&D Managers](RDManagersRole.md) | Retention and disposition schedules, disposition, freezing. |
| `105` | `[Search & Category Administrators]` | [Search & Category Administrators](SearchAdministratorsRole.md) | System-wide saved searches and search pages. |
| - | - | [Library Managers](LibraryManagersRole.md) | Not a group: a user appointed manager of one library. Acts on that library and on the users and groups local to it. |

- The six groups are system groups: they belong to no library and their ids are fixed. Group ids up to
  `IRConstants.LastSystemUserGroupId` (1000) are system groups.
- **Only Administrators can add or remove members of these groups.** A User Manager cannot make someone a
  User Manager, and a transfer of group memberships leaves these groups behind unless an administrator runs it.
- The `sysadmin` account always counts as an administrator and cannot be removed from `[Administrators]`.
- Holding several roles combines what they allow.

## How the server decides

For an administrative action the server allows the call when **any** of these is true, in this order:

1. The caller is an administrator: the `sysadmin` account or a member of `[Administrators]`.
2. The action allows **self-service** and the caller is acting on their own account.
3. The caller is in one of the role groups the action requires.
4. The action allows **library managers** and the caller manages the library the action is about. A user or
   group belongs to a library only when it is local to that library: for a global user or group, and for
   application-wide actions, there is no library and this step never passes.

Before step 2, an action that **changes an account** (profile, preferences, password, e-mail, delete, task
redirections, property set rows) is refused for a non-administrator when the account is an administrator's.

A refusal is `errorCode="4030"`, and the message names the roles that would have been allowed. Search
administration is the exception: it is checked by group membership alone (administrators pass too), not
through this list.

**Reaching a library by name.** The library calls that take a `DomainName` first look the library up, and a
library the caller cannot reach is `4041` "library not found". A library is reachable by its members, by
anyone where it allows anonymous access, and by whoever may administer it: Administrators, User Managers and
Policy Managers for every library, and a library's own managers for it. Audit Managers are not on that list,
but the audit logs resolve a path filter's library by name alone, so they may filter by any library. R&D
Managers are not on it either, by design: a library that needs records management gets the `[R&D Managers]`
group added as a member by its manager. See [R&D Managers](RDManagersRole.md).

## Finding out which roles the signed-in user has

There is no single "my roles" call. Use these:

- [GetGroupMembershipsOfUser](GetGroupMembershipsOfUser.md) with the caller's own name (always allowed for
  yourself): the `GroupID` values `100` to `105` in the answer are the roles held.
- [getApplicationParameters](getApplicationParameters.md) tells you whether the caller is an administrator:
  only administrators get the extended block.
- [GetManagedDomainsByUser](GetManagedDomainsByUser.md) with the caller's own name, or an empty name, lists
  the libraries the caller manages.
- [GetLibrariesForAdministration](GetLibrariesForAdministration.md) lists the libraries the caller may
  administer: every library for Administrators, User Managers and Policy Managers, the managed ones for a
  library manager, nothing for anyone else.

## Behaviour worth knowing

- **Administrators are not library members.** The item-level rights (documents, folders, access lists) have no
  administrator bypass: an administrator who is not a member of a library gets `4030` on its content, and
  [GetDomains](GetDomains.md) lists only member libraries. See [Administrators](AdministratorsRole.md).
- **R&D Managers reach only libraries they are a member of.** The role is system-wide, but an R&D Manager
  opens an item only in a library that lists them, or the `[R&D Managers]` group, as a member. A library that
  needs records management gets the group added by its manager
  ([AddUserGroupAsDomainMember](AddUserGroupAsDomainMember.md)); elsewhere the role has nothing to see. See
  [R&D Managers](RDManagersRole.md). The same reach rule applies to the per-item audit logs; see
  [Audit Managers](AuditManagersRole.md). (Audit Managers may filter the date-range logs by any library.)

## Notes for the Control Panel

- **Show or hide by role, then let the server decide.** A library manager's rights depend on the library:
  the same call can succeed for one library and return `4030` for another. Read `errorCode` rather than
  assuming.
- **Self-service** calls work for every signed-in user on their own account, with no role. The role pages
  mark them.
- **Which libraries to offer.** [GetDomains](GetDomains.md) lists only the libraries the caller belongs to,
  whatever their role. A page that manages users, memberships, managers or policies should list
  [GetLibrariesForAdministration](GetLibrariesForAdministration.md) instead.
