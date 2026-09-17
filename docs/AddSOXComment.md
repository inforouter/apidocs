# AddSOXComment API

Adds a Sarbanes-Oxley (SOX) compliance comment to the latest version of the specified document. The comment is recorded as a SOX log entry and is permanently stored with the document version. The calling user must have **Add Comment** permission on the document.

## Endpoint

```

/srv.asmx/AddSOXComment

```

## Methods

- **GET** `/srv.asmx/AddSOXComment?authenticationTicket=...&DocumentPath=...&CommentText=...`

- **POST** `/srv.asmx/AddSOXComment` (form data)

- **SOAP** Action: `http://tempuri.org/AddSOXComment`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `DocumentPath` | string | Yes | Full infoRouter path of the document to comment on (e.g. `/Finance/Controls/SOX-Control-A1.pdf`). |
| `CommentText` | string | Yes | The SOX compliance comment text to record. Leading/trailing whitespace is normalized before saving. |

## Response

### Success Response

```xml

<root success="true" />

```

### Error Response

```xml

<root success="false" error="[ErrorCode] Error message" />

```

---

## Required Permissions

- The caller must be an **authenticated user** with a valid ticket.

- The caller must have **Add Comment** (`DocumentCommentAdds`) permission on the target document. This is a standard document ACL permission -" no special workflow task is required (unlike `AddISOComment`).

- The document must not be in an **Offline (archived)** state.

---

## Example

### GET Request

```

GET /srv.asmx/AddSOXComment?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301&DocumentPath=/Finance/Controls/SOX-Control-A1.pdf&CommentText=Control+reviewed+and+confirmed+compliant+with+SOX+Section+404 HTTP/1.1

```

### POST Request

```

POST /srv.asmx/AddSOXComment HTTP/1.1

Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301

&DocumentPath=/Finance/Controls/SOX-Control-A1.pdf

&CommentText=Control reviewed and confirmed compliant with SOX Section 404

```

### SOAP Request

```xml

<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"

               xmlns:tns="http://tempuri.org/">

  <soap:Body>

    <tns:AddSOXComment>

      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>

      <tns:DocumentPath>/Finance/Controls/SOX-Control-A1.pdf</tns:DocumentPath>

      <tns:CommentText>Control reviewed and confirmed compliant with SOX Section 404</tns:CommentText>

    </tns:AddSOXComment>

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

Writes a SOX compliance entry against the document's current version. It is a log entry, not a
comment: [GetDocumentComments](GetDocumentComments.md) does not return it, and
[GetSoxLogs](GetSoxLogs.md) does.

```javascript
await call('AddSOXComment', {
  authenticationTicket: ticket,
  DocumentPath: '/Finance/Reports/Q1.pdf',
  CommentText: 'Reviewed under SOX 404.'
});

const logs = await call('GetSoxLogs', {
  authenticationTicket: ticket, DocumentPath: '/Finance/Reports/Q1.pdf'
});

for (const entry of logs.querySelectorAll('SoxLog')) {
  console.log(entry.querySelector('VersionNumber').textContent,
              entry.querySelector('UserName').textContent,
              entry.querySelector('Comment').textContent);
}
```

The entry records the version that was current when it was written, so a later version does not
inherit it.

## Notes

- The comment is always applied to the **latest version** of the document. There is no way to add a SOX comment to a specific older version via this API.

- Comment text is sanitized (whitespace normalized) before being stored.

- If the document is in an **Offline** state (archived to secondary storage), the API returns an error. The document must be online to accept SOX comments.

- Unlike `AddISOComment`, this API does **not** require an active workflow task. Permission is controlled solely by the document's ACL (`DocumentCommentAdds` action).

- SOX log entries are immutable once written and form a permanent audit trail for compliance purposes.

---

## Related APIs

- [AddISOComment](AddISOComment.md) - Add an ISO compliance review comment to a document

- [GetSoxLogs](GetSoxLogs.md) - Retrieve the SOX comment history for a document

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all - the anonymous user is refused |
| `4041` | no document at that path - including one the caller may not see |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Document not found | The specified `DocumentPath` does not exist or the user does not have access to it. |
| Access denied | The calling user does not have `DocumentCommentAdds` permission on the document. |
| Document is offline | The document is archived (offline state) and cannot accept SOX comments. |

---

