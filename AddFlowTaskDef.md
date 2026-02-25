# AddFlowTaskDef API

Adds a task definition to a specified step of an existing workflow definition. The entire task configuration — name, deadline, assignees, permissions, requirements, and instructions — is passed as a single XML string in the `TaskDefXML` parameter.

The workflow definition must be in **inactive** (deactivated) state. Multiple tasks can be added to the same step; each call adds one task to the step.

## Endpoint

```
/srv.asmx/AddFlowTaskDef
```

## Methods

- **GET** `/srv.asmx/AddFlowTaskDef?authenticationTicket=...&DomainName=...&FlowName=...&StepNumber=...&TaskDefXML=...`
- **POST** `/srv.asmx/AddFlowTaskDef` (form data)
- **SOAP** Action: `http://tempuri.org/AddFlowTaskDef`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DomainName` | string | Yes | Name of the domain/library that owns the workflow definition. |
| `FlowName` | string | Yes | Name of the workflow definition containing the target step. |
| `StepNumber` | integer | Yes | The step number to which this task definition will be added. Step numbers are returned by `AddFlowStepDef`. |
| `TaskDefXML` | string (XML) | Yes | URL-encoded XML document describing the task definition. See the **TaskDefXML Structure** section below. |

## TaskDefXML Structure

The `TaskDefXML` parameter must be a valid XML document whose root element carries the task attributes and may contain child elements for permissions, requirements, the instruction text, and the assignee list.

### Root element attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `TaskName` | string | Yes | Display name of the task. Maximum 32 alphanumeric characters. |
| `DeadLine` | integer | Yes | Task deadline in **hours** from the time the task is assigned. Must be greater than 0. |
| `RequiredAssigneeCount` | integer | No | Controls how the system selects and completes tasks among multiple assignees. Valid values: `0` = All assignees must complete (default), `1` = System picks one assignee automatically, `2` = All are assigned but only one needs to complete. |
| `SuperVisorId` | integer | No | User ID of the task supervisor. `0` = no supervisor. |
| `SupervisorNotificationOnDue` | integer | No | Number of hours **before** the deadline when the supervisor is notified (stored as a negative value, e.g. `-24` means 24 hours before due). `0` = no notification. Must not exceed the `DeadLine` value. |
| `Priority` | integer | No | Task priority. Valid values: `0` = No priority (default), `1` = Low, `5` = Normal, `10` = High, `11` = Urgent. |
| `AllowedStartTimeSpan` | integer | No | Number of hours after assignment in which the assignee must start the task. `0` = no restriction. |
| `ReminderTimeSpan` | integer | No | Number of hours before the deadline when a reminder is sent to the assignee. `0` = no reminder. Must not exceed `DeadLine`. |
| `righttype` | integer | No | Document access right level granted to the assignee for the duration of the task. Valid values: `0` = No access, `1` = List, `2` = Read, `3` = Add, `4` = Add + Read, `5` = Change, `6` = Full control. |
| `OnCompleteNotice` | string | No | Whether to send a notification to the document owner and supervisor when the task is completed. Valid values: `"True"` or `"False"` (default `"False"`). |

### Child elements

**`<instruction>`** (required)
Contains the plain-text instructions shown to the assignee.

```xml
<instruction>Please review and approve the document before the deadline.</instruction>
```

**`<Permissions>`** (optional)
Grants the assignee additional task-level permissions beyond simple completion.

```xml
<Permissions>
  <Permission Name="EditDocument"    Value="True" />
  <Permission Name="Postpone"        Value="True" />
  <Permission Name="ChangeFinishdate" Value="False" />
  <Permission Name="ChangePriority"  Value="False" />
  <Permission Name="EditNextStep"    Value="False" />
  <Permission Name="EditAllSteps"    Value="False" />
</Permissions>
```

| Permission Name | Description |
|-----------------|-------------|
| `EditDocument` | Assignee can edit the document content. |
| `Postpone` | Assignee can change the task due date. |
| `ChangeFinishdate` | Assignee can change the task finish date. |
| `ChangePriority` | Assignee can change the task priority. |
| `EditNextStep` | Assignee can modify the next workflow step. |
| `EditAllSteps` | Assignee can modify all remaining workflow steps. |

**`<AssigneeList>`** (optional)
Specifies users, user groups, and/or special roles assigned to the task.

```xml
<AssigneeList>
  <Users>
    <user UserID="101" />
    <user UserID="102" />
  </Users>
  <UserGroups>
    <group GroupID="55" />
  </UserGroups>
  <SpecialUserRoles>
    <role RoleId="1" />
  </SpecialUserRoles>
</AssigneeList>
```

**`<Requirements>`** (optional)
Specifies additional actions the assignee must complete before the task can be marked as done.

```xml
<Requirements>
  <Requirement Name="Approval" RefObjectId="0" Definition="" />
  <Requirement Name="LastestVersionRead" RefObjectId="0" Definition="" />
