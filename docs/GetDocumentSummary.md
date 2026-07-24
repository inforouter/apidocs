# GetDocumentSummary API

Returns the AI-generated summary for a specified version of a document. Summaries are stored in the `DOCSUMMARY` table and produced by the local **infoRouter Connect** summarization service.

This API is **generate-on-read**: if a summary has already been stored (by a previous call or by [`SetDocumentSummary`](SetDocumentSummary.md)), it is returned directly. If none exists yet, the service attempts to generate one on the spot from the document's content, stores it, and returns it. When a summary cannot be produced (service not configured, unsupported content, etc.), the API returns the placeholder `-` rather than an error.

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

## Behavior

On each call the API evaluates the following, in order:

1. **Version resolution** - `versionNumber=0` resolves to the latest published version. If the document has no published version, `-` is returned.
2. **Shortcut / URL documents** - always return `-` (they have no content to summarize).
3. **Read security** - the caller must have read access to the document/version (see [Required Permissions](#required-permissions)).
4. **Offline documents** - return an error (content temporarily inaccessible).
5. **Stored summary** - if a summary already exists for the version, it is returned immediately (this is the normal, fast path).
6. **Generate-on-read** - if no summary is stored, the service tries to create one:
   - The requested version must exist in the warehouse, otherwise `-` is returned.
   - The local Connect service must be configured (`IRConnect` settings). If not, `-` is returned.
   - If the version has extracted OCR text, that text is sent to the Connect service. Otherwise, if the document's extension is a supported type (see below), the original file bytes are sent. If neither applies, `-` is returned.
   - The Connect service summarizes the content; the result is **stored in `DOCSUMMARY`** and returned.

### Supported file types for generation

`pdf`, `docx`, `xlsx`, `pptx`, `html`, `htm`, `txt`, `md`, `csv` (configurable via `IRConnect.SummaryExtensions`). A document whose version has no OCR text and whose extension is not in this list will not be summarized on read and returns `-`.

> **Note on first read.** The first read of an un-summarized document triggers content extraction and a call to the local Connect service, so it is slower than subsequent reads and has a side effect (the generated summary is persisted). Later reads return the stored value directly.

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
| `<Value>` | The stored or freshly generated summary. Contains `-` when no summary exists and none could be generated. |

### Error Response

```xml
<response success="false" error="[901] Session expired or Invalid ticket" />
```

## Required Permissions

The calling user must have at least **read access** to the document (same check as [`GetDocumentAbstract1`](GetDocumentAbstract1.md)).

> Because reads can trigger generation, a read-access user may cause a one-time summary to be generated and persisted for the document. Generation only happens once per version; thereafter the stored value is served.

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
- Generation requires the local Connect service to be configured via the `IRConnect` application settings (`BaseUrl`, `ApiKey`, `SummaryExtensions`). When it is not configured, the API still works but only returns already-stored summaries (or `-`).
- To store or overwrite a summary explicitly (without invoking the Connect service), use [`SetDocumentSummary`](SetDocumentSummary.md).

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Document not found | The specified path does not resolve to an existing document. |
| Invalid argument exception. Version numbers cannot be less than 1000000... | `versionNumber` is between 1 and 999,999 (must be 0 or >= 1,000,000). |
| This document is marked as 'offline'... | The document is offline and its properties are temporarily inaccessible. |
| Summarize service returned no payload. | The Connect service was called during generation but returned no response. |

## Related APIs

- [SetDocumentSummary](SetDocumentSummary.md) - Store or overwrite the summary for a document version
- [GetDocumentAbstract1](GetDocumentAbstract1.md) - Get the full-text index abstract (auto-generated from the search index)
- [GetDocument](GetDocument.md) - Get full document metadata and properties
