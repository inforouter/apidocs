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

## Notes

- The `importance` parameter must be exactly one of the five defined integer codes. Any other value (e.g. `4`, `-2`) causes the API to return an error immediately without modifying the document.
- Use `importance = -1` (NoMarkings) to clear any previously set importance level and return the document to a neutral state.
- The importance level is stored as document metadata and does not affect versioning, publishing, or workflow state.
- Use `GetDocument` to read the current `Importance` attribute of a document before calling this API.

---

## Related APIs

- [GetDocument](GetDocument) - Get document properties including the current `Importance` attribute
- [SetDocumentCompletionStatus](SetDocumentCompletionStatus) - Set the completion status of a document
- [UpdateDocumentProperties](UpdateDocumentProperties) - Update multiple document properties in a single call

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| `the importance argument can be -1=NoMarkings; 0=Low; 1=Normal; 2=High; 3=Vital` | The supplied `importance` value is not in the valid range. |
| Document not found | The specified path does not resolve to an existing document. |
| Access denied | The user does not have write permission on the document. |
| `SystemError:...` | An unexpected server-side error occurred. |

---

*For detailed documentation visit: https://support.inforouter.com/api-docs/SetDocumentImportance*
