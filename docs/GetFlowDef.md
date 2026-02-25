# GetFlowDef API

Returns the complete definition of a workflow, including all step definitions and their task definitions.

## Endpoint

```
/srv.asmx/GetFlowDef
```

## Methods

- **GET** `/srv.asmx/GetFlowDef?AuthenticationTicket=...&DomainName=...&WorkflowName=...`
- **POST** `/srv.asmx/GetFlowDef` (form data)
- **SOAP** Action: `http://tempuri.org/GetFlowDef`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DomainName` | string | Yes | Name of the domain/library that owns the workflow definition. |
| `WorkflowName` | string | Yes | Name of the workflow definition to retrieve. |

## Response

### Success Response

```xml
<root success="true">
  <FlowDef
    FlowDefID="126"
    FlowName="ContractApproval"
    DomainId="45"
    DomainName="Corporate"
    ActiveFolderPath="/Corporate/Contracts"
    RequiresStartUpPlayers="false"
    Active="true"
    OnEndMoveToPath="/Corporate/Archive"
    OnEndEventUrl="https://erp.example.com/workflow-complete"
    Hide="False">
    <StepDef StepNumber="1" StepName="Review">
      <TaskDefs>
        <TaskDef
          TaskDefId="55"
          TaskName="LegalReview"
          DeadLine="48"
          RequiredAssigneeCount="0"
          SuperVisorId="7"
          SuperVisorName="john.smith"
          SupervisorNotificationOnDue="24"
          Priority="5"
          AllowedStartTimeSpan="0"
          ReminderTimeSpan="0">
          <Requirements>
            <Requirement Name="LastestVersionRead" Definition="" RefObjectId="0" />
          </Requirements>
          <Permissions>
            <Permission Name="EditDocument" Value="False" />
            <Permission Name="ChangeFinishdate" Value="False" />
            <Permission Name="Postpone" Value="False" />
            <Permission Name="ChangePriority" Value="False" />
            <Permission Name="EditNextStep" Value="False" />
            <Permission Name="EditAllSteps" Value="False" />
          </Permissions>
          <instruction>Please review the contract carefully.</instruction>
          <AssigneeList>
            <Users>
              <user id="12" login="jane.doe" fullname="Jane Doe" />
            </Users>
            <UserGroups>
              <group id="3" name="Legal" />
            </UserGroups>
            <SpecialUserRoles>
              <SpecialUserRole RoleId="-1" RoleDescription="DocumentOwner" />
            </SpecialUserRoles>
          </AssigneeList>
        </TaskDef>
      </TaskDefs>
    </StepDef>
    <Supervisors>
      <User id="7" />
    </Supervisors>
  </FlowDef>
