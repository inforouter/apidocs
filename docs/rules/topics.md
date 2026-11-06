# Topic list

Everything the server does, as a list of subjects read from the code: the 445 operation contracts in
`IRSoapApi/ISrv.cs`, the operation classes under `IRNET/Operations`, the models in `IRBase/Models` and the
enumerations in `IRBase/IRBaseEnum.cs`. The list is the table of contents this section fills in, and the
coverage ledger: a subject with a rule page is explained in plain words, a subject without one is documented
only by its API pages so far.

Each row names the subject, the facts it is made of, where in the code the rule is made, and the rule page.
The API page counts are the groups of the [API index](../index.md). Terms are defined in the
[glossary](glossary.md).

| Status | Meaning |
|---|---|
| ✅ | A rule page exists and is kept current with the code |
| ◐ | Part of the subject is on a rule page; the rest is API pages only |
| ○ | API pages only; a rule page is to come |

## Coverage

| Area | Subjects | Rule pages | API pages |
|---|---|---|---|
| Sessions and sign-in | 5 | 0 | 16 |
| People | 7 | 2 | 40 + 13 transfer |
| Libraries | 7 | 3 | 34 |
| Folders | 6 | 0 | 36 |
| Documents | 14 | 1 | 56 + 31 upload and download + 6 document types + 5 checkout |
| Security | 4 | 2 | 13 |
| Metadata | 5 | 1 | 24 + 5 tags |
| Search | 3 | 0 | 10 |
| Workflows and tasks | 8 | 1 | 55 |
| Retention and disposition | 4 | 1 | 29 |
| Notifications | 3 | 0 | 18 (with favourites) |
| Audit logs | 1 | 1 | 17 |
| Recycle bins | 2 | 1 | 7 |
| Personal lists | 3 | 0 | 7 associations |
| WebDAV and Office | 2 | 1 | – |
| System and administration | 5 | 0 | 30 |
| Connect | 3 | 1 | – |
| Conventions | 1 | 1 | – |

The rule pages so far: [administrator account](administrator-account.md), [libraries reach](libraries-reach.md),
[library from a model](library-from-template.md), [documents from forms](documents-from-forms.md),
[WebDAV](webdav.md), [task due date](tasks-due-date.md), [retention](retention-who-may.md),
[audit logs](audit-logs-who-reads.md), [Connect review state](connect-review-state.md),
[conventions](conventions.md), and the seven role pages under [Who may do what](../AdministrativeRoles.md).

## Sessions and sign-in

