# GetUserViewLog API

Returns the complete read/view log history for a specified user, showing all documents accessed by that user. This API retrieves entries from both the current view log (VIEWLOG table) and historical read logs (HISTORY_READ table).

## Endpoint

```
/srv.asmx/GetUserViewLog
```

## Methods

- **GET** `/srv.asmx/GetUserViewLog?authenticationTicket=...&userName=...`
- **POST** `/srv.asmx/GetUserViewLog` (form data)
- **SOAP** Action: `http://tempuri.org/GetUserViewLog`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `userName` | string | Yes | Login name of the user whose view log history should be retrieved. |

---

## Response

### Success Response

Returns a `<response>` root element containing a `<viewlogs>` element, which holds zero or more `<viewlog>` child elements. Each element represents a document view/read event.

```xml
<response success="true" error="">
  <viewlogs>
    <viewlog DocumentId="1523" 
             UserId="7" 
             UserFullname="John Smith" 
             DocumentName="Q1-Report.pdf" 
             VersionNumber="2.0.0" 
             ViewDate="2024-06-15T10:30:00.000Z" 
             DomainName="Finance" 
             Path="/Finance/Reports" />
    <viewlog DocumentId="1489" 
             UserId="7" 
             UserFullname="John Smith" 
             DocumentName="Budget-2024.xlsx" 
             VersionNumber="1.0.0" 
             ViewDate="2024-06-14T14:20:00.000Z" 
             DomainName="Finance" 
             Path="/Finance/Planning" />
  </viewlogs>
</response>
```

### Viewlog Element Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `DocumentId` | int | Unique identifier of the document that was accessed. |
| `UserId` | int | User ID of the user who accessed the document (matches the queried user). |
| `UserFullname` | string | Full name of the user who accessed the document. |
| `DocumentName` | string | Name of the document file (including extension). |
| `VersionNumber` | string | Version number in multi-part format (e.g. `"2.0.0"` for version 2). |
| `ViewDate` | string | UTC timestamp when the document was accessed, in ISO 8601 format (`yyyy-MM-ddTHH:mm:ss.fffZ`). Empty if not set. |
| `DomainName` | string | Name of the domain/library containing the document. |
| `Path` | string | Full folder path where the document resides (not including the document name). |

### Error Response

```xml
<response success="false" error="User not found." />
```

---

## Required Permissions

The calling user must be authenticated. Any authenticated user can retrieve view logs for **any user** -" there is no permission check restricting this to administrators or the user themselves.

---

## Example

### GET Request

```
GET /srv.asmx/GetUserViewLog
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &userName=jsmith
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetUserViewLog HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&userName=jsmith
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetUserViewLog>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:userName>jsmith</tns:userName>
    </tns:GetUserViewLog>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- This API retrieves **all view/read logs** for the specified user without date filtering. To filter by date range, use `GetUserViewLog1`.
- The response combines entries from both the active view log (VIEWLOG table) and the historical read log (HISTORY_READ table).
- Duplicate entries (same user, document, version, and timestamp) are automatically removed from the combined result set.
- Results are sorted by `ViewDate` in ascending order (oldest first).
- All date fields use UTC ISO 8601 format (`yyyy-MM-ddTHH:mm:ss.fffZ`). An empty string means the date is not recorded.
- The `VersionNumber` attribute shows the multi-part version format (`major.minor.revision`) rather than the internal integer format.
- If the specified user has never accessed any documents, an empty `<viewlogs/>` element is returned (not an error).
- The API does not verify that the calling user has permission to view the audit logs -" any authenticated user can query any other user's view history.

---

## Related APIs

- [GetUserViewLog1](GetUserViewLog1.md) - Get user view log history filtered by date range
- [GetDocumentViewLog](GetDocumentViewLog.md) - Get the view log for a specific document (all users who accessed it)
- [GetDocumentReadLogHistory](GetDocumentReadLogHistory.md) - Get detailed read log history for a specific document and user

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| User not found | The specified userName does not exist in the system. |
| `SystemError:...` | An unexpected server-side error occurred. |

---
