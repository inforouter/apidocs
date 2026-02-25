# GetDocumentComments API

Returns all comments attached to a document. Each comment includes the author's user ID, login name, timestamp, and text content.

## Endpoint

```
/srv.asmx/GetDocumentComments
```

## Methods

- **GET** `/srv.asmx/GetDocumentComments?AuthenticationTicket=...&Path=...`
- **POST** `/srv.asmx/GetDocumentComments` (form data)
- **SOAP** Action: `http://tempuri.org/GetDocumentComments`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1-Report.pdf`), or a short document ID path (`~D{id}` or `~D{id}.ext`). |

---

## Response

### Success Response

Returns a `<response>` root element containing a `<Comments>` child element with one `<Comment>` element per comment. If the document has no comments, `<Comments>` is present but empty.

```xml
<response success="true" error="">
  <Comments>
    <Comment AuthorID="7"
             AuthorName="jsmith"
             CommentDate="2024-03-15T14:30:00.000Z">This report looks good. Approved for distribution.</Comment>
    <Comment AuthorID="12"
             AuthorName="mwilliams"
             CommentDate="2024-04-01T09:15:22.500Z">Please update the executive summary section before the next review.</Comment>
  </Comments>
</response>
```

### Comment Element Attributes

| Attribute | Description |
|-----------|-------------|
| `AuthorID` | Integer user ID of the comment author. |
| `AuthorName` | Login name of the comment author. |
| `CommentDate` | UTC timestamp when the comment was posted, in ISO 8601 format (`yyyy-MM-ddTHH:mm:ss.fffZ`). Empty string if the date is not set. |

The text content of each `<Comment>` element is the comment body.

### No Comments Response

When the document exists but has no comments:

```xml
<response success="true" error="">
  <Comments />
</response>
```

### Error Response

```xml
<response success="false" error="[900] Authentication failed" />
```

---

## Required Permissions

The calling user must have at least read access to the document.

---

## Example

### GET Request

```
GET /srv.asmx/GetDocumentComments
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports/Q1-2024-Report.pdf
HTTP/1.1
```

### GET Request (short ID path)

```
GET /srv.asmx/GetDocumentComments
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=~D1051
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetDocumentComments HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance/Reports/Q1-2024-Report.pdf
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetDocumentComments>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:Path>/Finance/Reports/Q1-2024-Report.pdf</tns:Path>
    </tns:GetDocumentComments>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- All comments for the document are returned; there is no filtering or pagination.
- `CommentDate` values are always in UTC and formatted as `yyyy-MM-ddTHH:mm:ss.fffZ`.
- Both full infoRouter paths and short document ID paths (`~D{id}` or `~D{id}.ext`) are accepted for the `Path` parameter.
- To add a comment, use `AddDocumentComment`. To delete a specific comment, use `DeleteDocumentComment`.

---

## Related APIs

- [AddDocumentComment](AddDocumentComment) - Add a new comment to a document
- [DeleteDocumentComment](DeleteDocumentComment) - Delete a specific comment from a document
- [GetDocument](GetDocument) - Get full document metadata and properties

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Document not found | The specified path does not resolve to an existing document. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/GetDocumentComments*
