# CreateTask API

Creates a standalone ad-hoc workflow task and assigns it to a document.

## Endpoint

```
/srv.asmx/CreateTask
```

## Methods

- **GET** `/srv.asmx/CreateTask?authenticationTicket=...&documentPath=...&xmlParameters=...`
- **POST** `/srv.asmx/CreateTask` (form data)
- **SOAP** Action: `http://tempuri.org/CreateTask`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from AuthenticateUser |
| `documentPath` | string | Yes | Full infoRouter path of the document to assign the task to |
| `xmlParameters` | string | Yes | XML-serialized TaskCreationRequestModel (see structure below) |

### xmlParameters Structure

```xml
<TaskCreationRequestModel>
  <RequestedAssigneeName>jdoe</RequestedAssigneeName>
  <Instructions>Please review this document by the due date.</Instructions>
  <DueDate>2026-05-01T00:00:00</DueDate>
  <Priority>Normal</Priority>
  <RightType>READ</RightType>
  <PermissionChangeDueDate>false</PermissionChangeDueDate>
  <PermissionEnableEdit>false</PermissionEnableEdit>
  <PermissionChangePriority>false</PermissionChangePriority>
  <PermissionChangeFinishDate>false</PermissionChangeFinishDate>
  <TaskRequirements>
    <TaskRequirement>
      <RequirementType>Approval</RequirementType>
      <ObjectId>0</ObjectId>
      <Definition></Definition>
    </TaskRequirement>
  </TaskRequirements>
  <AllowedStartTimeSpan>0</AllowedStartTimeSpan>
  <ReminderTimeSpan>0</ReminderTimeSpan>
  <SendTaskNotice>true</SendTaskNotice>
  <OnCompleteNotification>false</OnCompleteNotification>
</TaskCreationRequestModel>
```

To specify no requirements, use an empty element:

```xml
<TaskRequirements />
```

#### TaskCreationRequestModel Fields

| Field | Type | Description |
|-------|------|-------------|
| `RequestedAssigneeName` | string | Login name of the user to assign the task to |
| `Instructions` | string | Task instructions shown to the assignee |
| `DueDate` | DateTime | Due date for the task (ISO 8601 format) |
| `Priority` | enum | Task priority — see **Priority Values** below |
| `RightType` | enum | Document access right granted while task is active — see **RightType Values** below |
| `PermissionChangeDueDate` | bool | Allow assignee to change the due date |
| `PermissionEnableEdit` | bool | Allow assignee to edit the document |
| `PermissionChangePriority` | bool | Allow assignee to change task priority |
| `PermissionChangeFinishDate` | bool | Allow assignee to change the finish date |
| `TaskRequirements` | TaskRequirement[] | Zero or more completion requirements the assignee must fulfill (see below) |
| `AllowedStartTimeSpan` | int | Hours before the due date from which the task becomes available to start (0 = immediately) |
| `ReminderTimeSpan` | int | Hours before the due date to send a reminder email (0 = no reminder) |
| `SendTaskNotice` | bool | Send an email notification to the assignee upon task creation |
| `OnCompleteNotification` | bool | Send an email notification to the assigner when the task is completed |

#### Priority Values

| Value | Description |
|-------|-------------|
| `NoPriortySetting` | No priority set |
| `Low` | Low priority |
| `Normal` | Normal priority (default) |
| `High` | High priority |
| `Urgent` | Urgent priority |

#### RightType Values

| Value | Description |
|-------|-------------|
| `NOACCESS` | No additional document rights granted |
| `LIST` | Assignee can see the document in folder listings |
| `READ` | Assignee can read the document |
| `ADD` | Assignee can add new documents to the folder |
| `ADDREAD` | Assignee can add and read documents |
| `CHANGE` | Assignee can change (edit) the document |
| `FULLCONTROL` | Assignee has full control over the document |

#### TaskRequirement Fields

Each `<TaskRequirement>` element inside `<TaskRequirements>` has the following fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `RequirementType` | enum | Yes | The type of action the assignee must perform (see values below) |
| `ObjectId` | int | No | Object identifier required by certain requirement types (e.g. form template ID). Use `0` when not applicable. |
| `Definition` | string | No | Additional definition or label for the requirement. Leave empty when not applicable. |

#### RequirementType Values

