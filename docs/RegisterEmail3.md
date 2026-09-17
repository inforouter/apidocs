# RegisterEmail3 API

Registers an email message as a document in infoRouter, passing all email fields as a single XML string. The destination folder and document name are specified as separate parameters. This variant is useful when the calling application already has the email data in an XML structure, and avoids the need to pass many individual query-string or form parameters. Behavior is otherwise identical to `RegisterEmail2`.

## Endpoint

```

/srv.asmx/RegisterEmail3

```

## Methods

- **GET** `/srv.asmx/RegisterEmail3?AuthenticationTicket=...&FolderPath=...&EmailName=...&parametersXml=...`

- **POST** `/srv.asmx/RegisterEmail3` (form data)

- **SOAP** Action: `http://tempuri.org/RegisterEmail3`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `FolderPath` | string | Yes | Full infoRouter path to the destination folder (e.g. `/Finance/Emails`). The folder must already exist. |
| `EmailName` | string | Yes | Document name for the email (e.g. `Meeting-Notes.EMAIL`). If the `.EMAIL` extension is omitted, it is appended automatically. Pass exactly `.EMAIL` to have the system auto-prefix the generated document ID as the name. |
| `parametersXml` | string | Yes | An XML string containing all email fields. See the **`parametersXml` Structure** section below. |

### `parametersXml` Structure

The value is a well-formed XML document. The root element name is arbitrary. Each email field is a direct child element. Element names are **case-insensitive**.

```xml

<email>

  <Senders>alice@example.com</Senders>

  <Recipients>bob@example.com;carol@example.com</Recipients>

  <CCAddress>manager@example.com</CCAddress>

  <BCCAddress>archive@example.com</BCCAddress>

  <SentDate>2024-03-15T14:30:00</SentDate>

  <Subject>Q1 Budget Meeting Notes</Subject>

  <Header></Header>

  <HtmlBody><![CDATA[<html><body><p>See attached.</p></body></html>]]></HtmlBody>

  <TextBody>See attached.</TextBody>

  <Keywords>budget,Q1,finance</Keywords>

  <MessageId>CABxyz123@mail.example.com</MessageId>

  <AttachmentHandlers>MeetingNotes.pdf:3f2504e0-4f89-11d3-9a0c-0305e82c3301</AttachmentHandlers>

</email>

```

| XML Element | Required | Description |
|-------------|----------|-------------|
| `Senders` | Yes | Sender email address(es). Multiple addresses separated by semicolon. Defaults to `"Unknown Sender"` if omitted or empty. |
| `Recipients` | Yes | Primary recipient address(es). Multiple addresses separated by semicolon. |
| `CCAddress` | No | CC address(es). Multiple addresses separated by semicolon. |
| `BCCAddress` | No | BCC address(es). Multiple addresses separated by semicolon. |
| `SentDate` | Yes | Date and time the email was sent. Must be parseable as a DateTime (e.g. `2024-03-15T14:30:00`). |
| `Subject` | No | Email subject line. |
| `Header` | No | Raw email header block. |
| `HtmlBody` | No | HTML body content of the email. Use a CDATA section if the HTML contains characters that would otherwise need escaping. |
| `TextBody` | No | Plain text body content of the email. |
| `Keywords` | No | Comma-separated list of user-defined keywords to assign to the document (e.g. `invoice,Q1,finance`). |
| `MessageId` | No | The email's Message-ID header value (e.g. `CABxyz123@mail.example.com`). Used for duplicate detection: if a document with the same `EmailName` and the same `MessageId` already exists in the folder, the call fails. |
| `AttachmentHandlers` | No | Semicolon-separated list of attachment descriptors in the format `{filename}:{upload-handler-guid}`. Upload handlers must be pre-created with `CreateUploadHandler`. |

> **Note:** `MessageId` is only available via `RegisterEmail3`. The other `RegisterEmail` variants do not expose this field.

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
| `DocumentName` | The actual document name used (may differ from `EmailName` if auto-naming or extension appending was applied). |

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

POST /srv.asmx/RegisterEmail3 HTTP/1.1

Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

&FolderPath=/Finance/Emails

&EmailName=Q1-Budget-Meeting.EMAIL

&parametersXml=<email><Senders>alice@example.com</Senders><Recipients>bob@example.com</Recipients><CCAddress></CCAddress><BCCAddress></BCCAddress><SentDate>2024-03-15T14:30:00</SentDate><Subject>Q1 Budget Meeting Notes</Subject><Header></Header><HtmlBody></HtmlBody><TextBody>See attached.</TextBody><Keywords>budget,Q1</Keywords><MessageId>CABxyz123@mail.example.com</MessageId><AttachmentHandlers>MeetingNotes.pdf:3f2504e0-4f89-11d3-9a0c-0305e82c3301</AttachmentHandlers></email>

```

### GET Request

```

GET /srv.asmx/RegisterEmail3

  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

  &FolderPath=/Finance/Emails

  &EmailName=Q1-Budget-Meeting.EMAIL

  &parametersXml=%3Cemail%3E%3CSenders%3Ealice%40example.com%3C%2FSenders%3E...%3C%2Femail%3E

HTTP/1.1

```

> **Note:** URL-encode the `parametersXml` value when using GET. POST is strongly recommended for this API because the XML body can be lengthy and contain characters that require encoding.

### SOAP Request

```xml

