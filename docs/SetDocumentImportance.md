# SetDocumentImportance API

Sets the importance level of the specified document. Importance is a metadata flag used to communicate the urgency or priority of a document to readers. The value can be one of five levels ranging from no marking through vital. Any authenticated user with write access to the document can update this flag.

## Endpoint

```
/srv.asmx/SetDocumentImportance
```

## Methods

- **GET** `/srv.asmx/SetDocumentImportance?authenticationTicket=...&path=...&importance=...`
- **POST** `/srv.asmx/SetDocumentImportance` (form data)
- **SOAP** Action: `http://tempuri.org/SetDocumentImportance`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1-Report.pdf`), or a short document ID path (`~D{id}` or `~D{id}.ext`). |
| `importance` | short (int16) | Yes | Importance level to assign. Valid values: `-1` = NoMarkings, `0` = Low, `1` = Normal, `2` = High, `3` = Vital. Any other value returns an error. |

---

## Response

### Success Response

```xml
<response success="true" error="" />
```

### Error Response

```xml
<response success="false" error="the importance argument can be -1=NoMarkings; 0=Low; 1=Normal; 2=High; 3=Vital" />
```

---

## Required Permissions

The calling user must be authenticated and have **write** (modify properties) permission on the document or its containing folder. No special administrator role is required.

---

## Example

### GET Request

```
GET /srv.asmx/SetDocumentImportance
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &path=/Finance/Reports/Q1-2024-Report.pdf
  &importance=3
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/SetDocumentImportance HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&path=/Finance/Reports/Q1-2024-Report.pdf
&importance=3
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:SetDocumentImportance>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:path>/Finance/Reports/Q1-2024-Report.pdf</tns:path>
      <tns:importance>3</tns:importance>
    </tns:SetDocumentImportance>
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

Sets how important a document is.

```javascript
await call('SetDocumentImportance', {
  authenticationTicket: ticket,
  Path: '/Finance/Reports/Q1.pdf',
  Importance: 2            // -1 NoMarkings, 0 Low, 1 Normal, 2 High, 3 Vital
});
```

[GetDocument](GetDocument.md) reads the value back as a name - `NoMarkings`, `Low`, `Normal`, `High`,
`Vital` - rather than as the number that was sent.

**A value outside that range is answered `5000`, not `4000`.** The operation lets an
`ArgumentOutOfRangeException` out rather than refusing the request, so a bad importance looks like a
server fault. The message does name the five valid values.
[SetClassificationLevel](SetClassificationLevel.md), doing the same kind of job, refuses its bad
values properly with `4000`.

## Notes

- The `importance` parameter must be exactly one of the five defined integer codes. Any other value (e.g. `4`, `-2`) causes the API to return an error immediately without modifying the document.
- Use `importance = -1` (NoMarkings) to clear any previously set importance level and return the document to a neutral state.
- The importance level is stored as document metadata and does not affect versioning, publishing, or workflow state.
- Use `GetDocument` to read the current `Importance` attribute of a document before calling this API.

---

## Related APIs

- [GetDocument](GetDocument.md) - Get document properties including the current `Importance` attribute
- [SetDocumentCompletionStatus](SetDocumentCompletionStatus.md) - Set the completion status of a document
- [UpdateDocumentProperties](UpdateDocumentProperties.md) - Update multiple document properties in a single call

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `5000` | `Importance` is outside -1 to 3; it should be a `4000` |
| `4041` | no document at that path - including a folder path, and one the caller may not see |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `the importance argument can be -1=NoMarkings; 0=Low; 1=Normal; 2=High; 3=Vital` | The supplied `importance` value is not in the valid range. |
| Document not found | The specified path does not resolve to an existing document. |
| Access denied | The user does not have write permission on the document. |
| `SystemError:...` | An unexpected server-side error occurred. |

---