# SetDocumentSummary API

Stores (inserts or updates) the summary for a specified version of a document in the `DOCSUMMARY` table. This is the **explicit** counterpart to [`GetDocumentSummary`](GetDocumentSummary.md): it writes the summary text you provide directly to the database and does **not** call the infoRouter Connect service. Calling it again for the same document version overwrites the previously stored summary.

Typical uses:
- Persist a summary produced by your own pipeline or an external Connect call.
- Correct or replace an auto-generated summary.
- Pre-seed a summary so that [`GetDocumentSummary`](GetDocumentSummary.md) serves it without queueing any work.

## Writing a summary protects it

Every stored summary records who wrote it. A summary written through this API is stamped with the calling user, and **the server never overwrites it**: regeneration only ever replaces a summary the system produced itself.

That matters when a folder has automatic summarization switched on, or when a new version is published. A summary the system generated is replaced freely; one a person wrote through this API stays as it is until a person changes it again.

The same applies to a summary stored before 9.0, when nothing recorded an author. Those carry no stamp, and an unstamped summary is left alone rather than assumed to be regenerable.

## Endpoint

```
/srv.asmx/SetDocumentSummary
```

## Methods

- **GET** `/srv.asmx/SetDocumentSummary?authenticationTicket=...&path=...&versionNumber=...&summary=...`
- **POST** `/srv.asmx/SetDocumentSummary` (form data)
- **SOAP** Action: `http://tempuri.org/SetDocumentSummary`

> For anything but very short summaries, use **POST** (or SOAP). Summary text can be large and is unsuitable for a URL query string.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `authenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `path` | string | Yes | Full infoRouter path to the document (e.g. `/Finance/Reports/Q1-Report.pdf`), or a short document ID path (`~D{id}` or `~D{id}.ext`). |
| `versionNumber` | int | Yes | Version number to store the summary for. Pass `0` for the published version, or for the latest version when the document has never been published. Must be `0` or a modern-format version number (>= 1,000,000). Values between `1` and `999,999` are rejected. |
| `summary` | string | Yes | The summary text to store. Trimmed to the maximum database string length. An empty string clears the stored summary text (the row is kept; [`GetDocumentSummary`](GetDocumentSummary.md) will then report `-`). |

### Version Number Format

infoRouter uses a large-integer version numbering scheme where version 1 = `1000000`, version 2 = `2000000`, etc. Pass `0` to target the published version, or the latest version when the document has never been published.

## Behavior

1. **Version resolution** - `versionNumber=0` resolves to the published version, or to the latest version when the document has never been published. Only a document with no versions at all is an error.
2. **Shortcut / URL documents** - rejected with an error (they cannot hold a summary).
3. **Write security** - the caller must have `'Add/Change Meta data'` access (see [Required Permissions](#required-permissions)).
4. **Offline documents** - rejected with an error (content temporarily inaccessible).
5. **Upsert** - the summary is inserted if none exists for the version, or updated (overwritten) if one does.

## Response

### Success Response

```xml
<response success="true" error="" />
```

| Element / Attribute | Description |
|--------------------|-------------|
| `success` | `"true"` when the summary was stored. |
| `error` | Empty string on success. |

### Error Response

```xml
<response success="false" error="[901] Session expired or Invalid ticket" />
```

## Required Permissions

The calling user must have **'Add/Change Meta data'** access (`IrAction.MetaDataAddChange`) to the document - the same privilege required to modify other document metadata. Read-only users cannot store a summary.

## Example

### Request (POST)

```
POST /srv.asmx/SetDocumentSummary HTTP/1.1
Content-Type: application/x-www-form-urlencoded

authenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301&path=/Finance/Reports/Q1-2024-Report.pdf&versionNumber=0&summary=Q1+2024+financial+report+covering+revenue+and+expenses.
```

### Request (SOAP)

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:SetDocumentSummary>
      <tns:authenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:authenticationTicket>
      <tns:path>/Finance/Reports/Q1-2024-Report.pdf</tns:path>
      <tns:versionNumber>0</tns:versionNumber>
      <tns:summary>Q1 2024 financial report covering revenue and expenses.</tns:summary>
    </tns:SetDocumentSummary>
  </soap:Body>
</soap:Envelope>
```

## Notes

- Insert-or-update semantics: the first call for a document version inserts a row; subsequent calls overwrite it.
- Storing a value here also prevents [`GetDocumentSummary`](GetDocumentSummary.md) from generating one, since it serves the stored value.
- `versionNumber=0` targets the **published version**, or the **latest version** when the document has never been published.
- Version numbers between `1` and `999,999` are rejected. Use `0` or the modern format (e.g. `1000000` for version 1).
- Both full infoRouter paths and short document ID paths (`~D{id}` / `~D{id}.ext`) are accepted.
- Summaries cannot be stored on shortcut or URL documents.
- The summary text is trimmed to the maximum database string length before storage.
- This API does not call the Connect service; it only writes to the database.

## Error Codes

| Error | Description |
|-------|-------------|
| `[900] Authentication failed` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | The ticket has expired or does not exist. |
| Access denied | The user lacks 'Add/Change Meta data' access to the document. |
| Document not found | The specified path does not resolve to an existing document. |
| Invalid argument exception. Version numbers cannot be less than 1000000... | `versionNumber` is between 1 and 999,999 (must be 0 or >= 1,000,000). |
| No version number was given, and this document has no published version to process. | `versionNumber` was 0 and the document has no versions at all, so there is nothing to store the summary against. |
| URL and shortcut files do not have text content. | The target is a shortcut or URL document, which cannot hold a summary. |
| This document is marked as 'offline'... | The document is offline and its properties are temporarily inaccessible. |

## Related APIs

- [GetDocumentSummary](GetDocumentSummary.md) - Retrieve (or generate-on-read) the summary for a document version
- [GetDocumentAbstract1](GetDocumentAbstract1.md) - Get the full-text index abstract (auto-generated from the search index)
- [GetDocument](GetDocument.md) - Get full document metadata and properties
