# GetDocumentTasks API

Returns all workflow tasks associated with a document, with optional filtering by completion status. Tasks are sorted by due date ascending.

## Endpoint

```
/srv.asmx/GetDocumentTasks
```

## Methods

- **GET** `/srv.asmx/GetDocumentTasks?authenticationTicket=...&documentPath=...&filter=...`
- **POST** `/srv.asmx/GetDocumentTasks` (form data)
- **SOAP** Action: `http://tempuri.org/GetDocumentTasks`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `documentPath` | string | Yes | Full infoRouter path of the document whose tasks should be returned (e.g. `/Finance/Reports/Q1Report.pdf`). |
| `filter` | string | No | Controls which tasks are returned. Valid values: `"current_tasks"` (active/due tasks only), `"task_history"` (archived/completed tasks only). Omit or pass any other value to return all tasks. |

## Response

### Success Response

```xml
<response success="true">
  <Value>
    <WorkflowExecutingTask>
      <TaskId>1042</TaskId>
      <FlowId>42</FlowId>
      <FlowDefId>7</FlowDefId>
      <FlowName>Document Approval</FlowName>
      <StepNumber>1</StepNumber>
      <StepName>Legal Review</StepName>
      <TaskDefId>305</TaskDefId>
      <TaskName>LegalReview</TaskName>
      <ShortInstruction>Please review the document for legal compliance.</ShortInstruction>
      <ShortComments></ShortComments>
      <StartDate>2026-04-01T08:00:00</StartDate>
      <FinishDate>0001-01-01T00:00:00</FinishDate>
      <DueDate>2026-04-04T08:00:00</DueDate>
      <DeadLine>72</DeadLine>
      <RightType RightTypeId="2" RightTypeName="READ" RightTypeText="Read Only" />
      <Permissions>
        <Permission Name="EditDocument" Value="False" />
        <Permission Name="ChangeFinishdate" Value="False" />
        <Permission Name="Postpone" Value="False" />
        <Permission Name="ChangePriority" Value="False" />
        <Permission Name="EditNextStep" Value="False" />
        <Permission Name="EditAllSteps" Value="False" />
      </Permissions>
      <Priority>Normal</Priority>
      <TaskStatus>InProgress</TaskStatus>
      <ApprovalStatus>NoResult</ApprovalStatus>
      <AssigneeId>101</AssigneeId>
      <AssigneeType>User</AssigneeType>
      <AssigneeName>jsmith</AssigneeName>
      <AssignedById>55</AssignedById>
      <AssignedByName>mwilson</AssignedByName>
      <SupervisorId>0</SupervisorId>
      <SupervisorName></SupervisorName>
      <DocumentId>1023</DocumentId>
      <DocumentName>agreement.pdf</DocumentName>
      <DocumentFolderId>88</DocumentFolderId>
      <DocumentLibraryId>3</DocumentLibraryId>
      <DocumentLibraryName>Corporate</DocumentLibraryName>
      <DocumentTypeId>1</DocumentTypeId>
      <DocumentTypeName>General</DocumentTypeName>
      <DocumentCheckedOutById>0</DocumentCheckedOutById>
      <DocumentCheckedOutByName></DocumentCheckedOutByName>
      <DocumentTemplateId>0</DocumentTemplateId>
      <StartVersionNumber>1</StartVersionNumber>
      <EndVersionNumber>1</EndVersionNumber>
      <LinkedTaskId>0</LinkedTaskId>
      <AdHoc>False</AdHoc>
      <AllowedStartTimeSpan>0</AllowedStartTimeSpan>
      <AllowedStartDate>0001-01-01T00:00:00</AllowedStartDate>
      <ReminderTimeSpan>0</ReminderTimeSpan>
      <ReminderDate>0001-01-01T00:00:00</ReminderDate>
      <SupervisorNotificationOnDue>0</SupervisorNotificationOnDue>
      <SupervisorNotificationDate>0001-01-01T00:00:00</SupervisorNotificationDate>
      <RedirectedFromUserId>0</RedirectedFromUserId>
      <RedirectedFromUserName></RedirectedFromUserName>
    </WorkflowExecutingTask>
  </Value>
</response>
```

When the document has no matching tasks the `<Value>` element is present but empty:

```xml
<response success="true">
  <Value />
</response>
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `TaskId` | integer | Unique ID of the task. Pass this to [GetTask](GetTask.md) to retrieve full task details including requirements and attachments. |
| `FlowId` | integer | ID of the running workflow instance the task belongs to. |
| `FlowDefId` | integer | ID of the workflow definition the task was created from. |
| `FlowName` | string | Name of the workflow. |
| `StepNumber` | integer | Step number within the workflow that owns this task. |
| `StepName` | string | Name of the workflow step. |
| `TaskDefId` | integer | ID of the task definition this task was created from. |
| `TaskName` | string | Display name of the task. |
| `ShortInstruction` | string | Short instruction text shown to the assignee. |
| `ShortComments` | string | Short comment text entered by the assignee. |
| `StartDate` | datetime | Date and time the task was started. `0001-01-01T00:00:00` if not yet started. |
| `FinishDate` | datetime | Date and time the task was finished. `0001-01-01T00:00:00` if still active. |
| `DueDate` | datetime | Deadline for the task. |
| `DeadLine` | integer | Deadline in hours from assignment time. `0` means no deadline. |
| `RightType` | XML element | Document access right required by this task. Attributes: `RightTypeId` (integer: `0`=NOACCESS, `1`=LIST, `2`=READ, `3`=ADD, `4`=ADDREAD, `5`=CHANGE, `6`=FULLCONTROL), `RightTypeName` (enum name, e.g. `READ`), `RightTypeText` (localized label). |
| `Permissions` | XML element | Six task-assignee permissions. Each `<Permission Name="..." Value="True\|False"/>`: `EditDocument`, `ChangeFinishdate`, `Postpone`, `ChangePriority`, `EditNextStep`, `EditAllSteps`. |
| `Priority` | string | Task priority. Values: `NoPriority`, `Low`, `Normal`, `High`, `Urgent`. |
| `TaskStatus` | string | Current task status. Values: `NotStarted`, `InProgress`, `DueDateChanged`, `Completed`, `Dropped`, `Reassigned`. |
| `ApprovalStatus` | string | Approval decision if the task has an Approval requirement. Values: `NoResult`, `Reject`, `Approve`. |
| `AssigneeId` | integer | User ID of the task assignee. |
| `AssigneeType` | string | Type of assignee. Values: `User`, `Group`. |
| `AssigneeName` | string | Username of the task assignee. |
| `AssignedById` | integer | User ID of the person who created/assigned the task. |
| `AssignedByName` | string | Username of the person who created/assigned the task. |
| `SupervisorId` | integer | User ID of the task supervisor. `0` if no supervisor. |
| `SupervisorName` | string | Username of the task supervisor. Empty string if no supervisor. |
| `DocumentId` | integer | Numeric ID of the document the task is on. |
| `DocumentName` | string | Display name of the document. |
| `DocumentFolderId` | integer | Numeric ID of the folder containing the document. |
| `DocumentLibraryId` | integer | Numeric ID of the domain/library that owns the document. |
| `DocumentLibraryName` | string | Name of the domain/library. |
| `DocumentTypeId` | integer | Numeric ID of the document type. |
| `DocumentTypeName` | string | Name of the document type. |
| `DocumentCheckedOutById` | integer | User ID of the user who has the document checked out. `0` if not checked out. |
| `DocumentCheckedOutByName` | string | Username of the user who has the document checked out. Empty string if not checked out. |
| `DocumentTemplateId` | integer | ID of the document template. `0` if none. |
| `StartVersionNumber` | integer | Starting document version number for this task. |
| `EndVersionNumber` | integer | Ending document version number for this task. |
| `LinkedTaskId` | integer | ID of the parent task this task was created from (for related/ad-hoc tasks). `0` if no parent. |
| `AdHoc` | boolean | `True` if this is an ad-hoc task created outside a workflow definition. |
| `AllowedStartTimeSpan` | integer | Number of hours before the due date within which the task may be started. `0` means no restriction. |
| `AllowedStartDate` | datetime | Earliest date/time the assignee can begin the task. `0001-01-01T00:00:00` if no restriction. |
| `ReminderTimeSpan` | integer | Number of hours before the due date when a reminder is sent. `0` means no reminder. |
| `ReminderDate` | datetime | Calculated date the reminder will be sent. `0001-01-01T00:00:00` if no reminder. |
| `SupervisorNotificationOnDue` | integer | Number of hours before the due date when the supervisor is notified. `0` means no notification. |
| `SupervisorNotificationDate` | datetime | Calculated date the supervisor notification will be sent. `0001-01-01T00:00:00` if no notification. |
| `RedirectedFromUserId` | integer | User ID of the original assignee if the task was redirected. `0` if not redirected. |
| `RedirectedFromUserName` | string | Username of the original assignee if the task was redirected. Empty string if not redirected. |

### Error Response

```xml
<response success="false" error="[901] Session expired or Invalid ticket" />
```

## Required Permissions

The calling user must have at least **read access** to the document.

## Example

### POST Request — active tasks only

```
POST /srv.asmx/GetDocumentTasks HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
&documentPath=%2FCorporate%2FContracts%2Fagreement.pdf
&filter=current_tasks
```

### GET Request — all tasks

```
GET /srv.asmx/GetDocumentTasks
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &documentPath=%2FCorporate%2FContracts%2Fagreement.pdf
HTTP/1.1
Host: yourserver
```

### GET Request — completed/archived tasks

```
GET /srv.asmx/GetDocumentTasks
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &documentPath=%2FCorporate%2FContracts%2Fagreement.pdf
    &filter=task_history
HTTP/1.1
Host: yourserver
```

## Notes

- `filter` is case-sensitive. Only `"current_tasks"` and `"task_history"` are treated specially; any other value (including omitting the parameter) returns all tasks.
- Results are sorted by due date ascending.
- `FinishDate`, `StartDate`, `AllowedStartDate`, `ReminderDate`, and `SupervisorNotificationDate` return `0001-01-01T00:00:00` when not applicable.
- Use [GetTask](GetTask.md) to retrieve the full details of a single task including extended instructions, full comments, requirements, and attachments.
- Use [GetTasks](GetTasks.md) to retrieve tasks across all documents using filter criteria.

## Related APIs

- [GetTask](GetTask.md) - Return the full details of a single workflow task by ID.
- [GetTasks](GetTasks.md) - Return tasks across all documents using XML filter criteria.
- [GetDocumentWorkflows](GetDocumentWorkflows.md) - Return workflow instances for a document.
- [CompleteTask](CompleteTask.md) - Complete a workflow task.
- [ReassignTask](ReassignTask.md) - Reassign a workflow task to a different user.

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed — invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Document not found | `documentPath` does not refer to an existing document. |