</root>
```

### Error Response

```xml
<root success="false" error="[901] Session expired or Invalid ticket" />
```

## FlowDef Attributes

| Attribute | Description |
|-----------|-------------|
| `FlowDefID` | Unique numeric identifier of the workflow definition. |
| `FlowName` | Name of the workflow definition. |
| `DomainId` | Numeric ID of the owning domain/library. |
| `DomainName` | Name of the owning domain/library. |
| `ActiveFolderPath` | Full infoRouter path of the folder where the workflow is active. |
| `RequiresStartUpPlayers` | `true` if the workflow requires startup players to be assigned at submission time. |
| `Active` | `true` if the workflow is currently active and accepting new submissions. |
| `OnEndMoveToPath` | Path documents are moved to when the workflow completes. Empty string if disabled. |
| `OnEndEventUrl` | Webhook URL called when the workflow completes. Empty string if disabled. |
| `Hide` | `True` if the workflow is hidden from the folder UI. |

## StepDef Attributes

| Attribute | Description |
|-----------|-------------|
| `StepNumber` | Numeric order of the step (1-based). |
| `StepName` | Display name of the step. |

## TaskDef Attributes

| Attribute | Description |
|-----------|-------------|
| `TaskDefId` | Unique numeric identifier of the task definition. |
| `TaskName` | Display name of the task. |
| `DeadLine` | Number of hours from task creation until the task is due. `0` means no deadline. |
| `RequiredAssigneeCount` | Assignee selection mode: `0` = all must complete, `1` = auto-select one, `2` = assign to all, one is enough. |
| `SuperVisorId` | User ID of the task supervisor. `0` if none. |
| `SuperVisorName` | Login name of the task supervisor. |
| `SupervisorNotificationOnDue` | Hours before due date when the supervisor is notified. `0` to disable. |
| `Priority` | Task priority: `0` = none, `1` = low, `5` = normal, `10` = high, `11` = urgent. |
| `AllowedStartTimeSpan` | Hours before due date that define the earliest the task can be started. `0` means no restriction. |
| `ReminderTimeSpan` | Hours before due date when the assignee receives a reminder notification. `0` to disable. |

## TaskDef Child Elements

### `<Requirements>`
Lists completion requirements. Each `<Requirement>` element has:
- `Name` -" Requirement type (e.g. `LastestVersionRead`, `Edit`, `Comments`, `Approval`, `SOXReview`, `ISOReview`).
- `Definition` -" Supplemental definition text (used for some requirement types).
- `RefObjectId` -" Referenced object ID (used for some requirement types).

### `<Permissions>`
Six named boolean permissions for the task assignee:
- `EditDocument` -" Assignee may edit the document.
- `ChangeFinishdate` -" Assignee may change the finish date.
- `Postpone` -" Assignee may change the due date.
- `ChangePriority` -" Assignee may change the task priority.
- `EditNextStep` -" Assignee may change next-step routing.
- `EditAllSteps` -" Assignee may change routing for all remaining steps.

### `<instruction>`
Free-text instruction for the task assignee.

### `<AssigneeList>`
Contains three sub-elements:
- `<Users>` -" Individual users (`<user id="..." login="..." fullname="..."/>`).
- `<UserGroups>` -" User groups (`<group id="..." name="..."/>`).
- `<SpecialUserRoles>` -" Special roles such as document owner or submitter (`<SpecialUserRole RoleId="..." RoleDescription="..."/>`).

## Required Permissions

Any authenticated user may call this API. Anonymous (unauthenticated) access is not permitted.

## Example

### GET Request

```
GET /srv.asmx/GetFlowDef
    ?AuthenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &DomainName=Corporate
    &WorkflowName=ContractApproval
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/GetFlowDef HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&DomainName=Corporate&WorkflowName=ContractApproval
```

## Notes

- The response always includes the full set of step and task definitions.
- To list all workflows for a domain without step detail, use [GetDomainFlows](GetDomainFlows.md).
- To list workflows active on a specific folder, use [GetFolderFlows](GetFolderFlows.md).

## Related APIs

- [GetDomainFlows](GetDomainFlows.md) -" List all workflow definitions for a domain (without step detail).
- [GetFolderFlows](GetFolderFlows.md) -" List workflow definitions active on a specific folder.
- [CreateFlowDef](CreateFlowDef.md) -" Create a new workflow definition.
- [ActivateFlowDef](ActivateFlowDef.md) -" Activate a workflow definition.
- [DeactivateFlowDef](DeactivateFlowDef.md) -" Deactivate a workflow definition to allow changes.
- [AddFlowStepDef](AddFlowStepDef.md) -" Add a step to a workflow definition.
- [AddFlowTaskDef](AddFlowTaskDef.md) -" Add a task definition to a workflow step.
- [DeleteWorkflow](DeleteWorkflow.md) -" Permanently delete a workflow definition.

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed -" invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Domain not found | The specified `DomainName` does not exist. |
| Workflow not found | No workflow named `WorkflowName` exists in the specified domain. |
| Permission error | Anonymous access is not permitted; a valid authenticated ticket is required. |
