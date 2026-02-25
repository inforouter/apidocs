# GetDocumentTextOnlyContent API

Returns the plain-text alternative content stored alongside the latest published version of a document. This text-only content is a separately stored artifact in the document warehouse -" it is only present if it has been explicitly set (for example, by a conversion process or via `SetDocumentTextOnlyContent`). If the document has no published version, is offline, or is a shortcut or URL type, an error is returned.

## Endpoint

```
/srv.asmx/GetDocumentTextOnlyContent
```

## Methods

- **GET** `/srv.asmx/GetDocumentTextOnlyContent?AuthenticationTicket=...&Path=...`
- **POST** `/srv.asmx/GetDocumentTextOnlyContent` (form data)
- **SOAP** Action: `http://tempuri.org/GetDocumentTextOnlyContent`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1-Report.pdf`), or a short document ID path (`~D{id}` or `~D{id}.ext`). |

> **Note:** This API always retrieves the text-only content for the **latest published version** of the document. There is no version number parameter.

---

## Response

### Success Response

On success, the plain text content is returned as the body of the `<response>` element (not inside a child element):

```xml
<response success="true" error="">This is the plain text content of the document.
It may span multiple lines and represents the text-only
alternative stored in the document warehouse.</response>
```

| Attribute | Description |
|-----------|-------------|
| `success` | `"true"` on success. |
| `error` | Empty string on success. |
| *(element body)* | The plain text content of the latest published version. May be an empty string if text-only content has never been set for this document. |

### Error Response

```xml
<response success="false" error="There is no published version for this document." />
```

---

## Required Permissions

The calling user must have at least read access to the document and its published version.

---

## Example

### GET Request

```
GET /srv.asmx/GetDocumentTextOnlyContent
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports/Q1-2024-Report.pdf
HTTP/1.1
```

### GET Request (short ID path)

```
GET /srv.asmx/GetDocumentTextOnlyContent
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=~D1051
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetDocumentTextOnlyContent HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance/Reports/Q1-2024-Report.pdf
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetDocumentTextOnlyContent>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:Path>/Finance/Reports/Q1-2024-Report.pdf</tns:Path>
    </tns:GetDocumentTextOnlyContent>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- The text content is returned directly as the body of the `<response>` element, not inside a named child element.
- This API retrieves a **separately stored** plain-text artifact from the document warehouse. It is distinct from the full-text search index abstract returned by `GetDocumentAbstract1`. The content is only present if it was previously written (e.g. by a document conversion process or via `SetDocumentTextOnlyContent`).
- Only the **latest published version** is accessible through this API. Documents with no published version return an error.
- Offline documents, URL documents, and shortcut documents do not have text-only content and will return an error.
- Both full infoRouter paths and short document ID paths (`~D{id}` or `~D{id}.ext`) are accepted for the `Path` parameter.

---

## Related APIs

- [GetDocumentAbstract1](GetDocumentAbstract1.md) - Get the full-text search index abstract for a document version
- [GetDocument](GetDocument.md) - Get full document metadata and properties
- [GetDocumentVersions](GetDocumentVersions.md) - Get the version history list for a document

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Document not found | The specified path does not resolve to an existing document. |
| No published version | The document has no published version. |
| Document is offline | The document is marked as offline and its content is unavailable. |
| URL or shortcut | URL documents and shortcuts do not have text-only content. |
| Access denied | The user does not have read access to the document or its published version. |
| `SystemError:...` | An unexpected server-side error occurred. |

---
