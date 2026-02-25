# GetDocumentRandDSchedule API

Returns the Retention and Disposition (R&D) schedule assigned to a document identified by path. Returns the full schedule definition. If no schedule is assigned, returns a `DefId` of `0`.

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
<root success="true">
  <RetentionDispositionSchedule
    DefId="47"
    Name="Standard 7-Year Retention"
    Description="Retain for 7 years then destroy"
    URL=""
    ReferenceNumber="FIN-001"
    SourceAuthority="IRS"
    RecordsSeriesName=""
    RetentionType="2"
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
</root>
```

### Document Has No Schedule

```xml
<root success="true">
  <RetentionDispositionSchedule DefId="0" />
</root>
```

### Error Response

```xml
<root success="false" error="[901]Session expired or Invalid ticket" />
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
| `RetentionType` | `0`=None, `1`=Permanent, `2`=Temporary. |
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

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed -" invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Document not found | No document was found at the specified `Path`. |
