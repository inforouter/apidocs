# AddDocumentComment API

Adds a comment to the specified document. Comments are visible to all users who have access to the document and are tracked with author and timestamp information.

## Endpoint

```
/srv.asmx/AddDocumentComment
```

## Methods

- **GET** `/srv.asmx/AddDocumentComment?AuthenticationTicket=...&DocumentPath=...&CommentText=...`
- **POST** `/srv.asmx/AddDocumentComment` (form data)
- **SOAP** Action: `http://tempuri.org/AddDocumentComment`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser` |
| `DocumentPath` | string | Yes | Full path to the document (e.g., `/Domain/Folder/Document.pdf`) |
| `CommentText` | string | Yes | The comment text to add to the document |

## Response

### Success Response

```xml
<root success="true" />
```

### Error Response

```xml
<root success="false" error="[ErrorCode] Error message" />
```

## Required Permissions

The caller must have **read access** to the document by default. The specific required permissions depend on the domain policy settings:

- **Default**: Read access to the document
- **Domain Policy Override**: May require "Add Comment" permission if configured in domain policies
- The user must be authenticated (anonymous users cannot add comments unless explicitly allowed by policy)

## Comment Behavior

- Comments are stored with author information (user ID, username, full name)
- Comments include timestamp (date and time added)
- Comments are permanent unless explicitly deleted using `DeleteDocumentComment`
- Multiple comments can be added to a single document
- Comments are retrieved using `GetDocumentComments` API
- Comment text is sanitized and HTML-encoded for security

## Example

### Request (GET)

```
GET /srv.asmx/AddDocumentComment?AuthenticationTicket=abc123-def456&DocumentPath=/Engineering/Specs/Design.pdf&CommentText=Please%20review%20section%203 HTTP/1.1
Host: server.example.com
```

### Request (POST)

```
POST /srv.asmx/AddDocumentComment HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=abc123-def456&DocumentPath=/Engineering/Specs/Design.pdf&CommentText=Please review section 3
```

### Request (SOAP 1.1)

```xml
POST /srv.asmx HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://tempuri.org/AddDocumentComment"

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <AddDocumentComment xmlns="http://tempuri.org/">
      <AuthenticationTicket>abc123-def456</AuthenticationTicket>
      <DocumentPath>/Engineering/Specs/Design.pdf</DocumentPath>
      <CommentText>Please review section 3</CommentText>
    </AddDocumentComment>
  </soap:Body>
</soap:Envelope>
```

### Success Response

```xml
<?xml version="1.0" encoding="utf-8"?>
<root success="true" />
```

### Error Response Example

```xml
<?xml version="1.0" encoding="utf-8"?>
<root success="false" error="[2285]Document not found at specified path" />
```

## Related APIs

### Document Comment Management
- `GetDocumentComments` - Retrieve all comments for a document
- `DeleteDocumentComment` - Delete a specific comment
- `AddISOComment` - Add an ISO-specific comment
- `AddSOXComment` - Add a SOX compliance comment

### Document Access
- `GetDocument` - Get document details
- `DocumentAccessAllowed` - Check if user has specific access rights
- `GetAccessList` - Get document access control list

## Notes

- This is an **asynchronous operation** - the API returns a `Task<XElement>`
- Comment text is automatically sanitized to prevent XSS attacks
- Maximum comment length may be limited by system configuration (typically 4000 characters)
- Comments are indexed and searchable if full-text indexing is enabled
- The API validates the document path format and normalizes it
- Comments trigger document subscription notifications if configured
- Comment authors cannot be changed after submission
- Empty or whitespace-only comments are not allowed

## Use Cases

1. **Document Review Process**
   - Reviewers add comments during document review workflows
   - Comments provide feedback without modifying the document

2. **Collaboration**
   - Team members add notes and discussions about document content
   - Comments serve as an audit trail of discussions

3. **Quality Control**
   - QA team adds findings and observations
   - Comments track issues without creating separate documents

4. **Approval Process**
   - Approvers add justification for approval/rejection decisions
   - Comments provide context for document history

## Error Codes

Common error responses:

| Error | Description |
|-------|-------------|
| `[901]Session expired or Invalid ticket` | Invalid or expired authentication ticket |
| `[2285]Document not found` | The specified document path does not exist |
| `[2730]Insufficient rights` | User does not have permission to add comments |
| `Invalid path format` | Document path is malformed or contains invalid characters |
| `Comment text cannot be empty` | No comment text provided or only whitespace |
| `Document is checked out` | May not be able to comment if document is checked out (policy-dependent) |
| `Document is archived` | Cannot add comments to archived documents |

## Comment Notifications

If document subscriptions are enabled, the following users are notified when a comment is added:

- Users subscribed to the document with "ON_COMMENT" notification enabled
- Document owner (if owner notification is enabled)
- Users in groups subscribed to the document
- Workflow participants if document is in an active workflow

## Security Considerations

- Comment text is HTML-encoded to prevent script injection
- Comments are subject to document-level security permissions
- Comment visibility follows document access permissions
- Audit logs track all comment additions
- Comments cannot be edited - only added or deleted

## Best Practices

1. **Clear Communication**: Write descriptive comments that provide context
2. **Reference Sections**: Include page numbers or section references when applicable
3. **Timely Feedback**: Add comments promptly during review processes
4. **Professional Tone**: Maintain professional language in comments
5. **Check Length**: Keep comments concise and focused (avoid exceeding character limits)
6. **URL Encoding**: When using GET requests, ensure comment text is properly URL-encoded
7. **Error Handling**: Always check the success attribute in the response

## Version History

- This API supports asynchronous operations (async/await pattern)
- Compatible with infoRouter 8.7 and later
- Comment features may vary based on installed add-ons and licenses
