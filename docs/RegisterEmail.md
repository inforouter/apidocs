# RegisterEmail API

Registers an email message as a document in infoRouter at the specified path. The email body, metadata (sender, recipients, CC, BCC, subject, sent date), and any attachments are stored as a single `.EMAIL` document in the target folder. Use this API to archive emails directly from an email client or integration.

## Endpoint

```
/srv.asmx/RegisterEmail
```

## Methods

- **GET** `/srv.asmx/RegisterEmail?AuthenticationTicket=...&TargetPath=...&Senders=...&...`
- **POST** `/srv.asmx/RegisterEmail` (form data)
- **SOAP** Action: `http://tempuri.org/RegisterEmail`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `TargetPath` | string | Yes | Full infoRouter path including the document name (e.g. `/Finance/Emails/Meeting-Notes.EMAIL`). The folder portion must exist. The file name portion becomes the document name. If you pass only `.EMAIL` as the file name, the system automatically prefixes the generated document ID. |
| `Senders` | string | Yes | Sender email address(es). Multiple addresses may be separated by a semicolon. |
| `Recipients` | string | Yes | Primary recipient address(es). Multiple addresses may be separated by a semicolon. |
| `CCAddress` | string | No | CC address(es). Multiple addresses may be separated by a semicolon. Pass empty string or omit if not applicable. |
| `BCCAddress` | string | No | BCC address(es). Multiple addresses may be separated by a semicolon. Pass empty string or omit if not applicable. |
| `SentDate` | DateTime | Yes | Date and time the email was sent. Format: `yyyy-MM-ddTHH:mm:ss` (ISO 8601). Used as the document's creation and modification date. |
| `Subject` | string | No | Email subject line. Pass empty string or omit if not applicable. |
| `header` | string | No | Raw email header block. Pass empty string or omit if not applicable. |
| `htmlBody` | string | No | HTML body content of the email. Pass empty string or omit if not applicable. |
| `textBody` | string | No | Plain text body content of the email. Pass empty string or omit if not applicable. |
| `AttachmentHandlers` | string | No | Semicolon-separated list of email attachment descriptors. Each entry has the format `{filename}:{upload-handler-guid}`. See the **Attachments** section below. Pass empty string or omit if there are no attachments. |

### Attachments

Email attachments must be pre-uploaded using `CreateUploadHandler` and `UploadFileChunk` before calling `RegisterEmail`. Each uploaded file is identified by its upload handler GUID.

The `AttachmentHandlers` parameter format is:

```
{filename1}:{handler-guid1};{filename2}:{handler-guid2}
```

**Example:**
```
Invoice.pdf:3f2504e0-4f89-11d3-9a0c-0305e82c3301;Contract.docx:7b3504e0-4f89-11d3-9a0c-0305e82c3302
```

- Entries are separated by `;`
- Within each entry, the file name and handler GUID are separated by `:`
- The handler GUID must correspond to a valid, unexpired upload handler created with `CreateUploadHandler`
- After a successful `RegisterEmail` call, the upload handlers are automatically deleted from the server

---

## Response

### Success Response

```xml
<response success="true" error="" DocumentID="1051" DocumentName="Meeting-Notes.EMAIL" />
```

| Attribute | Description |
|-----------|-------------|
| `success` | `"true"` on success. |
| `error` | Empty string on success. |
| `DocumentID` | The infoRouter document ID assigned to the newly registered email document. |
| `DocumentName` | The actual document name used (may differ from `TargetPath` if auto-naming was applied). |

### Error Response

```xml
<response success="false" error="Folder not found." />
```

---

## Required Permissions

The calling user must be **authenticated** (anonymous users cannot register emails). The user must have **add document** permission on the target folder.

---

## Example

### POST Request

