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
- [AuthenticateUser](AuthenticateUser.md) - Authenticate with user name and password, returns ticket and profile info
- [AuthenticateUser1](AuthenticateUser1.md) - Authenticate with user name, password, and an explicit session language
- [AuthenticateUserViaWindows](AuthenticateUserViaWindows.md) - Authenticate using the Windows identity (NTLM/Kerberos) from the HTTP request context
- [ChangePasswordUsingSecretText](ChangePasswordUsingSecretText.md) - Complete a password reset using the one-time token emailed by ForgotPassword
- [ChangeUserPassword](ChangeUserPassword.md) - Change a user's password (self-service or User Manager)
- [CreateTicketforUser](CreateTicketforUser.md) - Create an authentication ticket for any user using the server-side trusted password (server-to-server impersonation)
- [ForgotPassword](ForgotPassword.md) - Initiate a password reset by sending a one-time token to the user's registered email address
- [ForgotPasswordByUserName](ForgotPasswordByUserName.md) - Initiate a password reset by login name (sends token to the user's registered email address)
- [isValidTicket](isValidTicket.md) - Check whether an authentication ticket is still valid without supplying credentials or extending the expiration
- [LogOut](LogOut.md) - Invalidate an authentication ticket and clear the server-side session
- [RenewTicket](RenewTicket.md) - Validate credentials and renew an existing ticket or issue a fresh one

### Application Settings & Configuration
- [FlushApplicationCache](FlushApplicationCache.md) - Flush the in-memory application cache (admin only)
- [getApplicationParameters](getApplicationParameters.md) - Get application parameters (role-based response: public, regular user, or full admin view)
- [GetAllFolderColumns](GetAllFolderColumns.md) - Get all 34 available folder column definitions
- [GetAuthenticationAndPasswordPolicy](GetAuthenticationAndPasswordPolicy.md) - Get authentication and password policy settings (complexity requirements, re-prompt actions)
- [GetDefaultFolderColumns](GetDefaultFolderColumns.md) - Get the system default folder columns for list views
- [GetGeneralAppSettings](GetGeneralAppSettings.md) - Get general application settings including upload limits, work days, holidays, and system preferences
- [GetMimeTypes](GetMimeTypes.md) - Get the list of all defined MIME types in the system
- [GetSystemBehaviorSettings](GetSystemBehaviorSettings.md) - Get system behavior settings (login logging, anti-brute-force, library manager permissions)
- [SetAuthenticationAndPasswordPolicy](SetAuthenticationAndPasswordPolicy.md) - Update authentication and password policy settings (complexity rules, expiration policies)
- [SetDefaultFolderColumns](SetDefaultFolderColumns.md) - Set the system default folder columns using comma-separated column names
- [SetGeneralAppSettings](SetGeneralAppSettings.md) - Update general application settings (upload limits, recycle bin policies, workdays/holidays)
- [SetSystemBehaviorSettings](SetSystemBehaviorSettings.md) - Update system behavior settings (login logging and login delay configuration)

### Server & License Management
- [GetLicenseInfo](GetLicenseInfo.md) - Get application license details, user counts, and subscription dates (admin only)
- [GetLogs](GetLogs.md) - Get server log entries by type and date (admin only)
- [GetLogStatistics](GetLogStatistics.md) - Get available log dates and entry counts by log type (admin only)
- [GetMaintenanceJobsStatus](GetMaintenanceJobsStatus.md) - Get status of all system maintenance jobs (admin only)
- [GetWarehouseStatus](GetWarehouseStatus.md) - Get warehouse storage status, document counts, and disk information (admin only)
- [ServerInfo](ServerInfo.md) - Get server version, time, and basic license info (no authentication required)
- [UpdateApplicationLicense](UpdateApplicationLicense.md) - Update the application license file (admin only)

### Audit Logs
- [GetCheckInLog](GetCheckInLog.md) - Get check-in log entries for documents
- [GetCheckoutLog](GetCheckoutLog.md) - Get checkout log entries for documents
- [GetDeleteLog](GetDeleteLog.md) - Get deletion log entries for documents and folders
- [GetDispositionLog](GetDispositionLog.md) - Get disposition log entries for documents
- [GetNewDocumentsAndFoldersLog](GetNewDocumentsAndFoldersLog.md) - Get creation log entries for new documents and folders
- [GetOwnershipChangeLog](GetOwnershipChangeLog.md) - Get ownership change log entries for documents and folders
- [GetSecurityChangeLog](GetSecurityChangeLog.md) - Get security change log entries for documents and folders
- [GetUserViewLog](GetUserViewLog.md) - Get the complete read/view log history for a specified user
- [GetUserViewLog1](GetUserViewLog1.md) - Get the read/view log history for a specified user filtered by date range
- [GetVersionCreateLog](GetVersionCreateLog.md) - Get version creation log entries for documents
- [GetVersionDeleteLog](GetVersionDeleteLog.md) - Get version deletion log entries for documents

### Folder & Document Listing
- [GetFoldersAndDocuments](GetFoldersAndDocuments.md) - Return immediate sub-folders and documents in a path with full detail options
- [GetFoldersAndDocuments1](GetFoldersAndDocuments1.md) - Return immediate sub-folders and documents in short form (abbreviated elements, minimal attributes)
- [GetFoldersAndDocuments2](GetFoldersAndDocuments2.md) - Return immediate sub-folders and documents in lightweight ultra-fast format
- [GetFoldersAndDocumentsByPage](GetFoldersAndDocumentsByPage.md) - Return a paged list of sub-folders and documents with optional name filtering
- [GetFoldersAndDocumentsByPage2](GetFoldersAndDocumentsByPage2.md) - Return a paged list with advanced XML filtering and sorting via search engine
- [GetMyDocumentsAndFolders](GetMyDocumentsAndFolders.md) - Return all documents and folders owned by the currently authenticated user

### Folder Management
- [CreateFolder](CreateFolder.md) - Create a folder from a single full path (intermediate folders created automatically)
- [CreateFolder1](CreateFolder1.md) - Create a subfolder with optional description using separate parent path and name parameters
- [DeleteFolder](DeleteFolder.md) - Delete a folder and all its contents
- [FolderExists](FolderExists.md) - Check whether a folder exists at the specified path
- [FolderExists1](FolderExists1.md) - Check whether a named subfolder exists within a specified parent folder
- [GetFolder](GetFolder.md) - Get the full properties of a folder with optional rules, property sets, security, and owner details
- [GetFolderCatalog](GetFolderCatalog.md) - Get the catalog information for a folder
- [GetFolderRules](GetFolderRules.md) - Get the rules and policies configured for a folder
- [GetFolderStatistics](GetFolderStatistics.md) - Get statistics for a folder (subfolder count, document count, total size)
- [GetFolders](GetFolders.md) - Get the list of direct subfolders with full property details
- [GetFolders1](GetFolders1.md) - Get the list of direct subfolders in short form (no count limit)
- [GetFolders2](GetFolders2.md) - Get the list of direct subfolders in short form with configured UI display limit
- [GetFoldersByPage](GetFoldersByPage.md) - Get a paged list of direct subfolders with optional name filtering
- [GetParentFolderIDs](GetParentFolderIDs.md) - Get the chain of parent folder IDs from root to the specified folder
- [GetSubFoldersCount](GetSubFoldersCount.md) - Get the count of direct subfolders in a folder
- [Move](Move.md) - Move a document or folder to a new destination path
- [RemoveFolderCutoffDate](RemoveFolderCutoffDate.md) - Remove the cutoff date from a folder and optionally its subfolders and documents
- [SetFolderCutoffDate](SetFolderCutoffDate.md) - Set the cutoff date on a folder and optionally its subfolders and documents
- [SetFolderRules](SetFolderRules.md) - Set the rules and policies for a folder (with optional tree propagation)
- [UpdateFolderProperties](UpdateFolderProperties.md) - Update a folder's name and description

### Document Management
- [AddDocumentComment](AddDocumentComment.md) - Add a comment to a document
- [AddISOComment](AddISOComment.md) - Add an ISO compliance review comment to a document (requires an active ISO Review Task)
- [AddSOXComment](AddSOXComment.md) - Add a Sarbanes-Oxley (SOX) compliance comment to a document
- [AddToFavorites](AddToFavorites.md) - Add a document or folder to the current user's favorites list
- [Copy](Copy.md) - Copy a document or folder to a specified destination path
- [CreateDiskMountURL](CreateDiskMountURL.md) - Create a time-limited WebDAV root mount URL for the current user
- [CreateDocumentShortcut](CreateDocumentShortcut.md) - Create a shortcut (.lnk) document pointing to an existing document
- [CreateDocumentTypeDef](CreateDocumentTypeDef.md) - Create a new document type definition (admin only)
- [CreateDocumentUsingTemplate](CreateDocumentUsingTemplate.md) - Create a new HTML document or new version using a template and XML field data
- [CreateEditDocumentURL](CreateEditDocumentURL.md) - Create a time-limited WebDAV URL for opening and editing a specific document
- [CreateURL](CreateURL.md) - Create or update a URL document that stores a hyperlink
- [CreateUploadHandler](CreateUploadHandler.md) - Create a server-side upload handler for chunked large file uploads
- [DeleteDocument](DeleteDocument.md) - Move a document to the recycle bin
- [DeleteDocumentComment](DeleteDocumentComment.md) - Delete a specific comment from a document
- [DeleteDocumentTypeDef](DeleteDocumentTypeDef.md) - Delete a document type definition
- [DeleteDocumentVersion](DeleteDocumentVersion.md) - Permanently delete a specific version of a document
- [DeleteDownloadHandler](DeleteDownloadHandler.md) - Delete a download handler and discard its temporary file
- [DeleteUploadHandler](DeleteUploadHandler.md) - Delete an upload handler and discard its staged temporary file
- [DocumentExists](DocumentExists.md) - Check whether a document exists and return its CRC32 checksums
- [DocumentExists1](DocumentExists1.md) - Check whether a document exists by folder path and document name, returning CRC32 checksums
- [DownloadDocument](DownloadDocument.md) - Download the latest version of a document as a raw byte array
- [DownloadDocumentVersion](DownloadDocumentVersion.md) - Download a specific version of a document as a raw byte array
- [DownloadFileChunk](DownloadFileChunk.md) - Download a single chunk of a staged file using a download handler
- [DownloadZip](DownloadZip.md) - Zip and download specified documents and folders as a raw byte array
- [DownloadZipWithHandler](DownloadZipWithHandler.md) - Stage a zip archive server-side and return a handler GUID for chunked retrieval
- [GetAuthoredDocuments](GetAuthoredDocuments.md) - Get documents authored by a specified user
- [GetCheckedoutDocuments](GetCheckedoutDocuments.md) - Get checked out documents for the current authenticated user
- [GetCheckedoutDocumentsByUser](GetCheckedoutDocumentsByUser.md) - Get checked out documents for a specified user
- [GetDocument](GetDocument.md) - Get the full properties of a document by path or short ID
- [GetDocumentAbstract](GetDocumentAbstract.md) - Get the full-text abstract of a document version (obsolete; use GetDocumentAbstract1)
- [GetDocumentAbstract1](GetDocumentAbstract1.md) - Get the full-text abstract of a document version
- [GetDocumentComments](GetDocumentComments.md) - Get all comments attached to a document
- [GetDocumentKeywords](GetDocumentKeywords.md) - Get user-defined keywords assigned to a document
- [GetDocumentTextOnlyContent](GetDocumentTextOnlyContent.md) - Get the stored plain-text alternative content of the latest published version of a document
- [GetDocumentTypes](GetDocumentTypes.md) - Get all document type definitions configured in the system
- [GetDocumentVersion](GetDocumentVersion.md) - Get the metadata for a specific version of a document
- [GetDocumentVersions](GetDocumentVersions.md) - Get the complete version history for a document
- [GetDocumentViewLog](GetDocumentViewLog.md) - Get the complete view/access log for a specified document
- [GetDocuments](GetDocuments.md) - Get the full properties of every document in a folder path
- [GetDocuments1](GetDocuments1.md) - Get the list of documents in a folder path in short form
- [GetDocumentsByPage](GetDocumentsByPage.md) - Get a paged list of documents in a folder path in short form with optional name filtering
- [GetDownloadHandler](GetDownloadHandler.md) - Stage the latest version of a document and return a download handler GUID for chunked retrieval
- [GetDownloadHandlerByVersion](GetDownloadHandlerByVersion.md) - Stage a specific version of a document and return a download handler GUID for chunked retrieval
- [GetDownloadInfo](GetDownloadInfo.md) - Get download metadata for the latest version of a document without staging the file
- [GetDownloadInfoByVersion](GetDownloadInfoByVersion.md) - Get download metadata for a specific version of a document without staging the file
- [GetDownloadQue](GetDownloadQue.md) - Get the list of documents and folders in the current user's download queue
- [GetFavorites](GetFavorites.md) - Get the list of documents and folders marked as favorites by the current user
- [GetISOReviewAssignments](GetISOReviewAssignments.md) - Get documents assigned to a user for ISO review
- [GetPublishingRequirements](GetPublishingRequirements.md) - Get the publishing requirements configured for a domain/library
- [GetRecentDocuments](GetRecentDocuments.md) - Get the list of documents recently accessed by the current authenticated user
- [GetVersionTextOnlyContent](GetVersionTextOnlyContent.md) - Get the plain-text alternative content stored for a specific version of a document
- [IsLockPossible](IsLockPossible.md) - Check whether the current user can lock (check out) the document at the specified path
- [Lock](Lock.md) - Lock (check out) the document or all documents in a folder at the specified path
- [PublishDocument](PublishDocument.md) - Set the published version of a document
- [RegisterEmail](RegisterEmail.md) - Register an email message as a document in infoRouter
- [RegisterEmail1](RegisterEmail1.md) - Register an email message as a document in infoRouter and set user-defined keywords
- [RegisterEmail2](RegisterEmail2.md) - Register an email message using separate folder path and document name parameters
- [RegisterEmail3](RegisterEmail3.md) - Register an email message passing all fields as a single XML string
- [RemoveDocumentCutoffDate](RemoveDocumentCutoffDate.md) - Remove the cutoff date from a document, returning it to an unconstrained state
- [RemoveExpirationDate](RemoveExpirationDate.md) - Remove the expiration date from a document, returning it to a non-expiring state
- [RemoveFromFavorites](RemoveFromFavorites.md) - Remove a document or folder from the current user's favorites list
- [ServerSideImport](ServerSideImport.md) - **[Obsolete]** Server-side file system import — always returns an error, do not use
- [SetClassificationLevel](SetClassificationLevel.md) - Set the classification level (NoMarkings/Declassified/Confidential/Secret/TopSecret) of a document or folder
- [SetDocumentCompletionStatus](SetDocumentCompletionStatus.md) - Set the completion status (PercentComplete and CompletionDate) of a document
- [SetDocumentCutoffDate](SetDocumentCutoffDate.md) - Apply a cutoff date to a document, freezing it from further modification
- [SetDocumentImportance](SetDocumentImportance.md) - Set the importance level (NoMarkings/Low/Normal/High/Vital) of a document
- [SetDocumentRetention](SetDocumentRetention.md) - **[Obsolete since 8.1.155]** Disabled — always returns an error, use SetDocumentRandDSchedule instead
- [SetDocumentTextOnlyContent](SetDocumentTextOnlyContent.md) - Update the stored plain-text alternative content of the latest document version
- [SetExpirationDate](SetExpirationDate.md) - Set the expiration date and pre-expiration notification on a document
- [SetVersionTextOnlyContent](SetVersionTextOnlyContent.md) - Update the stored plain-text alternative content of a specific document version
- [UnLock](UnLock.md) - Unlock (check in) a document or all documents in a folder
- [UnpublishDocument](UnpublishDocument.md) - Set a document to unpublished state, hiding it from read-only users
- [UpdateDocumentKeywords](UpdateDocumentKeywords.md) - Replace the user-defined keyword string of a document
- [UpdateDocumentProperties](UpdateDocumentProperties.md) - Update a document's name, description, and update instructions
- [UpdateDocumentProperties1](UpdateDocumentProperties1.md) - Update a document's name, description, instructions, source, language, and author
- [UpdateDocumentProperties2](UpdateDocumentProperties2.md) - Update all document properties including importance level
- [UpdateDocumentType](UpdateDocumentType.md) - Change the document type assigned to a document
- [UpdateDocumentTypeDef](UpdateDocumentTypeDef.md) - Rename a document type definition and change its required property set
- [UploadDocument](UploadDocument.md) - Upload a new document or new version using a raw byte array
- [UploadDocument1](UploadDocument1.md) - Upload a new document or version with an optional version comment
- [UploadDocument2](UploadDocument2.md) - Upload a new document or version with a post-upload checkout option
- [UploadDocument3](UploadDocument3.md) - Upload a new document or version with both version comment and checkout
- [UploadDocument4](UploadDocument4.md) - Upload a new document or version with extended XML parameters
- [UploadDocumentWithHandler](UploadDocumentWithHandler.md) - Finalize a chunked upload and create/version a document
- [UploadDocumentWithHandler1](UploadDocumentWithHandler1.md) - Finalize a chunked upload with an optional version comment
- [UploadDocumentWithHandler2](UploadDocumentWithHandler2.md) - Finalize a chunked upload with version comment and manual version numbers
- [UploadDocumentWithHandler3](UploadDocumentWithHandler3.md) - Finalize a chunked upload with extended XML parameters
- [UploadFileChunk](UploadFileChunk.md) - Upload a single binary chunk to a server-side upload handler
- [UploadNewDocumentWidthHandler](UploadNewDocumentWidthHandler.md) - Upload a new document to a folder using a chunked handler and XML parameters
- [UploadTiffAsPDF](UploadTiffAsPDF.md) - Upload a TIFF image and store it as a PDF document
- [UploadTiffAsPDFWithHandler](UploadTiffAsPDFWithHandler.md) - Upload a large TIFF image using chunked handler and store as PDF
- [VerifyVersionHash](VerifyVersionHash.md) - Verify the integrity of a document version by comparing its stored content hash

### Security & Access Control
- [ApplyInheritedAccessList](ApplyInheritedAccessList.md) - Apply the inherited (parent) access list to a document or folder, removing any custom security settings
- [DocumentAccessAllowed](DocumentAccessAllowed.md) - Check whether the calling user is allowed to perform a specific action on a document
- [FolderAccessAllowed](FolderAccessAllowed.md) - Check whether the calling user is allowed to perform a specific action on a folder
- [GetAccessList](GetAccessList.md) - Get the current access list (security permissions) for a document or folder
- [GetAccessListHistory](GetAccessListHistory.md) - Get the current and historical access list records for a document or folder
- [GetOwner](GetOwner.md) - Get the owner of a document or folder
- [SetAccessList](SetAccessList.md) - Set the access list (security permissions) for a document or folder
- [SetOwner](SetOwner.md) - Set the owner of a document or folder

### Domain/Library Management
- [AddManagerToDomain](AddManagerToDomain.md) - Add an existing user as a manager of a domain/library
- [AddUserAsDomainMember](AddUserAsDomainMember.md) - Add a user to the member list of a domain/library
- [AddUserGroupAsDomainMember](AddUserGroupAsDomainMember.md) - Add a global user group to the member list of a domain/library
- [ArchiveDomain](ArchiveDomain.md) - Archive a domain/library to make it an archived (offline) library
- [CreateDomain](CreateDomain.md) - Create a new domain/library with name, access, and visibility settings
- [DeleteDomain](DeleteDomain.md) - Permanently delete a domain/library and all its contents
- [DomainExists](DomainExists.md) - Check whether a domain/library with the given name exists
- [GetDomain](GetDomain.md) - Get the properties of a domain/library (ID, name, archive status, visibility)
- [GetDomainFlows](GetDomainFlows.md) - Get workflow definitions associated with a domain/library
- [GetDomainMembers](GetDomainMembers.md) - Get the list of user and group members of a domain/library
- [GetDomainMembers1](GetDomainMembers1.md) - Get domain/library members with sort order and detail-mode control
- [GetDomainMembershipsOfUser](GetDomainMembershipsOfUser.md) - Get all domain/library memberships for a specified user
- [GetDomainPolicies](GetDomainPolicies.md) - Get policies and rules for a domain/library
- [GetDomainStatistics](GetDomainStatistics.md) - Get statistics for a domain/library
- [GetDomainUsers](GetDomainUsers.md) - Get all users of a domain/library including indirect group members
- [GetDomainUsers1](GetDomainUsers1.md) - Get all domain/library users with sort order and detail-mode control
- [GetDomains](GetDomains.md) - Get the list of all domains/libraries in the system
- [GetManagedDomainsByUser](GetManagedDomainsByUser.md) - Get domains/libraries managed by a specified user
- [GetManagers](GetManagers.md) - Get the list of managers of a domain/library
- [GetMemberDomains](GetMemberDomains.md) - Get the domains/libraries where the current user is a member
- [RemoveManagerFromDomain](RemoveManagerFromDomain.md) - Remove manager status from a user in a domain/library
- [RemoveUserFromDomainMembership](RemoveUserFromDomainMembership.md) - Remove a user from a domain/library member list
- [SetDomainPolicies](SetDomainPolicies.md) - Set policies for a domain/library
- [UnarchiveDomain](UnarchiveDomain.md) - Un-archive a domain/library to make it an active online library
- [UpdateDomain](UpdateDomain.md) - Update domain/library properties (name, anonymous access, visibility, welcome message)

### Workflow Management
- [ActivateFlowDef](ActivateFlowDef.md) - Activate a workflow definition
- [AddFlowStepDef](AddFlowStepDef.md) - Add a new step to an inactive workflow definition (step number auto-assigned)
- [AddFlowStepDef1](AddFlowStepDef1.md) - Add a new step to an inactive workflow definition with an optional on-start folder move
- [AddFlowTaskDef](AddFlowTaskDef.md) - Add a task definition to a step of an inactive workflow definition
- [ChangeTaskDueDate](ChangeTaskDueDate.md) - Change the due date and allowed start time span of an active workflow task
- [CompleteTask](CompleteTask.md) - Mark a workflow task as completed and trigger automatic workflow advancement
- [CreateFlowDef](CreateFlowDef.md) - Create a new workflow definition (minimal variant: name, domain, active folder)
- [CreateFlowDef1](CreateFlowDef1.md) - Create a new workflow definition with an on-end destination folder
- [CreateFlowDef2](CreateFlowDef2.md) - Create a new workflow definition with an on-end folder and a supervisor
- [CreateFlowDef3](CreateFlowDef3.md) - Create a new workflow definition with all options (on-end folder, supervisor, event URL, hidden flag)
- [DeactivateFlowDef](DeactivateFlowDef.md) - Set a workflow definition back to inactive state so its steps and tasks can be modified
- [DeleteFlowStepDef](DeleteFlowStepDef.md) - Delete a step from a workflow definition
- [DeleteTask](DeleteTask.md) - Delete an active workflow task and all its attachments by task ID
- [GetDueTaskDocuments](GetDueTaskDocuments.md) - Return documents that have active (due) workflow tasks assigned to the authenticated user, sorted by due date
- [GetFlowDef](GetFlowDef.md) - Return the complete definition of a workflow including all step and task definitions
- [GetFolderFlows](GetFolderFlows.md) - Return workflow definitions active on a folder, optionally including inherited flows from parent folders
- [GetTask](GetTask.md) - Return the full details of a single workflow task including status, assignee, dates, requirements, and attachments
- [GetUserTaskRedirectionTo](GetUserTaskRedirectionTo.md) - Return the task redirection configured for a user (the user their tasks are being forwarded to)
- [GetUserTaskRedirectionsFrom](GetUserTaskRedirectionsFrom.md) - Return the list of users who are redirecting their tasks to a specified user
- [DeleteFlowTaskDef](DeleteFlowTaskDef.md) - Delete a task definition from a workflow step
- [DeleteWorkflow](DeleteWorkflow.md) - Permanently delete a workflow definition by ID
- [getTasks](getTasks.md) - Get a filtered list of workflow tasks with sorting and XML-based search criteria
- [GetUsersTaskPerformance](GetUsersTaskPerformance.md) - Get user task performance statistics (due and overdue task counts)
- [GetUsersWorkflowRoles](GetUsersWorkflowRoles.md) - Get workflow roles assigned to a user (supervisor and assignee roles)
- [GetWorkflowStatistics](GetWorkflowStatistics.md) - Get workflow performance statistics (pending, completed, overdue counts)

### Retention & Disposition
- [GetRetentionSourceAuthorities](GetRetentionSourceAuthorities.md) - List all retention source authorities
- [CreateRetentionSourceAuthority](CreateRetentionSourceAuthority.md) - Create a new retention source authority
- [UpdateRetentionSourceAuthority](UpdateRetentionSourceAuthority.md) - Update (rename) a retention source authority
- [DeleteRetentionSourceAuthority](DeleteRetentionSourceAuthority.md) - Delete a retention source authority

### User Group Management
- [AddUsergroupMember](AddUsergroupMember.md) - Add a user to a user group
- [CreateUserGroup](CreateUserGroup.md) - Create a new user group (global or domain-level)
- [CreateUserGroup1](CreateUserGroup1.md) - Create a new user group with member visibility control
- [DeleteUsergroup](DeleteUsergroup.md) - Delete a user group
- [GetDomainGroups](GetDomainGroups.md) - Get all user groups (local and global) in a domain/library
- [GetGlobalGroups](GetGlobalGroups.md) - Get all global user groups in the system
- [GetGroupMembershipsOfUser](GetGroupMembershipsOfUser.md) - Get user group memberships for a specified user
- [GetLocalGroups](GetLocalGroups.md) - Get local user groups of a domain/library
- [GetUserGroup](GetUserGroup.md) - Get properties of a specific user group
- [GetUserGroupMembers](GetUserGroupMembers.md) - Get members of a user group (fixed sort, full detail)
- [GetUserGroupMembers1](GetUserGroupMembers1.md) - Get members of a user group with configurable sort and detail
- [RemoveUserGroupFromDomainMembership](RemoveUserGroupFromDomainMembership.md) - Remove a user group from a domain/library member list
- [RemoveUsergroupMember](RemoveUsergroupMember.md) - Remove a user from a user group
- [UpdateUserGroupName](UpdateUserGroupName.md) - Rename a user group
- [UpdateUserGroupName1](UpdateUserGroupName1.md) - Rename a user group and update member visibility setting

### Search
- [GetNextSearchPage](GetNextSearchPage.md) - Get the next page of a prepared search result set
- [GetPreviousSearchPage](GetPreviousSearchPage.md) - Get the previous page of a prepared search result set
- [Search](Search.md) - Prepare a search result set using XML-based criteria with sorting options

### Subscription Management
- [GetSubscriptionsByUser](GetSubscriptionsByUser.md) - Retrieve folder and document subscriptions for a specific user
- [RemoveAllSubscriptions](RemoveAllSubscriptions.md) - Remove all folder and document subscriptions for a user
- [RemoveUserFromFolderSubscribers](RemoveUserFromFolderSubscribers.md) - Remove a user from a folder's subscription list

### User Management
- [AddPropertySetRowForUser](AddPropertySetRowForUser.md) - Add a property set row to a user
- [ChangeUserStatus](ChangeUserStatus.md) - Enable or disable a user account
- [ChangeUserType](ChangeUserType.md) - Change a user's type (author or read-only)
- [CreateUser](CreateUser.md) - Create a new infoRouter user account
- [DeletePropertySetRowForUser](DeletePropertySetRowForUser.md) - Delete a property set row from a user
- [DeleteUser](DeleteUser.md) - Delete a user account
- [DeleteUser1](DeleteUser1.md) - Delete a user account with administrator password confirmation
- [GetAllUsers](GetAllUsers.md) - Get all users with full detail
- [GetAllUsers1](GetAllUsers1.md) - Paged and filtered user list with sorting
- [GetAllUsers2](GetAllUsers2.md) - Paged and filtered user list with user type filter
- [GetAllUsersWithoutDetails](GetAllUsersWithoutDetails.md) - Paged user list without preference details
- [GetCoWorkers](GetCoWorkers.md) - Get co-workers of the current user (fixed sort, full detail)
- [GetCoWorkers1](GetCoWorkers1.md) - Get co-workers with configurable sort and detail level
- [GetCurrentUser](GetCurrentUser.md) - Get properties of the currently authenticated user
- [GetDomainMembershipsOfUser](GetDomainMembershipsOfUser.md) - Get domain/library memberships of a specified user
- [GetLocalUsers](GetLocalUsers.md) - Get direct (local) user members of a domain/library
- [GetUser](GetUser.md) - Get full properties of a specific user
- [GetUserStatistics](GetUserStatistics.md) - Get activity and membership statistics for a user
- [TransferUserCheckedOutDocuments](TransferUserCheckedOutDocuments.md) - Transfer checked-out document ownership between users
- [TransferUserDocumentOwnerships](TransferUserDocumentOwnerships.md) - Transfer document ownerships between users
- [TransferUserDocumentSubscriptions](TransferUserDocumentSubscriptions.md) - Transfer document subscriptions between users
- [TransferUserDomainManagerRoles](TransferUserDomainManagerRoles.md) - Transfer domain manager roles between users
- [TransferUserDomainMemberships](TransferUserDomainMemberships.md) - Transfer domain/library memberships between users
- [TransferUserExpirationNotices](TransferUserExpirationNotices.md) - Transfer document expiration notices between users
- [TransferUserFolderOwnerships](TransferUserFolderOwnerships.md) - Transfer folder ownerships between users
- [TransferUserFolderSubscriptions](TransferUserFolderSubscriptions.md) - Transfer folder subscriptions between users
- [TransferUserGroupMemberships](TransferUserGroupMemberships.md) - Transfer user group memberships between users
- [TransferUserISOTasks](TransferUserISOTasks.md) - Transfer ISO review tasks between users
- [TransferUserSecurityPermissions](TransferUserSecurityPermissions.md) - Transfer security (ACL) permissions between users
- [TransferUserTasks](TransferUserTasks.md) - Transfer open workflow tasks between users
- [TransferUserWorkflowDefinitions](TransferUserWorkflowDefinitions.md) - Transfer workflow definition roles between users
- [UpdateUserEmail](UpdateUserEmail.md) - Update a user's email address
- [UpdateUserPreferences](UpdateUserPreferences.md) - Update a user's display and notification preferences
- [UpdateUserProfile](UpdateUserProfile.md) - Update a user's name, username, and authentication source
- [UserExists](UserExists.md) - Check if a username exists

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
