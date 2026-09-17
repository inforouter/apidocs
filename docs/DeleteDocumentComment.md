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

## JavaScript

Every call answers XML with HTTP 200, success or not, so `success` is the thing to branch on and
`errorCode` is the number to report.

```javascript
async function call(action, params) {
  const response = await fetch(`/srv.asmx/${action}?${new URLSearchParams(params)}`);
  const root = new DOMParser()
    .parseFromString(await response.text(), 'text/xml')
    .documentElement;

  if (root.getAttribute('success') !== 'true') {
    throw new Error(`${root.getAttribute('errorCode')}: ${root.getAttribute('error')}`);
  }
  return root;
}
```

Removes one comment, named by who wrote it and when. The `CommentDate` from
[GetDocumentComments](GetDocumentComments.md) can be passed straight back.

```javascript
const comments = await call('GetDocumentComments', {
  authenticationTicket: ticket, Path: '/Finance/Reports/Q1.pdf'
});

const comment = [...comments.querySelectorAll('Comment')]
  .find(c => c.textContent === 'Checked against the ledger.');

await call('DeleteDocumentComment', {
  authenticationTicket: ticket,
  DocumentPath: '/Finance/Reports/Q1.pdf',
  CommentAuthorID: comment.getAttribute('AuthorID'),
  CommentDate: comment.getAttribute('CommentDate')
});
```

**A delete that matched nothing is still a success.** An author who never commented here, or a date
nothing was written on, is answered `success="true"` with no indication that nothing was removed.
There is no `4041` and no count, so read the comments back if it matters.

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

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all - the anonymous user is refused |
| `4041` | no document at that path - including one the caller may not see |
| `none` | an author or date that matches no comment is a success, not an error |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `Document not found` | The `DocumentPath` does not refer to an existing document. |
| `Access denied` | The caller is not the comment author and does not have `DocumentCommentsChangeDelete` permission. |
| `Document is offline` | The document is in Offline state and comments cannot be modified. |

---

