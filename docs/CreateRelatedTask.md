# CreateRelatedTask API

Creates a related (linked) ad-hoc task tied to an existing workflow task, sharing the same document context.

## Endpoint

```
/srv.asmx/CreateRelatedTask
```

## Methods

- **GET** `/srv.asmx/CreateRelatedTask?authenticationTicket=...&taskId=...&xmlParameters=...`
- **POST** `/srv.asmx/CreateRelatedTask` (form data)
- **SOAP** Action: `http://tempuri.org/CreateRelatedTask`

## Prerequisites

The `taskId` parameter must be the numeric ID of an existing, active task that the authenticated user has access to. Obtain a task ID from the `CreateTask` API or from a running workflow. Passing a non-existent or inaccessible task ID returns an error.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from AuthenticateUser |
| `taskId` | integer | Yes | Numeric ID of the existing active task to link the new related task to |
| `xmlParameters` | string | Yes | XML-serialized RelatedTaskRequestModel (see structure below) |

### xmlParameters Structure

```xml
<RelatedTaskRequestModel>
  <RequestedAssigneeName>jdoe</RequestedAssigneeName>
  <Instructions>Please review the related document section.</Instructions>
  <DueDate>2026-05-15T00:00:00</DueDate>
  <Priority>Normal</Priority>
  <TaskRequirements>
    <TaskRequirement>
      <RequirementType>Approval</RequirementType>
      <ObjectId>0</ObjectId>
      <Definition></Definition>
    </TaskRequirement>
  </TaskRequirements>
  <ReminderTimeSpan>0</ReminderTimeSpan>
  <AllowedStartTimeSpan>0</AllowedStartTimeSpan>
  <SendToNotice>true</SendToNotice>
</RelatedTaskRequestModel>
```

To specify no requirements, use an empty element:

```xml
<TaskRequirements />
```

#### RelatedTaskRequestModel Fields

| Field | Type | Description |
|-------|------|-------------|
| `RequestedAssigneeName` | string | Login name of the user to assign the related task to |
| `Instructions` | string | Task instructions shown to the assignee |
| `DueDate` | DateTime | Due date for the task (ISO 8601 format) |
| `Priority` | enum | Task priority — see **Priority Values** below |
| `TaskRequirements` | TaskRequirement[] | Zero or more completion requirements the assignee must fulfill (see below) |
| `ReminderTimeSpan` | int | Hours before the due date to send a reminder email (0 = no reminder) |
| `AllowedStartTimeSpan` | int | Hours before the due date from which the task becomes available to start (0 = immediately) |
| `SendToNotice` | bool | Send an email notification to the assignee upon task creation |

#### Priority Values

| Value | Description |
|-------|-------------|
| `NoPriortySetting` | No priority set |
| `Low` | Low priority |
| `Normal` | Normal priority (default) |
| `High` | High priority |
| `Urgent` | Urgent priority |

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
    <TaskId>789</TaskId>
    <RedirectedUserName></RedirectedUserName>
  </Value>
</response>
```

| Element | Description |
|---------|-------------|
| `Value/TaskId` | The numeric ID of the newly created related task |
| `Value/RedirectedUserName` | If the assignee has a task redirection active, the login name of the actual user the task was assigned to; empty string if no redirection occurred |

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

## Required Permissions

The authenticated user must have access to the parent task and the document it is associated with.

## Example

### Request (POST) — with requirements

```
POST /srv.asmx/CreateRelatedTask HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&taskId=456&xmlParameters=<RelatedTaskRequestModel><RequestedAssigneeName>jdoe</RequestedAssigneeName><Instructions>Please review</Instructions><DueDate>2026-05-15T00:00:00</DueDate><Priority>Normal</Priority><TaskRequirements><TaskRequirement><RequirementType>Approval</RequirementType><ObjectId>0</ObjectId><Definition></Definition></TaskRequirement></TaskRequirements><ReminderTimeSpan>0</ReminderTimeSpan><AllowedStartTimeSpan>0</AllowedStartTimeSpan><SendToNotice>true</SendToNotice></RelatedTaskRequestModel>
```

### Request (POST) — no requirements

```
POST /srv.asmx/CreateRelatedTask HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&taskId=456&xmlParameters=<RelatedTaskRequestModel><RequestedAssigneeName>jdoe</RequestedAssigneeName><Instructions>Please review</Instructions><DueDate>2026-05-15T00:00:00</DueDate><Priority>Normal</Priority><TaskRequirements /><ReminderTimeSpan>0</ReminderTimeSpan><AllowedStartTimeSpan>0</AllowedStartTimeSpan><SendToNotice>true</SendToNotice></RelatedTaskRequestModel>
```

## Notes

- The related task is linked to the parent task and inherits its document context.
- If the specified assignee has an active task redirection, the task is silently redirected and `Value/RedirectedUserName` contains the actual assignee login name.
- Use `DeleteTask` to remove the task, `CompleteTask` to mark it done, or `ReassignTask` to transfer it to another user.
- Unlike `CreateTask`, this API does not accept `RightType` or document permission flags — access rights are inherited from the parent task's document.
- `Priority` values are case-sensitive enum names; all must be from the table above.
- `RequirementType` values are case-sensitive enum names; all must be from the table above.
- `FormTemplate` requirements require `ObjectId` to be set to the target form template's numeric ID.
- `AllowedStartTimeSpan` and `ReminderTimeSpan` are in **hours**, not days.
- The `RequirementNumber` field is managed internally and should be omitted from the XML input.
- Passing `taskId = 0` or a non-existent task ID returns an error.
