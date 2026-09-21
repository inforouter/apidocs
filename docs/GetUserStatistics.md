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
    <NotStartedTasks>2</NotStartedTasks>
    <OverDueTasks>4</OverDueTasks>
    <DueTodayTasks>1</DueTodayTasks>
    <DueThisWeekTasks>3</DueThisWeekTasks>
    <DueLaterTasks>1</DueLaterTasks>
    <DueTasks>9</DueTasks>
    <OpenTasks>11</OpenTasks>
    <TasksAssignedToOthers>2</TasksAssignedToOthers>
    <TaskFilterDates>
      <DueTodayFrom>2026-09-21T14:32:05</DueTodayFrom>
      <DueTodayTo>2026-09-22T00:00:00</DueTodayTo>
      <DueThisWeekFrom>2026-09-22T00:00:00</DueThisWeekFrom>
      <DueThisWeekTo>2026-09-28T00:00:00</DueThisWeekTo>
      <DueLaterFrom>2026-09-28T00:00:00</DueLaterFrom>
    </TaskFilterDates>
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
| `NotStartedTasks` | integer | Tasks whose workflow step has not been reached. They carry no due date and nobody can act on them yet |
| `OverDueTasks` | integer | Open, started, and past their due date |
| `DueTodayTasks` | integer | Due between now and midnight tonight, and so not yet overdue |
| `DueThisWeekTasks` | integer | Due after today and before the week is out |
| `DueLaterTasks` | integer | Due after this week |
| `DueTasks` | integer | Every open task that has started: the four above added together |
| `OpenTasks` | integer | `NotStartedTasks` + `DueTasks` |
| `TasksAssignedToOthers` | integer | Tasks the user assigned. Note this counts tasks assigned to **anyone**, the user included, and unlike every other count here it takes group- and role-assigned tasks too |
| `TaskFilterDates` | element | The window boundaries the counts were taken with - see below |

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

## JavaScript

Every call answers XML with HTTP 200, success or not, so `success` is the thing to branch on and
`errorCode` is the number to report.

```javascript
async function call(action, params) {
  const response = await fetch(`/srv.asmx/${action}?${new URLSearchParams(params)}`);
  const root = new DOMParser()
    .parseFromString(await response.text(), 'text/xml')
    .documentElement;

  if (root.getAttribute('success') !== 'true') {
    throw new Error(`${root.getAttribute('errorCode')}: ${root.getAttribute('error')}`);
  }
  return root;
}
```

Counts what one user has across the system.

```javascript
const value = (await call('GetUserStatistics', { authenticationTicket: ticket, userName: 'jsmith' }))
  .querySelector('Value');

Number(value.querySelector('TotalDocuments').textContent);
Number(value.querySelector('OverDueTasks').textContent);
```

The `<Value>` element holds twenty-one counters, each as its own child element:

`TotalDocuments`, `CheckedOutDocuments`, `ViewedDocuments`, `SubscribedDocuments`,
`FavoriteDocuments`, `VotedDocuments`, `DocumentsInDownloadQueue`, `RecycledDocuments`,
`TotalFolders`, `SubscribedFolders`, `FavoriteFolders`, `FoldersInDownloadQueue`,
`RecycledFolders`, `NotStartedTasks`, `OverDueTasks`, `DueTodayTasks`, `DueThisWeekTasks`,
`DueLaterTasks`, `DueTasks`, `OpenTasks`, `TasksAssignedToOthers` - and one element,
`TaskFilterDates`.

Every count is `0` for a new account. This is the call to make before
[DeleteUser](DeleteUser.md) to find out whether there is anything to transfer.

## Opening the list behind a count

**Every task count is one [getTasks](getTasks.md) call**, and is named after the
`TaskCompletionStatus` filter that reproduces it. Pass `AssigneeId` as the user's id in all of them:

| Count | `CompletionStatus` | `StartDate` | `EndDate` |
|---|---|---|---|
| `NotStartedTasks` | `NotStarted` | — | — |
| `OverDueTasks` | `OverDue` | — | — |
| `DueTodayTasks` | `Due` | `DueTodayFrom` | `DueTodayTo` |
| `DueThisWeekTasks` | `Due` | `DueThisWeekFrom` | `DueThisWeekTo` |
| `DueLaterTasks` | `Due` | `DueLaterFrom` | — |
| `DueTasks` | `Due` | — | — |

`AssigneeId` is load-bearing. Without it - or one of `AssignedById` / `SupervisorId` naming the same
user - GetTasks widens the query to everything the caller assigned, supervises **or manages**, which
for a library manager is every task in every library they administer. The number would then open a
list many times its own size.

`OpenTasks` has no single filter behind it: there is no "every open task" value in
`TaskCompletionStatus`. It is `NotStartedTasks + DueTasks`, so open it as those two calls, or show
it as a plain total rather than a link.

The dates to pass come back in the answer, in `TaskFilterDates`:

| | |
|---|---|
| `DueTodayFrom` | the moment the counts were taken; anything due before it is overdue |
| `DueTodayTo` | midnight tonight |
| `DueThisWeekFrom` | midnight tonight |
| `DueThisWeekTo` | midnight at the end of the week - the day after the coming Sunday |
| `DueLaterFrom` | the same moment as `DueThisWeekTo` |

Use them rather than working out "tomorrow" on the client: the client is in its own time zone, and
the list it opened would not be the one it counted.

## Notes

- **The four due counts are disjoint and add up.** `OverDueTasks + DueTodayTasks + DueThisWeekTasks + DueLaterTasks = DueTasks`, and `DueTasks + NotStartedTasks = OpenTasks`. They can be shown side by side without counting a task twice.
- Before 9.0 they were cumulative - "due today" meant *everything* due before midnight tonight, overdue tasks included, and "due this week" included both - so all three usually read the same number and adding them counted the same task three times. The names changed with the meaning.
- `NotStartedTasks` was called `QueuedTasks`; `OverdueTasks` is now `OverDueTasks`, spelled as the `TaskCompletionStatus` member is; `TotalTasks` is now `OpenTasks` and counts open work only, which is what it always did.
- A task can be due today **and** overdue: `OverDueTasks` is measured against the moment of the call, so a task due at 09:00 is overdue by lunchtime. The two counts are still disjoint, because `DueTodayTasks` starts where `OverDueTasks` ends. GetTasks measures `OverDue` against the moment of *its* call, so the boundary moves by the seconds between the two requests.
- Tasks assigned to a **group** the user belongs to are not in any of these counts, which all ask for tasks assigned to the user themselves. The exception is `TasksAssignedToOthers`, which filters on who assigned the task and not on who it went to.
- Only tasks on documents in ordinary libraries are counted.
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

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4041` | no user by that name |
| `4000` | the caller has no ticket - where most operations answer `4010` for that |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
