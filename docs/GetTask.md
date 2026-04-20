# GetTask API

Returns the full details of a single workflow task by its task ID.

## Endpoint

```
/srv.asmx/GetTask
```

## Methods

- **GET** `/srv.asmx/GetTask?authenticationTicket=...&taskId=...`
- **POST** `/srv.asmx/GetTask` (form data)
- **SOAP** Action: `http://tempuri.org/GetTask`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `taskId` | integer | Yes | Unique numeric ID of the task to retrieve. |

## Response

### Success Response

```xml
<root success="true">
  <Task>
    <TaskID>4812</TaskID>
    <TaskName>LegalReview</TaskName>
    <ShortInstruction>Please review the contract carefully.</ShortInstruction>
    <StepNumber>1</StepNumber>
    <StepName>Review</StepName>
    <FlowID>225</FlowID>
    <FlowName>ContractApproval</FlowName>
    <FlowDefID>126</FlowDefID>
    <Priority>Normal</Priority>
    <TaskStatus>InProgress</TaskStatus>
    <ApprovalStatus>NoResult</ApprovalStatus>
    <StartDate>2024-03-01 09:00:00</StartDate>
    <StartDtae>2024-03-01 09:00:00</StartDtae>
    <FinishDate>1900-01-01 00:00:00</FinishDate>
    <DueDate>2024-03-05 17:00:00</DueDate>
    <ShortComments></ShortComments>
    <TaskDefID>55</TaskDefID>
    <LinkedTaskID>0</LinkedTaskID>
    <AssigneeID>12</AssigneeID>
    <AssigneeType>User</AssigneeType>
    <AssigneeName>jane.doe</AssigneeName>
    <AssignedByID>7</AssignedByID>
    <AssignedByName>john.smith</AssignedByName>
    <SuperVisorID>7</SuperVisorID>
    <SupervisorName>john.smith</SupervisorName>
    <DocumentID>1024</DocumentID>
    <DocumentName>ContractDraft.pdf</DocumentName>
    <StartVersionNumber>1</StartVersionNumber>
    <EndVersionNumber>3</EndVersionNumber>
    <DocumentTypeId>0</DocumentTypeId>
    <DocumentTypeName></DocumentTypeName>
    <DocumentFolderID>88</DocumentFolderID>
    <DocumentLibraryID>45</DocumentLibraryID>
    <DocumentLibraryName>Corporate</DocumentLibraryName>
    <DocumentCheckedOutByID>0</DocumentCheckedOutByID>
    <DocumentCheckedOutByName></DocumentCheckedOutByName>
    <DocumentTemplateID>0</DocumentTemplateID>
    <RedirectedFrom_UserID>0</RedirectedFrom_UserID>
    <RedirectedFrom_UserName></RedirectedFrom_UserName>
    <AdHoc>False</AdHoc>
    <DeadLine>48</DeadLine>
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
        <Name>LastestVersionRead</Name>
        <RequirementType>4</RequirementType>
        <Definition></Definition>
        <ObjectId>0</ObjectId>
      </Requirement>
    </RequirementDetails>
    <Requirements></Requirements>
    <Supervisor_NotificationOnDue>24</Supervisor_NotificationOnDue>
    <SupervisorNotificationDate>2024-03-04 17:00:00</SupervisorNotificationDate>
    <AllowedStartTimeSpan>0</AllowedStartTimeSpan>
    <AllowedStartDate>1900-01-01 00:00:00</AllowedStartDate>
    <ReminderTimeSpan>0</ReminderTimeSpan>
    <ReminderDate>1900-01-01 00:00:00</ReminderDate>
    <extendedInstruction>Full task instruction text, may exceed 255 characters.</extendedInstruction>
    <extendedComment>Full assignee comment text, may exceed 255 characters.</extendedComment>
    <Attachments>
      <Attachment>
        <AttachmentDate>2024-03-02 10:30:00</AttachmentDate>
        <DocumentId>1025</DocumentId>
        <DocumentName>SupportingEvidence.pdf</DocumentName>
        <Path>/Corporate/Legal</Path>
        <WorkflowId>225</WorkflowId>
        <StepNumber>1</StepNumber>
        <StepName>Review</StepName>
        <UserId>12</UserId>
      </Attachment>
    </Attachments>
  </Task>
</root>
```