| Value | Description |
|-------|-------------|
| `Sign` | Assignee must digitally sign the document |
| `Edit` | Assignee must edit the document |
| `LastestVersionRead` | Assignee must read the latest version of the document |
| `PublishedVersionRead` | Assignee must read the published version of the document |
| `Comments` | Assignee must add comments to the document |
| `Approval` | Assignee must approve the document |
| `Archive` | Assignee must archive the document |
| `SOXReview` | Assignee must perform a SOX compliance review |
| `ISOReview` | Assignee must perform an ISO compliance review |
| `Dispose` | Assignee must dispose of the document |
| `Downgrade` | Assignee must downgrade the document classification |
| `Declassify` | Assignee must declassify the document |
| `Transfer` | Assignee must transfer the document |
| `Attachment` | Assignee must attach a file to the document |
| `FormTemplate` | Assignee must complete a form template (set `ObjectId` to the form template ID) |
| `MetaData` | Assignee must fill in metadata fields |
| `ReproptPassword` | Assignee must re-enter their password to confirm the action |

Multiple `<TaskRequirement>` entries may be added; each represents a distinct action the assignee must complete before the task can be finished.

## Response

### Success Response

```xml
<response success="true">
  <Value>
    <TaskId>456</TaskId>
    <RedirectedUserName></RedirectedUserName>
  </Value>
</response>
```

| Element | Description |
|---------|-------------|
| `Value/TaskId` | The numeric ID of the newly created task |
| `Value/RedirectedUserName` | If the assignee has a task redirection active, the login name of the actual user the task was assigned to; empty string if no redirection occurred |

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

## Required Permissions

The authenticated user must have permission to assign tasks on the target document. The document must exist and be accessible to the calling user.

## Example

### Request (POST) — with requirements

```
POST /srv.asmx/CreateTask HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&documentPath=/MyDomain/MyLibrary/report.pdf&xmlParameters=<TaskCreationRequestModel><RequestedAssigneeName>jdoe</RequestedAssigneeName><Instructions>Please review</Instructions><DueDate>2026-05-01T00:00:00</DueDate><Priority>Normal</Priority><RightType>READ</RightType><PermissionChangeDueDate>false</PermissionChangeDueDate><PermissionEnableEdit>false</PermissionEnableEdit><PermissionChangePriority>false</PermissionChangePriority><PermissionChangeFinishDate>false</PermissionChangeFinishDate><TaskRequirements><TaskRequirement><RequirementType>Approval</RequirementType><ObjectId>0</ObjectId><Definition></Definition></TaskRequirement></TaskRequirements><AllowedStartTimeSpan>0</AllowedStartTimeSpan><ReminderTimeSpan>0</ReminderTimeSpan><SendTaskNotice>true</SendTaskNotice><OnCompleteNotification>false</OnCompleteNotification></TaskCreationRequestModel>
```

### Request (POST) — no requirements

```
POST /srv.asmx/CreateTask HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&documentPath=/MyDomain/MyLibrary/report.pdf&xmlParameters=<TaskCreationRequestModel><RequestedAssigneeName>jdoe</RequestedAssigneeName><Instructions>Please review</Instructions><DueDate>2026-05-01T00:00:00</DueDate><Priority>Normal</Priority><RightType>READ</RightType><PermissionChangeDueDate>false</PermissionChangeDueDate><PermissionEnableEdit>false</PermissionEnableEdit><PermissionChangePriority>false</PermissionChangePriority><PermissionChangeFinishDate>false</PermissionChangeFinishDate><TaskRequirements /><AllowedStartTimeSpan>0</AllowedStartTimeSpan><ReminderTimeSpan>0</ReminderTimeSpan><SendTaskNotice>true</SendTaskNotice><OnCompleteNotification>false</OnCompleteNotification></TaskCreationRequestModel>
```

## Notes

- If the specified assignee has an active task redirection, the task is silently redirected to the configured target user and `Value/RedirectedUserName` contains the actual assignee login name.
- Use `DeleteTask` to remove the task, `CompleteTask` to mark it done, or `ReassignTask` to transfer it to another user.
- `Priority` and `RightType` values are case-sensitive enum names; all must be from the tables above.
- `RequirementType` values are case-sensitive; all must be from the table above.
- `FormTemplate` requirements require `ObjectId` to be set to the target form template's numeric ID.
- `AllowedStartTimeSpan` and `ReminderTimeSpan` are in **hours**, not days.
- The `RequirementNumber` field is managed internally and should be omitted from the XML input.
- Shortcut documents cannot have tasks assigned to them; the API returns an error for shortcuts.
- Offline documents cannot have tasks assigned to them; the API returns an error for offline documents.
