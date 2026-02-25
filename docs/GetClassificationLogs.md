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
| `Path` | string | Yes | Full infoRouter path to a document (e.g. `/Finance/Reports/Q1-Report.pdf`) or a folder (e.g. `/Finance/Reports`). The path must resolve to an existing document or folder. |

---

## Response

### Success Response

Returns a `<response>` element with `success="true"` containing a `<Value>` element, which holds zero or more `<ClassificationLogEntry>` child elements -" one per classification change event. Entries are ordered by `ActionDate` ascending.

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
      <ClassificationLevelId>1</ClassificationLevelId>
      <ClassificationLevel>Declassified</ClassificationLevel>
      <DowngradeOn>0001-01-01T00:00:00</DowngradeOn>
      <DeclassifyOn>0001-01-01T00:00:00</DeclassifyOn>
      <ReasonForAction>Review period concluded. Document declassified.</ReasonForAction>
      <ActionDate>2024-09-01T09:00:00</ActionDate>
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
| `Path` | string | Full infoRouter path of the item at the time of classification change. |
| `BeforeClassificationLevelId` | int | Classification level ID before the change (may be `0` if not recorded). |
| `BeforeClassificationLevel` | string | Classification level name before the change (see `ClassificationLevel` values). |
| `BeforeDowngradeOn` | DateTime | Scheduled downgrade date before the change (`0001-01-01` if not set). |
| `BeforeDeclassifyOn` | DateTime | Scheduled declassify date before the change (`0001-01-01` if not set). |
| `ClassificationLevelId` | int | New classification level ID after the change (see values below). |
| `ClassificationLevel` | string | New classification level name after the change. |
| `DowngradeOn` | DateTime | New scheduled downgrade date (`0001-01-01` if not set). |
| `DeclassifyOn` | DateTime | New scheduled declassify date (`0001-01-01` if not set). |
| `ReasonForAction` | string | Reason entered by the user when making the classification change. |
| `ActionDate` | DateTime | Date and time the classification was changed. |
| `ActionbyId` | int | Internal user ID of the person who made the change. |
| `ActionByName` | string | Username of the person who made the change. |
| `FolderId` | int | Parent folder ID (may be `0` for document-level entries). |
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

When no classification changes have been logged for the path:

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

The calling user must be authenticated and must have the **`ViewAuditLogs`** administration permission. This is typically granted to compliance officers, records managers, and system administrators.

---

## Example

### GET Request

```
GET /srv.asmx/GetClassificationLogs
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports/Q1-2024-Report.pdf
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetClassificationLogs HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance/Reports/Q1-2024-Report.pdf
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetClassificationLogs>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:Path>/Finance/Reports/Q1-2024-Report.pdf</tns:Path>
    </tns:GetClassificationLogs>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- **Documents and Folders**: The `Path` parameter accepts both document paths and folder paths. For a folder path, entries include classification changes applied directly to the folder object as well as any folder-level classification events.
- **Chronological Order**: Log entries are always returned in ascending `ActionDate` order (oldest first).
- **BeforeClassificationLevel Fields**: The `Before*` fields reflect the state before the change. In older log entries these may be `0` / `NoMarkings` / `0001-01-01` if the previous state was not recorded at the time.
- **Date Format**: `ActionDate`, `DowngradeOn`, `DeclassifyOn`, and their `Before*` counterparts are ISO 8601 date-time strings. A value of `0001-01-01T00:00:00` indicates that no date was set.
- **Path Not Found**: If the given `Path` does not resolve to any existing document or folder, an error is returned.
- **No Filter**: This API returns all classification events recorded for the exact document or folder specified; there is no date range or user filter. Use the `Path` parameter alone to scope the results.

---

## Related APIs

- [SetClassificationLevel](SetClassificationLevel.md) - Set the classification level of a document or folder
- [GetDeleteLog](GetDeleteLog.md) - Get the deletion log for documents and folders
- [GetSecurityChangeLog](GetSecurityChangeLog.md) - Get the security (access control) change log
- [GetOwnershipChangeLog](GetOwnershipChangeLog.md) - Get the ownership change log

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Insufficient rights.` | The calling user does not have the `ViewAuditLogs` admin permission. |
| Path not found | The specified `Path` does not resolve to an existing document or folder. |
| `SystemError:...` | An unexpected server-side error occurred. |

---
