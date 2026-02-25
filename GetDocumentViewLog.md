# GetDocumentViewLog API

Returns the complete view/access log for a specified document, showing all users who have accessed the document and when. This API retrieves entries from both the current view log (VIEWLOG table) and historical read logs (HISTORY_READ table).

## Endpoint

```
/srv.asmx/GetDocumentViewLog
```

## Methods

- **GET** `/srv.asmx/GetDocumentViewLog?authenticationTicket=...&path=...`
- **POST** `/srv.asmx/GetDocumentViewLog` (form data)
- **SOAP** Action: `http://tempuri.org/GetDocumentViewLog`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1-Report.pdf`), or a short document ID path (`~D{id}` or `~D{id}.ext`). |

---

## Response

### Success Response

Returns a `<response>` root element containing a `<ViewLog>` element, which holds zero or more `<Version>` child elements. Each element represents a view/access event for a specific version of the document.

```xml
<response success="true" error="">
  <ViewLog>
    <Version Number="2000000" 
             UserID="7" 
             Viewer="John Smith" 
             ViewDate="2024-06-15T10:30:00.000Z" />
    <Version Number="2000000" 
             UserID="12" 
             Viewer="Jane Doe" 
             ViewDate="2024-06-14T14:20:00.000Z" />
    <Version Number="1000000" 
             UserID="7" 
             Viewer="John Smith" 
             ViewDate="2024-05-01T09:15:00.000Z" />
  </ViewLog>
</response>
```

### Version Element Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `Number` | int | Version number in modern format (e.g. `1000000` for version 1, `2000000` for version 2). |
| `UserID` | int | User ID of the user who accessed the document. |
| `Viewer` | string | Full name of the user who accessed the document. |
| `ViewDate` | string | UTC timestamp when the document was accessed, in ISO 8601 format (`yyyy-MM-ddTHH:mm:ss.fffZ`). Empty if not set. |

### Error Response

```xml
<response success="false" error="Document not found." />
```

---

## Required Permissions

The calling user must have at least **read access** to the document. Additionally, the user must have the **"Read View Log"** permission (IRAction.DocumentReadViewLog) for the document. This permission is typically granted to:
- Document owner
- System administrators
- Domain/library managers
- Users with explicit "Read View Log" permission on the document's ACL

---

## Example

### GET Request

```
GET /srv.asmx/GetDocumentViewLog
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &path=/Finance/Reports/Q1-2024-Report.pdf
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetDocumentViewLog HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&path=/Finance/Reports/Q1-2024-Report.pdf
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetDocumentViewLog>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:Path>/Finance/Reports/Q1-2024-Report.pdf</tns:Path>
    </tns:GetDocumentViewLog>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- **Combined Data Sources**: The response combines entries from both the active view log (VIEWLOG table) and the historical read log (HISTORY_READ table).
- **Version-Specific**: Each log entry is associated with a specific version number. Users may appear multiple times if they accessed different versions.
- **Duplicate Entries Possible**: The same user may have multiple entries for the same version if they accessed it multiple times. Entries are not deduplicated.
- **Sorting**: Results are not guaranteed to be in any specific order. Consider sorting by ViewDate or UserID in your client application if needed.
- **Date Format**: All `ViewDate` attributes use UTC ISO 8601 format (`yyyy-MM-ddTHH:mm:ss.fffZ`).
- **Version Number Format**: The `Number` attribute uses the modern format (version 1 = `1000000`, version 2 = `2000000`, etc.).
- **Empty Results**: If no one has accessed the document, an empty `<ViewLog/>` element is returned (not an error).
- **Short Path Support**: The `path` parameter supports short document ID notation: `~D123` or `~D123.pdf`.
- **Permission Checking**: If the user lacks "Read View Log" permission, an access denied error is returned even if they have read access to the document.

---

## Use Cases

1. **Audit Reports**: Track who has accessed sensitive or regulated documents for compliance purposes.
2. **Security Monitoring**: Monitor access to confidential documents and detect unauthorized viewing attempts.
3. **User Activity Analysis**: Understand document usage patterns and identify which users are actively engaging with content.
4. **Compliance Verification**: Verify that required personnel have reviewed mandatory documents (e.g., policies, training materials).
5. **Version Adoption Tracking**: See which versions of a document users are accessing to gauge version adoption rates.

---

## Related APIs

- [GetUserViewLog](GetUserViewLog) - Get complete view log history for a specific user across all documents
- [GetUserViewLog1](GetUserViewLog1) - Get view log history for a specific user filtered by date range
- [GetDocumentReadLogHistory](GetDocumentReadLogHistory) - Get detailed read log history for a specific document and user

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Document not found | The specified path does not resolve to an existing document. |
| Access denied / Insufficient rights | The user lacks "Read View Log" permission for the document. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/GetDocumentViewLog*
