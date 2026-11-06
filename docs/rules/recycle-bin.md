# What happens to a deleted document or folder

Deleting in infoRouter destroys nothing at first. This page follows a deleted item through every stage, from
the delete to the moment it is gone, and says who can see it, bring it back or remove it at each one.

## The rule

There are two ways to take a document or folder out of a library, and they end in different places. An
ordinary **delete** sends it to a recycle bin, from which it can come back. A **dispose**, the deliberate end
of a record under its retention schedule, sends it **straight to the purge queue**, from which nothing comes
back. See [Delete or dispose](#delete-or-dispose).

A deleted document or folder goes to the **recycle bin of the user who deleted it**. That user sees it there
and can restore it. When the user's recycle bin is **emptied**, the item moves to the **system recycle bin**:
the user no longer sees it, but a system administrator still finds it, can restore it, or can purge it.
Emptying happens when the user empties their bin, when an administrator empties every user's bin, after a
set number of months (if the setting is on), or when the user is deleted. Only a **purge** removes an item
for good. A purge puts the item in the **purge queue**. From there **there is no way back**: the purge job
removes it from the database and from the warehouse, one item after another, within minutes. An item gets
into the purge queue in three ways: an administrator purges it, the system recycle bin purges itself after a
set number of months (if that setting is on), or an R&D Manager disposes of a document or folder whose
disposition is due.

## The stages

| Stage | `RecycledItemStatusId` | Who sees it | Who can restore it | How it leaves |
|---|---|---|---|---|
| In use | – | Whoever has the rights | – | Deleted ([DeleteDocument](../DeleteDocument.md), [DeleteFolder](../DeleteFolder.md)) |
| **User's recycle bin** | `0` | The user ([GetRecycleBinContent](../GetRecycleBinContent.md)); administrators ([SearchRecycledItems1](../SearchRecycledItems1.md)) | The user who deleted it; administrators | Restored, emptied, or purged |
| **System recycle bin** | `1` | Administrators only ([SearchRecycledItems1](../SearchRecycledItems1.md)) | Administrators only | Restored, or purged |
| **Purge queue** | `2` (not listed anywhere) | Nobody | Nobody | Removed by the purge job |
| Gone | – | Only the delete log remembers it | – | – |

Emptying and purging are different things. **Emptying** only moves items from a user's recycle bin to the
system recycle bin and frees no disk space. **Purging** destroys the item and frees the space.

## Deleting a document

[DeleteDocument](../DeleteDocument.md) moves the document into the caller's recycle bin. The caller's recycle
bin is a library of its own, `~RECYCLE_<id>`, created the first time the user deletes something. The document
keeps its versions, properties and history. A shortcut that is deleted is not logged.

The delete is refused when:

| The document | Answer |
|---|---|
| Is checked out, or its upload has not finished | `4230` |
| Is in a workflow | `4230` |
| Has a frozen retention schedule | `4000` |
| Is under permanent retention, or under temporary retention that has not ended | `4000` |
| Has a disposition date (it must be disposed of, not deleted; see [Disposal](#disposal)) | `4000` |
| Has open tasks | `4000` |
| Is a form template that documents were made from | `4000` |
| Is in a folder whose rules disallow document deletes | `4030` |
| Needs the `DocumentDelete` right under the library's policies, and the caller lacks it | `4030` |

The checks are made again inside the transaction that moves the document. A document that was checked out,
sent to a workflow or moved after the checks stays where it is.

## Deleting a folder

[DeleteFolder](../DeleteFolder.md) moves the folder, with everything in it, into the caller's recycle bin as
**one item**: the folder is restored or purged as a whole. The caller needs the `FolderDelete` right on the
folder. The rights on each document inside are not asked, but the state of everything inside is:

| The folder | Answer |
|---|---|
| Is a library's top level (use [DeleteDomain](../DeleteDomain.md), which does not use the recycle bin) | `4000` |
| Has folder rules that disallow folder deletes, or its parent has | `4030` |
| Disallows document deletes, or a folder under it does | `4000` |
| Is part of a workflow, or a folder under it is | `4000` |
| Holds a checked-out document, or a document in a workflow, anywhere below | `4000` |
| Is, or holds anything that is, under retention, frozen, or with a disposition date | `4000` |
| Is already in a recycle bin | `4000` |
| The caller lacks `FolderDelete` | `4030` |

## The user's recycle bin

- [GetRecycleBinContent](../GetRecycleBinContent.md) lists what the caller deleted that is still in their
  recycle bin. Each item has a **handler**: `D` and the document id, or `F` and the folder id.
- The user restores an item with [RestoreRecycleBinItem](../RestoreRecycleBinItem.md) (see
  [Restoring](#restoring)).
- A user cannot purge. A user who wants an item gone for good asks an administrator; a document whose
  disposition is due is disposed of by an R&D Manager (see [Disposal](#disposal)).

## Emptying

Emptying moves every item still in a user's recycle bin to the system recycle bin and records the date it was
emptied. Nothing is destroyed. There are five ways:

| How | Who | Which bins |
|---|---|---|
| [EmptyRecycleBin](../EmptyRecycleBin.md) | Any signed-in user | Their own |
| [EmptyUserRecycleBin](../EmptyUserRecycleBin.md) | System administrators | One user's, named; answers the counts and the total size |
| [EmptyAllUserRecycleBins](../EmptyAllUserRecycleBins.md) | System administrators | Every user's, one after another |
| The monthly move (setting `MoveUsersRecycleBinToSystemRecycleBinIn`) | The daily job | Every item deleted more than that many months ago |
| Deleting the user ([DeleteUser](../DeleteUser.md)) | Whoever deletes the user | That user's |

An administrator empties every user's recycle bin to **start the clock of the automatic purge**: the system
recycle bin's setting counts from the date an item was emptied, not the date it was deleted. To free disk space
now, the items are then purged.

Each item moves in a transaction of its own, together with its delete-log entries, so an emptying that is cut
off leaves every item either moved or untouched. Running it again carries on with what is left.

## The system recycle bin and searching it

The system recycle bin is not a place a user can open. It is every recycled item in the
"system recycle bin" state, and only system administrators search it:

- [SearchRecycledItems1](../SearchRecycledItems1.md) answers a page at a time, sorted (`DateDeleted`, `Name`,
  `Size`, `OriginalLocation`, `DeletedBy`, `RecycleStatus`, `DateEmptied`), with `totalCount` for the whole
  search. [SearchRecycledItems](../SearchRecycledItems.md) answers every match at once.
- **Where they look.** [SearchRecycledItems1](../SearchRecycledItems1.md) takes `searchIn`: `0` or empty
  searches everywhere, the users' recycle bins and the system recycle bin together; `1` the system recycle bin
  only; `2` the users' recycle bins only. [SearchRecycledItems](../SearchRecycledItems.md) always searches both.
  So to purge only what has been emptied, search with `searchIn=1` and purge each result. 8.7 did this in its
  user interface by opening the system recycle bin as a library; 9.0 does it with the parameter.
- Each result carries `RecycledItemStatusId` (`0` user's, `1` system); the date an item was emptied can be
  sorted on (`DateEmptied`) but is not in the answer. Items in the purge queue are never listed, whatever
  `searchIn` says.
- The filters are the name (exact, or with `*` for any run of characters), the deletion date range, the size
  range and who deleted it, and on [SearchRecycledItems1](../SearchRecycledItems1.md) where it was deleted
  from: `path=/Accounting/` for a library, `path=/Accounting/Invoices` for a folder and everything below it.
  A library is matched on the library itself, a folder on the item's recorded `DeletePath`, so items from a
  library deleted afterwards can still be found. Leaving them all out lists everything.
- The handler of each result restores ([RestoreRecycleBinItem](../RestoreRecycleBinItem.md)) or purges
  ([PurgeRecycleBinItem](../PurgeRecycleBinItem.md)) the item.

## Restoring

[RestoreRecycleBinItem](../RestoreRecycleBinItem.md) puts an item back in its original folder, or in a folder
the caller names.

- **Who:** a system administrator, any item in either bin. Any other user, an item that is still in **their
  own** recycle bin. Once an item has been emptied into the system recycle bin, the user who deleted it is
  refused with `4030`; only an administrator brings it back. The check is made again inside the restore's
  transaction, so an item emptied while the user's restore runs stays in the system recycle bin.
- The caller needs the right to create a document (or a folder) in the folder it comes back to. A folder that
  no longer exists is refused with `4000`.
- An item that was taking its folder's access list takes the list of the folder it is restored into. An item
  with a list of its own keeps it.
- An item in the purge queue cannot be restored: `4000`, the same answer as an item already restored.

## Purging

A purge puts an item in the **purge queue**. From that moment it is gone as far as everyone is concerned: no
list shows it and nothing restores it. There are three ways in:

| How | Who | What |
|---|---|---|
| [PurgeRecycleBinItem](../PurgeRecycleBinItem.md) | System administrators | One item, from a user's recycle bin or the system recycle bin |
| The automatic purge (setting `SystemRecycleBinAutoPurgeOption`) | The daily job | Every item emptied into the system recycle bin more than that many months ago |
| [DisposeItem](../DisposeItem.md) | R&D Managers | A document or folder whose disposition is due, without going through a recycle bin (see [Disposal](#disposal)) |

**The purge job** then removes the queued items for real:

- It runs **every five minutes** and takes up to **1,000 items** a run, oldest first. An administrator can also
  run it at once ([RunMaintenanceJob](../RunMaintenanceJob.md), job `14`).
- Each document is purged in **one transaction**: every row that belongs to it goes (versions, properties,
  keywords, tags, associations, subscriptions, favorites, tasks, workflow steps, shortcuts pointing at it,
  queued Connect work), and its **files are deleted from the warehouse last**, inside the same transaction. If
  the file delete fails, nothing is removed and the document stays in the queue for the next run.
- A folder is purged from the bottom up, up to 1,000 of its own documents a run. A large folder is emptied
  over several runs, and the folder itself goes once nothing is left in it.
- While people's work is contending for the database, the job pauses a moment before each document, so the
  people's requests go first.
- A failure is written to the server error log, and the item is tried again on the next run.
- What remains after a purge is the **delete log**: who deleted, emptied and purged the item, and when.
- A deleted user's recycle bin library is removed once it is empty.

## Disposal

Disposal is the deliberate end of a record under its retention schedule, not a cleanup.

### Delete or dispose

| | Delete ([DeleteDocument](../DeleteDocument.md), [DeleteFolder](../DeleteFolder.md)) | Dispose ([DisposeItem](../DisposeItem.md)) |
|---|---|---|
| **For** | Any item without a disposition date | Only an item whose disposition date has come |
| **Who** | Whoever has the `DocumentDelete` / `FolderDelete` right | R&D Managers (and system administrators, who pass every role check), who also need that delete right |
| **Goes to** | The deleter's recycle bin | Straight into the purge queue; no recycle bin |
| **Can come back** | Yes, until it is purged | No |
| **Open tasks on the document** | Refused | Allowed (a disposition task is one) |
| **Logged as** | `RECYCLE` | `PURGE`, plus a disposition record with the comments |

The two exclude each other. An item with a disposition date cannot be deleted ("This document is marked for
disposition. Please use the dispose function instead."). An item without one cannot be disposed of ("A
disposition date has not been assigned"). Both are refused with `4000`.

### Disposing of a document

The disposition date must have come. A date still in the future is refused, and so is a schedule whose
disposition is "transfer to an external agency". The document must not be frozen, under retention, checked
out, in a workflow or offline, and the caller needs the R&D Manager role and the `DocumentDelete` right. A
disposed document goes straight into the purge queue.

### Disposing of a folder

A folder is disposed of from the inside out:

1. Each document in it is disposed of on its own, by the document rule above.
2. Each subfolder is disposed of the same way, all the way down.
3. Last, the folder itself. It needs its own disposition date, come, and passes the folder checks (role,
   freeze, retention, workflow, rules, the `FolderDelete` right). It goes into the purge queue **only if it is
   empty by then**: everything that was in it has gone to the purge queue on its own. The emptiness is checked
   in the same transaction that queues the folder, so nothing added to the folder in the meantime is purged
   with it.

Anything that could not be disposed of (a document with no disposition date of its own, one that is checked
out, a subfolder the caller cannot list) **stays where it is, and so does the folder that holds it**. The
answer is `2070` MultiStatus, with one entry per item that was not disposed of. The folder's entry is "The
folder cannot be disposed of while it still holds documents or subfolders that were not disposed of." What
was disposed of is gone. The caller deals with what is left and disposes of the folder again.

### Who decides when

Nothing is disposed of automatically. When a disposition date arrives, the daily disposition check gives the
schedule's task user a disposition (or transfer) task and sends them a notice. A person then disposes of the
item.

## Settings

| Setting ([GetGeneralAppSettings](../GetGeneralAppSettings.md)) | Months, 0–36 | What it does |
|---|---|---|
| `MoveUsersRecycleBinToSystemRecycleBinIn` | `0` = never | Items deleted more than that many months ago leave the users' recycle bins for the system recycle bin. Daily. |
| `SystemRecycleBinAutoPurgeOption` | `0` = never | Items emptied into the system recycle bin more than that many months ago go to the purge queue. Daily. |

With both at `0`, nothing leaves a recycle bin by itself.

## The delete log

[GetDeleteLog](../GetDeleteLog.md) records each step, with who did it and when:

| `ACTION` | Written when |
|---|---|
| `RECYCLE` | An item is deleted into a recycle bin |
| `RECYCLE EMPTIED` | An item is emptied into the system recycle bin, by any of the four ways |
| `RESTORE` | An item is restored |
| `PURGE` | An item is put in the purge queue: purged by an administrator, by the automatic purge (by `SYSTEM`), or disposed of |

A folder's entry is written for the folder and for every document and subfolder in it.

## For developers

- Delete: `DocumentRecycleOperation` (checks in `DocumentDeleteCheckAsync`), `FolderRecycleOperation`
  (`FolderDeleteCheck`). The per-user recycle library is created by `UserOperations.GetRecycleBinIdAsync`.
- Empty: `RecycleBinOperations.EmptyUserRecycleBinAsync` (also behind EmptyUserRecycleBin and DeleteUser), `EmptyAllUserRecycleBinsAsync`,
  `MoveUsersRecycleBinToSystemRecycleBinAsync`; one transaction per item in `MoveToSystemRecycleBinAsync`.
- Search: `RecycleBinStore.SearchInRecycledItemsAsync` / `SearchInRecycledItemsPageAsync`. A status of
  "unspecified" means user's and system, never the purge state.
- Restore: `RecycleBinOperations.RestoreRecycledItemAsync`.
- Purge queue: `DocumentPurgeOperation.MoveRecycledDocToPurgeQueWithLogAsync`,
  `RecycleBinStore.SetRecycledItemToPurgeStateAsync`. The job: `SystemRecycleBin.RunAutoPurgeAsync` (every five
  minutes, `JobScheduleType.AnyTime`), `DocumentPurgeOperation.PurgeAsync`,
  `FolderPurgeOperation.RecursivePurgeAsync`, `PurgePacing`. The two month settings:
  `SystemRecycleBin.RunAutoMoveDeletedItemsAsync` (daily).
- Disposal: `DocumentExtensions.DisposeDocumentAsync`; for folders `FolderOperations.DisposeDocumentsRecursivelyAsync`
  then `DisposeFolderAsync`, which queues the folder through `FolderMoveOperation.RunOnlyTransactionAsync`
  (`recycleStatus: InPurgeState, onlyIfEmpty: true`). The disposition check: `Maintenance/DispositionCheck`.
- Tests: `RecycleBinBatchApiTests`, `EmptyAllUserRecycleBinsApiTests`, `EmptyUserRecycleBinApiTests`, `RecycleBinSettingsApiTests`,
  `DisposeFolderApiTests`, `RetentionBatchApiTests` (the dispose refusals).

## Since

- **9.0 (2026-11-06):** `searchIn` on [SearchRecycledItems1](../SearchRecycledItems1.md), to search the system
  recycle bin or the users' recycle bins alone. Before, both were always searched together. And `path`, to
  search the items deleted from one library or folder.
- **9.0 (2026-11-06):** an item emptied into the system recycle bin is restored by administrators only. Before,
  as in 8.7, the user who deleted it could still restore it by its handler, since the rule looked only at the
  recycle bin the item came from.
- **9.0 (2026-11-06):** a disposed folder goes to the purge queue, and only when it is empty. Before, it was
  moved into the disposer's own recycle bin together with whatever could not be disposed of. It could be
  restored from there, and the log recorded all of it as purged.
- **9.0 (2026-11-06):** [EmptyUserRecycleBin](../EmptyUserRecycleBin.md), for one user's recycle bin.
- **9.0 (2026-11-06):** [EmptyAllUserRecycleBins](../EmptyAllUserRecycleBins.md). Emptying moves each item
  with its log in one transaction. Before, an item two empties reached at once was logged twice, and an emptying
  cut off between the two writes left a moved item without its log entry.
