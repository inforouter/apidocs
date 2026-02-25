# SetClassificationLevel API

Sets the classification level of the specified document or folder. Classification markings control access visibility and are recorded in the classification change log. Optional downgrade and declassify dates can be provided for classified levels (Confidential, Secret, Top Secret).

## Endpoint

```
/srv.asmx/SetClassificationLevel
```

## Methods

- **GET** `/srv.asmx/SetClassificationLevel?AuthenticationTicket=...&Path=...&ClassificationLevel=...`
- **POST** `/srv.asmx/SetClassificationLevel` (form data)
- **SOAP** Action: `http://tempuri.org/SetClassificationLevel`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the document or folder (e.g. `/Finance/Reports/Q1-Report.pdf` or `/Finance/Reports`). Short document ID paths (`~D{id}`) are also accepted for documents. |
| `ClassificationLevel` | int | Yes | The classification level to apply. See the **Classification Level Values** table below. |
| `DowngradeOn` | DateTime | No | Date on which the classification should be downgraded. Only applicable for Confidential (2), Secret (3), and Top Secret (4) levels. Omit or pass `null` to leave unset. |
| `DeclassifyOn` | DateTime | No | Date on which the item should be declassified. Only applicable for Confidential (2), Secret (3), and Top Secret (4) levels. Omit or pass `null` to leave unset. |
| `ReasonForAction` | string | No | Free-text reason for the classification change. Recorded in the classification change log. |
| `Agency` | string | No | Name of the agency responsible for the classification action. Recorded in the classification change log. |

### Classification Level Values

| Value | Name | Description |
|-------|------|-------------|
| `0` | NoMarkings | No classification marking applied. |
| `1` | Declassified | Previously classified, now declassified. |
| `2` | Confidential | Confidential classification. |
| `3` | Secret | Secret classification. |
| `4` | TopSecret | Top Secret classification. |

> **Note:** `DowngradeOn` and `DeclassifyOn` are silently ignored (reset to no-date) when `ClassificationLevel` is `0` (NoMarkings) or `1` (Declassified), as these dates are only meaningful for classified items.

---

## Response

### Success Response

```xml
<response success="true" error="" />
```

### Error Response

```xml
<response success="false" error="Access denied." />
```

---

## Required Permissions

The calling user must have **Change Classification** permission on the target document or folder.

---

## Example

### GET Request

```
GET /srv.asmx/SetClassificationLevel
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports/Q1-2024-Report.pdf
  &ClassificationLevel=3
  &DowngradeOn=2026-01-01
  &DeclassifyOn=2030-01-01
  &ReasonForAction=Annual+review
  &Agency=Finance+Dept
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/SetClassificationLevel HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance/Reports/Q1-2024-Report.pdf
&ClassificationLevel=3
&DowngradeOn=2026-01-01
&DeclassifyOn=2030-01-01
&ReasonForAction=Annual+review
&Agency=Finance+Dept
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:SetClassificationLevel>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:Path>/Finance/Reports/Q1-2024-Report.pdf</tns:Path>
      <tns:ClassificationLevel>3</tns:ClassificationLevel>
      <tns:DowngradeOn>2026-01-01</tns:DowngradeOn>
      <tns:DeclassifyOn>2030-01-01</tns:DeclassifyOn>
      <tns:ReasonForAction>Annual review</tns:ReasonForAction>
      <tns:Agency>Finance Dept</tns:Agency>
    </tns:SetClassificationLevel>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Both **documents** and **folders** are supported. The path is resolved as a document first; if no document is found, it is resolved as a folder.
- For **documents**: if setting a classified level (Confidential, Secret, or Top Secret), the parent folder must allow classified documents (controlled by the `ALLOWCLASSIFIEDDOCUMENTS` folder rule). If not, the call returns an error.
- For **documents**: document subscribers are notified of the classification change upon success.
- For **folders**: no subscriber notification is sent.
- `DowngradeOn` and `DeclassifyOn` accept UTC values, which are automatically converted to server local time.
- Classification changes are written to the **classification change log** (`HistoryCLevelStore`), recording the before/after levels, dates, reason, and agency.
- Passing `ClassificationLevel=0` (NoMarkings) removes all classification markings from the item.

---

## Related APIs

- [GetDocument](GetDocument.md) - Get document properties including the current classification level and dates

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Invalid classification level | The supplied `ClassificationLevel` value is not one of the defined values (0-"4). |
| Document/Folder not found | The specified path does not resolve to an existing document or folder. |
| Folder disallows classified documents | The parent folder's rules do not permit classified documents (applies to documents with level 2-"4). |
| Access denied | The user does not have Change Classification permission on the target item. |
| `SystemError:...` | An unexpected server-side error occurred. |

---
