# DeleteDocumentComment API

Deletes a specific comment from a document. Comments are uniquely identified by the combination of the comment author's user ID and the date/time the comment was posted.

## Endpoint

```
/srv.asmx/DeleteDocumentComment
```

## Methods

- **GET** `/srv.asmx/DeleteDocumentComment?authenticationTicket=...&DocumentPath=...&CommentAuthorID=...&CommentDate=...`
- **POST** `/srv.asmx/DeleteDocumentComment` (form data)
- **SOAP** Action: `http://tempuri.org/DeleteDocumentComment`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DocumentPath` | string | Yes | Full infoRouter path of the document (e.g. `/MyLibrary/Reports/Report.pdf`). |
| `CommentAuthorID` | int | Yes | User ID of the user who authored the comment. Use `GetDocumentComments` to retrieve comment author IDs. |
| `CommentDate` | datetime | Yes | Date and time when the comment was originally posted. Must match the stored comment timestamp exactly. Accepts ISO 8601 format (e.g. `2024-01-15T10:30:00`). UTC timestamps are automatically converted to local time. |

## Response

### Success Response

```xml
<root success="true" />
```

### Error Response

```xml
<root success="false" error="Error message" />
```

---

## Required Permissions

The authenticated user must meet **one** of the following conditions:

- Be the **author of the comment** (the authenticated user's ID matches `CommentAuthorID`), **or**
- Have **DocumentCommentsChangeDelete** permission on the document.

Documents in **Offline** state do not allow comment deletions.

---

## Example

### GET Request

```
GET /srv.asmx/DeleteDocumentComment
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &DocumentPath=/MyLibrary/Reports/Report.pdf
  &CommentAuthorID=42
  &CommentDate=2024-01-15T10:30:00
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/DeleteDocumentComment HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&DocumentPath=/MyLibrary/Reports/Report.pdf
&CommentAuthorID=42
&CommentDate=2024-01-15T10:30:00
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:DeleteDocumentComment>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:DocumentPath>/MyLibrary/Reports/Report.pdf</tns:DocumentPath>
      <tns:CommentAuthorID>42</tns:CommentAuthorID>
      <tns:CommentDate>2024-01-15T10:30:00</tns:CommentDate>
    </tns:DeleteDocumentComment>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- A comment is uniquely identified by the combination of `CommentAuthorID` and `CommentDate`. Both values must exactly match the stored comment. Use `GetDocumentComments` to retrieve the correct values.
- If `CommentDate` is provided as a UTC timestamp, it is automatically converted to the server's local time before the lookup.
- Comments cannot be deleted from documents that are in **Offline** state.
- Comment authors can always delete their own comments. Users without authorship must have the `DocumentCommentsChangeDelete` permission explicitly granted.

---

## Related APIs

- [AddDocumentComment](AddDocumentComment.md) - Add a comment to a document
- [GetDocumentComments](GetDocumentComments.md) - Retrieve comments for a document (use to find CommentAuthorID and CommentDate values)

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Document not found` | The `DocumentPath` does not refer to an existing document. |
| `Access denied` | The caller is not the comment author and does not have `DocumentCommentsChangeDelete` permission. |
| `Document is offline` | The document is in Offline state and comments cannot be modified. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/DeleteDocumentComment*
