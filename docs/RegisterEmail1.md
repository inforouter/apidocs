# RegisterEmail1 API

Registers an email message as a document in infoRouter at the specified path, and also sets user-defined keywords on the created document in a single call. This is identical to `RegisterEmail` with the addition of the `keywords` parameter.

## Endpoint

```

/srv.asmx/RegisterEmail1

```

## Methods

- **GET** `/srv.asmx/RegisterEmail1?AuthenticationTicket=...&TargetPath=...&Senders=...&...&keywords=...`

- **POST** `/srv.asmx/RegisterEmail1` (form data)

- **SOAP** Action: `http://tempuri.org/RegisterEmail1`

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
| `AttachmentHandlers` | string | No | Semicolon-separated list of email attachment descriptors. Each entry has the format `{filename}:{upload-handler-guid}`. Upload handlers must be pre-created with `CreateUploadHandler` and populated with `UploadFileChunk`. Pass empty string or omit if there are no attachments. |
| `keywords` | string | No | Comma-separated list of user-defined keywords to assign to the registered email document (e.g. `invoice,Q1,finance`). Pass empty string or omit to register without keywords. |

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

POST /srv.asmx/RegisterEmail1 HTTP/1.1

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

&keywords=budget,Q1,finance

```

### GET Request

```

GET /srv.asmx/RegisterEmail1

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

  &keywords=budget,Q1,finance

HTTP/1.1

```

### SOAP Request

```xml

<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"

               xmlns:tns="http://tempuri.org/">

  <soap:Body>

    <tns:RegisterEmail1>

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

      <tns:keywords>budget,Q1,finance</tns:keywords>

    </tns:RegisterEmail1>

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

[RegisterEmail](RegisterEmail.md) with one more thing it can set: `keywords`.

```javascript
const root = await call('RegisterEmail1', {
  authenticationTicket: ticket,
  TargetPath: '/Finance/Emails/2026-09-supplier-query',   // the document path, without .email
  Senders: 'supplier@example.com',
  Recipients: 'accounts@example.com',
  CCAddress: '',
  BCCAddress: '',
  SentDate: '2026-09-01',
  Subject: 'Invoice query',
  header: '',
  htmlBody: '<p>Could you check invoice 4471?</p>',
  textBody: 'Could you check invoice 4471?',
  AttachmentHandlers: '',
  keywords: 'invoice,supplier'
});
```

Keywords are comma-separated and a keyword may contain spaces, exactly as
[GetDocumentKeywords](GetDocumentKeywords.md) reads them back.

### Which of the four to use

| | Where it goes | Keywords | Everything else |
|---|---|---|---|
| [RegisterEmail](RegisterEmail.md) | `TargetPath` - the **document** path | no | parameters |
| [RegisterEmail1](RegisterEmail1.md) | `TargetPath` - the **document** path | yes | parameters |
| [RegisterEmail2](RegisterEmail2.md) | `FolderPath` + `EmailName` | yes | parameters |
| [RegisterEmail3](RegisterEmail3.md) | `FolderPath` + `EmailName` | yes | one XML document |

Prefer `RegisterEmail2`. The first two take a single `TargetPath` which is the path of the *document*
to create, not the folder to put it in - so aiming one at a folder writes the document beside that
folder, named after it. `RegisterEmail2` takes the folder and the name separately and cannot be got
wrong that way.

`.email` is appended to the name unless it already ends with it, and the document is dated from
`SentDate` rather than from now.

## Notes

- This API is identical to `RegisterEmail` with the addition of the `keywords` parameter. All behavior, error conditions, and response attributes are the same.

- The `keywords` value is stored as the document's user-defined keywords and is searchable via the standard search APIs.

- The document name is taken from the **last path segment** of `TargetPath`. The parent folder path must already exist.

- If the document name is exactly `.EMAIL`, the system automatically prepends the generated document ID to create a unique name.

- Email documents are stored with `PercentComplete=100` (completed) and are not subject to the checkout/lock workflow.

- The document's **creation date** and **modification date** are set to `SentDate`. The **completion date** is set to the current server time.

- **Duplicate detection:** If a document with the same name and the same email Message-ID header already exists in the target folder, the call fails to prevent duplicate registrations.

- After a successful call, all referenced upload handlers are automatically deleted from the server.

---

## Related APIs

- [RegisterEmail](RegisterEmail.md) - Register an email without keywords

- [RegisterEmail2](RegisterEmail2.md) - Register an email with folder path and document name as separate parameters

- [RegisterEmail3](RegisterEmail3.md) - Register an email using an XML parameter envelope

- [CreateUploadHandler](CreateUploadHandler.md) - Create an upload handler for pre-uploading email attachments

- [UploadFileChunk](UploadFileChunk.md) - Upload file content in chunks to an upload handler

- [GetDocument](GetDocument.md) - Get the properties of the registered email document

- [UpdateDocumentKeywords](UpdateDocumentKeywords.md) - Update keywords on an existing document

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4090` | a document of that name is already in the folder |
| `4041` | no folder at the parent of `TargetPath` |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

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

