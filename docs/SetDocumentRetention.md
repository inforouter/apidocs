# SetDocumentRetention API

> **Obsolete since infoRouter 8.1.155.** This API always returns an error and must not be used in new integrations. Use [`SetDocumentRandDSchedule`](SetDocumentRandDSchedule.md) to manage document retention.

Sets the retention period of the specified document. This method was used to mark a document as having no retention, permanent retention, or retention until a specified date. As of version 8.1.155, the API is disabled — every call returns an error regardless of the parameters supplied. All retention management is now handled through the Retention & Disposition schedule system.

## Endpoint

```
/srv.asmx/SetDocumentRetention
```

## Methods

- **GET** `/srv.asmx/SetDocumentRetention?authenticationTicket=...&path=...&retentionStatus=...&retainUntil=...`
- **POST** `/srv.asmx/SetDocumentRetention` (form data)
- **SOAP** Action: `http://tempuri.org/SetDocumentRetention`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1-Report.pdf`). |
| `retentionStatus` | short (int16) | Yes | Retention mode. Valid values: `0` = No Retention, `1` = Forever, `2` = Until Specified Date. |
| `retainUntil` | DateTime | No | Required when `retentionStatus` is `2`. The date until which the document must be retained (e.g. `2030-12-31`). Ignored for other status values. |

> **Note:** These parameters are accepted by the endpoint signature but are not evaluated. The API returns an error for every call.

---

## Response

### Error Response (always returned)

```xml
<root success="false" error="'SetDocumentRetention' infoRouter Web Service API is obsolete. Please follow the new API documentation." />
```

This API **never** returns a success response. Every call returns the error above.

---

## Required Permissions

Not applicable — the API is disabled and returns an error for all callers regardless of permissions.

---

## Example

### GET Request

```
GET /srv.asmx/SetDocumentRetention
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &path=/Finance/Reports/Q1-2024-Report.pdf
  &retentionStatus=2
  &retainUntil=2030-12-31
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/SetDocumentRetention HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&path=/Finance/Reports/Q1-2024-Report.pdf
&retentionStatus=2
&retainUntil=2030-12-31
```

---

## Notes

- This API has been **disabled since infoRouter 8.1.155**. The implementation returns an error immediately without performing any operation.
- Do not use this API in any new or existing integration. Migrate to [`SetDocumentRandDSchedule`](SetDocumentRandDSchedule.md), which applies a named Retention & Disposition schedule to a document.
- The original retention model (NoRetention / Forever / Until Date) has been superseded by the more flexible R&D schedule system.

---

## Related APIs

- [SetDocumentRandDSchedule](SetDocumentRandDSchedule.md) - Assign a Retention & Disposition schedule to a document (replacement for this API)
- [GetDocumentRandDSchedule](GetDocumentRandDSchedule.md) - Get the current R&D schedule assigned to a document
- [RemoveDocumentRandDSchedule](RemoveDocumentRandDSchedule.md) - Remove the R&D schedule from a document
- [GetRandDSchedules](GetRandDSchedules.md) - List all defined R&D schedule definitions

---

## Error Codes

| Error | Description |
|-------|-------------|
| `'SetDocumentRetention' infoRouter Web Service API is obsolete. Please follow the new API documentation.` | This is the only response this API ever returns. The API is disabled. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/SetDocumentRetention*
