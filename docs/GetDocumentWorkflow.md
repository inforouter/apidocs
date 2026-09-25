# GetDocumentWorkflow API

Retrieves the details of a specific running workflow instance on a document. Returns workflow metadata including dates, submitter, supervisor lists and on-end settings, and every step of the workflow with each step's tasks in full.

Use [GetDocumentWorkflows](GetDocumentWorkflows.md) to list all workflow instances (current and historical) for a document before calling this API to identify the `workflowId`.

## Endpoint

```
/srv.asmx/GetDocumentWorkflow
```

## Methods

- **GET** `/srv.asmx/GetDocumentWorkflow?authenticationTicket=...&documentPath=...&workflowId=...`
- **POST** `/srv.asmx/GetDocumentWorkflow` (form data)
- **SOAP** Action: `http://tempuri.org/GetDocumentWorkflow`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `documentPath` | string | Yes | Full infoRouter path of the document (e.g. `/Finance/Reports/Q1Report.pdf`). |
| `workflowId` | integer | Yes | Numeric ID of the running workflow instance to retrieve. Use `GetDocumentWorkflows` to discover valid IDs. |

## Response

### Success Response

```xml
<response success="true">
  <Workflow>
    <WorkflowId>42</WorkflowId>
    <WorkflowName>Document Approval</WorkflowName>
    <WorkflowDefId>7</WorkflowDefId>
    <DocumentId>1023</DocumentId>
    <DomainId>3</DomainId>
    <StartDate>2026-04-01T08:00:00Z</StartDate>
    <DueDate>2026-04-15T08:00:00Z</DueDate>
    <FinishDate>0001-01-01T00:00:00Z</FinishDate>
    <SubmittedById>101</SubmittedById>
    <SubmittedByName>jsmith</SubmittedByName>
    <OnEndMoveToFolderId>0</OnEndMoveToFolderId>
    <OnEndEventUrl></OnEndEventUrl>
    <Supervisors>
      <Users>
        <User>
          <UserId>55</UserId>
          <UserName>mwilson</UserName>
        </User>
      </Users>
      <Groups>
        <Usergroup>
          <GroupId>12</GroupId>
          <GroupName>Legal Team</GroupName>
          <DomainName>Corporate</DomainName>
        </Usergroup>
      </Groups>
    </Supervisors>
    <Steps>
      <Step>
        <StepNumber>1</StepNumber>
        <StepName>Review</StepName>
        <StepStatus>Active</StepStatus>
        <StartDate>2026-04-01T08:00:00Z</StartDate>
        <DueDate>2026-04-01T13:00:00Z</DueDate>
        <FinishDate />
        <OnStartMoveToFolderId>0</OnStartMoveToFolderId>
        <Tasks>
          <Task>
            <TaskID>50772</TaskID>
            <TaskName>ReviewTask</TaskName>
            <StepNumber>1</StepNumber>
            <TaskStatus>InProgress</TaskStatus>
            <AssigneeName>Jane Smith</AssigneeName>
            <!-- ...every other task field, as GetDocumentTasks writes a task -->
          </Task>
        </Tasks>
      </Step>
      <Step>
        <StepNumber>2</StepNumber>
        <StepName>Approve</StepName>
        <StepStatus>Future</StepStatus>
        <StartDate />
        <DueDate />
        <FinishDate />
        <OnStartMoveToFolderId>0</OnStartMoveToFolderId>
        <Tasks>
          <Task>
            <TaskID>50773</TaskID>
            <TaskName>ApproveTask</TaskName>
            <StepNumber>2</StepNumber>
            <TaskStatus>NotStarted</TaskStatus>
            <!-- ... -->
          </Task>
        </Tasks>
      </Step>
    </Steps>
  </Workflow>
</response>
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `WorkflowId` | integer | Unique ID of the running workflow instance. |
| `WorkflowName` | string | Display name of the workflow. |
| `WorkflowDefId` | integer | ID of the workflow definition this instance was created from. |
| `DocumentId` | integer | Numeric ID of the document in the workflow. |
| `DomainId` | integer | Numeric ID of the domain/library that owns the workflow. |
| `StartDate` | datetime (UTC) | Date and time the workflow was started. |
| `DueDate` | datetime (UTC) | Deadline date for the workflow to complete. |
| `FinishDate` | datetime (UTC) | Date and time the workflow finished. `0001-01-01T00:00:00Z` if still running. |
| `SubmittedById` | integer | User ID of the person who submitted the document to the workflow. |
| `SubmittedByName` | string | Username of the person who submitted the document. |
| `OnEndMoveToFolderId` | integer | Folder ID to move the document to when the workflow ends. `0` if not configured. |
| `OnEndEventUrl` | string | URL called when the workflow ends. Empty string if not configured. |
| `Supervisors/Users/User/UserId` | integer | User ID of a workflow supervisor. |
| `Supervisors/Users/User/UserName` | string | Username of a workflow supervisor. |
| `Supervisors/Groups/Usergroup/GroupId` | integer | Group ID of a supervisor group. |
| `Supervisors/Groups/Usergroup/GroupName` | string | Name of a supervisor group. |
| `Supervisors/Groups/Usergroup/DomainName` | string | Domain/library that owns the supervisor group. |
| `Steps/Step` | element | One per step of the workflow — past, active and future — in step order. |
| `Steps/Step/StepNumber` | integer | The step's position, from 1. |
| `Steps/Step/StepName` | string | The step's name. |
| `Steps/Step/StepStatus` | string | `Past` (finished), `Active` (running now) or `Future` (not started). |
| `Steps/Step/StartDate` | datetime (UTC) | When the step started. Empty for a future step. |
| `Steps/Step/DueDate` | datetime (UTC) | When the step is due. Empty until the step is given one (the first step gets it on submit). |
| `Steps/Step/FinishDate` | datetime (UTC) | When the step finished. Empty while it is active or future. |
| `Steps/Step/OnStartMoveToFolderId` | integer | Folder the document moves to when the step starts. `0` if not configured. |
| `Steps/Step/Tasks/Task` | element | Every task of the step, finished or not, in full: the same fields as [GetDocumentTasks](GetDocumentTasks.md) returns, including instructions, comments, permissions, requirements and attachments. A future step's tasks are there too, with `TaskStatus` `NotStarted`. |

### Error Response

```xml
<response success="false" error="Session expired or invalid ticket" errorCode="4010" />
```

## Required Permissions

The calling user must have at least **read access** to the document.

## Example

### POST Request

```
POST /srv.asmx/GetDocumentWorkflow HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
&documentPath=%2FCorporate%2FContracts%2Fagreement.pdf
&workflowId=42
```

### GET Request

```
GET /srv.asmx/GetDocumentWorkflow
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &documentPath=%2FCorporate%2FContracts%2Fagreement.pdf
    &workflowId=42
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

