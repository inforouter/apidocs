# SetISOReviewDefinition API

Sets the ISO review schedule on a document. Defines when and how the document should be periodically reviewed, who should perform the review (via task or workflow), and what task permissions and completion requirements apply.

## Endpoint

```
/srv.asmx/SetISOReviewDefinition
```

## Methods

- **GET** `/srv.asmx/SetISOReviewDefinition?authenticationTicket=...&documentPath=...&xmlParameters=...`
- **POST** `/srv.asmx/SetISOReviewDefinition` (form data)
- **SOAP** Action: `http://tempuri.org/SetISOReviewDefinition`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `documentPath` | string | Yes | Full path of the document |
| `xmlParameters` | string | Yes | XML-serialized `ISOReviewDefinitionModel` (see below) |

## xmlParameters — ISOReviewDefinitionModel

```xml
<ISOReviewDefinitionModel>
  <StartDate>2024-06-01T00:00:00</StartDate>
  <ScheduleDef>MONTHLY-ON,1,1</ScheduleDef>
  <ReviewByUserId>42</ReviewByUserId>
  <Instructions>Please review this document for accuracy.</Instructions>
  <WorkflowDefId>0</WorkflowDefId>
  <DeadlineHours>48</DeadlineHours>
  <Priority>1</Priority>
  <PermissionChangeDueDate>false</PermissionChangeDueDate>
  <PermissionChangePriority>false</PermissionChangePriority>
  <PermissionChangeFinishDate>false</PermissionChangeFinishDate>
  <RequireSign>false</RequireSign>
  <RequireEdit>false</RequireEdit>
  <RequireLastVersionRead>true</RequireLastVersionRead>
  <RequirePublishedVersionRead>false</RequirePublishedVersionRead>
  <RequireComments>false</RequireComments>
  <RequireApproval>false</RequireApproval>
  <RequireISOReview>false</RequireISOReview>
  <RequireSOXReview>false</RequireSOXReview>
  <RequireArchive>false</RequireArchive>
  <RequireDowngrade>false</RequireDowngrade>
  <RequireDeclassify>false</RequireDeclassify>
</ISOReviewDefinitionModel>
```

### ISOReviewDefinitionModel Fields

| Field | Type | Description |
|-------|------|-------------|
| `StartDate` | datetime | Date from which the review schedule begins |
| `ScheduleDef` | string | Schedule definition string (see formats below) |
| `ReviewByUserId` | int | Reviewer: real user ID, or `-5` = DocumentOwner, `-8` = Submitter |
| `Instructions` | string | Task instructions shown to the reviewer (task mode only; ignored in workflow mode) |
| `WorkflowDefId` | int | `0` = task mode; positive integer = submit to this workflow definition ID |
| `DeadlineHours` | int | Task deadline in total hours from the review trigger date |
| `Priority` | int | Task priority: `0` = Low, `1` = Normal, `2` = High |
| `PermissionChangeDueDate` | bool | Allow reviewer to change the due date |
| `PermissionChangePriority` | bool | Allow reviewer to change the priority |
| `PermissionChangeFinishDate` | bool | Allow reviewer to change the finish date |
| `RequireSign` | bool | Reviewer must sign the document |
| `RequireEdit` | bool | Reviewer must edit the document |
| `RequireLastVersionRead` | bool | Reviewer must read the latest version |
| `RequirePublishedVersionRead` | bool | Reviewer must read the published version |
| `RequireComments` | bool | Reviewer must add a comment |
| `RequireApproval` | bool | Reviewer must approve the document |
| `RequireISOReview` | bool | Task requires ISO review completion |
| `RequireSOXReview` | bool | Task requires SOX review completion |
| `RequireArchive` | bool | Task requires archiving |
| `RequireDowngrade` | bool | Task requires downgrading |
| `RequireDeclassify` | bool | Task requires declassification |

### ScheduleDef Formats

| Format | Example | Description |
|--------|---------|-------------|
| `ONCE` | `ONCE` | Single review, no recurrence |
| `DAILY,N` | `DAILY,30` | Every N days |
| `WEEKLY,freq,dayOfWeek` | `WEEKLY,1,1` | Every `freq` weeks on `dayOfWeek` (0=Sun … 6=Sat) |
| `MONTHLY-ON,freq,day` | `MONTHLY-ON,1,15` | Every `freq` months on the Nth day of the month |
| `MONTHLY-THE,freq,week,dayOfWeek` | `MONTHLY-THE,1,1,1` | Every `freq` months on the Nth weekday |

## Response

### Success Response

```xml
<response success="true" error="" errorCode="0" />
```

### Error Response

```xml
<response success="false" error="Error message" errorCode="4000" />
```

## Required Permissions

The caller must have **Change Document Properties** permission on the document.

## Example

### Set a monthly ISO review assigned to the document owner (POST)

