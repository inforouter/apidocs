# Who may change an administrator's account

A User Manager manages users. An administrator is a user. This page says where the one stops short of the
other.

## The rule

The `sysadmin` account and every member of `[Administrators]` are changed by **administrators only**. A User
Manager, or the manager of the library a local administrator belongs to, may read such an account and may
manage every other user, but may not change the account, act in its name or take its work. Reading is not
guarded; a change is.

## What counts as changing the account

| Action | Operations |
|---|---|
| Name, authentication source, status, type | UpdateUserProfile, ChangeUserStatus, ChangeUserType |
| E-mail, mobile number, preferences | UpdateUserContactInfo, UpdateUserEmail, UpdateUserPreferences |
| Password | ChangeUserPassword |
| Delete | DeleteUser, DeleteUser1 |
| Task redirection: set, remove, reroute | SetUserTaskRedirection, RemoveUserTaskRedirection, RerouteUserTaskRedirection |
| Property set rows on the user | ApplyPropertySetToUser and the row calls for users |
| Taking the account's work | Every Transfer call with an administrator as the from-user: tasks, checkouts, ownerships, subscriptions, memberships, manager roles |

## Who passes, and the exceptions

- An **administrator**: the `sysadmin` account or a member of `[Administrators]`.
- The account **itself**, for what any user may do to their own account (ChangeUserPassword1 with the current
  password, contact details, preferences).
- **Rerouting** an administrator's tasks: also the user those tasks are currently redirected to, who passes
  them on; that recipient is the administrator's own choice.
- **Giving** work to an administrator (a transfer with an administrator as the to-user) is not guarded.
- Two further guards sit beside this one: a non-administrator may not make **themselves** a library manager,
  by appointment or by transfer; and a transfer of group memberships leaves the **role groups** (ids up to
  1000) behind unless an administrator runs it, so nobody acquires a role by inheriting another user's groups.

## What the server answers

`4030` "Access denied. Only administrators can change an administrator's account." The check runs before the
user is looked up by name, so it does not tell whether a name exists. GetUserTaskRedirectionsFrom, a read, is
caught by the same guard for the time being (open item 37 of the role review).

## For developers

- The rule: `IRSecurity.AccessAllowedforAdminFunctionsAsync` with `ChangesTheAccount` and
  `IsAdministratorAccountAsync` (`IRNET/IRSecurity.cs`); the transfer guard in `UserTakeOverOperations`;
  the self-appointment guard in `DomainExtensions.SetDomainManagerAsync`.
- Tests: `AdministratorAccountApiTests`, `TransferOwnershipApiTests`,
  `DomainBatch2ApiTests.AddManagerToDomain_AUserManagerAppointingThemselves_IsRefused`.
- Role pages: [Administrators](../AdministratorsRole.md), [User Managers](../UserManagersRole.md).

## Since

- **9.0 (2026-10-14):** the guard. Before it only the `sysadmin` account itself was protected: a User Manager
  could reset any other administrator's password and sign in as them.
- **9.0.200 (2026-10-28):** rerouting an administrator's tasks joined the guard.
