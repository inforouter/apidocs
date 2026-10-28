# A library made from a model library

A law firm opening a case or a team starting a project keeps a model library they never work in, and makes
each new library from it. This page says what comes across, what does not, and what happens to the access lists.

## The rule

[CreateDomainFromTemplate](../CreateDomainFromTemplate.md) makes a new library with the model's **settings and
rules, action policies, property sets, members, managers and local groups, the root folder's own settings and
access list, the folder tree with every folder's settings and list, and the documents** with all their versions.
The model is read, never written. The caller, a system administrator, is a member and a manager of the new
library whatever else comes across, because a library must keep a member.

## What comes across

| Item | Notes |
|---|---|
| Library settings | Anonymous and hidden flags and the welcome message unless the call sends its own; the library rules of GetDomainPolicies |
| Policies | Every action policy |
| Property sets listed on the library | So the copied rows have their sets |
| Members and managers | Every user and global group that is a member; every manager. `IncludeMembers=false` leaves the caller alone |
| Local groups | Made again in the new library, same name, same members, **new id** |
| Root folder | Folder rules, views, description, classification, file type restrictions, Connect preferences, subscriptions, property set rows, and its own access list |
| Folders | Each with the same, as Copy copies a folder |
| Documents | Each with every version, keywords, description, publishing rules, property set rows and access list, as Copy copies a document. `IncludeDocuments=false` gives a skeleton |

## What stays behind

Retention schedules, cut-off dates and freezes (a new case gets its own); workflow definitions; local users of
the model (a local user belongs to one library); checkouts, tasks, favorites, downloads, associations, saved
searches, portals; the archive flag (the new library is online even when the model is archived).

## Access lists

Access lists are shared rows: the copy points at the model's list, as a copied folder does, and changing the
copy's list later makes a new list for the copy and leaves the model's alone. The one list that cannot be shared
is one naming a group **local to the model**, because in another library that group counts for nothing. Every
such list is written again for the new library with the new library's copy of the group in its place; with
`IncludeMembers=false` the entry is dropped.

## When something is refused

The library itself is one transaction. The folders and documents are copied one by one, so one refused item
(an offline document, say) is logged and the rest goes on: the answer is `2070` MultiStatus with the `<domain>`
element and one `<log>` entry per refused item. The library exists; delete it with
[DeleteDomain](../DeleteDomain.md) for an all-or-nothing outcome, or keep it and add the missing item by hand.

## For developers

- Operation: [CreateDomainFromTemplate](../CreateDomainFromTemplate.md).
- The rule: `DomainCopyOperation` (`IRNET/Operations/DomainCopyOperation.cs`), on top of
  `FolderCopyOperation` and `DocumentCopyOperation`; the access list rewrite is its last pass.
- Tests: `CreateDomainFromTemplateApiTests` (fifteen tests, including the rewritten list proven by the copied
  member creating a folder through it).

## Since

- **9.0.200 (2026-10-28):** the operation. 8.7's control panel had *Use another library as a template*, which
  copied policies, folders and documents only: no members, no groups, and lists naming a local group silently
  granted nothing in the new library.
