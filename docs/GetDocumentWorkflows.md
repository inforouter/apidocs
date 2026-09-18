# GetDocumentWorkflows API

Returns all workflow instances (current and historical) for a document, with optional filtering. Each entry in the result contains the same fields as [GetDocumentWorkflow](GetDocumentWorkflow.md).

## Endpoint

```
/srv.asmx/GetDocumentWorkflows
```

## Methods

- **GET** `/srv.asmx/GetDocumentWorkflows?authenticationTicket=...&documentPath=...&filter=...`
- **POST** `/srv.asmx/GetDocumentWorkflows` (form data)
- **SOAP** Action: `http://tempuri.org/GetDocumentWorkflows`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `documentPath` | string | Yes | Full infoRouter path of the document (e.g. `/Finance/Reports/Q1Report.pdf`). |
| `filter` | string | No | Controls which workflow instances are returned. Valid values: `"current"` (active workflow only), `"history"` (completed workflows only). Omit or pass any other value to return all instances. |

## Response

### Success Response

```xml
<response success="true">
  <Workflows>
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
  </Workflows>
</response>
```

When the document has no matching workflow instances the `<Workflows>` element is present but empty:

```xml
<response success="true">
  <Workflows />
</response>
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `WorkflowId` | integer | Unique ID of the workflow instance. Pass this to [GetDocumentWorkflow](GetDocumentWorkflow.md) to retrieve a single instance. |
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
<response success="false" error="Session expired or invalid ticket" errorCode="4010" />
```

## Required Permissions

The calling user must have at least **read access** to the document.

## Example

### POST Request — all workflows

```
POST /srv.asmx/GetDocumentWorkflows HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
&documentPath=%2FCorporate%2FContracts%2Fagreement.pdf
```

### GET Request — current workflow only

```
GET /srv.asmx/GetDocumentWorkflows
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &documentPath=%2FCorporate%2FContracts%2Fagreement.pdf
    &filter=current
HTTP/1.1
Host: yourserver
```

### GET Request — completed workflows only

```
GET /srv.asmx/GetDocumentWorkflows
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &documentPath=%2FCorporate%2FContracts%2Fagreement.pdf
    &filter=history
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

Lists the workflows a document has been through. `filter` takes the two literals `current` and
`history`; anything else, an empty value included, means all of them.

```javascript
const root = await call('GetDocumentWorkflows', {
  authenticationTicket: ticket,
  documentPath: '/Public/Invoices/inv-1001.pdf',
  filter: 'current'
});

for (const workflow of root.querySelectorAll('Workflow')) {
  console.log(workflow.querySelector('WorkflowId').textContent,
              workflow.querySelector('WorkflowName').textContent,
              workflow.querySelector('FinishDate').textContent);   // empty while running
}
```

`WorkflowId` is an element, not an attribute, and it is what `GetDocumentWorkflow` takes.

## Notes

- `filter` is case-sensitive. Only `"current"` and `"history"` are treated specially; any other value (including omitting the parameter) returns all instances.
- `FinishDate` is `0001-01-01T00:00:00Z` for workflows that are still running.
- The `Supervisors` element is always present; the `Users` and `Groups` child lists may be empty if no supervisors are configured.
- If the document has never been submitted to a workflow the response is `success="true"` with an empty `<Workflows />` element.

## Related APIs

- [GetDocumentWorkflow](GetDocumentWorkflow.md) - Return the details of a single workflow instance by ID.
- [SubmitDocumentToFlow](SubmitDocumentToFlow.md) - Submit a document to a workflow definition.
- [StopCurrentWorkflow](StopCurrentWorkflow.md) - Gracefully stop a running workflow.
- [UpdateRunningWorkflowTaskDef](UpdateRunningWorkflowTaskDef.md) - Update a task definition on a currently running workflow step.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4041` | no document at that path |
| `4030` | the caller may not see that document |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
