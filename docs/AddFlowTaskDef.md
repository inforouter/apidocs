# AddFlowTaskDef API

Adds a task definition to a specified step of an existing workflow definition. The entire task configuration -" name, deadline, assignees, permissions, requirements, and instructions -" is passed as a single XML string in the `TaskDefXML` parameter.

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

**`<Permissions>`** (required)
Grants the assignee additional task-level permissions beyond simple completion.

All six rows below must be present and each must carry a `Value`. The server reads them with
`Convert.ToBoolean` without checking that the node is there, so a missing row - or a missing
`Value` - is a `FormatException` and the call answers `errorCode="5000"`.

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
<response success="true" error="" errorCode="0" />
```

### Error Response

```xml
<response success="false" error="Session expired or invalid ticket" errorCode="4010" />
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

Adds one task definition to a step. Every value is an attribute of the root element; the instruction
and the permissions are child elements. **All six permissions have to be present with a `Value`** -
a missing one is read as an empty string and the server answers 5000 with a `FormatException`.

```javascript
const taskDef = `
<TaskDef TaskName="ReviewTask" DeadLine="72" RequiredAssigneeCount="0" SuperVisorId="0"
         SupervisorNotificationOnDue="0" Priority="5" AllowedStartTimeSpan="0"
         ReminderTimeSpan="24" righttype="2" OnCompleteNotice="false">
  <instruction>Please review the invoice.</instruction>
  <Permissions>
    <Permission Name="EditDocument" Value="false" />
    <Permission Name="Postpone" Value="false" />
    <Permission Name="ChangeFinishdate" Value="false" />
    <Permission Name="ChangePriority" Value="false" />
    <Permission Name="EditNextStep" Value="false" />
    <Permission Name="EditAllSteps" Value="false" />
  </Permissions>
  <Requirements />
  <AssigneeList><Users><User UserID="101" /></Users></AssigneeList>
</TaskDef>`;

await call('AddFlowTaskDef', {
  authenticationTicket: ticket,
  DomainName: 'Public',
  FlowName: 'Invoice approval',
  StepNumber: 1,
  TaskDefXML: taskDef
});
```

## Notes

- The workflow definition must be **inactive** before task definitions can be added. Use `DeactivateFlowDef` if the workflow is currently active.
- The `TaskDefXML` value must be URL-encoded when sent via GET or form-encoded POST.
- `TaskName` follows the same validation rules as step names: alphanumeric only, maximum 32 characters.
- `DeadLine` is required and must be greater than `0`. The API will return an error if `DeadLine` is `0`.
- `instruction` is required and must not be empty.
- `SupervisorNotificationOnDue` (in hours) combined with `ReminderTimeSpan` must not exceed the `DeadLine` value, otherwise validation will fail.
- If `StepNumber` does not match any existing step the call fails with `errorCode="4041"` and the message "this step has been deleted". Verify step numbers with `GetFlowDef` first.
- Multiple tasks can be added to the same step by calling this API repeatedly.

## Related APIs

- [AddFlowStepDef](AddFlowStepDef.md) -" Add a step to the workflow definition before adding tasks.
- [AddFlowStepDef1](AddFlowStepDef1.md) -" Add a step with an on-start folder move.
- [CreateFlowDef](CreateFlowDef.md) -" Create the workflow definition.
- [DeactivateFlowDef](DeactivateFlowDef.md) -" Deactivate an active workflow before modifying it.
- [DeleteFlowTaskDef](DeleteFlowTaskDef.md) -" Delete a task definition from a workflow step.
- [GetFlowDef](GetFlowDef.md) -" Retrieve the full workflow definition including steps and tasks.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `5000` | `<Permissions>` is missing, or one of the six `<Permission>` rows has no `Value` |
| `4041` | `StepNumber` names no step of that definition |
| `4000` | no definition by that name, the definition is active, `DeadLine` is 0, `TaskName` is empty or too long, or `TaskDefXML` is not well formed |
| `4030` | the caller may not manage workflows in that library |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
