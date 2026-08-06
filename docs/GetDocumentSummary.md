# GetDocumentSummary API

Returns the AI-generated summary for a specified version of a document. Summaries are stored in the `DOCSUMMARY` table and produced by the local **infoRouter Connect** summarization service.

This API **never calls the Connect service itself**. Producing a summary takes as long as a language model takes to answer, which is far too long to hold a web request open, so the work is queued and a background worker runs it. A call either returns a stored summary or tells you the work is queued and you should ask again shortly. Asking twice does not queue the work twice, and a request from a user is placed ahead of everything queued automatically when documents were uploaded.

> **Changed in 9.0.** Earlier builds generated the summary during the call and returned it in the same response. Clients must now read the `status` attribute and come back for anything other than `Ready`.

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

Every successful call carries a `status` attribute saying whether the summary is there yet.

### Ready

The summary is stored and returned in the `<Value>` element, which is present only in this state.

```xml
<response success="true" status="Ready" error="">
  <Value>This document is a Q1 2024 financial report covering revenue, expenses, and year-over-year comparisons for the North America region.</Value>
</response>
```

### Queued

No summary is stored, and the work has been placed in the queue for the background worker. Ask again in a few seconds.

```xml
<response success="true" status="Queued" error="" />
```

### Processing

The worker has picked the job up and is waiting on the Connect service. Ask again shortly; a model call can take up to the configured timeout, 300 seconds by default.

```xml
<response success="true" status="Processing" error="" />
```

### Failed

Connect could not produce the summary and the job has used up its attempts (three by default). The `error` attribute carries the last error the worker saw. The job stays in the queue in a failed state until an administrator requeues it; calling again will not restart it.

```xml
<response success="false" status="Failed" errorcode="5030" error="Connect service is unreachable." />
```

### Status values

| `status` | `success` | `<Value>` | What a client should do |
|----------|-----------|-----------|-------------------------|
| `Ready` | `true` | present | use the summary |
| `Queued` | `true` | absent | ask again in a few seconds |
| `Processing` | `true` | absent | ask again in a few seconds |
| `Failed` | `false` | absent | report the error; retrying will not help |

## Behavior

On each call the API evaluates the following, in order:

1. **Version resolution** - `versionNumber=0` resolves to the latest published version. If the document has no published version, `Ready` with `-` is returned.
2. **Shortcut / URL documents** - always `Ready` with `-`; they have no content to summarize.
3. **Read security** - the caller must have read access to the document/version.
4. **Offline documents** - an error with `status` absent: the content is temporarily inaccessible.
5. **Stored summary** - if one exists for the version it is returned as `Ready`. This is the normal, fast path.
6. **Nothing to produce** - `Ready` with `-` when the version is missing from the warehouse, when the Connect service is not configured, or when the document's extension is not a supported type. These will never produce a summary, so no work is queued.
7. **Queue** - otherwise the summarize operation is queued for this document version at user priority and `Queued` is returned. If a job is already there, its state is reported instead, and a job that was queued automatically is moved to the front because somebody is now waiting for it.

### Supported file types

`pdf`, `docx`, `xlsx`, `pptx`, `html`, `htm`, `txt`, `md`, `csv` (configurable via `IRConnect.SummaryExtensions`).

### A dash is not an error

`Ready` with a `-` in `<Value>` means there will never be a summary for this version - an unsupported file type, no configured Connect service, or nothing published. It is a final answer, not a state to poll.

## Polling

A reasonable client asks once, and if the answer is `Queued` or `Processing` asks again every few seconds. The background worker polls the queue every 5 seconds by default (`IRConnect.QueuePollSeconds`) and runs one job at a time, so a busy server may leave a job queued for a while behind other work.

There is no callback or notification; polling is the only way to learn that a summary has arrived.

## Required Permissions

The calling user must have at least **read access** to the document.

> A read-access user can cause summarization work to be queued for a document, which consumes infoRouter Connect capacity. The work is only ever queued once per document version.

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
- A summary a user wrote with [`SetDocumentSummary`](SetDocumentSummary.md) is never overwritten by generated content. Only a summary the system produced is replaced when it is regenerated.
- Folders can have summarization done automatically on upload; see [SetFolderAIPreferences](SetFolderAIPreferences.md).

## Error Codes

Errors carry an `errorcode` attribute alongside the message. The code is the HTTP status multiplied by ten, so `4041` is 404 and `5030` is 503.

| Error | `errorcode` | Description |
|-------|-------------|-------------|
| `[900] Authentication failed` | `4010` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | `4010` | The ticket has expired or does not exist. |
| Document not found | `4041` | The specified path does not resolve to an existing document. |
| Access denied | `4030` | The caller does not have read access to the document. |
| Invalid argument exception. Version numbers cannot be less than 1000000... | `4000` | `versionNumber` is between 1 and 999,999. |
| This document is marked as 'offline'... | `4230` | The document is offline; try again later. |
| (any `status="Failed"` message) | `5030` | Connect could not produce the summary and the job is parked. |

## Related APIs

- [SetDocumentSummary](SetDocumentSummary.md) - Store or overwrite the summary for a document version
- [SetFolderAIPreferences](SetFolderAIPreferences.md) - Have summaries produced automatically for documents added to a folder
- [GetDocumentAbstract1](GetDocumentAbstract1.md) - Get the full-text index abstract, which is produced locally and not by Connect
- [GetDocument](GetDocument.md) - Get full document metadata and properties
