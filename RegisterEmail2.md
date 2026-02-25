# RegisterEmail2 API

Registers an email message as a document in infoRouter, specifying the destination folder path and the email document name as two separate parameters instead of a combined path. This makes it convenient when the folder and file name are already available as distinct values. Behavior is otherwise identical to `RegisterEmail1`.

## Endpoint

```
/srv.asmx/RegisterEmail2
```

## Methods

- **GET** `/srv.asmx/RegisterEmail2?AuthenticationTicket=...&FolderPath=...&EmailName=...&Senders=...&...`
- **POST** `/srv.asmx/RegisterEmail2` (form data)
- **SOAP** Action: `http://tempuri.org/RegisterEmail2`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `FolderPath` | string | Yes | Full infoRouter path to the destination folder (e.g. `/Finance/Emails`). The folder must already exist. |
| `EmailName` | string | Yes | Document name for the email, including extension (e.g. `Meeting-Notes.EMAIL`). Pass exactly `.EMAIL` to have the system auto-prefix the generated document ID as the name. |
| `Senders` | string | Yes | Sender email address(es). Multiple addresses may be separated by a semicolon. |
| `Recipients` | string | Yes | Primary recipient address(es). Multiple addresses may be separated by a semicolon. |
| `CCAddress` | string | No | CC address(es). Multiple addresses may be separated by a semicolon. Pass empty string or omit if not applicable. |
| `BCCAddress` | string | No | BCC address(es). Multiple addresses may be separated by a semicolon. Pass empty string or omit if not applicable. |
| `SentDate` | DateTime | Yes | Date and time the email was sent. Format: `yyyy-MM-ddTHH:mm:ss` (ISO 8601). Used as the document's creation and modification date. |
| `Subject` | string | No | Email subject line. Pass empty string or omit if not applicable. |
| `header` | string | No | Raw email header block. Pass empty string or omit if not applicable. |
| `htmlBody` | string | No | HTML body content of the email. Pass empty string or omit if not applicable. |
| `textBody` | string | No | Plain text body content of the email. Pass empty string or omit if not applicable. |
| `AttachmentHandlers` | string | No | Semicolon-separated list of email attachment descriptors. Each entry has the format `{filename}:{upload-handler-guid}`. Upload handlers must be pre-created with `CreateUploadHandler` and populated with `UploadFileChunk`. Pass empty string or omit if there are no attachments. |
| `keywords` | string | No | Comma-separated list of user-defined keywords to assign to the registered email document (e.g. `invoice,Q1,finance`). Pass empty string or omit to register without keywords. |

> **`RegisterEmail2` vs `RegisterEmail1`:** The only structural difference is that `TargetPath` (a combined folder + file name path) is replaced by two separate parameters: `FolderPath` and `EmailName`. All email fields, attachment handling, keywords, responses, and error conditions are identical.

### Attachments

The `AttachmentHandlers` parameter format is:

```
{filename1}:{handler-guid1};{filename2}:{handler-guid2}
```

- Entries are separated by `;`
- Within each entry, the file name and handler GUID are separated by `:`
- Handler GUIDs must correspond to valid, unexpired upload handlers
- After a successful call, the upload handlers are automatically deleted from the server

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
| `DocumentName` | The actual document name used (may differ from `EmailName` if auto-naming was applied). |

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
POST /srv.asmx/RegisterEmail2 HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&FolderPath=/Finance/Emails
&EmailName=Q1-Budget-Meeting.EMAIL
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
&keywords=budget,Q1,finance
```

### GET Request

```
GET /srv.asmx/RegisterEmail2
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &FolderPath=/Finance/Emails
  &EmailName=Q1-Budget-Meeting.EMAIL
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
  &keywords=budget,Q1,finance
HTTP/1.1
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:RegisterEmail2>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:FolderPath>/Finance/Emails</tns:FolderPath>
      <tns:EmailName>Q1-Budget-Meeting.EMAIL</tns:EmailName>
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
      <tns:keywords>budget,Q1,finance</tns:keywords>
    </tns:RegisterEmail2>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- `FolderPath` is the destination folder only — do not include the document name. `EmailName` is the document name only — do not include a folder path.
- `EmailName` must include the file extension. Pass `.EMAIL` as the name to have the system auto-generate a name using the document ID as a prefix.
- Email documents are stored with `PercentComplete=100` (completed) and are not subject to the checkout/lock workflow.
- The document's **creation date** and **modification date** are set to `SentDate`. The **completion date** is set to the current server time.
- **Duplicate detection:** If a document with the same name and the same email Message-ID header already exists in the target folder, the call fails to prevent duplicate registrations.
- After a successful call, all referenced upload handlers are automatically deleted from the server.
- Use `RegisterEmail3` to pass all email parameters in a single XML string instead of individual parameters.

---

## Related APIs

- [RegisterEmail](RegisterEmail) - Register an email using a combined `TargetPath` (no keywords)
- [RegisterEmail1](RegisterEmail1) - Register an email using a combined `TargetPath` with keywords
- [RegisterEmail3](RegisterEmail3) - Register an email using an XML parameter envelope
- [CreateUploadHandler](CreateUploadHandler) - Create an upload handler for pre-uploading email attachments
- [UploadFileChunk](UploadFileChunk) - Upload file content in chunks to an upload handler
- [GetDocument](GetDocument) - Get the properties of the registered email document

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Anonymous users cannot perform this action | The authenticated user is an anonymous/guest user. |
| Folder not found | The specified `FolderPath` does not exist. |
| Upload handler not found | One of the specified attachment handler GUIDs is invalid or has expired. |
| Invalid attachment handler format | The `AttachmentHandlers` string is malformed (missing `:` separator or invalid GUID). |
| Duplicate email | An email with the same document name and Message-ID already exists in the target folder. |
| Access denied | The user does not have add document permission on the target folder. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/RegisterEmail2*