```
POST /srv.asmx/SetISOReviewDefinition HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&documentPath=/Library/Policies/policy.pdf&xmlParameters=<ISOReviewDefinitionModel><StartDate>2024-06-01T00:00:00</StartDate><ScheduleDef>MONTHLY-ON,12,1</ScheduleDef><ReviewByUserId>-5</ReviewByUserId><Instructions>Annual policy review required</Instructions><WorkflowDefId>0</WorkflowDefId><DeadlineHours>168</DeadlineHours><Priority>1</Priority><PermissionChangeDueDate>false</PermissionChangeDueDate><PermissionChangePriority>false</PermissionChangePriority><PermissionChangeFinishDate>false</PermissionChangeFinishDate><RequireSign>false</RequireSign><RequireEdit>false</RequireEdit><RequireLastVersionRead>true</RequireLastVersionRead><RequirePublishedVersionRead>false</RequirePublishedVersionRead><RequireComments>true</RequireComments><RequireApproval>false</RequireApproval><RequireISOReview>false</RequireISOReview><RequireSOXReview>false</RequireSOXReview><RequireArchive>false</RequireArchive><RequireDowngrade>false</RequireDowngrade><RequireDeclassify>false</RequireDeclassify></ISOReviewDefinitionModel>
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

Puts a recurring ISO review on a document. The root element of `xmlParameters` has to be
`<ISOReviewDefinitionModel>` - the serialiser is given that type and nothing else fits.

```javascript
const definition = `
<ISOReviewDefinitionModel>
  <StartDate>2027-01-01T00:00:00</StartDate>
  <ScheduleDef>MONTHLY-ON,1,1</ScheduleDef>
  <ReviewByUserId>101</ReviewByUserId>
  <Instructions>Please review against the standard.</Instructions>
  <WorkflowDefId>0</WorkflowDefId>
  <DeadlineHours>24</DeadlineHours>
  <Priority>5</Priority>
  <PermissionChangeDueDate>false</PermissionChangeDueDate>
  <PermissionChangePriority>false</PermissionChangePriority>
  <PermissionChangeFinishDate>false</PermissionChangeFinishDate>
  <RequireSign>false</RequireSign>
  <RequireEdit>false</RequireEdit>
  <RequireLastVersionRead>false</RequireLastVersionRead>
  <RequirePublishedVersionRead>false</RequirePublishedVersionRead>
  <RequireComments>false</RequireComments>
  <RequireApproval>false</RequireApproval>
  <RequireISOReview>true</RequireISOReview>
  <RequireSOXReview>false</RequireSOXReview>
  <RequireArchive>false</RequireArchive>
  <RequireDowngrade>false</RequireDowngrade>
  <RequireDeclassify>false</RequireDeclassify>
</ISOReviewDefinitionModel>`;

await call('SetISOReviewDefinition', {
  authenticationTicket: ticket,
  documentPath: '/Quality/Procedures/qp-001.pdf',
  xmlParameters: definition
});
```

### ScheduleDef

A comma separated string, not an enum name. The first part is the keyword and the rest are numbers:

| `ScheduleDef` | Means |
|---|---|
| `ONCE` | review once, on the start date |
| `DAILY,<n>` | every *n* days |
| `WEEKLY,<n>,<dayOfWeek>` | every *n* weeks, on that day |
| `MONTHLY-ON,<n>,<day>` | every *n* months, on that day of the month |
| `MONTHLY-THE,<n>,<week>,<weekday>` | every *n* months, on the *week*th *weekday* |

**The numbers are not optional.** The parser reads `parts[1]`, `parts[2]` and `parts[3]` without
checking how many parts there are, so `DAILY` on its own - or `WEEKLY,1` without the day - is a
`5000` `IndexOutOfRangeException` rather than the `4000` an unrecognised keyword gets. An empty
`ScheduleDef` is refused too.

`StartDate` is used: a date in the future is the first review date, and one in the past is rolled
forward to the next occurrence of the schedule.

## Notes

- To remove an existing ISO review schedule, use [`RemoveISOReviewDefinition`](RemoveISOReviewDefinition.md)
- When `WorkflowDefId > 0`, `Instructions` is ignored; the workflow definition provides the task structure
- `ReviewByUserId = -5` assigns the review task to the document owner at review time; `-8` assigns it to the user who submitted the document to the workflow

## Related APIs

- [`RemoveISOReviewDefinition`](RemoveISOReviewDefinition.md) — Remove the ISO review schedule from a document
- [`GetISOReviewDefinition`](GetISOReviewDefinition.md) — Get the current ISO review schedule definition for a document

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | no document at that path, or `ReviewByUserId` is not a user |
| `4000` | `ScheduleDef` is empty or its keyword is not one of the five |
| `5000` | `ScheduleDef` is missing the numbers its keyword needs, or `xmlParameters` is not an `<ISOReviewDefinitionModel>` document |
| `4030` | the caller may not change that document |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