| Subject | What it is made of | Where in the code | Rule page |
|---|---|---|---|
| Tickets and sessions | A sign-in gives a GUID ticket backed by a SESSIONS row; the row carries the licence seat, three expiry rules and revocation. Session types: Generic, DAV, OfficeEdit. | `AuthenticationLibrary`, `SessionOperations`, `SessionInfo` | ○ |
| Sign-in sources | Native passwords, Windows authentication, external authorities (OAuth, LDAP) configured in `appsettings.json`; `GetSignInOptions` lists them. | `IRExternalAuthSrv`, `SecurityHelper.IsInternalAuthenticationSource` | ○ |
| Password policy | Length and complexity rules, expiry, re-prompt actions (which operations ask for the password again), forgot-password by secret text. | `AuthenticationAndPasswordPolicy`, `PasswordPolicy`, `PasswordRepromptActions` | ○ |
| Anonymous access | A caller with no user (`UserId <= 0`) reaches only libraries that allow anonymous access, and only for LIST and READ. | `ThreadVariables.IsAnonymous`, `AnonymousOperations`, `IRSecurity` | ◐ [conventions](conventions.md#things-that-surprise) |
| Licence seats | Author and reader seats are counted separately; a reader is capped at READ whatever the access list gives. Sign-in is refused when the seats are used up. | `LicenseInfo`, `InfoRouter.cs` seat check, `IRSecurity` reader cap | ○ |

## People

| Subject | What it is made of | Where in the code | Rule page |
|---|---|---|---|
| Users: global and local | A user with `DomainId` 0 is global; one with a library id is local to that library and managed by its managers. Author or Reader type; Enabled or Disabled. | `User`, `UserOperations`, `UserManagersRole` | ◐ [libraries reach, membership](libraries-reach.md#membership) |
| Special accounts | SYSTEM (id 3, user name SYS), also the identity Connect writes under; the system administrator (id 4). | `IRConstants`, `SpecialUser` | ○ |
| User groups: global and local | A group with `DomainId` 0 is global; a local group belongs to one library. `ShowMembers` false hides the membership. Groups with ids up to 1000 are built in. | `UserGroup`, `UsergroupOperations`, `DomainMembersStore` | ○ |
| Administrative roles | Six role groups with ids 100 to 105: User Managers, Audit Managers, Policy Managers, R&D Managers, Administrators, Search Administrators. Members are changed by administrators only. | `AdmistrativeRoles`, `IRSecurity` | ✅ [overview](../AdministrativeRoles.md) and the seven role pages |
| The administrator's account | Which changes to an administrator's account are refused to a User Manager, and the exceptions. | `IRSecurity.ChangesTheAccount` | ✅ [administrator account](administrator-account.md) |
| Taking over and transferring | Transfer a user's documents, tasks, subscriptions and memberships to another user; take over a user; delete a user and what moves to the recycle bin. | `UserTakeOverOperations`, `UserOperations` | ○ |
| Task redirection | A user redirects their tasks to another user for a period (`StartDate`, `EndDate`); rerouting an existing redirection elsewhere needs the server setting `RerouteRedirections`. | `TaskRedirectionInfo`, `GeneralSettings.RerouteRedirections` | ◐ [administrator account](administrator-account.md) for the guard |

## Libraries

| Subject | What it is made of | Where in the code | Rule page |
|---|---|---|---|
| Reach and membership | Who reaches a library, the last member, managers must be members, local users. | `DomainOperations.MayReachAsync`, `DomainMembersStore` | ✅ [libraries reach](libraries-reach.md) |
| Hidden, anonymous and archive libraries | `IsHidden` hides from listings, `AnonymousDomain` opens LIST and READ to everyone, `IsArchive` takes the library out of the default search scope. | `Domain`, `SearchScope` | ◐ [libraries reach](libraries-reach.md#who-reaches-what) |
| Library rules | Fourteen flags: hide incomplete, unapproved, expired and unpublished documents from readers and from anonymous callers; publishing requirements (document type, retention, completion, approval, not expired); drag-and-drop uploads. | `DomainRules`, `SetDomainRules` | ○ |
| Library policies | About fifty actions, each with six attributes: whether the library manager, the object owner, the sub-object owner and anonymous callers have it, the access right required, and whether it is logged. `AllowLibraryManagersToEditPolicy` decides who edits them. | `IrAction`, `DomainPolicyModel`, `DomainPolicyOperations`, `PolicyManagersRole` | ◐ [Policy Managers](../PolicyManagersRole.md) |
| A library from a model library | What `CreateDomainFromTemplate` copies, what it does not, and how access lists naming local groups are rewritten. | `DomainCopyOperation` | ✅ [library from a model](library-from-template.md) |
| Deleting a library | Irreversible, no recycle bin, stops workflows, deletes local users and groups; a document the caller may not delete stops it. | `DomainOperations.DeleteDomainByNameAsync`, `CleanupAsync` | ✅ [libraries reach, deleting](libraries-reach.md#deleting-a-library) |
| Library settings | Welcome message, library property sets, default folder columns, root folder settings, statistics. | `DomainsStore`, `FolderStore.CopyRootSettingsAsync`, `LibraryStatistics` | ○ |

## Folders

| Subject | What it is made of | Where in the code | Rule page |
|---|---|---|---|
| Create, rename, move, copy, delete | Names unique in a folder (`UQKEY_PUBLICATION`), moves inside and outside a library are separate policy actions (`MoveInside`, `MoveToOutSide`), copies carry an optional security origin, deletes go to the recycle bin. | `FolderOperations`, `FolderMoveOperation`, `FolderCopyOperation`, `FolderRecycleOperation` | ○ |
| Folder rules | Seven flags (no new folders, no folder delete, no checkout, no check-in, no document delete, no new document, classified documents allowed), an auto-prompt property set, default and mandatory view style. | `FolderRules`, `FolderRuleSet`, `SetFolderRules` | ○ |
| Folder columns | Which columns a folder listing shows by default; system-wide and per folder. | `FolderColumnDef`, `SetDefaultFolderColumns` | ○ |
| Ownership | The owner holds whatever the policies give object owners; ownership transfer needs `AllowOwnershipTransfer`. | `FolderChangeOwnerOperation`, `GeneralSettings.AllowOwnershipTransfer` | ○ |
| Access list catalogue and statistics | Every access list under a folder, counted; folder statistics (counts, sizes). | `FolderAccessListCatalogOperation`, `FolderStatistics` | ○ |
| Folder AI preferences | Which Connect operations run automatically for documents in a folder, with inheritance to subfolders. | `FolderAIPreferences`, `FOLDERAIPREFERENCES` | ○ |

## Documents

| Subject | What it is made of | Where in the code | Rule page |
|---|---|---|---|
| Kinds of document | File, template, URL, shortcut; the extension decides: `.url`, `.lnk`, `.email` (a registered email, downloaded as MIME). | `DocumentTypes`, `DocumentExtension.IsShortCut`, `IsUrl`, `IsEmail` | ○ |
| Creating and uploading | Upload in one call or in chunks, from a URL, by registering an email, by importing a tree; `DocumentCreate` policy; folder rule `DisallowNewDocument`; same bytes stored once. | `DocumentPublishOperation`, `DocumentImportOperation`, `RegisterEmail`, `UploadSettings` | ○ |
| Versions | Version numbers are legacy integers or multipart major.minor.revision stored as one integer; the last version, the published version; keep-versions limit, prune, rollback of an import. | `DocumentVersion`, `DocumentVersionOperations`, `PruneVersionOperation`, `DocumentRollbackImportOperation` | ○ |
| Publishing rules | Which version readers see: latest, last approved, tagged, a specific version, or unpublished; the library's publishing requirements. | `PublishingRule`, `SetPublishingRulesOperation`, `DomainRules.PublishReq*` | ○ |
| Checkout and check-in | A checkout holds the document for one user; others cannot publish a new version; undo, force check-in (`DocumentForceCheckin` policy), folder rules disallowing both. | `DocumentUndoCheckOutOperation`, `CheckoutPublicationsModel`, `DAV LOCK` | ◐ [WebDAV](webdav.md#what-each-verb-does) |
| Properties | Title, description, author, language, source; owner and registered-by; completion percentage and date; expiration with a notice before; offline state. | `DocumentPropertiesOperations`, `Expiration`, `DocumentState` | ○ |
| Importance and classification | Importance (none, low, normal, high, vital); classification (no markings, declassified, confidential, secret, top secret) with downgrade and declassify dates and a classification log. | `Importance`, `ClassificationLevel`, `ClassificationModel`, `ChangeClassification` policy | ○ |
| Comments | Text comments with author and date; adding and changing or deleting are separate policy actions, the sub-object owner being the comment's author. | `Comment`, `DocumentCommentAdds`, `DocumentCommentsChangeDelete` | ○ |
| Keywords and tags | Keywords are user-defined (kept) or generated (replaced wholesale by Connect); a tag is text of up to 128 characters on a version, and the TAGGED publishing rule points at it. | `KeywordType`, `AppliedTag`, `TagDef` | ○ |
| Documents from forms and templates | A document made by filling an HTML, PDF or Word form; when it is rendered again; when it stops being a form document. | `DocumentPublishOperation` template branch, `FormTemplateFieldsOperation` | ✅ [documents from forms](documents-from-forms.md) |
| Copy and move | What a copied or moved document carries (versions, security, property sets, subscriptions), and what it loses. | `DocumentCopyOperation`, `DocumentMoveOperation` | ○ |
| Associations | Related, rendition, copy, parent-child, derivation; between documents and folders, in either direction. | `AssociationTypes`, `Associations.cs` | ○ |
| Download and renditions | Download by version, zip downloads, PDF conversion, thumbnails, text renditions the warehouse keeps beside a version, checksums. | `DownloadHelper`, `VersionRendition`, `DocumentCheckSumOperations`, `IPDFConvertor` | ◐ [WebDAV, ETags](webdav.md#etags) |
| Export and import | Export a document with its metadata; import a tree with metadata; rollback. | `DocumentExportOperation`, `DocumentImportOperation`, `FolderImportOperation` | ○ |

## Security

| Subject | What it is made of | Where in the code | Rule page |
|---|---|---|---|
| Access lists | Entries for everyone, groups and users with a right from NOACCESS to FULLCONTROL; inherited from the parent or set on the item; a security definition is immutable and every change makes a new one. | `AccessList`, `SecurityDefinition`, `AccessListOperations`, `DocumentUpdateSecurityOperation`, `FolderSecurityOperation` | ○ |
| How a right is decided | The order the server checks: anonymous caller, library membership, sub-object owner, owner, library manager, the policy's required right against the access list, the reader cap, then an active task's right for documents. | `IRSecurity` (the policy evaluation) | ○ |
| Security history | One row per operation, with the items whose own list changed; who reads it. | `SecurityHistoryOperations`, `HistorySecStore` | ✅ [audit logs](audit-logs-who-reads.md#logs-about-items) |
| Rights and roles outside access lists | What administrators, Policy Managers and library managers may do on items without a right. | `IRSecurity`, role pages | ✅ [Who may do what](../AdministrativeRoles.md) |

## Metadata

| Subject | What it is made of | Where in the code | Rule page |
|---|---|---|---|
| Property sets | Named sets of typed fields (char, date, number, bool) stored in a `CUSTOM_<NAME>` table; global or restricted to libraries; private (hidden from anonymous callers); system-only; applied to documents, folders or users; one or many rows. | `PropertySet`, `PropertySetField`, `PropertySetOperations`, `PropertyDataType` | ○ |
| Lookup fields | A field whose values come from a database query. | `PropertySetFieldDefDataModel`, lookup operations | ○ |
| Document types | A name, an optional property set and an optional default retention schedule; the library rule can require one before publishing. | `DocumentType`, `DocumentTypeOperations` | ○ |
| Values Connect extracted | Confidence, saver and review state of a property set row. | `PropertySetDataRow`, `PropertySetRowReviewState` | ✅ [Connect review state](connect-review-state.md) |
| Folder auto-prompt | The property set a folder asks for on every new document. | `FolderRules.AutoPromptPropertysetId` | ○ |

## Search

| Subject | What it is made of | Where in the code | Rule page |
|---|---|---|---|
| Searching | Content search through a provider (Windows Search, dtSearch, remote), metadata search through the database, criteria XML, sorting and paging (`SearchPageSize`). | `ContentSearchLibrary`, `SearchServices`, `SearchParameters` | ○ |
| Scope | Online libraries, all, archived only, or online plus hidden; results are filtered by reach and rights. | `SearchScope`, `SessionInfo.ShowHiddens`, `ShowArchives` | ○ |
| Saved searches and search pages | Saved criteria per user; search pages and categories managed by Search Administrators. | `SearchPages`, `SearchParameterOperations`, `SearchAdministratorsRole` | ◐ [Search Administrators](../SearchAdministratorsRole.md) |

## Workflows and tasks

| Subject | What it is made of | Where in the code | Rule page |
|---|---|---|---|
| Workflow definitions | Per library: steps in order, task definitions per step, a supervisor list, a folder documents move to on start of a step and on end, an end-of-flow URL, active or not, hidden or not. | `WorkflowDef`, `WorkflowStepDef`, `WorkflowTaskDef`, `WorkflowManagerOperations` | ○ |
| Running a workflow | Submit a document (`DocumentSubmitWorkflow` policy), step statuses past, active, future; stop; what the end does; approval results. | `Workflow`, `WorkflowOperations`, `DocumentSubmitToWorkflowOperation`, `StepStatus` | ○ |
| Tasks | Workflow tasks and ad hoc tasks; assignee is a user, a group or a special role (document owner, submitter); all must complete, one is picked, or one is enough; priority; permissions; requirements; statuses. | `IrTask`, `WorkflowExecutingTask`, `TaskOperations`, `TaskPermissions`, `EnumTaskRequirement`, `TaskStatusX` | ○ |
| Due dates | Who may change a due date and reassign. | `WorkflowExecutingTaskExtensions.ChangeDueDateAsync` | ✅ [task due date](tasks-due-date.md) |
| Completing tasks | What completing needs (the requirement flags: sign, edit, read latest or published, comment, approve, archive, SOX or ISO review, dispose, downgrade, declassify, transfer, attachment, form, metadata, password re-prompt). | `TaskRequirements`, `WorkflowServices` | ○ |
| Supervisors | The task supervisor and the workflow supervisor list; notices on due; what supervision allows. | `CheckAllowSupervisionAsync`, `MemberListId` | ◐ [task due date](tasks-due-date.md#who-passes) |
| Task-based rights | An active task's `RightType` raises the assignee's right on the document for the task's duration. | `WorkflowOperations.GetUserActiveTaskPermissionAsync` | ○ |
| ISO review and disposition tasks | Scheduled ISO reviews on a document; the tasks retention creates at disposition and at transfer. | `ISODef`, `ScheduleDef`, `RDDefData.CreateTask` | ◐ [retention, transfer](retention-who-may.md#transfer-to-an-agency) |

## Retention and disposition

| Subject | What it is made of | Where in the code | Rule page |
|---|---|---|---|
| Who may change retention | R&D Managers, the role's reach, the rights on the item. | `RetentionAndDispositionOperations` | ✅ [retention](retention-who-may.md) |
| Schedules | Retention none, temporary or permanent, triggered by a custom date, creation or cut-off; a period in years, months, days; disposition final or transfer, triggered also by retention end; agency, source authority, records series, a folder to move to, a task, an email. | `RDDefData`, `RetentionType`, `RetentionTrigger`, `DispositionType`, `DispositionTrigger` | ○ |
| Dates on the item | Cut-off date, retain-until, disposition date, freeze; set on folders and documents, applied to subfolders. | `DocumentSetCutOffDateOperation`, `FolderSetCutOffDateOPeration`, `RdFreeze` | ◐ [retention](retention-who-may.md#who-passes) |
| The daily job | How the dates are computed and acted on, and the disposition notices. | `MainteanceJob`, `NotificationType.FOLDERDISPOSE`, `DOCUMENT_DISPOSE` | ○ |

## Notifications

| Subject | What it is made of | Where in the code | Rule page |
|---|---|---|---|
| Subscriptions | A user or group subscribes to a document or folder for eleven events (read, change, update, checkout, approve, reject, comment, move, delete, check-in, new document), or for new documents only; `AddRemoveSubscription` policy. | `SubscriptionModel`, `UserSubscription`, `GroupSubscription`, `SubscriberType` | ○ |
| Delivery | None, instant by email, or a daily report; attach the document or not; language of the notice. | `NotificationDeliveryType`, `Notification.cs`, `NotificationFunctions` | ○ |
| Notice types | Twenty-six notice types including task notices (new, overdue, reminder, completed, reassigned, dropped, escalated), expiration, disposition and workflow finished or stopped. | `NotificationType`, `TaskDetailsForNotification` | ○ |

## Audit logs

| Subject | What it is made of | Where in the code | Rule page |
|---|---|---|---|
| Which logs exist and who reads each | SOX, ISO, classification, view, security history, date-range logs, server logs. | `LogOperations`, `ServerLogs` | ✅ [audit logs](audit-logs-who-reads.md) |

## Recycle bins

| Subject | What it is made of | Where in the code | Rule page |
|---|---|---|---|
| User and system recycle bins | Each user has a recycle bin library named `~RECYCLE_<id>` of type UserRecycleBin; items move from it to the system recycle bin after a configured number of months, then to a purge state; restore to the original or another path; an administrator empties every user's bin at once. | `RecycleBinOperations`, `RecycledItemStatus`, `GeneralSettings.MoveUsersRecycleBinToSystemRecycleBinIn` | ✅ [What happens to a deleted document or folder](recycle-bin.md) |
| Purging | A purge puts the item in the purge queue, with no way back; the purge job removes queued items every five minutes, 1,000 a run, each document with its warehouse files in one transaction; auto-purge option; disposal goes straight to the queue. | `DocumentPurgeOperation`, `FolderPurgeOperation`, `SystemRecycleBin.RunAutoPurgeAsync`, `SystemRecycleBinAutoPurgeOption` | ✅ [What happens to a deleted document or folder, purging](recycle-bin.md#purging) |

## Personal lists

| Subject | What it is made of | Where in the code | Rule page |
|---|---|---|---|
| Favourites and the download queue | Per-user lists of documents; the queue is downloaded as one zip. | `DownloadQueOperations`, `FolderListType.MyFavorites`, `Que` | ○ |
| My documents and recent documents | The virtual lists: my documents, checked-out documents, authored documents, recent documents, subscriptions, ISO reviewer role. | `FolderListType`, `GetMyDocumentsAndFolders` | ○ |
| User folder settings | Per-user view style and column choices on folders. | `UserFolderSettings`, `ViewStyle` | ○ |

## WebDAV and Office

| Subject | What it is made of | Where in the code | Rule page |
|---|---|---|---|
| WebDAV | URLs, locks as checkouts, MOVE and COPY onto a document, ETags, caches, how Office saves. | `DAVCoreMiddleware` | ✅ [WebDAV](webdav.md) |
| Office edit sessions | A session of type OfficeEdit opened for an add-in or a browser edit; `CreateWebDavSession` and its listing. | `SessionType.OfficeEdit`, `CreateWebDavSession` | ○ |

## System and administration

| Subject | What it is made of | Where in the code | Rule page |
|---|---|---|---|
| Settings | General (uploads, ownership transfer, WebDAV, add-ins, recycle bin timings, redirections, diagnostics, workdays and holidays, zip downloads, page size), system behaviour (login logging, login delay, managers editing policy), email, UI. | `GeneralSettings`, `SystemBehaviorSettings`, `EmailAndNotificationSettings`, `UISettings`, `SettingServices` | ○ |
| Licence and server status | Seats, expiry, server status, warehouse status, statistics. | `LicenseInfo`, `Licensing`, `WarehouseStatus`, `SystemStatistics` | ◐ [audit logs, server](audit-logs-who-reads.md#date-range-logs-and-the-servers-own) |
| Maintenance jobs | The daily jobs: recycle bin moves and purges, retention, expiration notices, index, statistics; the cache flush. | `MainteanceJob`, `IRNET/Maintenance`, `FlushApplicationCache` | ○ |
| Business days | Workdays and holidays used for task deadlines. | `WorkDays`, `Holiday`, `BusinessDayCalculation` | ○ |
| Warehouse | Files stored under `<documentId>/<versionNumber>`; several warehouse paths; renditions beside a version. | `WH`, `IWarehouseService`, `WhAccessInfo` | ○ |

## Connect

| Subject | What it is made of | Where in the code | Rule page |
|---|---|---|---|
| Review state of extracted values | Confidence, saver, reviewed or not. | `PropertySetDataRow` | ✅ [Connect review state](connect-review-state.md) |
| The job queue | Operations a version is queued for, job states and priorities, attempts, call logs and log levels, PII scrubbing. | `AIJobQueueOperations`, `AIOperation`, `AIJobState`, `ConnectScrubPii`, `ConnectCallLogEntry` | ○ |
| Document type specifications | What Connect is told about a document type and its property sets; the per-document enhancement flags. | `ConnectDocumentTypeOperations`, `AIDocumentTypeSpec`, `AIEnhancements` | ○ |

## Conventions

| Subject | What it is made of | Where in the code | Rule page |
|---|---|---|---|
| How an answer is read | Error code bands, MultiStatus, name patterns, what surprises first-time callers. | `ApiError`, `IRConstants` patterns | ✅ [conventions](conventions.md) |

## Writing order

The subjects most asked about that have no page yet, in the order they are worth writing:

1. How a right is decided (Security).
2. Versions and publishing rules (Documents).
3. Checkout and check-in (Documents).
4. Library rules and library policies, one line per flag and per action (Libraries).
5. Completing tasks and supervisors (Workflows and tasks).
6. Copy and move (Documents and Folders).
7. Recycle bins and the daily job (Recycle bins, System).
8. Users and groups, global and local (People).
9. Subscriptions and notices (Notifications).
10. Retention schedules and the daily job (Retention).
