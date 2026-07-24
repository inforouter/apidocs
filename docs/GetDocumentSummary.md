# GetDocumentSummary API

Returns the stored AI-generated summary for a specified version of a document. The summary is produced by the infoRouter Connect summarization/categorization service and persisted in the `DOCSUMMARY` table. Unlike [`GetDocumentAbstract1`](GetDocumentAbstract1.md) (which extracts text from the full-text index and back-fills on demand), this API only returns a summary that has already been stored via [`SetDocumentSummary`](SetDocumentSummary.md); it does not generate one.

## Endpoint

```
/srv.asmx/GetDocumentSummary
```

## Methods

- **GET** `/srv.asmx/GetDocumentSummary?authenticationTicket=...&path=...&versionNumber=...`
- **POST** `/srv.asmx/GetDocumentSummary` (form data)
- **SOAP** Action: `http://tempuri.org/GetDocumentSummary`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1-Report.pdf`), or a short document ID path (`~D{id}` or `~D{id}.ext`). |
| `versionNumber` | int | Yes | Version number to retrieve the summary for. Pass `0` for the latest published version. Must be `0` or a modern-format version number (>= 1,000,000). Values between `1` and `999,999` are rejected. |

### Version Number Format

infoRouter uses a large-integer version numbering scheme where version 1 = `1000000`, version 2 = `2000000`, etc. Pass `0` to always target the latest published version.

## Response

### Success Response

On success, the summary text is returned inside a `<Value>` child element:

```xml
<response success="true" error="">
  <Value>This document is a Q1 2024 financial report covering revenue, expenses, and year-over-year comparisons for the North America region.</Value>
</response>
```

| Element / Attribute | Description |
|--------------------|-------------|
| `success` | `"true"` on success. |
| `error` | Empty string on success. |
| `<Value>` | Child element containing the stored summary for the requested document version. Contains `-` when no summary has been stored yet. |

### Error Response

```xml
<response success="false" error="[901] Session expired or Invalid ticket" />
```

## Required Permissions

The calling user must have at least **read access** to the document (same check as [`GetDocumentAbstract1`](GetDocumentAbstract1.md)). If the document has no stored summary, `<Value>` returns `-` rather than an error.

## Example

### Request (GET)

```
GET /srv.asmx/GetDocumentSummary?authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301&path=/Finance/Reports/Q1-2024-Report.pdf&versionNumber=0 HTTP/1.1
```

### Request (POST)

```
POST /srv.asmx/GetDocumentSummary HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301&path=/Finance/Reports/Q1-2024-Report.pdf&versionNumber=0
```

### Request (SOAP)

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:GetDocumentSummary>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:path>/Finance/Reports/Q1-2024-Report.pdf</tns:path>
      <tns:versionNumber>0</tns:versionNumber>
    </tns:GetDocumentSummary>
  </soap:Body>
</soap:Envelope>
```

## Notes

- `versionNumber=0` targets the **latest published version**.
- Version numbers between `1` and `999,999` are rejected. Use `0` or the modern format (e.g. `1000000` for version 1).
- Both full infoRouter paths and short document ID paths (`~D{id}` / `~D{id}.ext`) are accepted.
- Shortcut and URL documents have no summary; `<Value>` returns `-`.
- Store or update the summary with [`SetDocumentSummary`](SetDocumentSummary.md).

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Document not found | The specified path does not resolve to an existing document. |
| Invalid argument exception. Version numbers cannot be less than 1000000... | `versionNumber` is between 1 and 999,999 (must be 0 or >= 1,000,000). |
| This document is marked as 'offline'... | The document is offline and its properties are temporarily inaccessible. |

## Related APIs

- [SetDocumentSummary](SetDocumentSummary.md) - Store or update the summary for a document version
- [GetDocumentAbstract1](GetDocumentAbstract1.md) - Get the full-text index abstract (auto-generated)
- [GetDocument](GetDocument.md) - Get full document metadata and properties
