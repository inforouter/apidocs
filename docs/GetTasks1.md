# GetTasks1 API

Returns a paged list of workflow tasks based on XML search criteria. Identical to [getTasks](GetTasks.md) but adds `startingRow` and `rowCount` parameters for pagination. The response includes `startingRow` and `rowCount` attributes in addition to `taskCount` so clients can page through large result sets.

## Endpoint

```
/srv.asmx/GetTasks1
```

## Methods

- **GET** `/srv.asmx/GetTasks1?AuthenticationTicket=...&xmlcriteria=...&startingRow=...&rowCount=...&SortBy=...&AscendingOrder=...`
- **POST** `/srv.asmx/GetTasks1` (form data)
- **SOAP** Action: `http://tempuri.org/GetTasks1`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `xmlcriteria` | string | Yes | XML string containing filter criteria (see XML Criteria Format below) |
| `startingRow` | integer | Yes | Zero-based index of the first row to return. Pass `0` to start from the beginning |
| `rowCount` | integer | Yes | Maximum number of tasks to return per page. Defaults to `100` when `0` or negative |
| `SortBy` | string | Yes | Sort field name from `TaskSortOption` enum (see Sort Options below) |
| `AscendingOrder` | boolean | Yes | `true` for ascending sort, `false` for descending |

## XML Criteria Format

The `xmlcriteria` parameter accepts an XML string with `<param>` elements, each specifying a `NAME` and `VALUE` attribute. All filter parameters are optional — omit a parameter to skip that filter.

```xml
<criteria>
  <param NAME="TASKCOMPLETIONSTATUS" VALUE="Due" />
  <param NAME="PRIORITY" VALUE="High" />
  <param NAME="STARTDATE" VALUE="2026-01-01" />
  <param NAME="ENDDATE" VALUE="2026-12-31" />
  <param NAME="DOMAINID" VALUE="1" />
  <param NAME="ASSIGNEEID" VALUE="42" />
  <param NAME="ASSIGNEDBYID" VALUE="15" />
  <param NAME="SUPERVISORID" VALUE="10" />
  <param NAME="WORKFLOWDEFID" VALUE="5" />
  <param NAME="DOCUMENTID" VALUE="100" />
  <param NAME="FLOWID" VALUE="200" />
  <param NAME="DOCUMENTTYPE" VALUE="Invoice" />
</criteria>
```

### Filter Parameters

| NAME | Value Type | Description |
|------|-----------|-------------|
| `TASKCOMPLETIONSTATUS` | string (enum) | Filter by task completion status (see values below) |
| `PRIORITY` | string (enum) | Filter by task priority (see values below) |
| `STARTDATE` | DateTime | Filter tasks with start date on or after this date |
| `ENDDATE` | DateTime | Filter tasks with start date on or before this date |
| `DOMAINID` / `LIBRARYID` | integer | Filter by domain/library ID (both names accepted) |
| `ASSIGNEEID` | integer | Filter by assignee user ID |
| `ASSIGNEDBYID` | integer | Filter by the user ID who assigned the task |
| `SUPERVISORID` | integer | Filter by supervisor user ID |
| `WORKFLOWDEFID` | integer | Filter by workflow definition ID |
| `DOCUMENTID` | integer | Filter by document ID |
| `FLOWID` | integer | Filter by workflow instance (flow) ID |
| `DOCUMENTTYPE` | string | Filter by document type name |

### TaskCompletionStatus Values

| Value | Description |
|-------|-------------|
| `NoCompletionStatus` | No filter (default) |
| `Due` | Tasks that are currently due |
| `OverDue` | Tasks that are past their due date |
| `Completed` | Completed tasks |
| `NotStarted` | Tasks that have not been started yet |
| `Reassigned` | Tasks that have been reassigned |
| `Dropped` | Tasks that have been dropped |
| `Archived` | Archived tasks |

### TaskPriority Values

| Value | Description |
|-------|-------------|
| `NoPriortySetting` | No priority filter (default) |
| `Low` | Low priority |
| `Normal` | Normal priority |
| `High` | High priority |
| `Urgent` | Urgent priority |

## Sort Options

The `SortBy` parameter accepts one of the following `TaskSortOption` values:

