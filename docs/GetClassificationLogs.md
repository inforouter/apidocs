# GetClassificationLogs API

Returns the full classification history log for the specified document or folder path. Each log entry records a change to the security classification level, including the new level, who made the change, the reason, and any associated downgrade or declassify dates. Use this API to audit classification changes for compliance and governance reporting.

## Endpoint

```
/srv.asmx/GetClassificationLogs
```

## Methods

- **GET** `/srv.asmx/GetClassificationLogs?AuthenticationTicket=...&Path=...`
- **POST** `/srv.asmx/GetClassificationLogs` (form data)
- **SOAP** Action: `http://tempuri.org/GetClassificationLogs`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to a document (e.g. `\Finance\Reports\Q1-Report.pdf`) or a folder (e.g. `\Finance\Reports`). Must resolve to an existing document or folder. The library is derived from the resolved object and determines the required permission scope — see [Required Permissions](#required-permissions). |

---

## Required Permissions

The `Path` parameter is always resolved to a specific document or folder. The permission check is performed against the library that contains that object. This means **only library-level `ViewAuditLogs` permission is required** — system-wide admin rights are not needed.

| Scenario | Required permission |
|----------|---------------------|
| Path resolves to a document | **ViewAuditLogs** for the library containing that document |
| Path resolves to a folder | **ViewAuditLogs** for the library containing that folder |
| Path does not resolve | Error returned — no permission check is performed |

---

## Response

### Success Response

Returns a `<response>` element with `success="true"` containing a `<Value>` element with zero or more `<ClassificationLogEntry>` child elements. Entries are ordered by `ActionDate` **ascending** (oldest first).

```xml
<response success="true" error="">
  <Value>
    <ClassificationLogEntry>
      <ObjectTypeId>1</ObjectTypeId>
      <ObjectType>DOCUMENT</ObjectType>
      <ObjectId>9871</ObjectId>
      <ObjectName>Q1-2024-Report.pdf</ObjectName>
      <DomainId>5</DomainId>
      <DomainName>Finance</DomainName>
      <Path>/Finance/Reports/Q1-2024-Report.pdf</Path>
      <BeforeClassificationLevelId>0</BeforeClassificationLevelId>
      <BeforeClassificationLevel>NoMarkings</BeforeClassificationLevel>
      <BeforeDowngradeOn>0001-01-01T00:00:00</BeforeDowngradeOn>
      <BeforeDeclassifyOn>0001-01-01T00:00:00</BeforeDeclassifyOn>
      <ClassificationLevelId>3</ClassificationLevelId>
      <ClassificationLevel>Secret</ClassificationLevel>
      <DowngradeOn>2026-01-01T00:00:00</DowngradeOn>
      <DeclassifyOn>2028-06-01T00:00:00</DeclassifyOn>
      <ReasonForAction>Classified for Q1 sensitivity review period.</ReasonForAction>
      <ActionDate>2024-06-15T14:30:00</ActionDate>
      <ActionbyId>12</ActionbyId>
      <ActionByName>jsmith</ActionByName>
      <FolderId>0</FolderId>
      <Agency>Finance Division</Agency>
    </ClassificationLogEntry>
  </Value>
</response>
```

### ClassificationLogEntry Field Reference

| Field | Type | Description |
|-------|------|-------------|
| `ObjectTypeId` | int | Numeric object type: `1` = Document, `2` = Folder. |
| `ObjectType` | string | Object type label: `DOCUMENT` or `FOLDER`. |
| `ObjectId` | int | Internal ID of the document or folder. |
| `ObjectName` | string | Name of the document or folder. |
| `DomainId` | int | Internal ID of the library/domain. |
| `DomainName` | string | Name of the library/domain. |
| `Path` | string | Full infoRouter path of the item at the time of the classification change. |
| `BeforeClassificationLevelId` | int | Classification level ID before the change (`0` if not recorded). |
| `BeforeClassificationLevel` | string | Classification level name before the change. |
| `BeforeDowngradeOn` | DateTime | Scheduled downgrade date before the change (`0001-01-01` if not set). |
| `BeforeDeclassifyOn` | DateTime | Scheduled declassify date before the change (`0001-01-01` if not set). |
| `ClassificationLevelId` | int | New classification level ID after the change. |
| `ClassificationLevel` | string | New classification level name after the change. |
| `DowngradeOn` | DateTime | New scheduled downgrade date (`0001-01-01` if not set). |
| `DeclassifyOn` | DateTime | New scheduled declassify date (`0001-01-01` if not set). |
| `ReasonForAction` | string | Reason entered by the user when making the classification change. |
| `ActionDate` | DateTime | Date and time the classification was changed. |
| `ActionbyId` | int | Internal user ID of the person who made the change. |
| `ActionByName` | string | Username of the person who made the change. |
| `FolderId` | int | Parent folder ID (`0` for document-level entries). |
| `Agency` | string | Agency or organisational unit associated with the classification. |

### ClassificationLevel Values

| ID | Name | Description |
|----|------|-------------|
| `0` | `NoMarkings` | No classification markings applied. |
| `1` | `Declassified` | Document has been formally declassified. |
| `2` | `Confidential` | Confidential classification. |
| `3` | `Secret` | Secret classification. |
| `4` | `TopSecret` | Top Secret classification. |

### No Entries Response

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

## Example Requests

### GET

```
GET /srv.asmx/GetClassificationLogs?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301&Path=/Finance/Reports/Q1-2024-Report.pdf HTTP/1.1
Host: server.example.com
```

### POST

```
POST /srv.asmx/GetClassificationLogs HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301&Path=/Finance/Reports/Q1-2024-Report.pdf
```

### SOAP 1.1

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetClassificationLogs"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetClassificationLogs xmlns="http://tempuri.org/">
      <AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</AuthenticationTicket>
      <Path>/Finance/Reports/Q1-2024-Report.pdf</Path>
    </GetClassificationLogs>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- **Library-level permission only**: because `Path` always resolves to a specific object, the access check is always scoped to that object's library. System-wide admin rights are not required.
- **Documents and folders**: the `Path` parameter accepts both document and folder paths.
- **Chronological order**: entries are always returned in ascending `ActionDate` order (oldest first).
- **Before fields**: `Before*` fields reflect the state before the change. In older log entries these may be `0` / `NoMarkings` / `0001-01-01` if the previous state was not recorded at the time.
- **Date format**: `ActionDate`, `DowngradeOn`, `DeclassifyOn`, and their `Before*` counterparts are ISO 8601 date-time strings. A value of `0001-01-01T00:00:00` indicates that no date was set.
- **Path not found**: if `Path` does not resolve to any existing document or folder, an error is returned.
- **No date or user filter**: this API returns all classification events for the exact path specified. Use `Path` alone to scope the results.

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Insufficient rights.` | The caller does not have `ViewAuditLogs` permission for the library containing the resolved object. |
| Path not found | The specified `Path` does not resolve to an existing document or folder. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

## Related APIs

- [SetClassificationLevel](SetClassificationLevel.md) - Set the classification level of a document or folder
- [GetDeleteLog](GetDeleteLog.md) - Get the deletion log for documents and folders
- [GetSecurityChangeLog](GetSecurityChangeLog.md) - Get the security (access control) change log
- [GetOwnershipChangeLog](GetOwnershipChangeLog.md) - Get the ownership change log
