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
<root success="true">
  <RetentionAndDispositionSchedules>
    <RetentionAndDispositionSchedule
      RDDefID="47"
      RDName="Standard 7-Year Retention"
      Description="Retain documents for 7 years then destroy" />
    <RetentionAndDispositionSchedule
      RDDefID="48"
      RDName="Permanent Legal Hold"
      Description="Permanent retention for legal documents" />
  </RetentionAndDispositionSchedules>
</root>
```

### No Schedules Defined

```xml
<root success="true">
  <RetentionAndDispositionSchedules />
</root>
```

### Error Response

```xml
<root success="false" error="[901]Session expired or Invalid ticket" />
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

## Notes

- Returns a summary list (ID, name, description only). For the full definition including retention/disposition settings and audit information, call [GetRandDScheduleInfo](GetRandDScheduleInfo.md) with the `RDDefID`.
- All schedules in the system are returned regardless of assignment status.

## Related APIs

- [GetRandDScheduleInfo](GetRandDScheduleInfo.md) -" Get full details of a specific schedule.
- [CreateRandDSchedule](CreateRandDSchedule.md) -" Create a new R&D schedule definition.
- [UpdateRandDSchedule](UpdateRandDSchedule.md) -" Update an existing schedule definition.
- [DeleteRandDSchedule](DeleteRandDSchedule.md) -" Delete a schedule definition.
- [SetDocumentRandDSchedule](SetDocumentRandDSchedule.md) -" Assign a schedule to a document.
- [SetFolderRandDSchedule](SetFolderRandDSchedule.md) -" Assign a schedule to a folder.

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed -" invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
