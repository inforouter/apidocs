# SetDocumentCompletionStatus API

Sets the completion status of the specified document using a `PercentComplete` value and an optional `CompletionDate`. A document with `PercentComplete = 100` is considered fully completed and can no longer be checked out or modified. Document subscribers are notified on a successful change.

## Endpoint

```

/srv.asmx/SetDocumentCompletionStatus

```

## Methods

- **GET** `/srv.asmx/SetDocumentCompletionStatus?AuthenticationTicket=...&Path=...&PercentComplete=...`

- **POST** `/srv.asmx/SetDocumentCompletionStatus` (form data)

- **SOAP** Action: `http://tempuri.org/SetDocumentCompletionStatus`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1-Report.pdf`), or a short document ID path (`~D{id}` or `~D{id}.ext`). |
| `PercentComplete` | int | Yes | Completion percentage. Use `100` to mark the document as complete. Use any value less than `100` (typically `0`) to mark it as incomplete. |
| `CompletionDate` | DateTime | No | The date the document was completed. Only meaningful when `PercentComplete = 100`. Must not be a future date. If omitted or set to `1900-01-01` when completing, the server automatically sets it to today's date. Pass `1900-01-01` (or omit) when marking a document as incomplete. |

### PercentComplete / CompletionDate Interaction

| `PercentComplete` | `CompletionDate` | Effective Result |
|-------------------|-----------------|------------------|
| `100` | omitted / `1900-01-01` | Completed; `CompletionDate` auto-set to today. |
| `100` | past or today | Completed with the supplied date. |
| `100` | future date | **Error** -" completion date cannot be in the future. |
| `< 100` | omitted / `1900-01-01` | Incomplete; `CompletionDate` cleared. |
| `< 100` | any non-base date | `PercentComplete` is **silently forced to 100** and the document is marked complete with the supplied date. |

---

## Response

### Success Response

```xml

<response success="true" error="" />

```

### Error Response

```xml

<response success="false" error="In order to complete a document, Please check-in the document first." />

```

---

## Required Permissions

The calling user must have **Document Completion** permission on the document.

---

## Example

### Mark a document as complete (GET)

```

GET /srv.asmx/SetDocumentCompletionStatus

  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

  &Path=/Finance/Reports/Q1-2024-Report.pdf

  &PercentComplete=100

HTTP/1.1

```

### Mark a document as incomplete (POST)

```

POST /srv.asmx/SetDocumentCompletionStatus HTTP/1.1

Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

&Path=/Finance/Reports/Q1-2024-Report.pdf

&PercentComplete=0

&CompletionDate=1900-01-01

```

### SOAP Request

```xml

<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"

               xmlns:tns="http://tempuri.org/">

  <soap:Body>

    <tns:SetDocumentCompletionStatus>

      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>

      <tns:Path>/Finance/Reports/Q1-2024-Report.pdf</tns:Path>

      <tns:PercentComplete>100</tns:PercentComplete>

      <tns:CompletionDate>2024-03-31</tns:CompletionDate>

    </tns:SetDocumentCompletionStatus>

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

Sets how far through a document is, and when it was finished.

```javascript
await call('SetDocumentCompletionStatus', {
  authenticationTicket: ticket,
  Path: '/Finance/Reports/Q1.pdf',
  PercentComplete: 50,
  CompletionDate: ''          // empty for none
});
```

**A completion date in the future is refused** with `4000`: a document cannot be recorded as finished
on a day that has not happened.

**A percentage must be one.** `PercentComplete` outside 0 to 100 is refused `4000`. Until 9.0
`200` and `-5` were both accepted and both stored, so a client reading the value back could not
assume it meant anything.

## Notes

- **Shortcut documents** (`.LNK`) cannot have their completion status changed. The call returns an error directing you to set the status on the original document instead.

- **Email documents** (`.EMAIL`) cannot have their completion status changed.

- A document that is currently **checked out** cannot be marked as complete (`PercentComplete = 100`). Check the document in first.

- If `PercentComplete < 100` but a non-base `CompletionDate` is supplied, the server silently upgrades `PercentComplete` to `100` and marks the document as complete.

- `CompletionDate` accepts UTC values, which are automatically converted to server local time.

- Document subscribers are notified of the completion status change on success.

- Use `GetDocument` to check the current `PercentComplete` and `CompletionDate` attributes before calling this API.

---

## Related APIs

- [GetDocument](GetDocument.md) - Get document properties including the current `PercentComplete` and `CompletionDate`

- [Lock](Lock.md) - Check out a document (a checked-out document cannot be marked complete)

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4000` | `CompletionDate` is in the future |
| `none` | `PercentComplete` is not range-checked; any integer is stored |
| `4041` | no document at that path - including a folder path, and one the caller may not see |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Document not found | The specified path does not resolve to an existing document. |
| Shortcut document | Completion status cannot be set on shortcut (`.LNK`) documents. |
| Email document | Completion status cannot be changed for email (`.EMAIL`) documents. |
| Document is checked out | The document must be checked in before it can be marked as complete. |
| Completion date in the future | `CompletionDate` must not be a future date. |
| Access denied | The user does not have Document Completion permission. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

