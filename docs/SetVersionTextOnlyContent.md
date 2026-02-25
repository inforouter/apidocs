# SetVersionTextOnlyContent API

Updates the plain-text alternative content of a specific version of the specified document. The text-only content is a searchable plain-text representation stored alongside the binary file. It is used for full-text indexing when the binary content cannot be indexed directly. Calling this API replaces any previously stored text-only content for the specified version.

## Endpoint

```
/srv.asmx/SetVersionTextOnlyContent
```

## Methods

- **GET** `/srv.asmx/SetVersionTextOnlyContent?authenticationTicket=...&path=...&versionNumber=...&contentText=...`
- **POST** `/srv.asmx/SetVersionTextOnlyContent` (form data)
- **SOAP** Action: `http://tempuri.org/SetVersionTextOnlyContent`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1-Report.pdf`), or a short document ID path (`~D{id}`). |
| `versionNumber` | int | Yes | The internal version number to update. Use `GetDocumentVersions` to retrieve the list of available version numbers. Version numbers are large integers (--- 1,000,000) assigned internally by infoRouter. |
| `contentText` | string | Yes | The plain-text content to store for the specified version. Line endings are normalized automatically. |

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
GET /srv.asmx/SetVersionTextOnlyContent
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &path=/Finance/Reports/Q1-2024-Report.pdf
  &versionNumber=1000001
  &contentText=Revenue+for+Q1+2024+totals+1.2M+USD
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/SetVersionTextOnlyContent HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&path=/Finance/Reports/Q1-2024-Report.pdf
&versionNumber=1000001
&contentText=Revenue for Q1 2024 totals 1.2M USD
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:SetVersionTextOnlyContent>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:path>/Finance/Reports/Q1-2024-Report.pdf</tns:path>
      <tns:versionNumber>1000001</tns:versionNumber>
      <tns:contentText>Revenue for Q1 2024 totals 1.2M USD</tns:contentText>
    </tns:SetVersionTextOnlyContent>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- To update text content for the **latest** version without specifying a version number, use `SetDocumentTextOnlyContent`.
- Use `GetDocumentVersions` to retrieve all available version numbers before calling this API.
- infoRouter version numbers are large integers (--- 1,000,000) assigned internally -" they are not sequential user-facing version labels.
- Line endings in `contentText` are normalized to the server format before storing.
- This API does not modify the binary file -" only the stored plain-text metadata for the specified version.
- After updating, the document may need to be re-indexed before the new text becomes searchable.

---

## Related APIs

- [SetDocumentTextOnlyContent](SetDocumentTextOnlyContent.md) - Update text-only content for the latest document version
- [GetVersionTextOnlyContent](GetVersionTextOnlyContent.md) - Retrieve the stored text-only content of a specific version
- [GetDocumentVersions](GetDocumentVersions.md) - Retrieve the list of all versions for a document

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Document not found | The specified path does not resolve to an existing document. |
| Version not found | The specified version number does not exist for this document. |
| Access denied | The user does not have write permission on the document. |
| `SystemError:...` | An unexpected server-side error occurred. |

---