```
POST /srv.asmx/RegisterEmail HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&TargetPath=/Finance/Emails/Q1-Budget-Meeting.EMAIL
&Senders=alice@example.com
&Recipients=bob@example.com;carol@example.com
&CCAddress=manager@example.com
&BCCAddress=
&SentDate=2024-03-15T14:30:00
&Subject=Q1 Budget Meeting Notes
&header=
&htmlBody=<html><body><p>Please find the meeting notes attached.</p></body></html>
&textBody=Please find the meeting notes attached.
&AttachmentHandlers=MeetingNotes.pdf:3f2504e0-4f89-11d3-9a0c-0305e82c3301
```

### GET Request

```
GET /srv.asmx/RegisterEmail
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &TargetPath=/Finance/Emails/Q1-Budget-Meeting.EMAIL
  &Senders=alice@example.com
  &Recipients=bob@example.com
  &CCAddress=
  &BCCAddress=
  &SentDate=2024-03-15T14:30:00
  &Subject=Q1+Budget+Meeting+Notes
  &header=
  &htmlBody=
  &textBody=Please+find+the+meeting+notes+attached.
  &AttachmentHandlers=
HTTP/1.1
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:RegisterEmail>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:TargetPath>/Finance/Emails/Q1-Budget-Meeting.EMAIL</tns:TargetPath>
      <tns:Senders>alice@example.com</tns:Senders>
      <tns:Recipients>bob@example.com</tns:Recipients>
      <tns:CCAddress></tns:CCAddress>
      <tns:BCCAddress></tns:BCCAddress>
      <tns:SentDate>2024-03-15T14:30:00</tns:SentDate>
      <tns:Subject>Q1 Budget Meeting Notes</tns:Subject>
      <tns:header></tns:header>
      <tns:htmlBody></tns:htmlBody>
      <tns:textBody>Please find the meeting notes attached.</tns:textBody>
      <tns:AttachmentHandlers></tns:AttachmentHandlers>
    </tns:RegisterEmail>
  </soap:Body>
</soap:Envelope>
```

### Workflow — register email with attachments

```
1. For each attachment file:
   POST /srv.asmx/CreateUploadHandler?... → returns handler GUID (e.g. "abc123...")
   POST /srv.asmx/UploadFileChunk (repeat until all chunks uploaded)

2. POST /srv.asmx/RegisterEmail
   AttachmentHandlers=Invoice.pdf:abc123...;Contract.docx:def456...

3. On success, response includes DocumentID and DocumentName of the new .EMAIL document
```

---

## Notes

- The document name is taken from the **last path segment** of `TargetPath`. The parent folder path must already exist.
- If the document name is exactly `.EMAIL`, the system automatically prepends the generated document ID to create a unique name.
- Email documents are stored with `PercentComplete=100` (completed) and are not subject to the checkout/lock workflow.
- The document's **creation date** and **modification date** are set to `SentDate`. The **completion date** is set to the current server time.
- **Duplicate detection:** If a document with the same name and the same email Message-ID header already exists in the target folder, the call fails to prevent duplicate registrations.
- After a successful call, all referenced upload handlers are automatically deleted from the server.
- Use `RegisterEmail1` to register an email and also set user-defined keywords in a single call.
- Use `RegisterEmail2` to specify the folder path and email document name as separate parameters instead of combining them in `TargetPath`.

---

## Related APIs

- [RegisterEmail1](RegisterEmail1.md) - Register an email with user-defined keywords
- [RegisterEmail2](RegisterEmail2.md) - Register an email with the folder path and document name as separate parameters
- [CreateUploadHandler](CreateUploadHandler.md) - Create an upload handler for pre-uploading email attachments
- [UploadFileChunk](UploadFileChunk.md) - Upload file content in chunks to an upload handler
- [GetDocument](GetDocument.md) - Get the properties of the registered email document

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Anonymous users cannot perform this action | The authenticated user is an anonymous/guest user. |
| Folder not found | The folder portion of `TargetPath` does not exist. |
| Upload handler not found | One of the specified attachment handler GUIDs is invalid or has expired. |
| Invalid attachment handler format | The `AttachmentHandlers` string is malformed (missing `:` separator or invalid GUID). |
| Duplicate email | An email with the same document name and Message-ID already exists in the target folder. |
| Access denied | The user does not have add document permission on the target folder. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/RegisterEmail*
