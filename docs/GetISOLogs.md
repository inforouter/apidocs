# GetISOLogs API

Returns the complete ISO compliance review log for the specified document. Each log entry records a single ISO review event -" the version reviewed, the reviewer, the review date, and the review comment. Use this API to programmatically audit the ISO review history of a document, verify that required reviews have been completed, or export ISO log data for compliance reporting.

## Endpoint

```
/srv.asmx/GetISOLogs
```

## Methods

- **GET** `/srv.asmx/GetISOLogs?AuthenticationTicket=...&DocumentPath=...`
- **POST** `/srv.asmx/GetISOLogs` (form data)
- **SOAP** Action: `http://tempuri.org/GetISOLogs`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DocumentPath` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Procedures/QA-Procedure.pdf`). The path must resolve to an existing document. |

---

## Response

### Success Response

Returns a `<response>` element with `success="true"` containing a `<Value>` element with zero or more `<IsoLog>` child elements -" one per ISO review event recorded for the document, in the order they were stored.

```xml
<response success="true" error="">
  <Value>
    <IsoLog>
      <DocumentId>9871</DocumentId>
      <VersionNumber>1000000</VersionNumber>
      <ReviewDate>2024-06-15T14:30:00</ReviewDate>
      <Comment>Annual ISO 9001 review completed. Procedure verified as current. No changes required.</Comment>
      <UserId>12</UserId>
      <UserName>jsmith</UserName>
    </IsoLog>
    <IsoLog>
      <DocumentId>9871</DocumentId>
      <VersionNumber>1000000</VersionNumber>
      <ReviewDate>2023-06-10T09:00:00</ReviewDate>
      <Comment>Initial ISO review after document publication. Approved.</Comment>
      <UserId>8</UserId>
      <UserName>mjones</UserName>
    </IsoLog>
  </Value>
</response>
```

### IsoLog Field Reference

| Field | Type | Description |
|-------|------|-------------|
| `DocumentId` | int | Internal ID of the document. |
| `VersionNumber` | int | Internal version number of the document version that was reviewed. For standard versioning this is the external version number (`1000000` = Version 1, `2000000` = Version 2). For milestone/patch versioning the value encodes major, minor, and patch: e.g. `1001002` = version `1.1.2`. A value of `0` indicates the version was not recorded. |
| `ReviewDate` | DateTime | Date and time the review was recorded, in ISO 8601 format (`yyyy-MM-ddTHH:mm:ss`). |
| `Comment` | string | The ISO review comment text entered by the reviewer. |
| `UserId` | int | Internal user ID of the reviewer who recorded the log entry. |
| `UserName` | string | Username of the reviewer. |

### No Entries Response

When no ISO log entries exist for the document:

```xml
<response success="true" error="">
  <Value />
</response>
```

### Error Response

```xml
<response success="false" error="Insufficient rights." />
```

---

## Required Permissions

The calling user must satisfy **one of** the following conditions:

1. **`DocumentReadIsoLog`** permission on the document (the document-level "Read ISO Log" access right), **or**
2. **`ViewAuditLogs`** system administration permission on the document's library.

Domain managers and document owners typically have `DocumentReadIsoLog`. System administrators with `ViewAuditLogs` can read ISO logs for any document regardless of document-level permissions.

Additionally, the document must **not** be in an Offline (archived) state.

---

## Example

### GET Request

```
GET /srv.asmx/GetISOLogs
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DocumentPath=/Finance/Procedures/QA-Procedure.pdf
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetISOLogs HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&DocumentPath=/Finance/Procedures/QA-Procedure.pdf
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetISOLogs>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:DocumentPath>/Finance/Procedures/QA-Procedure.pdf</tns:DocumentPath>
    </tns:GetISOLogs>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- **Documents Only**: This API accepts document paths only. Passing a folder path will return a "Document not found" error.
- **Offline Documents**: If the document is in an Offline (archived) state, the API returns an error. Restore the document to an active library before querying its ISO log.
- **Version Number Format**: `VersionNumber` stores the raw internal version value. For standard documents, Version 1 = `1000000`, Version 2 = `2000000`. For documents using milestone/patch versioning, the value encodes `MMMNNNPPP` (major -- 10--- + minor -- 10³ + patch). A value of `0` means the version was not captured at the time of the review.
- **Adding ISO Logs**: Use `AddISOComment` to add a new ISO review comment to a document (requires an assigned ISO Review Task).
- **Dual Permission**: The `DocumentReadIsoLog` document permission and the `ViewAuditLogs` admin permission are checked independently -" either is sufficient.

---

## Related APIs

- [AddISOComment](AddISOComment.md) - Record a new ISO review comment on a document
- [GetISOReviewAssignments](GetISOReviewAssignments.md) - Get the list of ISO review task assignments for a document
- [GetSoxLogs](GetSoxLogs.md) - Get the SOX compliance review log for a document
- [GetDocumentViewLog](GetDocumentViewLog.md) - Get the full view/access log for a document

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Document not found.` | The `DocumentPath` does not resolve to an existing document. |
| `Insufficient rights.` | The caller does not have `DocumentReadIsoLog` permission on the document and does not have the `ViewAuditLogs` admin permission. |
| Document is Offline | The document is in an archived/offline state and its ISO log cannot be retrieved. |
| `SystemError:...` | An unexpected server-side error occurred. |

---
