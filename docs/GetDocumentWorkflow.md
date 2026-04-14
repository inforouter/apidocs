# GetDocumentWorkflow API

Retrieves the details of a specific running workflow instance on a document. Returns workflow metadata including dates, submitter, supervisor lists, and on-end settings.

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
<root success="true">
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
  </Workflow>
</root>
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

### Error Response

```xml
<root success="false" error="[901] Session expired or Invalid ticket" />
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

## Notes

- `FinishDate` returns `0001-01-01T00:00:00Z` when the workflow is still running.
- The `Supervisors` element is always present; the `Users` and `Groups` child lists may be empty if no supervisors are configured.
- Use [GetDocumentWorkflows](GetDocumentWorkflows.md) first to discover the `workflowId` of a document's current or historical workflow.

## Related APIs

- [GetDocumentWorkflows](GetDocumentWorkflows.md) - List all workflow instances (current and historical) for a document.
- [SubmitDocumentToFlow](SubmitDocumentToFlow.md) - Submit a document to a workflow definition.
- [StopCurrentWorkflow](StopCurrentWorkflow.md) - Gracefully stop a running workflow.
- [UpdateRunningWorkflowTaskDef](UpdateRunningWorkflowTaskDef.md) - Update a task definition on a currently running workflow step.

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed — invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Document not found | `documentPath` does not refer to an existing document. |
| Workflow not found | `workflowId` does not match a workflow instance on the document. |
