# GetISOReviewAssignments API

Returns the list of documents assigned to the specified user for ISO review across all libraries visible to the caller. The results are sorted alphabetically by document name.

## Endpoint

```
/srv.asmx/GetISOReviewAssignments
```

## Methods

- **GET** `/srv.asmx/GetISOReviewAssignments?authenticationTicket=...&userName=...`
- **POST** `/srv.asmx/GetISOReviewAssignments` (form data)
- **SOAP** Action: `http://tempuri.org/GetISOReviewAssignments`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `userName` | string | Yes | The user name to retrieve ISO review assignments for |

## Response Structure

### Success Response

```xml
<response success="true">
  <document id="1234" name="SOP_Quality_Control.docx" size="245760" modificationDate="2026-02-01T14:30:00" publishedVersionAuthorName="John Smith" ... />
  <document id="1235" name="ISO_Procedure_001.pdf" size="102400" modificationDate="2026-01-15T09:00:00" publishedVersionAuthorName="Jane Doe" ... />
  <!-- ... additional documents ... -->
</response>
```

### Empty Result

```xml
<response success="true" />
```

### Error Response

```xml
<response success="false" error="[ErrorCode] Error message" />
```

## Document Attributes

Each `<document>` element contains the standard document properties including:

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | integer | Unique document identifier |
| `name` | string | Document file name |
| `size` | long | Document size in bytes |
| `modificationDate` | DateTime | Last modification date |
| `publishedVersionAuthorName` | string | Name of the published version author |

Additional standard document attributes may be included depending on the document type and system configuration.

## Required Permissions

- User must be authenticated (valid authentication ticket required)
- If the caller is querying their own ISO review assignments, no additional permissions are required
- If the caller is querying another user's assignments, the caller must have `ListingAuditLogOfUser` admin permission for the target user

## Use Cases

1. **ISO Compliance Management**
   - View all documents assigned to a user for ISO review
   - Track ISO review responsibilities across the organization

2. **User Administration**
   - Audit ISO reviewer role assignments for a specific user
   - Review document assignments before account changes or deactivation

3. **Reporting**
   - Generate reports of ISO review assignments by user
   - Identify workload distribution for ISO review tasks

## Example Requests

### Request (GET)

```
GET /srv.asmx/GetISOReviewAssignments?authenticationTicket=abc123-def456&userName=jsmith HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/GetISOReviewAssignments HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=abc123-def456&userName=jsmith
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/GetISOReviewAssignments"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetISOReviewAssignments xmlns="http://tempuri.org/">
      <authenticationTicket>abc123-def456</authenticationTicket>
      <userName>jsmith</userName>
    </GetISOReviewAssignments>
  </soap:Body>
</soap:Envelope>
```

## Notes

- Results include documents from all libraries visible to the caller.
- Documents are sorted alphabetically by document name in ascending order.
- The response uses the standard document serialization format, consistent with other document-listing APIs like `GetAuthoredDocuments`.
- If the user has no ISO review assignments, the response will be a success with no `<document>` child elements.

## Error Codes

Common error responses:

| Error | Description |
|-------|-------------|
| `[901]Session expired or Invalid ticket` | Invalid or expired authentication ticket |
| `[921]Insufficient rights` | Caller does not have `ListingAuditLogOfUser` admin permission for the target user |
| User not found error | The specified `userName` does not exist in the system |

## Related APIs

- `GetAuthoredDocuments` - Get documents authored by a specified user
- `GetCheckedoutDocumentsByUser` - Get checked out documents for a specified user
- `GetSubscriptionsByUser` - Get folder and document subscriptions for a user
- `AuthenticateUser` - Authenticate and obtain a ticket

## Version History

- **New**: Added to provide programmatic access to ISO review assignments previously only available through the Control Panel UI