</Requirements>
```

Valid `Name` values for requirements:

| Name | Description |
|------|-------------|
| `NoRequirement` | No additional requirements. |
| `Sign` | Assignee must electronically sign. |
| `Edit` | Assignee must edit the document. |
| `LastestVersionRead` | Assignee must read the latest version. |
| `Comments` | Assignee must add a comment. |
| `Approval` | Assignee must set an approval status. |
| `Archive` | Assignee must archive the document. |
| `SOXReview` | Assignee must complete a SOX review. |
| `ISOReview` | Assignee must complete an ISO review. |
| `Dispose` | Assignee must dispose of the document. |
| `Downgrade` | Assignee must downgrade the classification. |
| `Declassify` | Assignee must declassify the document. |
| `PublishedVersionRead` | Assignee must read the published version. |
| `Transfer` | Assignee must transfer the document. |
| `Attachment` | Assignee must add an attachment. |
| `FormTemplate` | Assignee must complete a form template. |
| `MetaData` | Assignee must update metadata/property sets. |
| `ReproptPassword` | Assignee must re-enter password for repropmt. |

### Complete TaskDefXML example

```xml
<taskdef
    TaskName="LegalReview"
    DeadLine="72"
    RequiredAssigneeCount="0"
    SuperVisorId="0"
    SupervisorNotificationOnDue="0"
    Priority="5"
    AllowedStartTimeSpan="0"
    ReminderTimeSpan="24"
    righttype="2"
    OnCompleteNotice="False">
  <instruction>Please review the document for legal compliance and approve or reject it before the deadline.</instruction>
  <Permissions>
    <Permission Name="EditDocument"    Value="False" />
    <Permission Name="Postpone"        Value="True"  />
    <Permission Name="ChangeFinishdate" Value="False" />
    <Permission Name="ChangePriority"  Value="False" />
    <Permission Name="EditNextStep"    Value="False" />
    <Permission Name="EditAllSteps"    Value="False" />
  </Permissions>
  <AssigneeList>
    <Users>
      <user UserID="101" />
    </Users>
  </AssigneeList>
  <Requirements>
    <Requirement Name="Approval" RefObjectId="0" Definition="" />
  </Requirements>
</taskdef>
```

## Response

### Success Response

```xml
<root success="true" />
```

### Error Response

```xml
<root success="false" error="[901] Session expired or Invalid ticket" />
```

## Required Permissions

The calling user must be a **workflow supervisor**, a **domain/library manager**, or a **system administrator**.

## Example

### POST Request

```
POST /srv.asmx/AddFlowTaskDef HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
&DomainName=Corporate
&FlowName=Document+Approval
&StepNumber=1
&TaskDefXML=%3Ctaskdef+TaskName%3D%22LegalReview%22+DeadLine%3D%2272%22+...%2F%3E
```

### GET Request

```
GET /srv.asmx/AddFlowTaskDef
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &DomainName=Corporate
    &FlowName=Document+Approval
    &StepNumber=1
    &TaskDefXML=%3Ctaskdef+TaskName%3D%22LegalReview%22+DeadLine%3D%2272%22+...%2F%3E
HTTP/1.1
Host: yourserver
```

## Notes

- The workflow definition must be **inactive** before task definitions can be added. Use `DeactivateFlowDef` if the workflow is currently active.
- The `TaskDefXML` value must be URL-encoded when sent via GET or form-encoded POST.
- `TaskName` follows the same validation rules as step names: alphanumeric only, maximum 32 characters.
- `DeadLine` is required and must be greater than `0`. The API will return an error if `DeadLine` is `0`.
- `instruction` is required and must not be empty.
- `SupervisorNotificationOnDue` (in hours) combined with `ReminderTimeSpan` must not exceed the `DeadLine` value, otherwise validation will fail.
- If `StepNumber` does not match any existing step, the API returns success but no task is added (the loop finds no matching step). Always verify step numbers with `GetFlowDef` first.
- Multiple tasks can be added to the same step by calling this API repeatedly.

## Related APIs

- [AddFlowStepDef](AddFlowStepDef) – Add a step to the workflow definition before adding tasks.
- [AddFlowStepDef1](AddFlowStepDef1) – Add a step with an on-start folder move.
- [CreateFlowDef](CreateFlowDef) – Create the workflow definition.
- [DeactivateFlowDef](DeactivateFlowDef) – Deactivate an active workflow before modifying it.
- [DeleteFlowTaskDef](DeleteFlowTaskDef) – Delete a task definition from a workflow step.
- [GetFlowDef](GetFlowDef) – Retrieve the full workflow definition including steps and tasks.

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed — invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Invalid XML | `TaskDefXML` could not be parsed as valid XML. |
| Workflow not found | The specified `DomainName`/`FlowName` combination does not exist. |
| Task name empty | `TaskName` attribute is missing or empty. |
| Name validation error | `TaskName` exceeds 32 characters or contains invalid characters. |
| Deadline zero | `DeadLine` must be greater than 0. |
| Instruction empty | `instruction` child element is missing or empty. |
| Notification exceeds deadline | `SupervisorNotificationOnDue` or `ReminderTimeSpan` exceeds the `DeadLine`. |
| Permission error | Calling user does not have workflow management permissions for this domain. |
