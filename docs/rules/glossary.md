# Glossary

The words the server uses, with the fact behind each read from the code. General document-management
terms come first in each group, then the ones infoRouter uses in its own way. Where a term is an enumeration
in the code, the values are listed in the order the code numbers them, because the numbers appear in API
answers.

## People

**User.** An account that can sign in: a user name of up to 64 ASCII characters (letters, digits, `@ . - _`),
first and last names, an email address, an authentication source, a status and a type. A user is identified
by a numeric id that never changes; the user name can.

**Global user.** A user that belongs to no library (`DomainId` 0). Global users are created and managed by
User Managers and administrators, and can be made members of any library.

**Local user.** A user that belongs to one library (`DomainId` set). A library's managers create and manage
its local users; the user exists only for that library and cannot be made a member of another. A library made
from a model library does not copy its local users.

**Author and reader.** The two user types, counted against separate licence seats. A reader is capped at the
READ right whatever an access list gives, and is refused any action whose required right is above READ, with
the exceptions the library policy grants to owners and library managers for LIST and READ actions. Changing a
reader to an author needs a free author seat.

**Enabled and disabled.** The two user statuses. A disabled user cannot sign in and holds no seat; their
documents, tasks and memberships stay as they are.

**System administrator.** The built-in account with id 4. It passes every administrative check and is the
one account that cannot be guarded against by the [administrator's-account rule](administrator-account.md).

**SYSTEM account.** The built-in account with id 3, user name `SYS`, under whose identity the server itself
writes: maintenance jobs, and infoRouter Connect, which saves extracted values as this user. A property set
row saved by user 3 is one nobody has reviewed yet.

**Anonymous caller.** A request with no user, or a ticket that resolves to none (`UserId <= 0`). Anonymous
callers reach only libraries that allow anonymous access, for LIST and READ actions, and only where the
library policy grants the action to anonymous callers. A call with no ticket at all is an anonymous call,
which is why it answers `4030` and not `4010`.

**Administrator.** The system administrator or a member of the `[Administrators]` group. Administrators pass
every role check and reach every library.

**Administrative roles.** Six built-in groups with ids 100 to 105: User Managers (100), Audit Managers (101),
Policy Managers (102), R&D Managers (103), Administrators (104), Search Administrators (105). Membership of
these groups is changed by administrators only. What each may do is on the [role pages](../AdministrativeRoles.md).

**Library manager.** A member of a library appointed as its manager. A manager must be a member; a
non-administrator cannot appoint themselves. The manager holds whatever the library's policies grant to
"domain manager", manages the library's local users and groups, members and managers, and reads the library's
logs.

**Owner.** The user a document or folder belongs to, set to the creator and changeable by ownership transfer
when the server setting allows it. The owner holds whatever the library's policies grant to "object owner".

**Sub-object owner.** The author of a part of an item, today the author of a comment. The policy attribute for
sub-object owners decides whether a comment's author may change or delete it.

**User group.** A named set of users (name up to 64 characters). A group with `DomainId` 0 is **global** and can
be a member of any library; a **local group** belongs to one library, is managed by its managers, and is
dropped from access lists when they are copied into another library. `ShowMembers` false hides a group's
membership from everyone who may not administer the group. Groups with ids up to 1000 are built in.

**Member.** A user, or a global group, on a library's member list. Membership is what makes a library reachable;
a library must always keep at least one member.

**Special roles.** Two placeholders usable as task assignees: Document Owner (-5) and Submitter (-8), resolved
to a user when the task is created.

**Session and ticket.** A sign-in creates a session row and returns its GUID as the ticket. Every call carries
the ticket; the session carries the user, the language, the IP address, whether hidden and archived libraries
are shown, and the type: Generic (0), DAV (1) for WebDAV clients, OfficeEdit (2) for Office add-ins and
browser editing. The session row is what the licence seat, the expiry rules and revocation hang on.

**Task redirection.** A period (`StartDate` to `EndDate`) during which a user's new tasks go to another user.
Setting one and removing one are always allowed to those who may change the account; rerouting an existing
redirection to a different recipient needs the server setting `RerouteRedirections`.

## Places

**Library.** The top-level container, called a domain in the API (`DomainId`, `DomainName`). A library has its
own members, managers, local users and groups, rules, policies, workflow definitions and root folder. Its root
folder has the library's own id. A library is Ordinary (0) or a UserRecycleBin (1).

**Hidden library.** A library with `IsHidden` set: left out of listings unless the session shows hiddens, but
reachable by name by its members and by the administrators who reach every library.

**Anonymous library.** A library with `AnonymousDomain` set: anyone, signed in or not, can LIST and READ in it,
subject to each access list's "allow anonymous" entry and the policy's anonymous attribute.

**Archived library.** A library with `IsArchive` set: searched only when the scope says so (search scope
InArchivedLibraries or InAllLibraries), and listed only when the session shows archives.

**Folder.** A container inside a library, with a name, a description, an owner, an access list, folder rules,
retention dates and a classification level. `IsRoot` marks the library's root. Folder and document names are
unique within a folder, enforced by the database.

**Path.** `/<library>/<folder>/.../<name>`. Many operations also take an id form: `~D<id>` for a document,
`~F<id>` for a folder, `~L<id>` for a library, `~U<id>` for a user.

**Recycle bin.** Every user has one, a library named `~RECYCLE_<id>` of type UserRecycleBin. A deleted item is
InUserRecycleBin (0) until the server moves it to the **system recycle bin** (1) after the configured number
of months (1 to 36), and InPurgeState (2) once a purge is requested; the daily job removes purged items from the
warehouse. Items can be restored to their original path or another one.

**Warehouse.** The file store. Each version's file lives under `<documentId>/<versionNumber>`, with the
renditions the server derives from it (text, thumbnail) beside it. Several warehouse paths may be configured;
`WhLibraryId` on a document says which one holds it.

## Documents

**Document.** A named item in a folder with versions, an owner, a registered-by user, an access list, a
document type, properties, keywords, comments, subscriptions, tasks and retention dates. The document id never
changes across renames, moves, new versions or restores from the recycle bin.

**Kinds of document.** FILE (1), TEMPLATE (2), URL (3), SHORTCUT (4). The extension tells them apart: a
`.url` document holds a link, a `.lnk` document is a shortcut to another item, an `.email` document is a
registered email and downloads as MIME.

**Version.** One stored file of a document, numbered, with an owner (the user who published it), a creation
date, a size, a checksum, an optional comment and an approval status. New versions are published by upload,
by check-in, by WebDAV PUT or MOVE, or by filling a form again.

**Version number.** A legacy version is a plain integer and displays as `n.0.0`. A multipart version
major.minor.revision is stored as one integer, major × 1,000,000 + minor × 1,000 + revision, with major up to
9,999 and minor and revision up to 999. `VersionNumberExternal` is the number clients see: a legacy number
multiplied by one million so that both kinds sort together. WebDAV ETags are `<documentId>:<versionNumber>`.

**Last version and published version.** The last version is the newest stored one. The published version is
the one readers get, chosen by the document's publishing rule; `PublishedVersionNumber` and the published
size, author and checksum are on the document.

**Publishing rule.** NONE (-1), LATEST (0), LASTAPPROVED (1), TAGGED (2, the version carrying a given tag
text), SPESIFICVERSION (3), UNPUBLISHED (4). Changing it is the `SetPublishingRules` policy action.

**Publishing requirements.** Library rules that refuse to publish a version unless the document has a document
type, a retention schedule, is complete, is approved, or is not expired.

**Approval status.** NoResult (0), Rejected (5), Approved (6), set on a version by a workflow approval task,
with the workflow that decided it.

**Checkout.** A hold on a document by one user: `CheckOutByUserId` on the document. While held, only that user
can publish a new version (others get `4230`) or change its properties (others get `4000`). A checkout ends
with check-in (a new version), undo (no version) or a forced check-in by someone the `DocumentForceCheckin`
policy allows. A WebDAV LOCK is a checkout.

**Prune.** Removing a document's older versions on request. Since 9.0 a document with no published version
can be pruned as well. `KeepVersions` is a per-document count that a copy carries along.

**Comment.** Text attached to a document with its author and date. Adding is one policy action; changing or
deleting is another, where the author is the sub-object owner.

**Title, description, author, language, source.** Descriptive properties of a document distinct from its name;
changing them is the `DocumentPropertyChange` policy action.

**Keyword.** A word attached to a document for search. UserDefined (0) keywords are curated by people and never
overwritten; Generated (1) keywords are produced by infoRouter Connect and replaced wholesale when regenerated.
A keyword is at most 128 characters.

**Tag.** Text of up to 128 characters applied to a specific version, recording who applied it and, if a
workflow did, which workflow and step. The TAGGED publishing rule publishes the version carrying a given tag.

**Importance.** NoMarkings (-1), Low (0), Normal (1), High (2), Vital (3).

**Classification.** NoMarkings (0), Declassified (1), Confidential (2), Secret (3), TopSecret (4), with a
downgrade date and a declassify date. A folder must allow classified documents; changes are the
`ChangeClassification` policy action and are logged in the classification log.

**Completion.** A percentage and a completion date on a document; the `DocumentCompletion` policy action.
Library rules can hide incomplete documents from readers and anonymous callers.

**Expiration.** A date after which a document is expired, with a notice a number of days before, sent to a
named agent. Library rules can hide expired documents and refuse to publish them.

**Offline.** The document state Offline (1): the document's content and some of its properties are not
accessible for now. Operations that need them answer `4230` with "marked as offline"; in a batch the item is
reported in the MultiStatus log.

**Form document.** A document made by filling an HTML, PDF or Word form template. It keeps a link to the
template (`TemplateId`) and is rendered again only on form submission, as the
[forms page](documents-from-forms.md) says. `DynamicContent` marks a form document rendered on the fly.

**Rendition.** A file the warehouse keeps beside a version and derives from it: its plain text (from a text
layer or OCR), its thumbnail, its PDF. None is the document; each can be rebuilt from the version.

**Checksum.** A ten-letter digest stored with a version and verifiable on demand.

**Association.** A typed link between items: Related (0), Rendition (1), Copy (2), ParentChild (3), Derivation
(4), between a document or folder and another document or folder, removable from either side.

**Shortcut.** A `.lnk` document pointing at another item; listings mark it with `IsShortcut`.

## Access and policies

**Access list.** Who may do what on an item: an entry for everyone, entries for groups and entries for users,
each with a right; an "allow anonymous" flag. An item either **inherits** its parent's list or has its own.
Changing a list is the `SecurityChange` policy action and is recorded in the security history.

**Right.** NOACCESS (0), LIST (1), READ (2), ADD (3), ADDREAD (4), CHANGE (5), FULLCONTROL (6). Each policy
action names the right it requires; the caller's given right from the access list must reach it. A group
entry counts only for groups local to the library or global groups that are members.

**Security definition.** The stored shape of an access list, identified by `SecDefId`, with who applied it and
when. Definitions are immutable: every change creates a new one and points the item at it, so history can
show each one.

**Library rules.** Fourteen on-off flags per library: hide incomplete, unapproved, expired and unpublished
documents from readers and from anonymous callers (eight flags), the five publishing requirements, and
disallow drag-and-drop uploads.

**Library policies.** One row per policy action per library. A policy action is one of about fifty operations
(delete a document, check out, change properties, add a comment, read a log, submit to a workflow, move
inside or outside the library, and so on). Each row says whether the library manager, the object owner, the
sub-object owner and anonymous callers may do it, the right required of everyone else, and whether the action
is logged. Policy Managers edit them, and library managers too when the server setting allows.

**How a right is decided.** In this order: the policy's log flag is noted; an anonymous caller passes only if
the policy grants anonymous callers; a non-member is refused unless the library allows anonymous access; a
member who is the sub-object owner, the owner (authors only) or a library manager passes if the policy grants
that role; a LIST or READ action in an anonymous library passes; a reader is refused anything above READ; the
caller's given right from the access list is compared with the required right, a reader's capped at READ; for
a document, an active task's right is tried last unless the list says NOACCESS outright.

**Task-based right.** A workflow task definition carries a right; while the task is active the assignee holds
that right on the document, on top of the access list.

**Folder rules.** Seven on-off flags on a folder: no new folders, no folder delete, no checkout, no check-in,
no document delete, no new document, classified documents allowed; plus an auto-prompt property set and a
default and a mandatory view style.

## Metadata

**Property set.** A named set of custom fields applied to documents, folders or users. The name is uppercase,
up to 40 characters of letters, digits and underscore, and becomes the table `CUSTOM_<NAME>`. A set is
**global** (available in every library) or **restricted** to listed libraries; **private** (hidden from
anonymous callers) or public; **system-only** sets are the server's own, such as the email set (id 950).

**Field.** A column of a property set: a name of up to 32 characters, a data type (CharType, DateType,
NumberType, BoolType), a caption, a maximum input length, an optional option list, an optional filter. A
**lookup field** takes its values from a database query.

**Row.** One set of field values on an item. A property set may hold several rows per item (`RowNumber`).
Each row records who saved it and when, and for rows Connect wrote, a confidence and a review state.

**Document type.** A name of up to 30 characters, an optional property set and an optional default retention
schedule. Setting and changing a document's type are policy actions; a library rule can require one before
publishing.

**Auto-prompt.** The property set a folder rule names, asked for on every new document in the folder.

**Folder columns.** The columns a folder listing shows, chosen system-wide or per folder.

## Workflows and tasks

**Workflow definition.** A named process (name up to 32 characters) in one library: ordered steps, task
definitions in each step, a supervisor list, a folder documents move to when a step starts and when the flow
ends, an optional URL called at the end, active or not, hidden or not.

**Step.** A numbered stage of a definition with a name of up to 32 characters. A running step is Past (1),
Active (2) or Future (3).

**Task definition.** A task a step creates: name, assignees, how assignees are chosen, deadline in business
days, priority, the right the assignee gets, permissions, requirements, reminder and allowed-start spans,
supervisor and supervisor notice.

**Workflow.** A running instance of a definition on one document: submitted by a user on a date, with a due
date, the current step, and a finish date when done. Submitting is the `DocumentSubmitWorkflow` policy
action; a document is in at most one workflow at a time (`CurrentFlowId` on the document).

**Task.** Work assigned to a user on a document: from a workflow step, or **ad hoc** (created directly, `AdHoc`
true). A task has an assignee, an assigner, a start and due date, a priority, a status, permissions,
requirements, instructions, an optional supervisor, the version range it concerns, and a linked task when it
was reassigned or redirected.

**Assignee.** A User (3), a Group (4) or a SpecialUserRole (7). When a task definition names several, the
selection is AllMustCompleteTheTask (0), AutomaticallySelectOneAssignee (1) or
AssignToAllOneIsEnoughToComplete (2).

**Task priority.** NoPrioritySetting (0), Low (1), Normal (5), High (10), Urgent (11).

**Task status.** Reassigned (-2), Dropped (-1), NotStarted (0), InProgress (10), DueDateChanged (20),
Completed (30). Listings also report a completion view: OverDue, Completed, Due, NotStarted, Reassigned,
Dropped, Archived.

**Task permissions.** Flags on a task: ChangeDueDate (1), ChangePriority (2), ChangeFinishdate (4),
EditNextStep (8), EditAllSteps (16), EditDocument (32). CompleteOnly is none of them.

**Task requirements.** What completing needs, as flags: Sign, Edit, LastestVersionRead, Comments, Approval,
Archive, SOXReview, ISOReview, Dispose, Downgrade, Declassify, PublishedVersionRead, Transfer, Attachment,
FormTemplate, MetaData, ReproptPassword.

**Supervisor.** A user named on a task, and the workflow's supervisor list; supervision allows what the
assignee's own permissions do not, such as changing a due date, as the [due-date page](tasks-due-date.md) says.

**Reassignment and redirection.** Reassigning gives a task to another user by hand; redirection does it
automatically for a period. Both leave a linked task behind.

**Deadline and business days.** Deadlines are counted in workdays, skipping the configured holidays.

**ISO review.** A scheduled review of a document: a reviewer, instructions, a workflow or a task definition,
and the next review date on the document.

## Retention and disposition

**Retention schedule.** A named definition (up to 128 characters) of how long records are kept and what
happens then: a retention type and trigger with a period in years, months and days; a disposition type and
trigger with its own period; the agency records transfer to; a source authority, a reference number, a
records series name, a folder to move disposed items to; whether a task is created and an email sent.

**Retention type and trigger.** None (0), Temporary (1), Permanent (2); triggered by Custom_Date_Entry (0),
On_Create (1) or On_CutOff (2).

**Disposition type and trigger.** None (0), Final_Dispostion (1), Transfer_To_External_Agency (2); triggered by
Custom_Date_Entry (0), On_Create (1), On_CutOff (2) or On_RetentionEnd (3).

**Cut-off date.** The date a record's life is measured from when the trigger is On_CutOff; set on a document
or a folder, and from a folder onto its subfolders.

**Retain until and disposition date.** The dates the schedule computes onto the item; `RdFreeze` freezes them
so no disposition happens while a hold is on.

**Transfer to an agency.** The disposition that hands records to an external agency, completed through
[TransferToExternalAgency](../TransferToExternalAgency.md) by the task's assignee.

**Source authority.** The law, regulation or policy a schedule cites; kept as a managed list.

## Notifications and personal lists

**Subscription.** A user's or group's request to be told about a document or folder for any of eleven events:
read, change, update, checkout, approve, reject, comment, move, delete, check-in, new document; or new
documents only. Adding and removing is the `AddRemoveSubscription` policy action; reading a subscriber list is
another.

**Delivery.** none (0), instant_ByEmail (1), dailyReport_ByEmail (2), per user, with the option to attach the
document.

**Notice type.** One of twenty-six kinds of message the server sends: the eleven subscription events, task
notices (notification, overdue, supervision, reminder, completed, reassigned with an originator copy, dropped,
escalated, overdue copy to the assigner), about-to-expire, folder and document disposition, workflow finished
and stopped.

**Favourites.** A per-user list of documents.

**Download queue.** A per-user list of documents fetched together as one zip, within the zip download setting.

**Virtual lists.** The lists the API serves as if they were folders: MyDocuments (-1), Subscriptions (-2),
CheckedOutDocuments (-3), Find (-4), MyFavorites (-5), Que (-6), RecentDocs (-7), AuthoredDocuments (-8),
ISOReviewerRole (-9).

## Logs

**SOX log.** Compliance notes on a document, written under the Sarbanes-Oxley review requirement, read with
the `DocumentReadSoxLog` right.

**ISO log.** Review entries on a document from ISO reviews, read with the `DocumentReadIsoLog` right.

**Classification log.** Each change of classification, with its policy-governed readers; entries can be
deleted under the `DeleteClassificationLog` policy.

**View log.** Who read a document and when (`DocumentReadViewLog` right), and a user's own view log.

**Security history.** One row per security operation with the items whose own list changed, kept for every
item and readable per item or under a path.

**Date-range logs.** System-wide logs of checkouts, check-ins, deletes, moves, renames, creates, content
changes, ownership changes and dispositions over a period, Audit Managers' to read.

## Connect

**infoRouter Connect.** The AI service the server queues document versions to for summaries, descriptions,
keywords, classification and property set extraction. It writes as the SYSTEM account.

**Job.** A queued request for one Connect operation on one version, with a state, a priority and an attempt
count; call logs record each exchange at a configured log level.

**Confidence.** The score Connect gave a property set row it wrote; present and above zero means the row was
extracted by Connect and is never reset by the server.

**Review state.** Whether a person has saved a Connect-written row since, as the
[review page](connect-review-state.md) says.

**PII scrubbing.** The setting that strips personal data from text before it is sent to Connect.

## Conventions

**Error code.** A number whose first three digits are the HTTP status it corresponds to: 4000 bad request,
4010 not authenticated, 4030 denied, 4041 not found, 4090 already exists, 4230 locked, 5000 server error, 6000
licence, 6010 no Anonymous Access, 2070 MultiStatus. The [conventions page](conventions.md) has the bands.

**MultiStatus.** An answer that succeeded for some items and not others, code 2070, with a log per item.

**Name patterns.** User names up to 64 characters; group, workflow, step and task names up to 64, 32, 32 and
32; tags, keywords and schedule names up to 128; document type and portal names up to 30; property set names
up to 40 and field names up to 32. The exact character classes are in `IRConstants`.