### Error Response

```xml
<root success="false" error="[901] Session expired or Invalid ticket" />
```

## Response Field Reference

### Task Identity & Workflow

| Element | Description |
|---------|-------------|
| `TaskID` | Unique numeric identifier of this task instance. |
| `TaskName` | Display name of the task (from the task definition). |
| `TaskDefID` | ID of the task definition this task was created from. |
| `LinkedTaskID` | ID of the linked task when this task was created from a redirect. `0` if none. |
| `FlowID` | ID of the active workflow instance the task belongs to. |
| `FlowName` | Name of the workflow. |
| `FlowDefID` | ID of the workflow definition. |
| `StepNumber` | Step number within the workflow (1-based). |
| `StepName` | Display name of the step. |
| `AdHoc` | `True` if this task was created ad-hoc (not from the workflow definition). |

### Status & Priority

| Element | Values | Description |
|---------|--------|-------------|
| `TaskStatus` | `NotStarted`, `InProgress`, `DueDateChanged`, `Completed`, `Dropped`, `Reassigned` | Current status of the task. |
| `Priority` | `NoPriortySetting`, `Low`, `Normal`, `High`, `Urgent` | Task priority. |
| `ApprovalStatus` | `NoResult`, `Approved`, `Rejected` | Approval result set by the assignee (if the task has an Approval requirement). |

### Assignee & Supervisor

| Element | Description |
|---------|-------------|
| `AssigneeID` | User ID of the task assignee. |
| `AssigneeType` | `User`, `Group`, or `SpecialUserRole`. |
| `AssigneeName` | Login name of the task assignee. |
| `AssignedByID` | User ID of the person who assigned the task. |
| `AssignedByName` | Login name of the assigner. |
| `SuperVisorID` | User ID of the task supervisor. `0` if none. |
| `SupervisorName` | Login name of the supervisor. |
| `RedirectedFrom_UserID` | If the task was redirected, the original assignee's user ID. `0` if not redirected. |
| `RedirectedFrom_UserName` | Login name of the original assignee before redirection. Empty if not redirected. |

### Dates

| Element | Description |
|---------|-------------|
| `StartDate` | Date and time the task was started. **Use this element.** |
| `StartDtae` | **Deprecated.** Same value as `StartDate`. This element exists only for backward compatibility due to a typo in an earlier release (`Dtae` instead of `Date`). Do not use it in new integrations — it will be removed in a future version. |
| `FinishDate` | Date and time the task was completed. `1900-01-01 00:00:00` if not yet finished. |
| `DueDate` | Deadline for the task. `1900-01-01 00:00:00` if no deadline set. |
| `DeadLine` | Number of hours from task creation until due. `0` means no deadline. |
| `AllowedStartTimeSpan` | Hours before due date when the task becomes eligible to be started. `0` means no restriction. |
| `AllowedStartDate` | Computed date/time from which the task may be started. `1900-01-01 00:00:00` if not applicable. |
| `ReminderTimeSpan` | Hours before due date when the assignee reminder is sent. `0` to disable. |
| `ReminderDate` | Computed reminder date/time. `1900-01-01 00:00:00` if not applicable. |
| `Supervisor_NotificationOnDue` | Hours before due date when the supervisor is notified. `0` to disable. |
| `SupervisorNotificationDate` | Computed supervisor notification date/time. `1900-01-01 00:00:00` if not applicable. |

### Document

| Element | Description |
|---------|-------------|
| `DocumentID` | Numeric ID of the document the task is associated with. |
| `DocumentName` | Name of the document. |
| `DocumentFolderID` | Folder ID containing the document. |
| `DocumentLibraryID` | Domain/library ID of the document. |
| `DocumentLibraryName` | Domain/library name. |
| `DocumentTypeId` | Document type ID. `0` if none. |
| `DocumentTypeName` | Document type name. Empty if none. |
| `DocumentCheckedOutByID` | User ID who has the document checked out. `0` if not checked out. |
| `DocumentCheckedOutByName` | Login name of the checkout user. |
| `DocumentTemplateID` | Template ID associated with the document. `0` if none. |
| `StartVersionNumber` | Document version number when the task was created. |
| `EndVersionNumber` | Current document version number. |

