# UpdateDocumentProperties2 API

Updates the core properties of the specified document: display name, description, update instructions, source, language, author, and importance level. All fields are optional -" only the fields provided are updated. This is the most complete version of the UpdateDocumentProperties family.

## Endpoint

```
/srv.asmx/UpdateDocumentProperties2
```

## Methods

- **GET** `/srv.asmx/UpdateDocumentProperties2?authenticationTicket=...&path=...&newDocumentName=...&newDescription=...&newUpdateInstructions=...&newDocumentSource=...&newDocumentLanguage=...&newDocumentAuthor=...&importance=...`
- **POST** `/srv.asmx/UpdateDocumentProperties2` (form data)
- **SOAP** Action: `http://tempuri.org/UpdateDocumentProperties2`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1-Report.pdf`), or a short document ID path (`~D{id}`). |
| `newDocumentName` | string | No | New display name for the document. Pass `null` or omit to leave unchanged. |
| `newDescription` | string | No | New description for the document. Line endings are normalized automatically. |
| `newUpdateInstructions` | string | No | New update instructions for contributors. Line endings are normalized automatically. |
| `newDocumentSource` | string | No | New source value (e.g. originating organization or URL). Line endings are normalized automatically. |
| `newDocumentLanguage` | string | No | New language tag (e.g. `en`, `en-US`, `fr`). Line endings are normalized automatically. |
| `newDocumentAuthor` | string | No | New author name. Line endings are normalized automatically. |
| `importance` | short (int16) | No | Importance level: `-1` = NoMarkings, `0` = Low, `1` = Normal, `2` = High, `3` = Vital. Pass `null` or omit to leave unchanged. |

---

## Response

### Success Response

```xml
<response success="true" error="" />
```

### Error Response

```xml
<response success="false" error="Document not found." />
```

---

## Required Permissions

The calling user must have **write** (modify properties) permission on the document or its containing folder.

---

## Example

### GET Request

```
GET /srv.asmx/UpdateDocumentProperties2
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &path=/Finance/Reports/Q1-2024-Report.pdf
  &newDocumentName=Q1+2024+Financial+Report
  &newDescription=Quarterly+financial+summary
  &newDocumentAuthor=Jane+Smith
  &importance=2
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/UpdateDocumentProperties2 HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&path=/Finance/Reports/Q1-2024-Report.pdf
&newDocumentName=Q1 2024 Financial Report
&newDescription=Quarterly financial summary
&newDocumentAuthor=Jane Smith
&importance=2
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:UpdateDocumentProperties2>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:path>/Finance/Reports/Q1-2024-Report.pdf</tns:path>
      <tns:newDocumentName>Q1 2024 Financial Report</tns:newDocumentName>
      <tns:newDescription>Quarterly financial summary</tns:newDescription>
      <tns:newDocumentAuthor>Jane Smith</tns:newDocumentAuthor>
      <tns:importance>2</tns:importance>
    </tns:UpdateDocumentProperties2>
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

[UpdateDocumentProperties1](UpdateDocumentProperties1.md) with importance as well.

```javascript
await call('UpdateDocumentProperties2', {
  authenticationTicket: ticket,
  Path: path,
  NewDocumentName: 'Q1.pdf',
  NewDescription: 'Quarterly results',
  NewUpdateInstructions: '',
  NewDocumentSource: 'Finance system export',
  NewDocumentLanguage: 'en',
  NewDocumentAuthor: 'J Smith',
  importance: 3                 // -1 NoMarkings, 0 Low, 1 Normal, 2 High, 3 Vital
});
```

`importance` is nullable here, so leaving it out keeps the current value - the one field in this
family that is not overwritten when omitted. [GetDocument](GetDocument.md) reads it back as a name
(`Vital`) rather than as the number.

### Which of the three to use

| | Name, description, update instructions | Source, language, author | Importance |
|---|---|---|---|
| [UpdateDocumentProperties](UpdateDocumentProperties.md) | yes | | |
| [UpdateDocumentProperties1](UpdateDocumentProperties1.md) | yes | yes | |
| [UpdateDocumentProperties2](UpdateDocumentProperties2.md) | yes | yes | yes |

Each writes **every** field it takes, so a value left empty is cleared rather than left alone. Read
the document with [GetDocument](GetDocument.md) first and send back what should survive. Using the
wider variant to change one narrow field will empty the fields it adds.

`NewDocumentName` is nullable, so an empty one reaches the operation and is refused with `4000` "a
document must have a name" rather than by model binding. A name carrying any of
`/ \ : * ? " < > | # % & +` or a tab is refused `4000` too - unlike creating a document, where such a
name is silently cleaned up.

## Notes

- Passing `null` for any optional parameter leaves that field unchanged on the document.
- The `importance` field maps to: `-1` = NoMarkings, `0` = Low, `1` = Normal, `2` = High, `3` = Vital. To set importance independently, you can also use `SetDocumentImportance`.
- Line endings in all text fields are normalized to the server format.
- This is the most complete variant. Use `UpdateDocumentProperties` or `UpdateDocumentProperties1` if you don't need the importance field.

---

## Related APIs

- [UpdateDocumentProperties](UpdateDocumentProperties.md) - Update name, description, and update instructions only
- [UpdateDocumentProperties1](UpdateDocumentProperties1.md) - Update properties including source, language, and author
- [SetDocumentImportance](SetDocumentImportance.md) - Set the importance level independently
- [GetDocument](GetDocument.md) - Get all current document properties

---

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4041` | no document at that path - including a folder path, and one the caller may not see |
| `4000` | `NewDocumentName` is empty or carries a character a document name may not |
| `4090` | a document of the new name is already in the folder |
| `4030` | the caller may not change this document |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Document not found | The specified path does not resolve to an existing document. |
| Access denied | The user does not have write permission on the document. |
| `SystemError:...` | An unexpected server-side error occurred. |

---