| Value | Description |
|-------|-------------|
| `DefaultSort` | Default sort order |
| `DocumentID` | Sort by document ID |
| `Instruction` | Sort by task instruction |
| `DateAssigned` | Sort by date assigned |
| `RecurringEndBy` | Sort by recurring end date |
| `DueDate` | Sort by due date |
| `ReminderDate` | Sort by reminder date |
| `Priority` | Sort by priority level |
| `TaskStatus` | Sort by task status |
| `FinishDate` | Sort by finish date |
| `Assignee` | Sort by assignee name |
| `AssignedBy` | Sort by assigner name |
| `WorkflowName` | Sort by workflow name |
| `DocTypeName` | Sort by document type name |
| `DocumentLibrary` | Sort by document library |
| `DocumentName` | Sort by document name |
| `SuperVisor` | Sort by supervisor name |

## Response Structure

### Success Response

```xml
<response success="true" taskCount="250" startingRow="0" rowCount="100">
  <tasks>
    <Task>
      <TaskID>301</TaskID>
      <TaskName>Review Document</TaskName>
      <ShortInstruction>Please review and approve this document.</ShortInstruction>
      <StepNumber>2</StepNumber>
      <StepName>Review Step</StepName>
      <FlowID>50</FlowID>
      <FlowName>Document Approval</FlowName>
      <FlowDefID>5</FlowDefID>
      <Priority>High</Priority>
      <TaskStatus>InProgress</TaskStatus>
      <ApprovalStatus>Pending</ApprovalStatus>
      <StartDate>2026-02-01 09:00:00</StartDate>
      <StartDtae>2026-02-01 09:00:00</StartDtae>
      <FinishDate></FinishDate>
      <DueDate>2026-02-15 17:00:00</DueDate>
      <ShortComments></ShortComments>
      <TaskDefID>101</TaskDefID>
      <LinkedTaskID>0</LinkedTaskID>
      <AssigneeID>42</AssigneeID>
      <AssigneeType>User</AssigneeType>
      <AssigneeName>John Smith</AssigneeName>
      <AssignedByID>15</AssignedByID>
      <AssignedByName>Jane Doe</AssignedByName>
      <SuperVisorID>10</SuperVisorID>
      <SupervisorName>Admin User</SupervisorName>
      <DocumentID>1234</DocumentID>
      <DocumentName>Q1_Report.docx</DocumentName>
      <StartVersionNumber>1.0</StartVersionNumber>
      <EndVersionNumber>0.0</EndVersionNumber>
      <DocumentTypeId>3</DocumentTypeId>
      <DocumentTypeName>Report</DocumentTypeName>
      <DocumentFolderID>500</DocumentFolderID>
      <DocumentLibraryID>1</DocumentLibraryID>
      <DocumentLibraryName>Main Library</DocumentLibraryName>
      <DocumentCheckedOutByID>0</DocumentCheckedOutByID>
      <DocumentCheckedOutByName></DocumentCheckedOutByName>
      <DocumentTemplateID>0</DocumentTemplateID>
      <RedirectedFrom_UserID>0</RedirectedFrom_UserID>
      <RedirectedFrom_UserName></RedirectedFrom_UserName>
      <AdHoc>false</AdHoc>
      <DeadLine>14</DeadLine>
      <RightType RightTypeId="2" RightTypeName="READ" RightTypeText="Read Only" />
      <Permissions>
        <Permission Name="EditDocument" Value="False" />
        <Permission Name="ChangeFinishdate" Value="False" />
        <Permission Name="Postpone" Value="False" />
        <Permission Name="ChangePriority" Value="False" />
        <Permission Name="EditNextStep" Value="False" />
        <Permission Name="EditAllSteps" Value="False" />
      </Permissions>
      <RequirementDetails>
        <Requirement>
          <Name>Approval Required</Name>
          <RequirementType>Approval</RequirementType>
          <Definition>Manager approval needed</Definition>
          <ObjectId>1</ObjectId>
        </Requirement>
      </RequirementDetails>
      <Requirements></Requirements>
      <Supervisor_NotificationOnDue>1</Supervisor_NotificationOnDue>
      <SupervisorNotificationDate>2026-02-14 09:00:00</SupervisorNotificationDate>
      <AllowedStartTimeSpan>0</AllowedStartTimeSpan>
      <AllowedStartDate></AllowedStartDate>
      <ReminderTimeSpan>1</ReminderTimeSpan>
      <ReminderDate>2026-02-14 09:00:00</ReminderDate>
      <Attachments>
        <Attachment>
          <AttachmentDate>2026-02-05 10:30:00</AttachmentDate>
          <DocumentId>1235</DocumentId>
          <DocumentName>SupportingEvidence.pdf</DocumentName>
          <Path>/Main Library/Contracts</Path>
          <WorkflowId>50</WorkflowId>
          <StepNumber>1</StepNumber>
          <StepName>Submit Step</StepName>
          <UserId>15</UserId>
        </Attachment>
      </Attachments>
    </Task>
    <!-- ... up to rowCount tasks ... -->
  </tasks>
</response>
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

## Response Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `success` | boolean | `true` if the request succeeded, `false` otherwise |
| `taskCount` | integer | Total number of tasks matching the filter criteria (across all pages) |
| `startingRow` | integer | The zero-based row offset used for this page |
| `rowCount` | integer | Number of `<Task>` elements returned in this response (≤ requested `rowCount`) |
| `error` | string | Present only when `success="false"`. Contains the error code and message |

## Task Element Properties

| Element | Type | Description |
|---------|------|-------------|
| `TaskID` | integer | Unique identifier of the task instance |
| `TaskName` | string | Name of the task |
| `ShortInstruction` | string | First 255 characters of the task instruction. For the full text use [GetTask](GetTask.md) which also returns `extendedInstruction` |
| `StepNumber` | integer | Step number within the workflow |
| `StepName` | string | Name of the workflow step |
| `FlowID` | integer | Workflow instance (flow) ID |
| `FlowName` | string | Name of the workflow definition |
| `FlowDefID` | integer | Workflow definition ID |
| `Priority` | string | Task priority: `Low`, `Normal`, `High`, `Urgent` |
| `TaskStatus` | string | Current task status |
| `ApprovalStatus` | string | Approval status of the task |
| `StartDate` | DateTime | Task start date. **Use this element.** |
| `StartDtae` | DateTime | **Deprecated.** Same value as `StartDate`. Retained for backward compatibility only (typo in an earlier release). Do not use in new integrations |
| `FinishDate` | DateTime | Task completion date (empty if not finished) |
| `DueDate` | DateTime | Task due date |
| `ShortComments` | string | First 255 characters of the assignee's comments. For the full text use [GetTask](GetTask.md) which also returns `extendedComment` |
| `TaskDefID` | integer | Task definition ID |
| `LinkedTaskID` | integer | ID of a linked task (0 if none) |
| `AssigneeID` | integer | User ID of the task assignee |
| `AssigneeType` | string | Type of assignee: `User` or `Group` |
| `AssigneeName` | string | Display name of the assignee |
| `AssignedByID` | integer | User ID of who assigned the task |
| `AssignedByName` | string | Display name of the assigner |
| `SuperVisorID` | integer | User ID of the task supervisor |
| `SupervisorName` | string | Display name of the supervisor |
| `DocumentID` | integer | ID of the document associated with the task |
| `DocumentName` | string | Name of the associated document |
| `StartVersionNumber` | string | Document version when the task started |
| `EndVersionNumber` | string | Document version when the task ended |
| `DocumentTypeId` | integer | Document type definition ID |
| `DocumentTypeName` | string | Document type name |
| `DocumentFolderID` | integer | Folder ID containing the document |
| `DocumentLibraryID` | integer | Library/domain ID of the document |
| `DocumentLibraryName` | string | Library/domain name |
| `DocumentCheckedOutByID` | integer | User ID who has the document checked out (0 if not checked out) |
| `DocumentCheckedOutByName` | string | Name of user who has document checked out |
| `DocumentTemplateID` | integer | Template ID used for the document (0 if none) |
| `RedirectedFrom_UserID` | integer | Original assignee user ID if task was redirected (0 if not redirected) |
| `RedirectedFrom_UserName` | string | Original assignee name if redirected |
| `AdHoc` | boolean | Whether this is an ad-hoc task |
| `DeadLine` | integer | Deadline in hours from task creation. `0` means no deadline. |
| `RightType` | XML element | Document access right required by this task. Attributes: `RightTypeId` (integer: `0`=NOACCESS … `6`=FULLCONTROL), `RightTypeName` (enum name, e.g. `READ`), `RightTypeText` (localized label). |
| `Permissions` | XML element | Six task-assignee permissions. Each `<Permission Name="..." Value="True\|False"/>`: `EditDocument`, `ChangeFinishdate`, `Postpone`, `ChangePriority`, `EditNextStep`, `EditAllSteps`. |
| `RequirementDetails` | XML | Nested list of task requirements |
| `Requirements` | string | Requirements summary |
| `Supervisor_NotificationOnDue` | integer | Days before due date to notify supervisor |
| `SupervisorNotificationDate` | DateTime | Date when supervisor notification is sent |
| `AllowedStartTimeSpan` | integer | Time span before task can be started |
| `AllowedStartDate` | DateTime | Earliest allowed start date |
| `ReminderTimeSpan` | integer | Reminder time span in days |
| `ReminderDate` | DateTime | Date when reminder is sent |
| `Attachments` | XML | Nested list of workflow attachments. Each `<Attachment>` includes `<AttachmentDate>`, `<DocumentId>`, `<DocumentName>`, `<Path>` (folder path only), `<WorkflowId>`, `<StepNumber>`, `<StepName>`, and `<UserId>` |

## Required Permissions

- User must be authenticated (valid authentication ticket required)
- Anonymous users cannot call this API (returns insufficient rights error)
- Tasks returned are scoped to the authenticated user's permissions

## Pagination

Use `taskCount`, `startingRow`, and `rowCount` together to implement full pagination:

```
Page 1: startingRow=0,   rowCount=100  → returns tasks 0–99
Page 2: startingRow=100, rowCount=100  → returns tasks 100–199
Page 3: startingRow=200, rowCount=100  → returns tasks 200–249 (taskCount=250)
```

When the returned `rowCount` attribute is less than the requested `rowCount`, you have reached the last page.

## Example Requests

### Request (GET)

```
GET /srv.asmx/GetTasks1?AuthenticationTicket=abc123&xmlcriteria=<criteria><param NAME="TASKCOMPLETIONSTATUS" VALUE="Due" /></criteria>&startingRow=0&rowCount=50&SortBy=DueDate&AscendingOrder=true HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/GetTasks1 HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=abc123&xmlcriteria=<criteria><param NAME="TASKCOMPLETIONSTATUS" VALUE="Due" /></criteria>&startingRow=0&rowCount=50&SortBy=DueDate&AscendingOrder=true
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetTasks1"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetTasks1 xmlns="http://tempuri.org/">
      <AuthenticationTicket>abc123-def456</AuthenticationTicket>
      <xmlcriteria><![CDATA[<criteria><param NAME="TASKCOMPLETIONSTATUS" VALUE="Due" /></criteria>]]></xmlcriteria>
      <startingRow>0</startingRow>
      <rowCount>50</rowCount>
      <SortBy>DueDate</SortBy>
      <AscendingOrder>true</AscendingOrder>
    </GetTasks1>
  </soap:Body>
