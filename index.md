# infoRouter Web API Documentation

Welcome to the comprehensive documentation for the infoRouter Web Services API.

## Overview

The infoRouter Web Services API provides programmatic access to infoRouter's document management, workflow, and collaboration features. All APIs are available via SOAP, REST (GET), and REST (POST) protocols.

## Getting Started

1. **Authentication**: Obtain an authentication ticket using `AuthenticateUser`
2. **Make API Calls**: Use the ticket in subsequent API calls
3. **Handle Responses**: All responses are in XML format

## API Categories

### Authentication
- [AuthenticateUser](AuthenticateUser) - Authenticate with user name and password, returns ticket and profile info
- [AuthenticateUser1](AuthenticateUser1) - Authenticate with user name, password, and an explicit session language
- [AuthenticateUserViaWindows](AuthenticateUserViaWindows) - Authenticate using the Windows identity (NTLM/Kerberos) from the HTTP request context
- [ChangePasswordUsingSecretText](ChangePasswordUsingSecretText) - Complete a password reset using the one-time token emailed by ForgotPassword
- [ChangeUserPassword](ChangeUserPassword) - Change a user's password (self-service or User Manager)
- [CreateTicketforUser](CreateTicketforUser) - Create an authentication ticket for any user using the server-side trusted password (server-to-server impersonation)
- [ForgotPassword](ForgotPassword) - Initiate a password reset by sending a one-time token to the user's registered email address
- [ForgotPasswordByUserName](ForgotPasswordByUserName) - Initiate a password reset by login name (sends token to the user's registered email address)
- [isValidTicket](isValidTicket) - Check whether an authentication ticket is still valid without supplying credentials or extending the expiration
- [LogOut](LogOut) - Invalidate an authentication ticket and clear the server-side session
- [RenewTicket](RenewTicket) - Validate credentials and renew an existing ticket or issue a fresh one

### Application Settings & Configuration
- [FlushApplicationCache](FlushApplicationCache) - Flush the in-memory application cache (admin only)
- [getApplicationParameters](getApplicationParameters) - Get application parameters (role-based response: public, regular user, or full admin view)
- [GetAllFolderColumns](GetAllFolderColumns) - Get all 34 available folder column definitions
- [GetAuthenticationAndPasswordPolicy](GetAuthenticationAndPasswordPolicy) - Get authentication and password policy settings (complexity requirements, re-prompt actions)
- [GetDefaultFolderColumns](GetDefaultFolderColumns) - Get the system default folder columns for list views
- [GetGeneralAppSettings](GetGeneralAppSettings) - Get general application settings including upload limits, work days, holidays, and system preferences
- [GetMimeTypes](GetMimeTypes) - Get the list of all defined MIME types in the system
- [GetSystemBehaviorSettings](GetSystemBehaviorSettings) - Get system behavior settings (login logging, anti-brute-force, library manager permissions)
- [SetAuthenticationAndPasswordPolicy](SetAuthenticationAndPasswordPolicy) - Update authentication and password policy settings (complexity rules, expiration policies)
- [SetDefaultFolderColumns](SetDefaultFolderColumns) - Set the system default folder columns using comma-separated column names
- [SetGeneralAppSettings](SetGeneralAppSettings) - Update general application settings (upload limits, recycle bin policies, workdays/holidays)
- [SetSystemBehaviorSettings](SetSystemBehaviorSettings) - Update system behavior settings (login logging and login delay configuration)

### Server & License Management
- [GetLicenseInfo](GetLicenseInfo) - Get application license details, user counts, and subscription dates (admin only)
- [GetLogs](GetLogs) - Get server log entries by type and date (admin only)
- [GetLogStatistics](GetLogStatistics) - Get available log dates and entry counts by log type (admin only)
- [GetMaintenanceJobsStatus](GetMaintenanceJobsStatus) - Get status of all system maintenance jobs (admin only)
- [GetWarehouseStatus](GetWarehouseStatus) - Get warehouse storage status, document counts, and disk information (admin only)
- [ServerInfo](ServerInfo) - Get server version, time, and basic license info (no authentication required)
- [UpdateApplicationLicense](UpdateApplicationLicense) - Update the application license file (admin only)

### Audit Logs
- [GetCheckInLog](GetCheckInLog) - Get check-in log entries for documents
- [GetCheckoutLog](GetCheckoutLog) - Get checkout log entries for documents
- [GetDeleteLog](GetDeleteLog) - Get deletion log entries for documents and folders
- [GetDispositionLog](GetDispositionLog) - Get disposition log entries for documents
- [GetNewDocumentsAndFoldersLog](GetNewDocumentsAndFoldersLog) - Get creation log entries for new documents and folders
- [GetOwnershipChangeLog](GetOwnershipChangeLog) - Get ownership change log entries for documents and folders
- [GetSecurityChangeLog](GetSecurityChangeLog) - Get security change log entries for documents and folders
- [GetUserViewLog](GetUserViewLog) - Get the complete read/view log history for a specified user
- [GetUserViewLog1](GetUserViewLog1) - Get the read/view log history for a specified user filtered by date range
- [GetVersionCreateLog](GetVersionCreateLog) - Get version creation log entries for documents
- [GetVersionDeleteLog](GetVersionDeleteLog) - Get version deletion log entries for documents

### Folder & Document Listing
- [GetFoldersAndDocuments](GetFoldersAndDocuments) - Return immediate sub-folders and documents in a path with full detail options
- [GetFoldersAndDocuments1](GetFoldersAndDocuments1) - Return immediate sub-folders and documents in short form (abbreviated elements, minimal attributes)
- [GetFoldersAndDocuments2](GetFoldersAndDocuments2) - Return immediate sub-folders and documents in lightweight ultra-fast format
- [GetFoldersAndDocumentsByPage](GetFoldersAndDocumentsByPage) - Return a paged list of sub-folders and documents with optional name filtering
- [GetFoldersAndDocumentsByPage2](GetFoldersAndDocumentsByPage2) - Return a paged list with advanced XML filtering and sorting via search engine
- [GetMyDocumentsAndFolders](GetMyDocumentsAndFolders) - Return all documents and folders owned by the currently authenticated user

### Folder Management
- [CreateFolder](CreateFolder) - Create a folder from a single full path (intermediate folders created automatically)
- [CreateFolder1](CreateFolder1) - Create a subfolder with optional description using separate parent path and name parameters
- [DeleteFolder](DeleteFolder) - Delete a folder and all its contents
- [FolderExists](FolderExists) - Check whether a folder exists at the specified path
- [FolderExists1](FolderExists1) - Check whether a named subfolder exists within a specified parent folder
- [GetFolder](GetFolder) - Get the full properties of a folder with optional rules, property sets, security, and owner details
- [GetFolderCatalog](GetFolderCatalog) - Get the catalog information for a folder
- [GetFolderRules](GetFolderRules) - Get the rules and policies configured for a folder
- [GetFolderStatistics](GetFolderStatistics) - Get statistics for a folder (subfolder count, document count, total size)
- [GetFolders](GetFolders) - Get the list of direct subfolders with full property details
- [GetFolders1](GetFolders1) - Get the list of direct subfolders in short form (no count limit)
- [GetFolders2](GetFolders2) - Get the list of direct subfolders in short form with configured UI display limit
- [GetFoldersByPage](GetFoldersByPage) - Get a paged list of direct subfolders with optional name filtering
- [GetParentFolderIDs](GetParentFolderIDs) - Get the chain of parent folder IDs from root to the specified folder
- [GetSubFoldersCount](GetSubFoldersCount) - Get the count of direct subfolders in a folder
- [Move](Move) - Move a document or folder to a new destination path
- [RemoveFolderCutoffDate](RemoveFolderCutoffDate) - Remove the cutoff date from a folder and optionally its subfolders and documents
- [SetFolderCutoffDate](SetFolderCutoffDate) - Set the cutoff date on a folder and optionally its subfolders and documents
- [SetFolderRules](SetFolderRules) - Set the rules and policies for a folder (with optional tree propagation)
- [UpdateFolderProperties](UpdateFolderProperties) - Update a folder's name and description

### Document Management
- [AddDocumentComment](AddDocumentComment) - Add a comment to a document
- [AddISOComment](AddISOComment) - Add an ISO compliance review comment to a document (requires an active ISO Review Task)
- [AddSOXComment](AddSOXComment) - Add a Sarbanes-Oxley (SOX) compliance comment to a document
- [AddToFavorites](AddToFavorites) - Add a document or folder to the current user's favorites list
- [Copy](Copy) - Copy a document or folder to a specified destination path
- [CreateDiskMountURL](CreateDiskMountURL) - Create a time-limited WebDAV root mount URL for the current user
- [CreateDocumentShortcut](CreateDocumentShortcut) - Create a shortcut (.lnk) document pointing to an existing document
- [CreateDocumentTypeDef](CreateDocumentTypeDef) - Create a new document type definition (admin only)
- [CreateDocumentUsingTemplate](CreateDocumentUsingTemplate) - Create a new HTML document or new version using a template and XML field data
- [CreateEditDocumentURL](CreateEditDocumentURL) - Create a time-limited WebDAV URL for opening and editing a specific document
- [CreateURL](CreateURL) - Create or update a URL document that stores a hyperlink
- [CreateUploadHandler](CreateUploadHandler) - Create a server-side upload handler for chunked large file uploads
- [DeleteDocument](DeleteDocument) - Move a document to the recycle bin
- [DeleteDocumentComment](DeleteDocumentComment) - Delete a specific comment from a document
- [DeleteDocumentTypeDef](DeleteDocumentTypeDef) - Delete a document type definition
- [DeleteDocumentVersion](DeleteDocumentVersion) - Permanently delete a specific version of a document
- [DeleteDownloadHandler](DeleteDownloadHandler) - Delete a download handler and discard its temporary file
- [DeleteUploadHandler](DeleteUploadHandler) - Delete an upload handler and discard its staged temporary file
- [DocumentExists](DocumentExists) - Check whether a document exists and return its CRC32 checksums
- [DocumentExists1](DocumentExists1) - Check whether a document exists by folder path and document name, returning CRC32 checksums
- [DownloadDocument](DownloadDocument) - Download the latest version of a document as a raw byte array
- [DownloadDocumentVersion](DownloadDocumentVersion) - Download a specific version of a document as a raw byte array
- [DownloadFileChunk](DownloadFileChunk) - Download a single chunk of a staged file using a download handler
- [DownloadZip](DownloadZip) - Zip and download specified documents and folders as a raw byte array
- [DownloadZipWithHandler](DownloadZipWithHandler) - Stage a zip archive server-side and return a handler GUID for chunked retrieval
- [GetAuthoredDocuments](GetAuthoredDocuments) - Get documents authored by a specified user
- [GetCheckedoutDocuments](GetCheckedoutDocuments) - Get checked out documents for the current authenticated user
- [GetCheckedoutDocumentsByUser](GetCheckedoutDocumentsByUser) - Get checked out documents for a specified user
- [GetDocument](GetDocument) - Get the full properties of a document by path or short ID
- [GetDocumentAbstract](GetDocumentAbstract) - Get the full-text abstract of a document version (obsolete; use GetDocumentAbstract1)
- [GetDocumentAbstract1](GetDocumentAbstract1) - Get the full-text abstract of a document version
- [GetDocumentComments](GetDocumentComments) - Get all comments attached to a document
- [GetDocumentKeywords](GetDocumentKeywords) - Get user-defined keywords assigned to a document
- [GetDocumentTextOnlyContent](GetDocumentTextOnlyContent) - Get the stored plain-text alternative content of the latest published version of a document
- [GetDocumentTypes](GetDocumentTypes) - Get all document type definitions configured in the system
- [GetDocumentVersion](GetDocumentVersion) - Get the metadata for a specific version of a document
- [GetDocumentVersions](GetDocumentVersions) - Get the complete version history for a document
- [GetDocumentViewLog](GetDocumentViewLog) - Get the complete view/access log for a specified document
- [GetDocuments](GetDocuments) - Get the full properties of every document in a folder path
- [GetDocuments1](GetDocuments1) - Get the list of documents in a folder path in short form
- [GetDocumentsByPage](GetDocumentsByPage) - Get a paged list of documents in a folder path in short form with optional name filtering
- [GetDownloadHandler](GetDownloadHandler) - Stage the latest version of a document and return a download handler GUID for chunked retrieval
- [GetDownloadHandlerByVersion](GetDownloadHandlerByVersion) - Stage a specific version of a document and return a download handler GUID for chunked retrieval
- [GetDownloadInfo](GetDownloadInfo) - Get download metadata for the latest version of a document without staging the file
- [GetDownloadInfoByVersion](GetDownloadInfoByVersion) - Get download metadata for a specific version of a document without staging the file
- [GetDownloadQue](GetDownloadQue) - Get the list of documents and folders in the current user's download queue
- [GetFavorites](GetFavorites) - Get the list of documents and folders marked as favorites by the current user
- [GetISOReviewAssignments](GetISOReviewAssignments) - Get documents assigned to a user for ISO review
- [GetPublishingRequirements](GetPublishingRequirements) - Get the publishing requirements configured for a domain/library
- [GetRecentDocuments](GetRecentDocuments) - Get the list of documents recently accessed by the current authenticated user
- [GetVersionTextOnlyContent](GetVersionTextOnlyContent) - Get the plain-text alternative content stored for a specific version of a document
- [IsLockPossible](IsLockPossible) - Check whether the current user can lock (check out) the document at the specified path
- [Lock](Lock) - Lock (check out) the document or all documents in a folder at the specified path
- [PublishDocument](PublishDocument) - Set the published version of a document
- [RegisterEmail](RegisterEmail) - Register an email message as a document in infoRouter
- [RegisterEmail1](RegisterEmail1) - Register an email message as a document in infoRouter and set user-defined keywords
- [RegisterEmail2](RegisterEmail2) - Register an email message using separate folder path and document name parameters
- [RegisterEmail3](RegisterEmail3) - Register an email message passing all fields as a single XML string
- [RemoveDocumentCutoffDate](RemoveDocumentCutoffDate) - Remove the cutoff date from a document, returning it to an unconstrained state
- [RemoveExpirationDate](RemoveExpirationDate) - Remove the expiration date from a document, returning it to a non-expiring state
- [RemoveFromFavorites](RemoveFromFavorites) - Remove a document or folder from the current user's favorites list
- [ServerSideImport](ServerSideImport) - **[Obsolete]** Server-side file system import — always returns an error, do not use
- [SetClassificationLevel](SetClassificationLevel) - Set the classification level (NoMarkings/Declassified/Confidential/Secret/TopSecret) of a document or folder
- [SetDocumentCompletionStatus](SetDocumentCompletionStatus) - Set the completion status (PercentComplete and CompletionDate) of a document
- [SetDocumentCutoffDate](SetDocumentCutoffDate) - Apply a cutoff date to a document, freezing it from further modification
- [SetDocumentImportance](SetDocumentImportance) - Set the importance level (NoMarkings/Low/Normal/High/Vital) of a document
- [SetDocumentRetention](SetDocumentRetention) - **[Obsolete since 8.1.155]** Disabled — always returns an error, use SetDocumentRandDSchedule instead
- [SetDocumentTextOnlyContent](SetDocumentTextOnlyContent) - Update the stored plain-text alternative content of the latest document version
- [SetExpirationDate](SetExpirationDate) - Set the expiration date and pre-expiration notification on a document
- [SetVersionTextOnlyContent](SetVersionTextOnlyContent) - Update the stored plain-text alternative content of a specific document version
- [UnLock](UnLock) - Unlock (check in) a document or all documents in a folder
- [UnpublishDocument](UnpublishDocument) - Set a document to unpublished state, hiding it from read-only users
- [UpdateDocumentKeywords](UpdateDocumentKeywords) - Replace the user-defined keyword string of a document
- [UpdateDocumentProperties](UpdateDocumentProperties) - Update a document's name, description, and update instructions
- [UpdateDocumentProperties1](UpdateDocumentProperties1) - Update a document's name, description, instructions, source, language, and author
- [UpdateDocumentProperties2](UpdateDocumentProperties2) - Update all document properties including importance level
- [UpdateDocumentType](UpdateDocumentType) - Change the document type assigned to a document
- [UpdateDocumentTypeDef](UpdateDocumentTypeDef) - Rename a document type definition and change its required property set
- [UploadDocument](UploadDocument) - Upload a new document or new version using a raw byte array
- [UploadDocument1](UploadDocument1) - Upload a new document or version with an optional version comment
- [UploadDocument2](UploadDocument2) - Upload a new document or version with a post-upload checkout option
- [UploadDocument3](UploadDocument3) - Upload a new document or version with both version comment and checkout
- [UploadDocument4](UploadDocument4) - Upload a new document or version with extended XML parameters
- [UploadDocumentWithHandler](UploadDocumentWithHandler) - Finalize a chunked upload and create/version a document
- [UploadDocumentWithHandler1](UploadDocumentWithHandler1) - Finalize a chunked upload with an optional version comment
- [UploadDocumentWithHandler2](UploadDocumentWithHandler2) - Finalize a chunked upload with version comment and manual version numbers
- [UploadDocumentWithHandler3](UploadDocumentWithHandler3) - Finalize a chunked upload with extended XML parameters
- [UploadFileChunk](UploadFileChunk) - Upload a single binary chunk to a server-side upload handler
- [UploadNewDocumentWidthHandler](UploadNewDocumentWidthHandler) - Upload a new document to a folder using a chunked handler and XML parameters
- [UploadTiffAsPDF](UploadTiffAsPDF) - Upload a TIFF image and store it as a PDF document
- [UploadTiffAsPDFWithHandler](UploadTiffAsPDFWithHandler) - Upload a large TIFF image using chunked handler and store as PDF
- [VerifyVersionHash](VerifyVersionHash) - Verify the integrity of a document version by comparing its stored content hash

### Security & Access Control
- [ApplyInheritedAccessList](ApplyInheritedAccessList) - Apply the inherited (parent) access list to a document or folder, removing any custom security settings
- [DocumentAccessAllowed](DocumentAccessAllowed) - Check whether the calling user is allowed to perform a specific action on a document
- [FolderAccessAllowed](FolderAccessAllowed) - Check whether the calling user is allowed to perform a specific action on a folder
- [GetAccessList](GetAccessList) - Get the current access list (security permissions) for a document or folder
- [GetAccessListHistory](GetAccessListHistory) - Get the current and historical access list records for a document or folder
- [GetOwner](GetOwner) - Get the owner of a document or folder
- [SetAccessList](SetAccessList) - Set the access list (security permissions) for a document or folder
- [SetOwner](SetOwner) - Set the owner of a document or folder

### Domain/Library Management
- [AddManagerToDomain](AddManagerToDomain) - Add an existing user as a manager of a domain/library
- [AddUserAsDomainMember](AddUserAsDomainMember) - Add a user to the member list of a domain/library
- [AddUserGroupAsDomainMember](AddUserGroupAsDomainMember) - Add a global user group to the member list of a domain/library
- [ArchiveDomain](ArchiveDomain) - Archive a domain/library to make it an archived (offline) library
- [CreateDomain](CreateDomain) - Create a new domain/library with name, access, and visibility settings
- [DeleteDomain](DeleteDomain) - Permanently delete a domain/library and all its contents
- [DomainExists](DomainExists) - Check whether a domain/library with the given name exists
- [GetDomain](GetDomain) - Get the properties of a domain/library (ID, name, archive status, visibility)
- [GetDomainFlows](GetDomainFlows) - Get workflow definitions associated with a domain/library
- [GetDomainMembers](GetDomainMembers) - Get the list of user and group members of a domain/library
- [GetDomainMembers1](GetDomainMembers1) - Get domain/library members with sort order and detail-mode control
- [GetDomainMembershipsOfUser](GetDomainMembershipsOfUser) - Get all domain/library memberships for a specified user
- [GetDomainPolicies](GetDomainPolicies) - Get policies and rules for a domain/library
- [GetDomainStatistics](GetDomainStatistics) - Get statistics for a domain/library
- [GetDomainUsers](GetDomainUsers) - Get all users of a domain/library including indirect group members
- [GetDomainUsers1](GetDomainUsers1) - Get all domain/library users with sort order and detail-mode control
- [GetDomains](GetDomains) - Get the list of all domains/libraries in the system
- [GetManagedDomainsByUser](GetManagedDomainsByUser) - Get domains/libraries managed by a specified user
- [GetManagers](GetManagers) - Get the list of managers of a domain/library
- [GetMemberDomains](GetMemberDomains) - Get the domains/libraries where the current user is a member
- [RemoveManagerFromDomain](RemoveManagerFromDomain) - Remove manager status from a user in a domain/library
- [RemoveUserFromDomainMembership](RemoveUserFromDomainMembership) - Remove a user from a domain/library member list
- [SetDomainPolicies](SetDomainPolicies) - Set policies for a domain/library
- [UnarchiveDomain](UnarchiveDomain) - Un-archive a domain/library to make it an active online library
- [UpdateDomain](UpdateDomain) - Update domain/library properties (name, anonymous access, visibility, welcome message)

### Workflow Management
- [ActivateFlowDef](ActivateFlowDef) - Activate a workflow definition
- [AddFlowStepDef](AddFlowStepDef) - Add a new step to an inactive workflow definition (step number auto-assigned)
- [AddFlowStepDef1](AddFlowStepDef1) - Add a new step to an inactive workflow definition with an optional on-start folder move
- [AddFlowTaskDef](AddFlowTaskDef) - Add a task definition to a step of an inactive workflow definition
- [ChangeTaskDueDate](ChangeTaskDueDate) - Change the due date and allowed start time span of an active workflow task
- [CompleteTask](CompleteTask) - Mark a workflow task as completed and trigger automatic workflow advancement
- [CreateFlowDef](CreateFlowDef) - Create a new workflow definition (minimal variant: name, domain, active folder)
- [CreateFlowDef1](CreateFlowDef1) - Create a new workflow definition with an on-end destination folder
- [CreateFlowDef2](CreateFlowDef2) - Create a new workflow definition with an on-end folder and a supervisor
- [CreateFlowDef3](CreateFlowDef3) - Create a new workflow definition with all options (on-end folder, supervisor, event URL, hidden flag)
- [DeactivateFlowDef](DeactivateFlowDef) - Set a workflow definition back to inactive state so its steps and tasks can be modified
- [DeleteFlowStepDef](DeleteFlowStepDef) - Delete a step from a workflow definition
- [DeleteTask](DeleteTask) - Delete an active workflow task and all its attachments by task ID
- [GetDueTaskDocuments](GetDueTaskDocuments) - Return documents that have active (due) workflow tasks assigned to the authenticated user, sorted by due date
- [GetFlowDef](GetFlowDef) - Return the complete definition of a workflow including all step and task definitions
- [GetFolderFlows](GetFolderFlows) - Return workflow definitions active on a folder, optionally including inherited flows from parent folders
- [GetTask](GetTask) - Return the full details of a single workflow task including status, assignee, dates, requirements, and attachments
- [GetUserTaskRedirectionTo](GetUserTaskRedirectionTo) - Return the task redirection configured for a user (the user their tasks are being forwarded to)
- [GetUserTaskRedirectionsFrom](GetUserTaskRedirectionsFrom) - Return the list of users who are redirecting their tasks to a specified user
- [DeleteFlowTaskDef](DeleteFlowTaskDef) - Delete a task definition from a workflow step
- [DeleteWorkflow](DeleteWorkflow) - Permanently delete a workflow definition by ID
- [getTasks](getTasks) - Get a filtered list of workflow tasks with sorting and XML-based search criteria
- [GetUsersTaskPerformance](GetUsersTaskPerformance) - Get user task performance statistics (due and overdue task counts)
- [GetUsersWorkflowRoles](GetUsersWorkflowRoles) - Get workflow roles assigned to a user (supervisor and assignee roles)
- [GetWorkflowStatistics](GetWorkflowStatistics) - Get workflow performance statistics (pending, completed, overdue counts)

### Retention & Disposition
- [GetRetentionSourceAuthorities](GetRetentionSourceAuthorities) - List all retention source authorities
- [CreateRetentionSourceAuthority](CreateRetentionSourceAuthority) - Create a new retention source authority
- [UpdateRetentionSourceAuthority](UpdateRetentionSourceAuthority) - Update (rename) a retention source authority
- [DeleteRetentionSourceAuthority](DeleteRetentionSourceAuthority) - Delete a retention source authority

### User Group Management
- [AddUsergroupMember](AddUsergroupMember) - Add a user to a user group
- [CreateUserGroup](CreateUserGroup) - Create a new user group (global or domain-level)
- [CreateUserGroup1](CreateUserGroup1) - Create a new user group with member visibility control
- [DeleteUsergroup](DeleteUsergroup) - Delete a user group
- [GetDomainGroups](GetDomainGroups) - Get all user groups (local and global) in a domain/library
- [GetGlobalGroups](GetGlobalGroups) - Get all global user groups in the system
- [GetGroupMembershipsOfUser](GetGroupMembershipsOfUser) - Get user group memberships for a specified user
- [GetLocalGroups](GetLocalGroups) - Get local user groups of a domain/library
- [GetUserGroup](GetUserGroup) - Get properties of a specific user group
- [GetUserGroupMembers](GetUserGroupMembers) - Get members of a user group (fixed sort, full detail)
- [GetUserGroupMembers1](GetUserGroupMembers1) - Get members of a user group with configurable sort and detail
- [RemoveUserGroupFromDomainMembership](RemoveUserGroupFromDomainMembership) - Remove a user group from a domain/library member list
- [RemoveUsergroupMember](RemoveUsergroupMember) - Remove a user from a user group
- [UpdateUserGroupName](UpdateUserGroupName) - Rename a user group
- [UpdateUserGroupName1](UpdateUserGroupName1) - Rename a user group and update member visibility setting

### Search
- [GetNextSearchPage](GetNextSearchPage) - Get the next page of a prepared search result set
- [GetPreviousSearchPage](GetPreviousSearchPage) - Get the previous page of a prepared search result set
- [Search](Search) - Prepare a search result set using XML-based criteria with sorting options

### Subscription Management
- [GetSubscriptionsByUser](GetSubscriptionsByUser) - Retrieve folder and document subscriptions for a specific user
- [RemoveAllSubscriptions](RemoveAllSubscriptions) - Remove all folder and document subscriptions for a user
- [RemoveUserFromFolderSubscribers](RemoveUserFromFolderSubscribers) - Remove a user from a folder's subscription list

### User Management
- [AddPropertySetRowForUser](AddPropertySetRowForUser) - Add a property set row to a user
- [ChangeUserStatus](ChangeUserStatus) - Enable or disable a user account
- [ChangeUserType](ChangeUserType) - Change a user's type (author or read-only)
- [CreateUser](CreateUser) - Create a new infoRouter user account
- [DeletePropertySetRowForUser](DeletePropertySetRowForUser) - Delete a property set row from a user
- [DeleteUser](DeleteUser) - Delete a user account
- [DeleteUser1](DeleteUser1) - Delete a user account with administrator password confirmation
- [GetAllUsers](GetAllUsers) - Get all users with full detail
- [GetAllUsers1](GetAllUsers1) - Paged and filtered user list with sorting
- [GetAllUsers2](GetAllUsers2) - Paged and filtered user list with user type filter
- [GetAllUsersWithoutDetails](GetAllUsersWithoutDetails) - Paged user list without preference details
- [GetCoWorkers](GetCoWorkers) - Get co-workers of the current user (fixed sort, full detail)
- [GetCoWorkers1](GetCoWorkers1) - Get co-workers with configurable sort and detail level
- [GetCurrentUser](GetCurrentUser) - Get properties of the currently authenticated user
- [GetDomainMembershipsOfUser](GetDomainMembershipsOfUser) - Get domain/library memberships of a specified user
- [GetLocalUsers](GetLocalUsers) - Get direct (local) user members of a domain/library
- [GetUser](GetUser) - Get full properties of a specific user
- [GetUserStatistics](GetUserStatistics) - Get activity and membership statistics for a user
- [TransferUserCheckedOutDocuments](TransferUserCheckedOutDocuments) - Transfer checked-out document ownership between users
- [TransferUserDocumentOwnerships](TransferUserDocumentOwnerships) - Transfer document ownerships between users
- [TransferUserDocumentSubscriptions](TransferUserDocumentSubscriptions) - Transfer document subscriptions between users
- [TransferUserDomainManagerRoles](TransferUserDomainManagerRoles) - Transfer domain manager roles between users
- [TransferUserDomainMemberships](TransferUserDomainMemberships) - Transfer domain/library memberships between users
- [TransferUserExpirationNotices](TransferUserExpirationNotices) - Transfer document expiration notices between users
- [TransferUserFolderOwnerships](TransferUserFolderOwnerships) - Transfer folder ownerships between users
- [TransferUserFolderSubscriptions](TransferUserFolderSubscriptions) - Transfer folder subscriptions between users
- [TransferUserGroupMemberships](TransferUserGroupMemberships) - Transfer user group memberships between users
- [TransferUserISOTasks](TransferUserISOTasks) - Transfer ISO review tasks between users
- [TransferUserSecurityPermissions](TransferUserSecurityPermissions) - Transfer security (ACL) permissions between users
- [TransferUserTasks](TransferUserTasks) - Transfer open workflow tasks between users
- [TransferUserWorkflowDefinitions](TransferUserWorkflowDefinitions) - Transfer workflow definition roles between users
- [UpdateUserEmail](UpdateUserEmail) - Update a user's email address
- [UpdateUserPreferences](UpdateUserPreferences) - Update a user's display and notification preferences
- [UpdateUserProfile](UpdateUserProfile) - Update a user's name, username, and authentication source
- [UserExists](UserExists) - Check if a username exists

## Common Patterns

### Authentication
```xml
POST /srv.asmx/AuthenticateUser
Content-Type: application/x-www-form-urlencoded

UID=username&PWD=password
```

Response:
```xml
<root success="true" ticket="abc123-def456-..." />
```

### Error Handling
All APIs return errors in this format:
```xml
<root success="false" error="[ErrorCode] Error message" />
```

## Response Format

All API responses follow this structure:
```xml
<root success="true|false" error="error message if failed">
  <!-- Response data -->
</root>
```

## API Endpoints

- **SOAP**: `https://yourserver/srv.asmx`
- **REST**: `https://yourserver/srv.asmx/[MethodName]`

## Support

For additional information and support:
- GitHub: [https://github.com/inforouter/webserver](https://github.com/inforouter/webserver)
- Support Site: [https://support.inforouter.com](https://support.inforouter.com)

## Version

Compatible with infoRouter 8.7 and later.

---

*Last Updated: 2026*
