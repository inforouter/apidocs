# GetDocumentSummary API

Returns the AI-generated summary for a specified version of a document. Summaries are stored in the `DOCSUMMARY` table and produced by the local **infoRouter Connect** summarization service.

This API **only reads**. It never calls the Connect service, and it never queues work: a version with no stored summary answers with a dash, not with a job. Producing a summary is a separate, deliberate act - either a folder preference that summarizes documents as they are uploaded, or an explicit request to produce one - and only that act spends the instance's AI budget.

> **Changed in 9.0.** Earlier builds generated the summary during the call and returned it in the same response.
>
> **Changed again in 9.2.** Between those releases this API queued the work itself and answered `Queued` or `Processing` while it ran, so opening a document could spend money. It no longer does. A summary appears here once something else has produced one; until then the answer is `Ready` with `-`. Clients written for the queueing behaviour keep working - they simply never see a status other than `Ready`.

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

A successful call always carries `status="Ready"`. The attribute is kept for the clients written when this API queued work, and for the other AI responses that still use it.

### Ready — with a summary

```xml
<response success="true" status="Ready" error="">
  <Value>This document is a Q1 2024 financial report covering revenue, expenses, and year-over-year comparisons for the North America region.</Value>
</response>
```

### Ready — with no summary

Nothing has produced one for this version. `<Value>` carries a dash.

```xml
<response success="true" status="Ready" error="">
  <Value>-</Value>
</response>
```

This is a final answer, not a state to poll. To have a summary produced, see *Producing a summary* below.

### Status values

| `status` | `success` | `<Value>` | What a client should do |
|----------|-----------|-----------|-------------------------|
| `Ready` | `true` | present, may be `-` | use the summary, or treat `-` as "none" |

Failures are ordinary errors - a bad ticket, a path that resolves to nothing, an offline document - and carry `success="false"` with an `errorcode`, as listed at the end.

## Behavior

On each call the API evaluates the following, in order:

1. **Version resolution** - `versionNumber=0` resolves to the latest published version. If the document has no published version, `Ready` with `-` is returned.
2. **Shortcut / URL documents** - always `Ready` with `-`; they have no content to summarize.
3. **Read security** - the caller must have read access to the document/version.
4. **Offline documents** - an error: the content is temporarily inaccessible.
5. **Stored summary** - returned as `Ready` if there is one, `Ready` with `-` if there is not.

That is the whole of it. Nothing here consults the warehouse, the Connect service or the work queue, so the answer costs one indexed row read.

### A dash is not an error

`Ready` with `-` means no summary is stored for this version. It may be that nothing has produced one yet, or that nothing ever will - an unsupported file type, or no Connect service configured. This API does not distinguish the two, because it does not ask.

## Producing a summary

Two things produce summaries, and neither of them is this API:

- **Automatically on upload** - a folder with `AutoSummarize` or `AutoProfile` set queues the work for every version added to it. See [SetFolderAIPreferences](SetFolderAIPreferences.md).
- **On request** - an extract call queues the work at user priority, ahead of anything queued automatically, and reports its progress while it runs. That call is where `Queued` and `Processing` live now.

Either way the result lands in `DOCSUMMARY`, and this API returns it from that point on.

## Required Permissions

The calling user must have at least **read access** to the document.

> Reading a summary costs nothing and queues nothing. Until 9.2 a read-access user could cause summarization work to be queued simply by opening a document; that is no longer the case.

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
- The summary is per **version**. A new version starts with no summary of its own until something produces one.

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

## Related APIs

- [SetDocumentSummary](SetDocumentSummary.md) - Store or overwrite the summary for a document version
- [SetFolderAIPreferences](SetFolderAIPreferences.md) - Have summaries produced automatically for documents added to a folder
- [GetDocumentAbstract1](GetDocumentAbstract1.md) - Get the full-text index abstract, which is produced locally and not by Connect
- [GetDocument](GetDocument.md) - Get full document metadata and properties
