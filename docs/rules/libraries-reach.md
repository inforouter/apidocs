# Which libraries a caller can reach

Almost every refusal that reads "not found" for a library, folder or document comes from one rule. This page
says what it is.

## The rule

A caller reaches a library if they are a **member** of it, directly or through a global group that is, or if
the library **allows anonymous access**. On top of that, for administration, the libraries are reachable by
**administrators, User Managers, Policy Managers and the library's own managers**, members or not. Nobody
else reaches it, and what cannot be reached does not exist for the caller: the answer is `4041`, not `4030`, so
the name of a library is not confirmed to someone outside it.

## Who reaches what

| Caller | Reaches |
|---|---|
| A member | The library |
| Anyone, signed in or not | A library that allows anonymous access |
| Administrators, User Managers, Policy Managers | Every library, by name or id |
| A library manager | The libraries they manage |
| Audit Managers | Not by this rule; but a library path filter on the date-range logs is resolved for them by name |
| R&D Managers | Not by this rule, by design: the library's manager adds `[R&D Managers]` as a member where records management is wanted |

A **hidden** library is hidden from listings, not from reach: its members and the administrators above still
open it by name.

## Membership

- Whoever **creates** a library is its member and its manager, without being added. A library made from a
  model library ([CreateDomainFromTemplate](../CreateDomainFromTemplate.md)) takes the model's members as well.
- A library **must keep a member**: removing the last one is refused with `4000`, because a library nobody is a
  member of cannot be reached by anyone, a system administrator included, and no operation on it would work
  again. A member group counts only for the people in it.
- A **manager** must be a member; appointing one who is not is refused. A non-administrator may not appoint
  themselves.
- A **local user** belongs to one library and is managed by its managers; a global user belongs to none and is
  managed by User Managers.
- Adding and removing members and managers: administrators, User Managers, and the library's managers for the
  users local to it. Members of the administrative role groups are changed by administrators only.

## Deleting a library

[DeleteDomain](../DeleteDomain.md) is irreversible and does not go through the recycle bin: it stops running
workflows, deletes workflow definitions, recycles the folders and documents, deletes the local groups and users,
and removes the library. A document the caller may not delete under the library's policies (an owner-only
delete, say) stops it with "the library contains documents"; the caller must be able to delete everything in it.

## For developers

- The rule: `DomainOperations.MayReachAsync`, used by the lookups by name and by id;
  `DomainsStore.GetViewableLibraryListAsync` for the item lookups (`DocumentLoadOperation.GetDocumentAsync`,
  `FolderOperations.GetFolderAsync`).
- Tests: `DomainBatchApiTests`, `DomainBatch2ApiTests`, `GetLibrariesForAdministrationApiTests`.
- Pages: [GetDomains](../GetDomains.md), [GetLibrariesForAdministration](../GetLibrariesForAdministration.md),
  [CreateDomain](../CreateDomain.md), [Library Managers](../LibraryManagersRole.md).

## Since

- **9.0 (2026-10-21):** one reach rule for lookups by name and by id. Before, the by-name lookup had no
  administrator bypass, so a non-member administrator got "Library not found" filtering logs or managing the
  library by name.
