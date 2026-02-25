# SetDocumentTextOnlyContent API

Updates the plain-text alternative content of the latest version of the specified document. The text-only content is a searchable plain-text representation stored alongside the binary document file. It is used for full-text indexing when the binary content cannot be indexed directly (e.g. encrypted or proprietary formats). Calling this API replaces any previously stored text-only content for the latest version.

## Endpoint

```
/srv.asmx/SetDocumentTextOnlyContent
```

## Methods

- **GET** `/srv.asmx/SetDocumentTextOnlyContent?authenticationTicket=...&path=...&contentText=...`
- **POST** `/srv.asmx/SetDocumentTextOnlyContent` (form data)
- **SOAP** Action: `http://tempuri.org/SetDocumentTextOnlyContent`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1-Report.pdf`), or a short document ID path (`~D{id}`). |
| `contentText` | string | No | The plain-text content to store for the latest version. Pass an empty string or omit to clear the stored text. Line endings are normalized automatically. |

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

The calling user must have **write** (modify) permission on the document or its containing folder.

---

## Example

### GET Request

```
GET /srv.asmx/SetDocumentTextOnlyContent
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &path=/Finance/Reports/Q1-2024-Report.pdf
  &contentText=Revenue+for+Q1+2024+totals+1.2M+USD
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/SetDocumentTextOnlyContent HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&path=/Finance/Reports/Q1-2024-Report.pdf
&contentText=Revenue for Q1 2024 totals 1.2M USD
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:SetDocumentTextOnlyContent>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:path>/Finance/Reports/Q1-2024-Report.pdf</tns:path>
      <tns:contentText>Revenue for Q1 2024 totals 1.2M USD</tns:contentText>
    </tns:SetDocumentTextOnlyContent>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- This API always targets the **latest version** of the document. To update text content for a specific version, use `SetVersionTextOnlyContent`.
- Line endings in `contentText` are normalized to the server format before storing.
- Passing `null` or an empty string clears the previously stored text-only content.
- The stored text content is used by the full-text search index. After updating, the document may need to be re-indexed before the new text becomes searchable.
- This API does not modify the binary file -" only the stored plain-text metadata.

---

## Related APIs

- [SetVersionTextOnlyContent](SetVersionTextOnlyContent.md) - Update text-only content for a specific document version
- [GetDocumentTextOnlyContent](GetDocumentTextOnlyContent.md) - Retrieve the stored text-only content of the latest version
- [GetVersionTextOnlyContent](GetVersionTextOnlyContent.md) - Retrieve the stored text-only content of a specific version

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Document not found | The specified path does not resolve to an existing document. |
| Access denied | The user does not have write permission on the document. |
| `SystemError:...` | An unexpected server-side error occurred. |

---