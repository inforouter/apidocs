# GetDocumentAbstract1 API

Returns the full-text abstract (indexed text content) of a specified version of a document. This is the current preferred API for retrieving document abstracts. It uses a consistent XML response structure for both success and error cases, unlike the obsolete [`GetDocumentAbstract`](GetDocumentAbstract.md).

## Endpoint

```
/srv.asmx/GetDocumentAbstract1
```

## Methods

- **GET** `/srv.asmx/GetDocumentAbstract1?authenticationTicket=...&path=...&versionNumber=...`
- **POST** `/srv.asmx/GetDocumentAbstract1` (form data)
- **SOAP** Action: `http://tempuri.org/GetDocumentAbstract1`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1-Report.pdf`), or a short document ID path (`~D{id}` or `~D{id}.ext`). |
| `versionNumber` | int | Yes | Version number to retrieve the abstract for. Pass `0` to retrieve the abstract for the latest published version. Must be `0` or a version number in the modern format (--- 1,000,000). Values between `1` and `999,999` are rejected with an error. |

### Version Number Format

infoRouter uses a large-integer version numbering scheme where version 1 = `1000000`, version 2 = `2000000`, etc. Pass `0` to always get the latest published version's abstract.

---

## Response

### Success Response

On success, the abstract text is returned inside a `<Value>` child element:

```xml
<response success="true" error="">
  <Value>This document covers the Q1 2024 financial results including
revenue figures, expense breakdowns, and year-over-year comparisons...</Value>
</response>
```

| Element / Attribute | Description |
|--------------------|-------------|
| `success` | `"true"` on success. |
| `error` | Empty string on success. |
| `<Value>` | Child element containing the full-text abstract (indexed content) of the requested document version. |

### Error Response

```xml
<response success="false" error="[900] Authentication failed" />
```

Both success and error use the same `<response>` root element -" the only difference is the presence of the `<Value>` child on success. This consistent structure is what makes `GetDocumentAbstract1` the preferred API over the obsolete [`GetDocumentAbstract`](GetDocumentAbstract.md).

---

## Required Permissions

The calling user must have at least read access to the document. The abstract is extracted from the full-text search index; if the document has not been indexed, the returned abstract may be empty.

---

## Example

### GET Request

```
GET /srv.asmx/GetDocumentAbstract1
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &path=/Finance/Reports/Q1-2024-Report.pdf
  &versionNumber=0
HTTP/1.1
```

### GET Request (specific version)

```
GET /srv.asmx/GetDocumentAbstract1
  ?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &path=/Finance/Reports/Q1-2024-Report.pdf
  &versionNumber=2000000
HTTP/1.1
```

### POST Request

```
POST /srv.asmx/GetDocumentAbstract1 HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&path=/Finance/Reports/Q1-2024-Report.pdf
&versionNumber=0
```

### SOAP Request

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetDocumentAbstract1>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:path>/Finance/Reports/Q1-2024-Report.pdf</tns:path>
      <tns:versionNumber>0</tns:versionNumber>
    </tns:GetDocumentAbstract1>
  </soap:Body>
</soap:Envelope>
```

---

## Notes

- `versionNumber=0` retrieves the abstract for the **latest published version** of the document.
- Version numbers between `1` and `999,999` are rejected with an error. Use `0` or the modern format (e.g. `1000000` for version 1, `2000000` for version 2).
- Both full infoRouter paths and short document ID paths (`~D{id}` or `~D{id}.ext`) are accepted for the `path` parameter.
- The abstract is sourced from the full-text search index. If the document has not been indexed, the `<Value>` element may be empty.
- This API supersedes the obsolete [`GetDocumentAbstract`](GetDocumentAbstract.md), which used an `<abstract>` child element on success and had inconsistent XML structure between success and error cases.

---

## Related APIs

- [GetDocumentAbstract](GetDocumentAbstract.md) - Obsolete predecessor with inconsistent XML structure
- [GetDocument](GetDocument.md) - Get full document metadata and properties
- [GetDocumentVersions](GetDocumentVersions.md) - Get the version history list for a document

---

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Document not found | The specified path does not resolve to an existing document. |
| Invalid version number | `versionNumber` is between 1 and 999,999 (must be 0 or --- 1,000,000). |
| `SystemError:...` | An unexpected server-side error occurred. |

---
