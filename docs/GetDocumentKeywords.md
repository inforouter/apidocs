# GetDocumentKeywords API

Returns the user-defined keywords assigned to a document. Keywords are returned as a comma-separated list inside a single `<Keywords>` element.

## Endpoint

```
/srv.asmx/GetDocumentKeywords
```

## Methods

- **GET** `/srv.asmx/GetDocumentKeywords?AuthenticationTicket=...&Path=...`
- **POST** `/srv.asmx/GetDocumentKeywords` (form data)
- **SOAP** Action: `http://tempuri.org/GetDocumentKeywords`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1-Report.pdf`), or a short document ID path (`~D{id}` or `~D{id}.ext`). |

---

## Response

### Success Response

Returns a `<response>` root element containing a `<Keywords>` child element whose text content is a comma-separated list of all keywords assigned to the document.

```xml
<response success="true" error="">
  <Keywords>finance,quarterly,2024,approved</Keywords>
</response>
```

| Element / Attribute | Description |
|--------------------|-------------|
| `success` | `"true"` on success. |
| `error` | Empty string on success. |
| `<Keywords>` | Comma-separated list of user-defined keywords. Empty text if no keywords are assigned. |

### No Keywords Response

When the document exists but has no keywords assigned:

```xml
<response success="true" error="">
  <Keywords></Keywords>
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
GET /srv.asmx/GetDocumentKeywords
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports/Q1-2024-Report.pdf
HTTP/1.1
```

### GET Request (short ID path)

```
GET /srv.asmx/GetDocumentKeywords
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=~D1051
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetDocumentKeywords HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance/Reports/Q1-2024-Report.pdf
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetDocumentKeywords>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:Path>/Finance/Reports/Q1-2024-Report.pdf</tns:Path>
    </tns:GetDocumentKeywords>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- Keywords are returned as a single comma-separated string inside `<Keywords>`, not as individual child elements.
- If the document has no keywords, `<Keywords>` is present but contains empty text.
- Both full infoRouter paths and short document ID paths (`~D{id}` or `~D{id}.ext`) are accepted for the `Path` parameter.

---

## Related APIs

- [GetDocument](GetDocument.md) - Get full document metadata and properties
- [GetDocumentComments](GetDocumentComments.md) - Get all comments attached to a document

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Document not found | The specified path does not resolve to an existing document. |
| `SystemError:...` | An unexpected server-side error occurred. |

---
