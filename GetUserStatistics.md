# GetUserStatistics API

Returns activity and membership statistics for a specified user, including document counts, folder counts, task counts, workflow roles, and library memberships.

## Endpoint

```
/srv.asmx/GetUserStatistics
```

## Methods

- **GET** `/srv.asmx/GetUserStatistics?authenticationTicket=...&userName=...`
- **POST** `/srv.asmx/GetUserStatistics` (form data)
- **SOAP** Action: `http://tempuri.org/GetUserStatistics`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `userName` | string | Yes | The user name to retrieve statistics for |

## Response

### Success Response

```xml
<root success="true">
  <UserStatistics>
    <!-- Document Statistics -->
    <TotalDocuments>142</TotalDocuments>
    <CheckedOutDocuments>3</CheckedOutDocuments>
    <ViewedDocuments>58</ViewedDocuments>
    <SubscribedDocuments>12</SubscribedDocuments>
    <FavoriteDocuments>7</FavoriteDocuments>
    <VotedDocuments>4</VotedDocuments>
    <DocumentsInDownloadQueue>0</DocumentsInDownloadQueue>
    <RecycledDocuments>2</RecycledDocuments>
    <!-- Folder Statistics -->
    <TotalFolders>35</TotalFolders>
    <SubscribedFolders>8</SubscribedFolders>
    <FavoriteFolders>3</FavoriteFolders>
    <FoldersInDownloadQueue>0</FoldersInDownloadQueue>
    <RecycledFolders>1</RecycledFolders>
    <!-- Task Statistics -->
    <QueuedTasks>5</QueuedTasks>
    <TasksDueToday>1</TasksDueToday>
    <TasksDueThisWeek>3</TasksDueThisWeek>
    <OverdueTasks>0</OverdueTasks>
    <TotalTasks>5</TotalTasks>
    <TasksAssignedToOthers>2</TasksAssignedToOthers>
    <!-- Workflow and ISO Statistics -->
    <WorkflowRoles>2</WorkflowRoles>
    <IsoReviewerRoles>1</IsoReviewerRoles>
    <!-- Library Memberships and Roles -->
    <DomainMemberships>4</DomainMemberships>
    <GlobalGroupMemberships>3</GlobalGroupMemberships>
    <LocalGroupMemberships>5</LocalGroupMemberships>
    <DomainManagerRoles>1</DomainManagerRoles>
    <ExpirationAgentRoles>0</ExpirationAgentRoles>
  </UserStatistics>
</root>
```

### Error Response

```xml
<root success="false" error="[ErrorCode] Error message" />
```

## UserStatistics Properties

### Document Statistics

| Property | Type | Description |
|----------|------|-------------|
| `TotalDocuments` | integer | Total number of documents owned or authored by the user |
| `CheckedOutDocuments` | integer | Number of documents currently checked out by the user |
| `ViewedDocuments` | integer | Number of documents the user has viewed |
| `SubscribedDocuments` | integer | Number of documents the user is subscribed to |
| `FavoriteDocuments` | integer | Number of documents marked as favorites by the user |
| `VotedDocuments` | integer | Number of documents the user has voted on |
| `DocumentsInDownloadQueue` | integer | Number of documents in the user's download queue |
| `RecycledDocuments` | integer | Number of documents in the user's recycle bin |

### Folder Statistics

| Property | Type | Description |
|----------|------|-------------|
| `TotalFolders` | integer | Total number of folders owned by the user |
| `SubscribedFolders` | integer | Number of folders the user is subscribed to |
| `FavoriteFolders` | integer | Number of folders marked as favorites by the user |
| `FoldersInDownloadQueue` | integer | Number of folders in the user's download queue |
| `RecycledFolders` | integer | Number of folders in the user's recycle bin |

### Task Statistics

| Property | Type | Description |
|----------|------|-------------|
| `QueuedTasks` | integer | Number of workflow tasks currently queued for the user |
| `TasksDueToday` | integer | Number of tasks due today |
| `TasksDueThisWeek` | integer | Number of tasks due this week (including today) |
| `OverdueTasks` | integer | Number of overdue tasks assigned to the user |
| `TotalTasks` | integer | Total number of workflow tasks assigned to the user |
| `TasksAssignedToOthers` | integer | Number of tasks the user has assigned to other users |

### Workflow and ISO Statistics

| Property | Type | Description |
|----------|------|-------------|
| `WorkflowRoles` | integer | Number of workflow definitions in which the user has an assignee or supervisor role |
| `IsoReviewerRoles` | integer | Number of ISO review assignments for the user |

### Library Memberships and Roles

| Property | Type | Description |
|----------|------|-------------|
| `DomainMemberships` | integer | Number of libraries/domains the user is a member of |
| `GlobalGroupMemberships` | integer | Number of global user groups the user belongs to |
| `LocalGroupMemberships` | integer | Number of local (domain-level) user groups the user belongs to |
| `DomainManagerRoles` | integer | Number of libraries/domains for which the user is a domain manager |
| `ExpirationAgentRoles` | integer | Number of libraries/domains for which the user is assigned as expiration agent |

## Required Permissions

- The caller must be authenticated.
- A user may call this API for themselves.
- Calling this API for another user requires the `ListingAuditLogOfUser` permission.

## Example

### Request (GET)

```
GET /srv.asmx/GetUserStatistics?authenticationTicket=abc123-def456&userName=jsmith HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/GetUserStatistics HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&userName=jsmith
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetUserStatistics"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetUserStatistics xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
      <userName>jsmith</userName>
    </GetUserStatistics>
  </soap:Body>
</soap:Envelope>
```

## Notes

- `TasksDueToday` and `TasksDueThisWeek` counts include only tasks that have not yet been completed or rejected.
- `OverdueTasks` counts tasks whose due date has passed and are not yet completed.
- `TasksAssignedToOthers` reflects tasks the user created/submitted that are assigned to other users.
- `DomainMemberships`, `GlobalGroupMemberships`, and `LocalGroupMemberships` reflect direct and indirect memberships.
- Statistics are calculated in real-time from the current database state.

## Related APIs

- `GetCurrentUser` - Get properties of the currently authenticated user
- `getTasks` - Get workflow tasks with filtering options
- `GetCheckedoutDocumentsByUser` - Get checked out documents for a user
- `GetSubscriptionsByUser` - Get folder and document subscriptions for a user
- `GetUsersWorkflowRoles` - Get workflow roles assigned to a user
- `GetGroupMembershipsOfUser` - Get user group memberships for a user

## Error Codes

| Error | Description |
|-------|-------------|
| `[901] Session expired or Invalid ticket` | Invalid or expired authentication ticket |
| `User not found` | The specified user name does not exist |
| `Insufficient rights` | Caller does not have permission to view another user's statistics |
