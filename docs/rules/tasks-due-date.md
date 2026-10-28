# Who may change a task's due date

Changing a task's due date is not a role and not a right on the document. It is decided task by task, from a
permission the task was created with and from who stands over the task.

## The rule

The **assignee** may change the due date only if the task was created with the *change due date* permission
(the "Postpone" option; `PermissionChangeDueDate`), which is off unless whoever made the task turned it on.
Whoever **supervises** the task may change it whatever the permission says: the user who assigned the task, a
supervisor of the workflow it belongs to, or a manager of the library the task is in. Nobody else may.

## Who passes

| Caller | May change the due date | Needs |
|---|---|---|
| The assignee | Yes, if the task carries the *change due date* permission | The task made with `PermissionChangeDueDate` on |
| The user who assigned the task | Yes | Nothing else |
| A supervisor of the workflow | Yes | Named as supervisor in the workflow definition |
| A manager of the task's library | Yes | Library manager of the library the task belongs to |
| Any other member, a co-worker, a reader | No | - |

An ordinary user therefore changes a due date in exactly two cases: they are the assignee of a task made with
the permission, or they are the one who created and assigned the task.

### Administrators

There is no administrator bypass on this rule. A system administrator who did not assign the task, does not
supervise its workflow and does not manage its library is refused like anyone else. (A comment in the code
shows this was considered at 8.5.138 and not done.)

## What the server answers

| Situation | Answer |
|---|---|
| The caller is none of the above | `4030` "Access denied." |
| The task is not active (completed, dropped, not started) | `4000` "The task must be started and active before the due date can be changed." |
| The new due date is in the past | `4000` "Due date must be in the future." (ReassignTask: "Task due date cannot be in the past.") |
| No such task | `4041` |

Changing the due date also moves the reminder (kept at the same number of hours before the new date) and the
allowed-start date, when the task has them.

## Where the permission comes from

| Task made by | The permission is |
|---|---|
| [CreateTask](../CreateTask.md), [CreateRelatedTask](../CreateRelatedTask.md) | The `PermissionChangeDueDate` element of the request, `false` by default |
| A workflow step | The task definition of the step, set when the workflow was defined |
| An ISO review | The review definition's task permission |
| The daily disposition job | Off: disposition tasks are not postponed by their assignee |

The three sibling permissions, change priority, change finish date and edit the document, are stored with it
and decided the same way.

## Reassigning sets a due date too

[ReassignTask](../ReassignTask.md) takes a new due date and asks for no permission: the **assignee** may always
reassign their task to somebody else, and so may the same supervision as above. The new due date must not be
in the past, and the task must be active and not already reassigned. So an assignee without the *change due
date* permission can still give the task a new due date on its way to another user; what they cannot do is
keep the task and move its date.

## For developers

- Operations: [ChangeTaskDueDate](../ChangeTaskDueDate.md) (`taskId`, `newDueDate`, `allowedStartTimeSpan`),
  [ReassignTask](../ReassignTask.md).
- The rule: `WorkflowExecutingTaskExtensions.ChangeDueDateAsync` and `CheckAllowSupervisionAsync`
  (`IRNET/Extensions/WorkflowExecutingTaskExtensions.cs`). Supervision is `IsSupervisorAsync`, the task's
  `AssignedById`, or a row in DOMAINMANAGERS for the task's library.
- The permission: `enum_IR.TaskPermissions.ChangeDueDate`, bit 1 of the task definition's PERMISSIONS column.
- Tests: `CreateTaskApiTests` (the permission flags on creation), `WorkflowBatch3ApiTests` (reassignment and
  due dates).

## Since

Unchanged since 8.x. Documented here on 2026-10-28; the API page used to name only the assignee with the
permission and the workflow supervisor, leaving out the assigner and the library manager.
