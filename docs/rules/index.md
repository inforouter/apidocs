# Server rules

How infoRouter decides: who may do what, what a change carries with it, and why a call is refused. The API
pages say what each call takes and returns; the pages here say the rule behind the calls, in plain words first,
with the operations and error codes for developers at the end of each page.

Every rule here is read from the server code and is covered by a test named on the page. When a rule changes,
its page changes in the same commit, and the page says since which version.

## Subjects

| Subject | What it answers |
|---|---|
| **Who may do what** | The six administrative roles and the library manager ([overview](../AdministrativeRoles.md)): [Administrators](../AdministratorsRole.md), [User Managers](../UserManagersRole.md), [Audit Managers](../AuditManagersRole.md), [Policy Managers](../PolicyManagersRole.md), [R&D Managers](../RDManagersRole.md), [Search & Category Administrators](../SearchAdministratorsRole.md), [Library Managers](../LibraryManagersRole.md). [Who may change an administrator's account](administrator-account.md). [Which libraries a caller can reach](libraries-reach.md). |
| **Tasks and workflows** | [Who may change a task's due date](tasks-due-date.md). To come: completing tasks, supervisors, task redirections, disposition tasks. |
| **Documents** | [Documents made from forms and templates](documents-from-forms.md). To come: versions and publishing requirements, checkout and check-in, what Copy and Move carry, classification. |
| **WebDAV** | [How WebDAV maps onto documents](webdav.md): locks are checkouts, a MOVE onto a document is a new version, ETags, how Office saves. |
| **Libraries** | [Which libraries a caller can reach](libraries-reach.md), membership and deletion. [A library made from a model library](library-from-template.md). |
| **Retention and disposition** | [Who may change retention and disposition](retention-who-may.md): schedules, freeze, cut-off dates, the role's reach, transfer to an agency. |
| **Audit logs** | [Which logs exist, and who reads each](audit-logs-who-reads.md). |
| **Connect** | [Values Connect extracted, and whether somebody reviewed them](connect-review-state.md). |
| **Conventions** | [How an answer is read](conventions.md): error code bands, MultiStatus, what surprises first-time callers. |

The [questions index](questions.md) lists the questions people ask and points at the paragraph that answers
each.

## How a page is written

1. **The question** as a customer asks it, as the title.
2. **The rule**, in one paragraph anyone can read.
3. **Who passes**, as a list or a table, with the one condition each needs.
4. **What the server answers** when it refuses, with the code.
5. **Settings** that change the rule, if any.
6. **For developers**: the operations, where in the code the rule is made, and the test that proves it.
7. **Since**: the version a rule changed in, with the old behaviour in one line.
