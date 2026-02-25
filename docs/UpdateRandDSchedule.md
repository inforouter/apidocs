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
| `RetentionType` | int | -" | Yes | `0`=None, `1`=Permanent, `2`=Temporary. |
| `RetentionTrigger` | int | -" | Yes for Temporary | `0`=Custom Date Entry, `1`=On Create, `2`=On Cutoff. |
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

## Response

### Success Response

```xml
<root success="true" />
```

### Error Response

```xml
<root success="false" error="[901]Session expired or Invalid ticket" />
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

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&RDdefId=47&ApplyToExistingDocumentFolders=true&NewRDDefXML=<RDSchedule Name="10-Year Finance" Description="Updated to 10yr" RetentionType="2" RetentionTrigger="1" RetentionPeriodYears="10" RetentionPeriodMonths="0" RetentionPeriodDays="0" DispositionType="1" DispositionTrigger="3" DispositionPeriodYears="0" DispositionPeriodMonths="0" DispositionPeriodDays="0"/>
```

## Notes

- When `ApplyToExistingDocumentFolders = true`, all documents and folders currently assigned this schedule have their retention end dates and disposition dates recalculated immediately. For large organizations with many affected objects this operation may take some time.
- When `ApplyToExistingDocumentFolders = false`, existing dates are left unchanged; only the schedule definition itself is updated.
- Changes that trigger recalculation include: RetentionType, RetentionTrigger, any RetentionPeriod values, DispositionType, DispositionTrigger, any DispositionPeriod values, and MoveFolderId.
- To get the schedule ID, call [GetRandDSchedules](GetRandDSchedules.md).
- To view the full schedule definition before updating, call [GetRandDScheduleInfo](GetRandDScheduleInfo.md).

## Related APIs

- [CreateRandDSchedule](CreateRandDSchedule.md) -" Create a new R&D schedule definition.
- [DeleteRandDSchedule](DeleteRandDSchedule.md) -" Delete an R&D schedule definition.
- [GetRandDSchedules](GetRandDSchedules.md) -" List all R&D schedule definitions.
- [GetRandDScheduleInfo](GetRandDScheduleInfo.md) -" Get full details of a specific schedule.

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed -" invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Access Denied | Caller is not a Retention & Disposition Manager or System Administrator. |
| Schedule not found | No schedule with the specified `RDdefId` exists. |
| Invalid XML | The `NewRDDefXML` is malformed or missing required attributes. |
