# UpdateRandDSchedule API

Updates an existing Retention and Disposition (R&D) schedule definition. Optionally recalculates retention and disposition dates for all documents and folders currently using this schedule.

## Endpoint

```
/srv.asmx/UpdateRandDSchedule
```

## Methods

- **GET** `/srv.asmx/UpdateRandDSchedule?authenticationTicket=...&RDdefId=...&ApplyToExistingDocumentFolders=...&NewRDDefXML=...`
- **POST** `/srv.asmx/UpdateRandDSchedule` (form data)
- **SOAP** Action: `http://tempuri.org/UpdateRandDSchedule`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `RDdefId` | integer | Yes | ID of the R&D schedule definition to update. |
| `ApplyToExistingDocumentFolders` | boolean | Yes | `true` to recalculate dates for all documents and folders already assigned this schedule. `false` to apply the changes only to future assignments. |
| `NewRDDefXML` | string | Yes | XML string with the updated schedule definition. Same format as [CreateRandDSchedule](CreateRandDSchedule.md). |

### `NewRDDefXML` Format

The XML must have a root element (element name is not significant) with the following attributes:

| Attribute | Type | Max Length | Required | Description |
|-----------|------|------------|----------|-------------|
| `Name` | string | 128 | Yes | Schedule name. |
| `Description` | string | 255 | Yes | Schedule description. |
| `URL` | string | 255 | No | External documentation URL. |
| `ReferenceNumber` | string | 20 | No | Regulatory reference number. |
| `SourceAuthority` | string | 64 | No | Regulatory authority name. |
| `RecordsSeriesName` | string | 100 | No | Records series name. |
| `RetentionType` | int | -" | Yes | `0`=None, `1`=**Temporary**, `2`=**Permanent**. |
| `RetentionTrigger` | int | -" | Yes for Temporary | `1`=On Create, `2`=On Cutoff. Required when `RetentionType=1`, and `0` (Custom Date Entry) is refused there. |
| `RetentionPeriodYears` | int | -" | Yes for Temporary | Years to retain. |
| `RetentionPeriodMonths` | int | -" | Yes for Temporary | Additional months. |
| `RetentionPeriodDays` | int | -" | Yes for Temporary | Additional days. |
| `DispositionType` | int | -" | Yes | `0`=None, `1`=Final Disposition, `2`=Transfer to External Agency. |
| `DispositionTrigger` | int | -" | Yes if DispositionType > 0 | `0`=Custom Date Entry, `1`=On Create, `2`=On Cutoff, `3`=On Retention End. |
| `DispositionPeriodYears` | int | -" | No | Years after retention trigger. |
| `DispositionPeriodMonths` | int | -" | No | Additional months. |
| `DispositionPeriodDays` | int | -" | No | Additional days. |
| `TransferAgency` | string | 100 | Yes if DispositionType=2 | Agency name for transfer destination. |
| `MoveFolderId` | int | -" | No | Target folder ID for transfer. |
| `CreateTask` | boolean | -" | No | `true` to create a workflow task when disposition is triggered. Defaults to `true` if omitted; automatically forced to `false` when `DispositionType=0`. |
| `SendEmail` | boolean | -" | No | `true` to send an email notification when disposition is triggered. Defaults to `true` if omitted; automatically forced to `false` when `DispositionType=0`. |

## Response

### Success Response

```xml
<response success="true" />
```

### Error Response

```xml
<response success="false" error="[901]Session expired or Invalid ticket" />
```

## Required Permissions

**Retention & Disposition Manager** or **System Administrator**. Regular users receive an access denied error.

## Example

### GET Request

```
GET /srv.asmx/UpdateRandDSchedule
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &RDdefId=47
    &ApplyToExistingDocumentFolders=true
    &NewRDDefXML=<RDSchedule+Name="10-Year+Finance"+.../>
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/UpdateRandDSchedule HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&RDdefId=47&ApplyToExistingDocumentFolders=true&NewRDDefXML=<RDSchedule Name="10-Year Finance" Description="Updated to 10yr" RetentionType="2" RetentionTrigger="1" RetentionPeriodYears="10" RetentionPeriodMonths="0" RetentionPeriodDays="0" DispositionType="1" DispositionTrigger="3" DispositionPeriodYears="0" DispositionPeriodMonths="0" DispositionPeriodDays="0" CreateTask="true" SendEmail="true"/>
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

Rewrites a schedule in place, keeping its id. `NewRDDefXML` takes exactly the document
[CreateRandDSchedule](CreateRandDSchedule.md) describes and runs the same validation.

```javascript
await call('UpdateRandDSchedule', {
  authenticationTicket: ticket,
  RDdefId: 18706,
  ApplyToExistingDocumentFolders: true,   // recompute the dates on everything already carrying it
  NewRDDefXML: `
    <RetentionDispositionSchedule
        Name="Seven year retention"
        Description="Keep for seven years, then destroy"
        RetentionType="1" RetentionTrigger="2" RetentionPeriodYears="7"
        DispositionType="1" DispositionTrigger="3" DispositionPeriodDays="1" />`
});
```

The id survives, and the schedule records who made the change - `GetRandDScheduleInfo` answers
`LastUpdatedByName` and `LastUpdatedOn`, which a schedule that has never been updated leaves empty.

## Notes

- When `ApplyToExistingDocumentFolders = true`, all documents and folders currently assigned this schedule have their retention end dates and disposition dates recalculated immediately. For large organizations with many affected objects this operation may take some time.
- When `ApplyToExistingDocumentFolders = false`, existing dates are left unchanged; only the schedule definition itself is updated.
- Changes that trigger recalculation include: RetentionType, RetentionTrigger, any RetentionPeriod values, DispositionType, DispositionTrigger, any DispositionPeriod values, and MoveFolderId.
- `CreateTask` and `SendEmail` are only meaningful when `DispositionType > 0`. When `DispositionType = 0` (None), both are automatically forced to `false` regardless of the values supplied.
- If `CreateTask` or `SendEmail` are omitted from the XML, they default to `true` (and will then be subject to the DispositionType rule above).
- To get the schedule ID, call [GetRandDSchedules](GetRandDSchedules.md).
- To view the full schedule definition before updating, call [GetRandDScheduleInfo](GetRandDScheduleInfo.md).

## Related APIs

- [CreateRandDSchedule](CreateRandDSchedule.md) -" Create a new R&D schedule definition.
- [DeleteRandDSchedule](DeleteRandDSchedule.md) -" Delete an R&D schedule definition.
- [GetRandDSchedules](GetRandDSchedules.md) -" List all R&D schedule definitions.
- [GetRandDScheduleInfo](GetRandDScheduleInfo.md) -" Get full details of a specific schedule.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4030` | the caller may not manage retention schedules - including a caller with no ticket at all |
| `4041` | no schedule by that id |
| `4090` | the new name is already another schedule's |
| `4000` | any of the validation rules on CreateRandDSchedule, or `NewRDDefXML` is not well formed |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
