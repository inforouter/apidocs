# Who may change retention and disposition

Retention schedules decide how long a document or folder is kept and what happens to it then. This page says
who may put a schedule on an item, take it off, freeze it, set the dates it runs from, and record the transfer
that ends it.

## The rule

Changing retention **on an item** takes the `RetentionPeriodChange` right on that item **or** the R&D Manager
role: either one is enough. That covers applying a schedule, removing it, freezing and unfreezing it, and
setting or removing a cut-off date, on a document or on a folder and everything below it. **Defining** the
schedules themselves is R&D Managers only. Recording a transfer to an external agency takes the role, or an
administrator, and the right on the item.

## Who passes

| Action | Operations | Who |
|---|---|---|
| Apply or remove a schedule on a document or folder | SetDocumentRandDSchedule, RemoveDocumentRandDSchedule, SetFolderRandDSchedule, RemoveFolderRandDSchedule | `RetentionPeriodChange` on the item, or R&D Manager |
| Freeze or unfreeze | SetRdFreezeFlag and the folder form | The same |
| Set or remove a cut-off date | SetDocumentCutoffDate, RemoveDocumentCutoffDate, SetFolderCutoffDate, RemoveFolderCutoffDate | The same |
| Define, change or delete a schedule | CreateRandDSchedule, UpdateRandDSchedule, DeleteRandDSchedule | R&D Managers (administrators pass every role) |
| Record a transfer to an external agency | [TransferToExternalAgency](../TransferToExternalAgency.md) | R&D Manager or administrator, asked before the path is looked up, plus `RetentionPeriodChange` on the item |
| Dispose | [DisposeItem](../DisposeItem.md) | Its own rules on the page; refuses an item whose schedule says *transfer* |

The role stands in for a missing right; it does not add anything to a caller who already holds the right. A
folder call checks once, on the folder, and applies below it.

## Reach: which libraries an R&D Manager sees

The role gives no reach. An R&D Manager finds an item only in a library they are a member of or that allows
anonymous access, like any member. That is by design: a library that needs records management is opened to
the role by its manager adding the `[R&D Managers]` group as a member, and one that does not has nothing for
them to see. Add the group **before** applying schedules there: the daily disposition job assigns its tasks to
R&D Managers without checking that they can reach the library.

## Transfer to an agency

A schedule can end in disposal or in transfer to an external agency. For the second, the daily job creates a
*Transfer* task for each document that falls due, and that task cannot be completed until the document's
disposition status carries a transfer submission date. TransferToExternalAgency writes that record; nothing is
moved or deleted. Until 9.0.200 nothing in the API could write it, so every Transfer task stayed open.

## What the server answers

| Situation | Answer |
|---|---|
| Neither the right nor the role | `4030` |
| The item has no schedule, or the schedule is frozen, or the disposition date has not come | `4000` with the reason (TransferToExternalAgency lists them) |
| Transfer on an item whose schedule says *dispose*, or DisposeItem on one that says *transfer* | `4000` |
| The folder form with some items refused | `2070` with a `<log>` entry per item; the rest was done |

## For developers

- The rule: `RetentionAndDispositionOperations.MayChangeRetentionAsync` (the right or the role), used by the
  document and folder schedule, freeze and cut-off operations.
- Tests: `RetentionBatch2ApiTests.ApplyingAndFreezing_TakeTheRightOnTheItem_OrTheRdManagerRole`,
  `TransferToExternalAgencyApiTests`.
- Role page: [R&D Managers](../RDManagersRole.md).

## Since

- **9.0 (2026-10-14):** one rule for applying, removing, freezing and unfreezing. Before, folder schedule
  changes never asked for the role at all and subfolders got no check.
- **9.0.200 (2026-10-27):** cut-off dates take the role too; TransferToExternalAgency added.
