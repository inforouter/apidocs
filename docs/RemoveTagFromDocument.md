# RemoveTagFromDocument API

Removes a specific applied tag from a document. Because a document may have the same tag applied multiple times (e.g. by different users or at different times), the API requires an exact match on **all** identifying fields -" tag text, version number, date applied, and the user who applied it. Use this API to remove a tag that was applied via a workflow step or via `SetTagToDocument` when it is no longer appropriate.

## Endpoint

```
/srv.asmx/RemoveTagFromDocument
```

## Methods

- **GET** `/srv.asmx/RemoveTagFromDocument?authenticationTicket=...&path=...&tagText=...&tagDate=...&taggedBy=...&versionNumber=...`
- **POST** `/srv.asmx/RemoveTagFromDocument` (form data)
- **SOAP** Action: `http://tempuri.org/RemoveTagFromDocument`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1-Report.pdf`). |
| `tagText` | string | Yes | Exact text of the tag to remove. Must be case-sensitive and match the stored value exactly. Obtain the exact tag text from the document's applied tag list or from `GetTagDefintions`. |
| `tagDate` | DateTime | Yes | The exact date and time the tag was applied, in `yyyy-MM-ddTHH:mm:ss` format. UTC values are automatically converted to server local time before matching. Must match the stored `TAGDATE` value exactly. |
| `taggedBy` | int | Yes | Internal user ID of the user who applied the tag. Must match the stored `TAGGEDBYID` value exactly. Obtain via `GetUser` or `GetAllUsers`. |
| `versionNumber` | int | Yes | Internal version number of the document version the tag was applied to. This is the raw internal version number (e.g. `1000000` for Version 1, `2000000` for Version 2). Must match the stored `VERSIONNUMBER` value exactly. |

---

## Response

### Success Response

```xml
<response success="true" />
```

> **Note:** A `success="true"` response is returned even if no matching tag record was found. The underlying `DELETE` statement deletes zero rows silently -" no error is raised for a non-matching combination.

### Error Response

```xml
<response success="false" error="Insufficient rights." />
```

---

## Required Permissions

The calling user must have the **`DocumentPropertyChange`** permission on the document. This is typically granted to document owners, domain managers, and users with Edit access. Read-only users cannot remove tags.

---

## Example

### GET Request

```
GET /srv.asmx/RemoveTagFromDocument
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &path=/Finance/Reports/Q1-2024-Report.pdf
  &tagText=Approved
  &tagDate=2024-06-15T14:30:00
  &taggedBy=12
  &versionNumber=1000000
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/RemoveTagFromDocument HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&path=/Finance/Reports/Q1-2024-Report.pdf
&tagText=Approved
&tagDate=2024-06-15T14:30:00
&taggedBy=12
&versionNumber=1000000
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:RemoveTagFromDocument>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:path>/Finance/Reports/Q1-2024-Report.pdf</tns:path>
      <tns:tagText>Approved</tns:tagText>
      <tns:tagDate>2024-06-15T14:30:00</tns:tagDate>
      <tns:taggedBy>12</tns:taggedBy>
      <tns:versionNumber>1000000</tns:versionNumber>
    </tns:RemoveTagFromDocument>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- **Exact Match Required**: The deletion targets the `APPLIEDTAGS` database table using an exact match on `DOCUMENTID + VERSIONNUMBER + TAGTEXT + TAGDATE + TAGGEDBYID`. If any value differs by even one character, millisecond, or digit, no rows will be deleted and success is still returned. Always obtain the tag values programmatically rather than constructing them manually.
- **Silent No-Match**: If the specified tag record does not exist (e.g. it was already removed, or the values do not match), the API returns `success="true"` without error. There is no way to distinguish a successful removal from a no-match removal.
- **tagDate UTC Conversion**: If `tagDate` is passed as a UTC value (with `Kind = Utc`), it is automatically converted to server local time before the database comparison. If passed as an unspecified or local time, it is used as-is.
- **versionNumber is Internal**: The `versionNumber` parameter uses the raw internal version number stored in the database -" e.g. `1000000` for Version 1, `2000000` for Version 2. This is also the value stored when `SetTagToDocument` applies a tag (it stores the document's current published version number).
- **Obtaining Tag Metadata**: To get the correct `tagDate`, `taggedBy`, and `versionNumber` values needed to remove a specific tag, retrieve the document's applied tags from the document properties (e.g. via `GetDocument` or `GetDocuments`).
- **Cannot Remove Tags on Shortcuts**: Tags cannot be applied to shortcut documents. If a tag was set via `SetTagToDocument` on a shortcut, this is also not possible.

---

## Related APIs

- [SetTagToDocument](SetTagToDocument.md) - Apply a tag to the latest version of a document
- [GetTagDefintions](GetTagDefintions.md) - Get the list of all configured tag definitions
- [GetDocument](GetDocument.md) - Get document properties including applied tags

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Document not found.` | The `path` does not resolve to an existing document. |
| `Insufficient rights.` | The calling user does not have the `DocumentPropertyChange` permission on the document. |
| `SystemError:...` | An unexpected server-side error occurred. |

---
