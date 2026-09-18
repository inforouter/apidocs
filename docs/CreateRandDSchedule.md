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
| `RetentionType` | int | -" | Yes | `0` = None, `1` = **Temporary**, `2` = **Permanent**. |
| `RetentionTrigger` | int | -" | Yes for Temporary | `1` = On Create, `2` = On Cutoff. Required when `RetentionType=1`, and `0` (Custom Date Entry) is **refused** there. Forced to `1` when `RetentionType=2`. |
| `RetentionPeriodYears` | int | -" | Yes for Temporary | Years to retain. At least one of years, months and days must be > 0 when `RetentionType=1`. All three are forced to `0` when `RetentionType=2`. |
| `RetentionPeriodMonths` | int | -" | Yes for Temporary | Additional months to retain. |
| `RetentionPeriodDays` | int | -" | Yes for Temporary | Additional days to retain. |
| `DispositionType` | int | -" | Yes | `0` = None, `1` = Final Disposition, `2` = Transfer to External Agency. |
| `DispositionTrigger` | int | -" | Yes if DispositionType > 0 | `0` = Custom Date Entry, `1` = On Create, `2` = On Cutoff, `3` = On Retention End. **Must be `3` when `RetentionType=1`**, and `3` is refused when `RetentionType=0`. |
| `DispositionPeriodYears` | int | -" | Yes if DispositionType > 0 | Years after the disposition trigger. At least one of years, months and days must be > 0. |
| `DispositionPeriodMonths` | int | -" | No | Additional months. |
| `DispositionPeriodDays` | int | -" | No | Additional days. |
| `TransferAgency` | string | 100 | Yes if DispositionType=2 | Agency name for the transfer destination. |
| `MoveFolderId` | int | -" | No | Folder ID for transfer destination folder. |
| `CreateTask` | boolean | -" | No | `true` to create a workflow task when disposition is triggered. Defaults to `true` if omitted; automatically forced to `false` when `DispositionType=0`. |
| `SendEmail` | boolean | -" | No | `true` to send an email notification when disposition is triggered. Defaults to `true` if omitted; automatically forced to `false` when `DispositionType=0`. |

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
  CreateTask="true"
  SendEmail="true"
/>
```

## Response

### Success Response

```xml
<response success="true">
  <RetentionDispositionSchedule DefId="47" />
</response>
```

- `DefId`: Auto-generated integer ID of the new schedule definition. Use this value when assigning the schedule to documents or folders.

### Error Response

```xml
<response success="false" error="[error message]" />
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

Creates a schedule. Every value is an attribute of the root element, and the element's own name is
never looked at.

```javascript
const definition = `
<RetentionDispositionSchedule
    Name="Seven year retention"
    Description="Keep for seven years, then destroy"
    ReferenceNumber="FIN-001"
    SourceAuthority="IRS"
    RecordsSeriesName="Finance"
    RetentionType="1"          <!-- 1 is Temporary, 2 is Permanent -->
    RetentionTrigger="1"       <!-- 1 On create, 2 On cut off -->
    RetentionPeriodYears="7"
    DispositionType="1"        <!-- 1 Final disposition, 2 Transfer -->
    DispositionTrigger="3"     <!-- must be 3, On retention end, when retention is Temporary -->
    DispositionPeriodDays="1"
    CreateTask="false"
    SendEmail="false" />`;

const root = await call('CreateRandDSchedule', {
  authenticationTicket: ticket, RDDefXML: definition
});

const defId = root.querySelector('RetentionDispositionSchedule').getAttribute('DefId');
```

The rules the server enforces, in the order it checks them:

- `Name` and `Description` are both required. The name is at most 128 characters and takes letters,
  digits, `_`, `-`, `.`, `,`, `(`, `)` and spaces only.
- `RetentionType` and `DispositionType` cannot both be `0`.
- **Temporary retention** (`RetentionType="1"`) needs `RetentionTrigger` of `1` or `2` -
  `0`, the default, is refused - and at least one of the three retention periods above zero.
- **Permanent retention** (`RetentionType="2"`) forces the trigger and all three periods to zero and
  **silently turns the disposition off**, whatever the document asked for. The call still succeeds.
- A disposition needs at least one of its three periods above zero.
- `DispositionTrigger="3"`, on retention end, needs a retention type other than `0`.
- With **Temporary** retention and any disposition, `DispositionTrigger` **must** be `3`. The refusal
  for that one quotes a stray minutes abbreviation - the string `dk.` - rather than the rule.

## Notes

- When `RetentionType = 1` (Permanent), all period values are automatically reset to 0 and `RetentionTrigger` is set to `On Create`.
- When `RetentionType = 2` (Temporary), at least one of `RetentionPeriodYears`, `RetentionPeriodMonths`, or `RetentionPeriodDays` must be greater than 0.
- `CreateTask` and `SendEmail` are only meaningful when `DispositionType > 0`. When `DispositionType = 0` (None), both are automatically forced to `false` regardless of the values supplied.
- If `CreateTask` or `SendEmail` are omitted from the XML, they default to `true` (and will then be subject to the DispositionType rule above).
- The returned `DefId` is needed for [SetDocumentRandDSchedule](SetDocumentRandDSchedule.md), [SetFolderRandDSchedule](SetFolderRandDSchedule.md), [GetRandDScheduleInfo](GetRandDScheduleInfo.md), [UpdateRandDSchedule](UpdateRandDSchedule.md), and [DeleteRandDSchedule](DeleteRandDSchedule.md).

## Related APIs

- [GetRandDSchedules](GetRandDSchedules.md) -" List all defined R&D schedule definitions.
- [GetRandDScheduleInfo](GetRandDScheduleInfo.md) -" Get full details of a specific schedule.
- [UpdateRandDSchedule](UpdateRandDSchedule.md) -" Update an existing schedule definition.
- [DeleteRandDSchedule](DeleteRandDSchedule.md) -" Delete a schedule definition.
- [SetDocumentRandDSchedule](SetDocumentRandDSchedule.md) -" Assign a schedule to a document.
- [SetFolderRandDSchedule](SetFolderRandDSchedule.md) -" Assign a schedule to a folder.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown |
| `4030` | the caller may not manage retention schedules - including a caller with no ticket at all |
| `4090` | a schedule of that name already exists |
| `4000` | any of the validation rules above, or `RDDefXML` is not well formed |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |
