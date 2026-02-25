# CreateRandDSchedule API

Creates a new Retention and Disposition (R&D) schedule definition. Once created, the schedule can be assigned to documents and folders via [SetDocumentRandDSchedule](SetDocumentRandDSchedule.md) and [SetFolderRandDSchedule](SetFolderRandDSchedule.md).

## Endpoint

```
/srv.asmx/CreateRandDSchedule
```

## Methods

- **GET** `/srv.asmx/CreateRandDSchedule?authenticationTicket=...&RDDefXML=...`
- **POST** `/srv.asmx/CreateRandDSchedule` (form data)
- **SOAP** Action: `http://tempuri.org/CreateRandDSchedule`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `RDDefXML` | string | Yes | XML string defining the schedule. See format below. |

### `RDDefXML` Format

The XML must have a root element (element name is not significant) with the following attributes:

| Attribute | Type | Max Length | Required | Description |
|-----------|------|------------|----------|-------------|
| `Name` | string | 128 | Yes | Schedule name. |
| `Description` | string | 255 | Yes | Schedule description. |
| `URL` | string | 255 | No | External documentation URL. |
| `ReferenceNumber` | string | 20 | No | Regulatory reference or citation number. |
| `SourceAuthority` | string | 64 | No | Name of the regulatory authority (e.g., `NARA`). |
| `RecordsSeriesName` | string | 100 | No | Records series name. |
| `RetentionType` | int | -" | Yes | `0` = None, `1` = Permanent, `2` = Temporary. |
| `RetentionTrigger` | int | -" | Yes for Temporary | `0` = Custom Date Entry, `1` = On Create, `2` = On Cutoff. Required when `RetentionType=2`. |
| `RetentionPeriodYears` | int | -" | Yes for Temporary | Years to retain. Must be > 0 combined with months/days when `RetentionType=2`. |
| `RetentionPeriodMonths` | int | -" | Yes for Temporary | Additional months to retain. |
| `RetentionPeriodDays` | int | -" | Yes for Temporary | Additional days to retain. |
| `DispositionType` | int | -" | Yes | `0` = None, `1` = Final Disposition, `2` = Transfer to External Agency. |
| `DispositionTrigger` | int | -" | Yes if DispositionType > 0 | `0` = Custom Date Entry, `1` = On Create, `2` = On Cutoff, `3` = On Retention End. |
| `DispositionPeriodYears` | int | -" | No | Years after retention trigger. |
| `DispositionPeriodMonths` | int | -" | No | Additional months. |
| `DispositionPeriodDays` | int | -" | No | Additional days. |
| `TransferAgency` | string | 100 | Yes if DispositionType=2 | Agency name for the transfer destination. |
| `MoveFolderId` | int | -" | No | Folder ID for transfer destination folder. |

**Example XML:**
```xml
<RDSchedule
  Name="Standard 7-Year Retention"
  Description="Retain documents for 7 years then destroy"
  ReferenceNumber="FIN-001"
  SourceAuthority="IRS"
  RetentionType="2"
  RetentionTrigger="1"
  RetentionPeriodYears="7"
  RetentionPeriodMonths="0"
  RetentionPeriodDays="0"
  DispositionType="1"
  DispositionTrigger="3"
  DispositionPeriodYears="0"
  DispositionPeriodMonths="0"
  DispositionPeriodDays="0"
  TransferAgency=""
  MoveFolderId="0"
/>
```

## Response

### Success Response

```xml
<root success="true">
  <RetentionDispositionSchedule DefId="47" />
</root>
```

- `DefId`: Auto-generated integer ID of the new schedule definition. Use this value when assigning the schedule to documents or folders.

### Error Response

```xml
<root success="false" error="[error message]" />
```

## Required Permissions

Any authenticated user. Anonymous access is not allowed.

## Example

### GET Request

```
GET /srv.asmx/CreateRandDSchedule
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &RDDefXML=<RDSchedule+Name="7-Year+Finance"+Description="Finance+documents+7yr".../>
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/CreateRandDSchedule HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&RDDefXML=<RDSchedule Name="7-Year Finance" Description="Finance documents 7yr" RetentionType="2" RetentionTrigger="1" RetentionPeriodYears="7" RetentionPeriodMonths="0" RetentionPeriodDays="0" DispositionType="1" DispositionTrigger="3" DispositionPeriodYears="0" DispositionPeriodMonths="0" DispositionPeriodDays="0"/>
```

## Notes

- When `RetentionType = 1` (Permanent), all period values are automatically reset to 0 and `RetentionTrigger` is set to `On Create`.
- When `RetentionType = 2` (Temporary), at least one of `RetentionPeriodYears`, `RetentionPeriodMonths`, or `RetentionPeriodDays` must be greater than 0.
- The returned `DefId` is needed for [SetDocumentRandDSchedule](SetDocumentRandDSchedule.md), [SetFolderRandDSchedule](SetFolderRandDSchedule.md), [GetRandDScheduleInfo](GetRandDScheduleInfo.md), [UpdateRandDSchedule](UpdateRandDSchedule.md), and [DeleteRandDSchedule](DeleteRandDSchedule.md).

## Related APIs

- [GetRandDSchedules](GetRandDSchedules.md) -" List all defined R&D schedule definitions.
- [GetRandDScheduleInfo](GetRandDScheduleInfo.md) -" Get full details of a specific schedule.
- [UpdateRandDSchedule](UpdateRandDSchedule.md) -" Update an existing schedule definition.
- [DeleteRandDSchedule](DeleteRandDSchedule.md) -" Delete a schedule definition.
- [SetDocumentRandDSchedule](SetDocumentRandDSchedule.md) -" Assign a schedule to a document.
- [SetFolderRandDSchedule](SetFolderRandDSchedule.md) -" Assign a schedule to a folder.

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed -" invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Invalid XML | The `RDDefXML` is malformed or missing required attributes. |
| Invalid retention period | `RetentionType=2` but no period values > 0. |
| Missing transfer agency | `DispositionType=2` but `TransferAgency` is empty. |