Reads one workflow of a document by its id.

```javascript
const root = await call('GetDocumentWorkflow', {
  authenticationTicket: ticket,
  documentPath: '/Public/Invoices/inv-1001.pdf',
  workflowId: 7332
});

const workflow = root.querySelector('Workflow');
console.log(workflow.querySelector('SubmittedByName').textContent,   // the full name, not the login
            workflow.querySelector('StartDate').textContent,
            workflow.querySelector('DueDate').textContent);
```

## Notes

- `FinishDate` is empty while the workflow is still running.
- Every step and every task is included: all of them are created when the document is submitted, so a future step already lists its tasks (`NotStarted`). The UI can draw the whole workflow from this one call.
- Step and workflow dates are ISO 8601 UTC (`2026-04-01T08:00:00Z`); task dates are written as GetDocumentTasks writes them (`2026-04-01 08:00:00`, server time).
- The `Supervisors` element is always present; the `Users` and `Groups` child lists may be empty if no supervisors are configured.
- Use [GetDocumentWorkflows](GetDocumentWorkflows.md) first to discover the `workflowId` of a document's current or historical workflow.

## Related APIs

- [GetDocumentWorkflows](GetDocumentWorkflows.md) - List all workflow instances (current and historical) for a document.
- [SubmitDocumentToFlow](SubmitDocumentToFlow.md) - Submit a document to a workflow definition.
- [StopCurrentWorkflow](StopCurrentWorkflow.md) - Gracefully stop a running workflow.
- [UpdateRunningWorkflowTaskDef](UpdateRunningWorkflowTaskDef.md) - Update a task definition on a currently running workflow step.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4041` | no document at that path |
| `4000` | no workflow by that id on that document |
| `4030` | the caller may not see that document |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
