# GetRandDScheduleInfo API

Returns the full definition of a specific Retention and Disposition (R&D) schedule identified by its numeric ID.

## Endpoint

```
/srv.asmx/GetRandDScheduleInfo
```

## Methods

- **GET** `/srv.asmx/GetRandDScheduleInfo?authenticationTicket=...&RDDefId=...`
- **POST** `/srv.asmx/GetRandDScheduleInfo` (form data)
- **SOAP** Action: `http://tempuri.org/GetRandDScheduleInfo`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `RDDefId` | integer | Yes | ID of the R&D schedule definition to retrieve. |

## Response

### Success Response

```xml
<response success="true">
  <RetentionDispositionSchedule
    DefId="47"
    Name="Standard 7-Year Retention"
    Description="Retain documents for 7 years then destroy"
    URL="https://regulations.example.com/fin-001"
    ReferenceNumber="FIN-001"
    SourceAuthority="IRS"
    RecordsSeriesName="Financial Records"
    RetentionType="1"
    RetentionTypeText="Temporary"
    RetentionTrigger="1"
    RetentionTriggerText="On Create"
    RetentionPeriodYears="7"
    RetentionPeriodMonths="0"
    RetentionPeriodDays="0"
    DispositionType="1"
    DispositionTypeText="Final Disposition"
    DispositionTrigger="3"
    DispositionTriggerText="Upon Retention End"
    DispositionPeriodYears="0"
    DispositionPeriodMonths="0"
    DispositionPeriodDays="0"
    TransferAgency=""
    MoveFolderId="0"
    MoveFolderPath=""
    CreateTask="true"
    SendEmail="false"
    CreatedById="1"
    CreatedByName="Admin"
    CreationDate="2024-01-15T09:30:00"
    LastUpdatedById="1"
    LastUpdatedByName="Admin"
    LastUpdatedOn="2024-06-20T14:15:00" />
</response>
```

### Error Response

```xml
<response success="false" error="[901]Session expired or Invalid ticket" />
```

## Response Structure

### `<RetentionDispositionSchedule>`

| Attribute | Description |
|-----------|-------------|
| `DefId` | Schedule definition ID. |
| `Name` | Schedule name. |
| `Description` | Schedule description. |
| `URL` | External documentation URL. |
| `ReferenceNumber` | Regulatory reference number. |
| `SourceAuthority` | Regulatory authority name. |
| `RecordsSeriesName` | Records series name. |
| `RetentionType` | `0`=None, `1`=**Temporary**, `2`=**Permanent**. |
| `RetentionTypeText` | Human-readable retention type. |
| `RetentionTrigger` | `0`=Custom Date Entry, `1`=On Create, `2`=On Cutoff. |
| `RetentionTriggerText` | Human-readable trigger name. |
| `RetentionPeriodYears` / `Months` / `Days` | Retention period duration. |
| `DispositionType` | `0`=None, `1`=Final Disposition, `2`=Transfer to External Agency. |
| `DispositionTypeText` | Human-readable disposition type. |
| `DispositionTrigger` | `0`=Custom Date Entry, `1`=On Create, `2`=On Cutoff, `3`=On Retention End. |
| `DispositionTriggerText` | Human-readable trigger name. |
| `DispositionPeriodYears` / `Months` / `Days` | Disposition period duration. |
| `TransferAgency` | Agency name for external transfer (when DispositionType=2). |
| `MoveFolderId` | Target folder ID for transfer. `0` if not set. |
| `MoveFolderPath` | Target folder path for transfer. |
| `CreateTask` | `true` if a workflow task is created when disposition is triggered; `false` otherwise. Always `false` when `DispositionType=0`. |
| `SendEmail` | `true` if an email notification is sent when disposition is triggered; `false` otherwise. Always `false` when `DispositionType=0`. |
| `CreatedById` | User ID of the creator. |
| `CreatedByName` | Username of the creator. |
| `CreationDate` | Date and time the schedule was created. |
| `LastUpdatedById` | User ID of the last updater. |
| `LastUpdatedByName` | Username of the last updater. |
| `LastUpdatedOn` | Date and time the schedule was last modified. |

## Required Permissions

Any authenticated user. Anonymous access is not allowed.

## Example

### GET Request

```
GET /srv.asmx/GetRandDScheduleInfo
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &RDDefId=47
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/GetRandDScheduleInfo HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&RDDefId=47
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

Reads one schedule in full. Each coded value is answered with a translated `...Text` twin, so a
client can show the number or the words.

```javascript
const root = await call('GetRandDScheduleInfo', {
  authenticationTicket: ticket, RDDefId: 18706
});

const schedule = root.querySelector('RetentionDispositionSchedule');
console.log(schedule.getAttribute('Name'),
            schedule.getAttribute('RetentionType'),       // "1"
            schedule.getAttribute('RetentionTypeText'),   // the word, in the caller's language
            schedule.getAttribute('DispositionType'),
            schedule.getAttribute('CreatedByName'),
            schedule.getAttribute('CreationDate'));
```

## Notes

- To get a summary list of all schedules with their IDs, use [GetRandDSchedules](GetRandDSchedules.md).
- To get the schedule currently assigned to a document, use [GetDocumentRandDSchedule](GetDocumentRandDSchedule.md).
- To get the schedule currently assigned to a folder, use [GetFolderRandDSchedule](GetFolderRandDSchedule.md).

## Related APIs

- [GetRandDSchedules](GetRandDSchedules.md) -" List all R&D schedule definitions (summary only).
- [CreateRandDSchedule](CreateRandDSchedule.md) -" Create a new R&D schedule definition.
- [UpdateRandDSchedule](UpdateRandDSchedule.md) -" Update an existing schedule definition.
- [DeleteRandDSchedule](DeleteRandDSchedule.md) -" Delete a schedule definition.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4041` | no schedule by that id |
