# SubmitDocumentToFlow API

Submits a document to a workflow definition. Once submitted, the workflow engine creates running tasks based on the workflow definition, assigns them to the configured task assignees, and sends task notification emails.

To override the task assignees for the first step at submission time, use [SubmitDocumentToFlow1](SubmitDocumentToFlow1.md).

## Endpoint

```
/srv.asmx/SubmitDocumentToFlow
```

## Methods

- **GET** `/srv.asmx/SubmitDocumentToFlow?authenticationTicket=...&Path=...&FlowDefID=...`
- **POST** `/srv.asmx/SubmitDocumentToFlow` (form data)
- **SOAP** Action: `http://tempuri.org/SubmitDocumentToFlow`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full path of the document to submit (e.g. `/Cabinet/Project/document.pdf`). |
| `FlowDefID` | integer | Yes | Numeric ID of the workflow definition to submit the document to. Must be a positive integer. |

## Response

### Success Response

```xml
<response success="true" error="" errorCode="0" />
```

### Error Response

```xml
<response success="false" error="Workflow submission failed. Document is currently checked out." />
```

## Required Permissions

The calling user must have the **Submit to Workflow** permission on the document.

Anonymous access is not permitted. The infoRouter server must have a Workflow license.

## Preconditions

| Condition | Required |
|-----------|----------|
| Document must exist at the specified path | Yes |
| Document must not be offline | Yes |
| Document must not be checked out | Yes |
| Document must not already be in a workflow | Yes |
| Document must not be a shortcut | Yes |
| Workflow definition must exist and be **active** | Yes |
| Workflow definition must belong to the same library as the document | Yes |

## Example

### GET Request

```
GET /srv.asmx/SubmitDocumentToFlow
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &Path=/Cabinet/ProjectDocs/proposal.pdf
    &FlowDefID=42
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/SubmitDocumentToFlow HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&Path=/Cabinet/ProjectDocs/proposal.pdf&FlowDefID=42
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

Starts a workflow over a document. `FlowDefID` is the numeric id `CreateFlowDef3` or `GetFlowDef`
reports - not the workflow name - and the definition has to be active.

```javascript
const flow = await call('GetFlowDef', {
  authenticationTicket: ticket, DomainName: 'Public', WorkflowName: 'Invoice approval'
});
const flowDefId = flow.querySelector('FlowDef').getAttribute('FlowDefID');

await call('SubmitDocumentToFlow', {
  authenticationTicket: ticket,
  Path: '/Public/Invoices/inv-1001.pdf',
  FlowDefID: flowDefId
});
```

## Notes

- The `FlowDefID` is the ID of the workflow **definition** (created with [CreateFlowDef](CreateFlowDef.md)), not the ID of a running workflow instance.
- Task assignees are taken from the workflow definition. To specify custom assignees for the first step at submission time, use [SubmitDocumentToFlow1](SubmitDocumentToFlow1.md).
- To find the workflow definition ID, use [GetFolderFlows](GetFolderFlows.md) or [GetDomainFlows](GetDomainFlows.md).
- After a successful submission, the document's `CurrentFlowId` is set to the running workflow ID. Use [GetTask](GetTask.md) or [getTasks](getTasks.md) to retrieve the created tasks.
- A document can only be in one active workflow at a time. Stop or remove the current workflow before re-submitting.

## Related APIs

- [SubmitDocumentToFlow1](SubmitDocumentToFlow1.md) -" Submit with custom first-step task assignees.
- [GetFolderFlows](GetFolderFlows.md) -" List workflow definitions available for a folder.
- [GetDomainFlows](GetDomainFlows.md) -" List workflow definitions for a library/domain.
- [StopCurrentWorkflow](StopCurrentWorkflow.md) -" Stop a running workflow gracefully.
- [RemoveCurrentWorkflow](RemoveCurrentWorkflow.md) -" Remove a running workflow (hard delete).
- [getTasks](getTasks.md) -" Get the workflow tasks created after submission.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4041` | no document at that path |
| `4000` | `FlowDefID` is not a positive integer, the definition is not active, or the document is already in a workflow |
| `4030` | the caller may not submit that document |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
