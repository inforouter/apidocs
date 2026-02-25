# GetDocumentAbstract API

> **OBSOLETE** -" This API is retained for backward compatibility only. Use [`GetDocumentAbstract1`](GetDocumentAbstract1.md) for new integrations. `GetDocumentAbstract1` returns a consistent XML structure for both success and error cases; this API does not.

Returns the full-text abstract (indexed text content) of a specified version of a document.

## Endpoint

```
/srv.asmx/GetDocumentAbstract
```

## Methods

- **GET** `/srv.asmx/GetDocumentAbstract?AuthenticationTicket=...&Path=...&VersionNumber=...`
- **POST** `/srv.asmx/GetDocumentAbstract` (form data)
- **SOAP** Action: `http://tempuri.org/GetDocumentAbstract`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1-Report.pdf`), or a short document ID path (`~D{id}` or `~D{id}.ext`). |
| `VersionNumber` | int | Yes | Version number to retrieve the abstract for. Pass `0` to retrieve the abstract for the latest published version. Must be `0` or a version number in the modern format (--- 1,000,000). Values between `1` and `999,999` are rejected with an error. |

### Version Number Format

infoRouter uses a large-integer version numbering scheme where version 1 = `1000000`, version 2 = `2000000`, etc. Pass `0` to always get the latest published version's abstract.

---

## Response

> **Warning:** The success and error responses use different XML structures -" this inconsistency is the primary reason this API is considered obsolete. See [`GetDocumentAbstract1`](GetDocumentAbstract1.md) for a consistent response format.

### Success Response

On success, the abstract text is returned inside an `<abstract>` child element:

```xml
<response success="true" error="">
  <abstract>This document covers the Q1 2024 financial results including
revenue figures, expense breakdowns, and year-over-year comparisons...</abstract>
</response>
```

| Element / Attribute | Description |
|--------------------|-------------|
| `success` | `"true"` on success. |
| `error` | Empty string on success. |
| `<abstract>` | Child element containing the full-text abstract (indexed content) of the requested document version. |

### Error Response

On any error, a flat `<response>` element is returned **without** the `<abstract>` child:

```xml
<response success="false" error="[900] Authentication failed" />
```

This structural difference between success (has `<abstract>` child) and error (flat element with only attributes) is what the obsolete warning refers to.

---

## Required Permissions

The calling user must have at least read access to the document. The abstract is extracted from the full-text search index; if the document has not been indexed, the returned abstract may be empty.

---

## Example

### GET Request

```
GET /srv.asmx/GetDocumentAbstract
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports/Q1-2024-Report.pdf
  &VersionNumber=0
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetDocumentAbstract HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance/Reports/Q1-2024-Report.pdf
&VersionNumber=0
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetDocumentAbstract>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:Path>/Finance/Reports/Q1-2024-Report.pdf</tns:Path>
      <tns:VersionNumber>0</tns:VersionNumber>
    </tns:GetDocumentAbstract>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- This API is **obsolete**. Use [`GetDocumentAbstract1`](GetDocumentAbstract1.md) for all new integrations.
- The abstract text is sourced from the full-text search index. If the document has not been indexed, the abstract may be empty.
- `VersionNumber=0` retrieves the abstract for the **latest published version** of the document.
- Version numbers between `1` and `999,999` are rejected. Use `0` or the modern format (e.g. `1000000` for version 1, `2000000` for version 2).
- Both full infoRouter paths and short document ID paths (`~D{id}` or `~D{id}.ext`) are accepted for the `Path` parameter.

---

## Related APIs

- [GetDocumentAbstract1](GetDocumentAbstract1.md) - Preferred replacement with consistent XML response structure
- [GetDocument](GetDocument.md) - Get full document metadata and properties
- [GetDocumentVersions](GetDocumentVersions.md) - Get the version history list for a document

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Document not found | The specified path does not resolve to an existing document. |
| Invalid version number | `VersionNumber` is between 1 and 999,999 (must be 0 or --- 1,000,000). |
| `SystemError:...` | An unexpected server-side error occurred. |

---