</soap:Envelope>
```

## Notes

- When `rowCount` is `0` or negative the server defaults to `100` rows per page.
- `taskCount` always reflects the total number of matching tasks, not just the current page.
- The `xmlcriteria` parameter must be valid XML. An empty criteria element `<criteria></criteria>` returns all tasks visible to the authenticated user.
- Filter parameters are case-insensitive for the `NAME` attribute (internally converted to uppercase).
- Unrecognized parameter names in `xmlcriteria` will cause an error response.
- Invalid enum values for `SortBy`, `TASKCOMPLETIONSTATUS`, or `PRIORITY` will return a descriptive error.
- The response includes both `<StartDate>` (correct spelling, use this) and `<StartDtae>` (legacy typo, deprecated).
- Task requirements and attachments are dynamically loaded for each task in the result set.

## Error Codes

| Error | Description |
|-------|-------------|
| `[901]Session expired or Invalid ticket` | Invalid or expired authentication ticket |
| `[2730]Insufficient rights. Anonymous users cannot perform this action` | User is not authenticated (anonymous) |
| `[SortBy] error:...` | Invalid `SortBy` value — must be a valid `TaskSortOption` enum name |
| `xmlcriteria parsing error:...` | The `xmlcriteria` parameter is not valid XML |
| `[PARAMETER_NAME] error:...` | Invalid value for a specific filter parameter |
| `[PARAMETER_NAME] Parameter not found` | Unrecognized parameter name in `xmlcriteria` |

## Related APIs

- [getTasks](GetTasks.md) - Same API without paging (returns all matching tasks)
- [GetTask](GetTask.md) - Get a single task by task ID with full instruction and comment text
- [GetUsersTaskPerformance](GetUsersTaskPerformance.md) - Get user task performance statistics
