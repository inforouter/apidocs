# GetRandDSchedules API

Returns a summary list of all Retention and Disposition (R&D) schedule definitions defined in the system. For full details on a specific schedule, use [GetRandDScheduleInfo](GetRandDScheduleInfo.md).

## Endpoint

```
/srv.asmx/GetRandDSchedules
```

## Methods

- **GET** `/srv.asmx/GetRandDSchedules?authenticationTicket=...`
- **POST** `/srv.asmx/GetRandDSchedules` (form data)
- **SOAP** Action: `http://tempuri.org/GetRandDSchedules`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |

## Response

### Success Response

```xml
<response success="true">
  <RetentionAndDispositionSchedules>
    <RetentionAndDispositionSchedule
      RDDefID="47"
      RDName="Standard 7-Year Retention"
      Description="Retain documents for 7 years then destroy"
      RetentionType="1"
      RetentionTypeText="Temporary"
      DispositionType="2"
      DispositionTypeText="Destroy" />
    <RetentionAndDispositionSchedule
      RDDefID="48"
      RDName="Permanent Legal Hold"
      Description="Permanent retention for legal documents"
      RetentionType="2"
      RetentionTypeText="Permanent"
      DispositionType="0"
      DispositionTypeText="None" />
  </RetentionAndDispositionSchedules>
</response>
```

### No Schedules Defined

```xml
<response success="true">
  <RetentionAndDispositionSchedules />
</response>
```

### Error Response

```xml
<response success="false" error="[901]Session expired or Invalid ticket" />
```

## Response Structure

### `<RetentionAndDispositionSchedules>`
Container element for all schedule summaries.

### `<RetentionAndDispositionSchedule>`
| Attribute | Description |
|-----------|-------------|
| `RDDefID` | Numeric ID of the schedule definition. Use this value in other R&D APIs. |
| `RDName` | Schedule name. |
| `Description` | Schedule description. |
| `RetentionType` | Numeric code for the retention type. |
| `RetentionTypeText` | Human-readable label for the retention type (localized). |
| `DispositionType` | Numeric code for the disposition type. |
| `DispositionTypeText` | Human-readable label for the disposition type (localized). |

## Required Permissions

Any authenticated user. Anonymous access is not allowed.

## Example

### GET Request

```
GET /srv.asmx/GetRandDSchedules
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/GetRandDSchedules HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
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

Lists every schedule, as a summary rather than the whole definition.

```javascript
const root = await call('GetRandDSchedules', { authenticationTicket: ticket });

for (const schedule of root.querySelectorAll('RetentionAndDispositionSchedule')) {
  console.log(schedule.getAttribute('RDDefID'),
              schedule.getAttribute('RDName'),
              schedule.getAttribute('RetentionTypeText'));
}
```

**The names are not the ones the single-schedule reader uses.** This list answers
`<RetentionAndDispositionSchedule RDDefID="…" RDName="…">`, where `GetRandDScheduleInfo` answers
`<RetentionDispositionSchedule DefId="…" Name="…">`. The list carries the two types and their
translated text and nothing else - for the triggers and periods, read the schedule by its id.

## Notes

- Returns a summary list of all schedules including retention and disposition type codes and their localized text labels. For the complete definition with all settings and audit information, call [GetRandDScheduleInfo](GetRandDScheduleInfo.md) with the `RDDefID`.
- All schedules in the system are returned regardless of assignment status.

## Related APIs

- [GetRandDScheduleInfo](GetRandDScheduleInfo.md) -" Get full details of a specific schedule.
- [CreateRandDSchedule](CreateRandDSchedule.md) -" Create a new R&D schedule definition.
- [UpdateRandDSchedule](UpdateRandDSchedule.md) -" Update an existing schedule definition.
- [DeleteRandDSchedule](DeleteRandDSchedule.md) -" Delete a schedule definition.
- [SetDocumentRandDSchedule](SetDocumentRandDSchedule.md) -" Assign a schedule to a document.
- [SetFolderRandDSchedule](SetFolderRandDSchedule.md) -" Assign a schedule to a folder.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