### Instructions & Comments

| Element | Description |
|---------|-------------|
| `ShortInstruction` | First 255 characters of the task instruction. |
| `ShortComments` | First 255 characters of the assignee's comments. |
| `extendedInstruction` | Full task instruction text. Identical to `ShortInstruction` when the instruction is 255 characters or fewer; contains the complete text when it is longer. |
| `extendedComment` | Full assignee comment text. Identical to `ShortComments` when the comment is 255 characters or fewer; contains the complete text when it is longer. |

### Right Type & Permissions

The `<RightType>` element describes the document access right required by this task:

| Attribute | Type | Description |
|-----------|------|-------------|
| `RightTypeId` | integer | Numeric right type value (`0`=NOACCESS, `1`=LIST, `2`=READ, `3`=ADD, `4`=ADDREAD, `5`=CHANGE, `6`=FULLCONTROL). |
| `RightTypeName` | string | C# enum member name of the right type (e.g. `READ`, `CHANGE`, `FULLCONTROL`). |
| `RightTypeText` | string | Localized display label of the right type. |

The `<Permissions>` element lists six boolean task-assignee permissions, each as `<Permission Name="..." Value="True|False"/>`:

| Name | Description |
|------|-------------|
| `EditDocument` | Assignee may edit the document. |
| `ChangeFinishdate` | Assignee may change the finish date. |
| `Postpone` | Assignee may change the due date. |
| `ChangePriority` | Assignee may change the task priority. |
| `EditNextStep` | Assignee may change next-step routing. |
| `EditAllSteps` | Assignee may change routing for all remaining steps. |

### Requirements

The `<RequirementDetails>` element lists each task requirement with:
- `<Name>` -" Requirement type name (e.g. `LastestVersionRead`, `Edit`, `Comments`, `Approval`, `SOXReview`).
- `<RequirementType>` -" Numeric value of the requirement type.
- `<Definition>` -" Supplemental definition (for certain requirement types).
- `<ObjectId>` -" Referenced object ID (for certain requirement types).

The `<Requirements>` element is always empty (legacy field, reserved).

### Attachments

The `<Attachments>` element lists documents attached to the task during execution. Each `<Attachment>` has:
- `<AttachmentDate>` — Date/time the attachment was added.
- `<DocumentId>` — Document ID of the attachment.
- `<DocumentName>` — File name of the attached document.
- `<Path>` — Folder path containing the attached document (does not include the document name).
- `<WorkflowId>` — Workflow instance ID.
- `<StepNumber>` — Step number where the attachment was added.
- `<StepName>` — Step name.
- `<UserId>` — User ID of the person who added the attachment.

## Required Permissions

Any authenticated user may call this API. Anonymous (unauthenticated) access is not permitted.

## Example

### GET Request

```
GET /srv.asmx/GetTask
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &taskId=4812
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/GetTask HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&taskId=4812
```

## Notes

- Task IDs are available from [getTasks](getTasks.md) and [GetDueTaskDocuments](GetDueTaskDocuments.md).
- Dates of `1900-01-01 00:00:00` indicate the field has no value (not set).
- Use `<StartDate>` to read the task start date. The response also includes `<StartDtae>` (a legacy typo) for backward compatibility only — do not use it in new code.

## Related APIs

- [getTasks](getTasks.md) -" Get a filtered list of task IDs and summaries.
- [GetDueTaskDocuments](GetDueTaskDocuments.md) -" Get documents with due tasks for the current user.
- [CompleteTask](CompleteTask.md) -" Mark a task as completed.
- [DeleteTask](DeleteTask.md) -" Delete a task.
- [ReassignTask](ReassignTask.md) -" Reassign a task to another user.
- [ChangeTaskDueDate](ChangeTaskDueDate.md) -" Change the due date of an active task.

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed -" invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Task not found | No task with the specified `taskId` exists. |
| Permission error | Anonymous access is not permitted. |
