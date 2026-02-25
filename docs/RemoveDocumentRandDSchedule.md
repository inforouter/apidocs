# RemoveDocumentRandDSchedule API

Removes (unassigns) the Retention and Disposition (R&D) schedule from a document identified by path. After this call the document has no R&D schedule.

## Endpoint

```
/srv.asmx/RemoveDocumentRandDSchedule
```

## Methods

- **GET** `/srv.asmx/RemoveDocumentRandDSchedule?authenticationTicket=...&Path=...`
- **POST** `/srv.asmx/RemoveDocumentRandDSchedule` (form data)
- **SOAP** Action: `http://tempuri.org/RemoveDocumentRandDSchedule`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1.pdf`). |

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

The calling user must have write access to the document.

## Example

### GET Request

```
GET /srv.asmx/RemoveDocumentRandDSchedule
    ?authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
    &Path=/Finance/Reports/Q1-2024.pdf
HTTP/1.1
Host: yourserver
```

### POST Request

```
POST /srv.asmx/RemoveDocumentRandDSchedule HTTP/1.1
Host: yourserver
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c&Path=/Finance/Reports/Q1-2024.pdf
```

## Notes

- If the document has no schedule assigned, the call succeeds without error (no-op).
- Removing a schedule clears the computed retention and disposition dates from the document.
- This operation is required before deleting the schedule definition via [DeleteRandDSchedule](DeleteRandDSchedule.md) if the schedule is assigned to documents.
- To assign a schedule, use [SetDocumentRandDSchedule](SetDocumentRandDSchedule.md).
- To remove a schedule from a folder hierarchy, use [RemoveFolderRandDSchedule](RemoveFolderRandDSchedule.md).

## Related APIs

- [SetDocumentRandDSchedule](SetDocumentRandDSchedule.md) -" Assign an R&D schedule to a document.
- [GetDocumentRandDSchedule](GetDocumentRandDSchedule.md) -" Get the R&D schedule currently assigned to a document.
- [RemoveFolderRandDSchedule](RemoveFolderRandDSchedule.md) -" Remove the R&D schedule from a folder hierarchy.
- [DeleteRandDSchedule](DeleteRandDSchedule.md) -" Delete an R&D schedule definition.

## Error Codes

| Error | Description |
|-------|-------------|
| `[900]` | Authentication failed -" invalid credentials. |
| `[901]` | Session expired or invalid authentication ticket. |
| Access Denied | Caller does not have write access to the document. |
| Document not found | No document was found at the specified `Path`. |