<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"

               xmlns:tns="http://tempuri.org/">

  <soap:Body>

    <tns:RegisterEmail3>

      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>

      <tns:FolderPath>/Finance/Emails</tns:FolderPath>

      <tns:EmailName>Q1-Budget-Meeting.EMAIL</tns:EmailName>

      <tns:parametersXml><![CDATA[

        <email>

          <Senders>alice@example.com</Senders>

          <Recipients>bob@example.com</Recipients>

          <CCAddress></CCAddress>

          <BCCAddress></BCCAddress>

          <SentDate>2024-03-15T14:30:00</SentDate>

          <Subject>Q1 Budget Meeting Notes</Subject>

          <Header></Header>

          <HtmlBody></HtmlBody>

          <TextBody>See attached.</TextBody>

          <Keywords>budget,Q1</Keywords>

          <MessageId>CABxyz123@mail.example.com</MessageId>

          <AttachmentHandlers>MeetingNotes.pdf:3f2504e0-4f89-11d3-9a0c-0305e82c3301</AttachmentHandlers>

        </email>

      ]]></tns:parametersXml>

    </tns:RegisterEmail3>

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

Files an e-mail as a document, with every field of the message in one XML document instead of as
separate parameters.

> **It loses the blind-copy address, and writes it into the visible one.**
> `RegisterEmailModel.ParseFromXml` handles `<BCCAddress>` by assigning the *CC* property - the same
> one `<CCAddress>` sets - so the last of the two wins and `BCC` is stored empty. A message registered
> this way with a `<BCCAddress>` ends up with that address in the `CC` field of its `SYSTBL_EMAIL`
> property set, where anyone who may read the document can see it. Use
> [RegisterEmail2](RegisterEmail2.md), which takes the two as parameters and stores both correctly,
> until this is fixed.

```javascript
const parametersXml = `
  <email>
    <Senders>supplier@example.com</Senders>
    <Recipients>accounts@example.com</Recipients>
    <CCAddress>manager@example.com</CCAddress>
    <SentDate>2026-09-01</SentDate>
    <Subject>Invoice query</Subject>
    <TextBody>Could you check invoice 4471?</TextBody>
    <Keywords>invoice,supplier</Keywords>
  </email>`;

const root = await call('RegisterEmail3', {
  authenticationTicket: ticket,
  FolderPath: '/Finance/Emails',
  EmailName: '2026-09-supplier-query',
  parametersXml
});
```

Element names are matched without regard to case. **Malformed XML here is an HTTP 500 with no error
document at all** - the parse runs before the operation is entered and outside any handler - so
validate the document before sending it.

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

- `FolderPath` and `EmailName` are always separate parameters -" they cannot be placed inside `parametersXml`. Any `EmailName` field inside the XML is ignored.

- If `EmailName` does not end with `.EMAIL` (case-insensitive), the extension is appended automatically (e.g. `Meeting-Notes` becomes `Meeting-Notes.email`).

- If `EmailName` is exactly `.EMAIL`, the system auto-prefixes the generated document ID to create a unique name.

- XML element names inside `parametersXml` are **case-insensitive** (`<sentdate>` and `<SentDate>` are equivalent).

- The `MessageId` element enables explicit **duplicate detection**: if a document with the same `EmailName` and `MessageId` already exists in the folder, the registration is rejected. This is only supported in `RegisterEmail3`; the other variants do not accept a `MessageId` input.

- POST is strongly recommended over GET because `parametersXml` may contain lengthy or special-character content that is awkward to URL-encode.

- Email documents are stored with `PercentComplete=100` (completed) and are not subject to the checkout/lock workflow.

- The document's **creation date** and **modification date** are set to the `SentDate` in the XML. The **completion date** is set to the current server time.

- After a successful call, all referenced upload handlers are automatically deleted from the server.

---

## Related APIs

- [RegisterEmail](RegisterEmail.md) - Register an email using a combined `TargetPath` (no keywords, no MessageId)

- [RegisterEmail1](RegisterEmail1.md) - Register an email using a combined `TargetPath` with keywords

- [RegisterEmail2](RegisterEmail2.md) - Register an email using separate `FolderPath` and `EmailName` with individual field parameters

- [CreateUploadHandler](CreateUploadHandler.md) - Create an upload handler for pre-uploading email attachments

- [UploadFileChunk](UploadFileChunk.md) - Upload file content in chunks to an upload handler

- [GetDocument](GetDocument.md) - Get the properties of the registered email document

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4090` | a document of that name is already in the folder |
| `4041` | no folder at `FolderPath` |
| `HTTP 500` | `parametersXml` is not well-formed XML; the exception escapes and there is no error document |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Anonymous users cannot perform this action | The authenticated user is an anonymous/guest user. |
| The email message xml document does not have a root element | `parametersXml` is empty, malformed, or has no root element. |
| SentDate cannot be parsed | The `<SentDate>` value in `parametersXml` is not a valid DateTime. |
| Folder not found | The specified `FolderPath` does not exist. |
| Upload handler not found | One of the attachment handler GUIDs is invalid or has expired. |
| Invalid attachment handler format | The `AttachmentHandlers` value is malformed (missing `:` separator or invalid GUID). |
| Duplicate email | An email with the same document name and `MessageId` already exists in the target folder. |
| Access denied | The user does not have add document permission on the target folder. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

