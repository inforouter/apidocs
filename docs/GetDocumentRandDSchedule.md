# GetDocumentRandDSchedule API

Returns the Retention and Disposition (R&D) schedule assigned to a document identified by
path, as the full schedule definition.

**A document with no schedule answers in one of two shapes.** One that never had a schedule,
and one whose schedule was taken off with
[RemoveDocumentRandDSchedule](RemoveDocumentRandDSchedule.md), answer success with no child
element at all. One whose schedule was cleared by a forced
[DeleteRandDSchedule1](DeleteRandDSchedule1.md) answers a stub
`<RetentionDispositionSchedule DefId="0" />`. Test for both.

## Endpoint

```
/srv.asmx/GetDocumentRandDSchedule
```

## Methods

- **GET** `/srv.asmx/GetDocumentRandDSchedule?authenticationTicket=...&Path=...`
- **POST** `/srv.asmx/GetDocumentRandDSchedule` (form data)
- **SOAP** Action: `http://tempuri.org/GetDocumentRandDSchedule`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1.pdf`). |

## Response

### Document Has a Schedule

```xml
<response success="true">
  <RetentionDispositionSchedule
    DefId="47"
    Name="Standard 7-Year Retention"
    Description="Retain for 7 years then destroy"
    URL=""
    ReferenceNumber="FIN-001"
    SourceAuthority="IRS"
    RecordsSeriesName=""
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
    MoveFolderPath="" />
</response>
```

### Document Has No Schedule

```xml
<response success="true">
  <RetentionDispositionSchedule DefId="0" />
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
| `DefId` | Schedule definition ID. `0` means no schedule is assigned. |
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
| `TransferAgency` | Agency name for external transfer. |
| `MoveFolderId` | Target folder ID for transfer. `0` if not set. |
| `MoveFolderPath` | Target folder path for transfer. |

## Required Permissions

Any authenticated user with read access to the document.

## Example

### GET Request

```
GET /srv.asmx/GetDocumentRandDSchedule
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &Path=/Finance/Reports/Q1-2024.pdf
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/GetDocumentRandDSchedule HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&Path=/Finance/Reports/Q1-2024.pdf
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

Reads the schedule applied to a document, in the same shape `GetRandDScheduleInfo` answers.

```javascript
const root = await call('GetDocumentRandDSchedule', {
  authenticationTicket: ticket, Path: '/Finance/Invoices/inv-1001.pdf'
});

const schedule = root.querySelector('RetentionDispositionSchedule');
if (!schedule || schedule.getAttribute('DefId') === '0') {
  console.log('no schedule on this document');
} else {
  console.log(schedule.getAttribute('Name'));
}
```

**A document with no schedule can answer in two different shapes.** One that never had one, and one
whose schedule was taken off with `RemoveDocumentRandDSchedule`, answer success with **no child
element at all**. One whose schedule was cleared by a forced `DeleteRandDSchedule1` answers a stub
`<RetentionDispositionSchedule DefId="0" />`. Test for both, as the sample does.

A call with no ticket is the anonymous user rather than an error, and it is answered.

## Notes

- Returns `DefId="0"` (with no other attributes) when the document has no R&D schedule assigned.
- To assign a schedule, use [SetDocumentRandDSchedule](SetDocumentRandDSchedule.md).
- To remove an assigned schedule, use [RemoveDocumentRandDSchedule](RemoveDocumentRandDSchedule.md).
- To get the schedule for a folder, use [GetFolderRandDSchedule](GetFolderRandDSchedule.md).

## Related APIs

- [SetDocumentRandDSchedule](SetDocumentRandDSchedule.md) -" Assign an R&D schedule to a document.
- [RemoveDocumentRandDSchedule](RemoveDocumentRandDSchedule.md) -" Remove the R&D schedule from a document.
- [GetFolderRandDSchedule](GetFolderRandDSchedule.md) -" Get the R&D schedule assigned to a folder.
- [GetRandDSchedules](GetRandDSchedules.md) -" List all defined R&D schedule definitions.
- [GetRandDScheduleInfo](GetRandDScheduleInfo.md) -" Get full details of a specific schedule definition.


## What this does not return

The **schedule**, not the document's own dates. The retention period and disposition action come
back here; when the clock started for this particular document, and where it lands, are the
`CutoffDate`, `RetentionDate` and `DispositionDate` attributes of [GetDocument](GetDocument.md).

A document with no schedule (`RDDefId` of `0` on [GetDocument](GetDocument.md)) gets a successful but
empty response from this API rather than an error.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4041` | no document at that path |
| `4030` | the caller may not see that document |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
