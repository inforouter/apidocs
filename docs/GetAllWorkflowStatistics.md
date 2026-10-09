# GetAllWorkflowStatistics API

Returns the statistics of every workflow definition of a domain/library, or of all the caller's libraries, in one call. Each entry is what [GetWorkflowStatistics](GetWorkflowStatistics.md) returns for one workflow, so a workflow report needs no call per workflow.

## Endpoint

```
/srv.asmx/GetAllWorkflowStatistics
```

## Methods

- **GET** `/srv.asmx/GetAllWorkflowStatistics?authenticationTicket=...&domainName=...&startDate=...&endDate=...`
- **POST** `/srv.asmx/GetAllWorkflowStatistics` (form data)
- **SOAP** Action: `http://tempuri.org/GetAllWorkflowStatistics`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `domainName` | string | No | The library whose workflows are wanted. Empty returns the workflows of every library the caller is a member of. |
| `startDate` | DateTime | No | Start of a date range. With `endDate`, each entry also carries `SubmittedInRange`, `CompletedInRange` and `PendingInRange`. |
| `endDate` | DateTime | No | End of the date range. |

## Response

### Success Response

A `<Workflows>` element with one `<WorkflowStatistics>` per workflow definition, active or not. `DomainName` and `WorkflowName` say which workflow an entry is of. The elements are those of [GetWorkflowStatistics](GetWorkflowStatistics.md), including the two overdue counts explained there.

```xml
<response success="true" error="">
  <Workflows>
    <WorkflowStatistics>
      <DomainName>Invoices</DomainName>
      <WorkflowName>AP Invoice Approval</WorkflowName>
      <ActiveFolderPath>\Invoices</ActiveFolderPath>
      <AverageTimeSpanInHours>192</AverageTimeSpanInHours>
      <AverageTimeSpanInText>8 Days</AverageTimeSpanInText>
      <TotalPending>9</TotalPending>
      <TotalCompleted>0</TotalCompleted>
      <TotalOverdue>0</TotalOverdue>
      <TotalWithOverdueTasks>9</TotalWithOverdueTasks>
    </WorkflowStatistics>
    <WorkflowStatistics>
      ...
    </WorkflowStatistics>
  </Workflows>
</response>
```

Without a date range the three `...InRange` elements are present and nil, as in the single call.

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

## Required Permissions

Any authenticated (not anonymous) user. The workflows are the ones [GetWorkflowDefinitions](GetWorkflowDefinitions.md) returns for the same `domainName`.

## Example

### Request (POST)

```
POST /srv.asmx/GetAllWorkflowStatistics HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123&domainName=Invoices
```

## Notes

- With `domainName` empty the libraries are those the caller is a **member** of, not every library in the system. This is the rule `GetWorkflowDefinitions` has.
- `TotalWithOverdueTasks` is the count of running workflows that have a task past its due date; `TotalOverdue` is the count past the workflow's own due date. See [How overdue is counted](GetWorkflowStatistics.md#how-overdue-is-counted).
- The numbers of each workflow are counted as `GetWorkflowStatistics` counts them, one workflow after the other. The call saves the request and sign-in per workflow, not the counting.

## Related APIs

- [GetWorkflowStatistics](GetWorkflowStatistics.md) - The statistics of one workflow
- [GetWorkflowDefinitions](GetWorkflowDefinitions.md) - The workflow definitions
- [GetAllDomainStatistics](GetAllDomainStatistics.md) - The statistics of every library in one call

## Error Codes

| `errorCode` | When |
|---:|---|
| `4010` | `[901]` the ticket is expired or unknown, or the caller is anonymous |
| `4041` | `domainName` is not a library the caller can see |
