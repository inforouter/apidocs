# ExtractDocumentKeywords API

Has the local **infoRouter Connect** service read a document version and produce keywords for it. The keywords it returns are stored as the document's *generated* keywords, a separate kind from the ones a user curated.

This API **never calls the Connect service itself**. Producing keywords takes as long as a language model takes to answer, which is far too long to hold a web request open, so the work is queued and a background worker runs it. A call either returns the keywords already on the document or tells you the work is queued and you should ask again shortly. Asking twice does not queue the work twice, and a request from a user is placed ahead of everything queued automatically when documents were uploaded.

## Endpoint

```
/srv.asmx/ExtractDocumentKeywords
```

## Methods

- **GET** `/srv.asmx/ExtractDocumentKeywords?AuthenticationTicket=...&Path=...&VersionNumber=...&ReplaceExisting=...`
- **POST** `/srv.asmx/ExtractDocumentKeywords` (form data)
- **SOAP** Action: `http://tempuri.org/ExtractDocumentKeywords`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the document, or a short document ID path (`~D{id}` or `~D{id}.ext`). |
| `VersionNumber` | int | Yes | Version to read. Pass `0` for the latest published version. Must be `0` or a modern-format version number (>= 1,000,000). |
| `ReplaceExisting` | bool | Yes | `true` clears the keywords the user curated, leaving the document with the generated ones only. `false` keeps them. See below. |

### The two kinds of keyword

A document carries keywords a user curated and keywords infoRouter Connect generated, stored separately. This API only ever writes the generated ones, so **running it can never destroy a keyword a user entered**. Both kinds come back together from [`GetDocumentKeywords`](GetDocumentKeywords.md).

`ReplaceExisting=true` is the exception, and it is destructive: it clears the user's own keywords. That happens **immediately, when the request is made**, not when the job runs - it is what the caller asked for and does not depend on Connect answering. A job that later fails leaves the document with neither.

Use `false` unless you specifically intend to discard what the user entered.

## Response

Every successful call carries a `status` attribute saying whether the keywords are there yet.

### Ready

The document already has generated keywords. `<Keywords>` holds every keyword on the document, the user's own first and the generated ones after, comma separated.

```xml
<response success="true" status="Ready" error="">
  <Keywords>finance,quarterly report,acceptance letter</Keywords>
</response>
```

### Queued

No generated keywords are stored, and the work has been placed in the queue. Ask again in a few seconds.

```xml
<response success="true" status="Queued" error="" />
```

### Processing

The worker has picked the job up and is waiting on the Connect service.

```xml
<response success="true" status="Processing" error="" />
```

### Failed

Connect could not produce keywords and the job has used up its attempts. The job stays parked until an administrator requeues it; calling again will not restart it.

```xml
<response success="false" status="Failed" errorcode="5030" error="Connect service is unreachable." />
```

### Status values

| `status` | `success` | `<Keywords>` | What a client should do |
|----------|-----------|--------------|-------------------------|
| `Ready` | `true` | present | use the keywords |
| `Queued` | `true` | absent | ask again in a few seconds |
| `Processing` | `true` | absent | ask again in a few seconds |
| `Failed` | `false` | absent | report the error; retrying will not help |

## Behavior

1. **Version resolution** - `VersionNumber=0` resolves to the latest published version. A document with no published version is an error.
2. **Shortcut and URL documents** - an error; they have no content to read.
3. **Offline documents** - an error; the content is temporarily inaccessible.
4. **Connect not configured** - an error, since nothing can produce keywords.
5. **`ReplaceExisting=true`** - the user's own keywords are cleared now.
6. **Already generated** - if the document already has generated keywords they are returned as `Ready`, and no new work is queued. To have them produced again, remove them first.
7. **Queue** - otherwise the work is queued at user priority and `Queued` is returned. If a job is already there its state is reported instead, and a job queued automatically is moved to the front because somebody is now waiting for it.

### Keyword shape

Generated keywords are phrases as often as single words - `acceptance letter`, `quarterly report` - and are stored as they come back, up to 128 characters each. Split a keyword list on commas, never on whitespace.

## Polling

Ask once, and if the answer is `Queued` or `Processing` ask again every few seconds. The background worker polls every 5 seconds by default (`IRConnect.QueuePollSeconds`) and runs one job at a time, so a busy server may leave a job queued for a while. There is no callback; polling is the only way to learn the work has finished.

## Required Permissions

The calling user must be able to change the document's properties.

## Example

### Request (GET)

```
GET /srv.asmx/ExtractDocumentKeywords
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports/Q1-2024-Report.pdf
  &VersionNumber=0
  &ReplaceExisting=false
HTTP/1.1
```

### Request (POST)

```
POST /srv.asmx/ExtractDocumentKeywords HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance/Reports/Q1-2024-Report.pdf
&VersionNumber=0
&ReplaceExisting=false
```

### Request (SOAP)

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:ExtractDocumentKeywords>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:Path>/Finance/Reports/Q1-2024-Report.pdf</tns:Path>
      <tns:VersionNumber>0</tns:VersionNumber>
      <tns:ReplaceExisting>false</tns:ReplaceExisting>
    </tns:ExtractDocumentKeywords>
  </soap:Body>
</soap:Envelope>
```

## Notes

- Folders can have keywords produced automatically for documents added to them; see [SetFolderAIPreferences](SetFolderAIPreferences.md). A folder that asks for profiling gets keywords from that single call instead, along with the description, abstract and summary.
- Keywords the user curated are set with [`UpdateDocumentKeywords`](UpdateDocumentKeywords.md) and are never written by this API.
- Generation requires infoRouter Connect to be configured through the `IRConnect` application settings.

## Error Codes

Errors carry an `errorcode` attribute alongside the message. The code is the HTTP status multiplied by ten, so `4041` is 404 and `5030` is 503.

| Error | `errorcode` | Description |
|-------|-------------|-------------|
| `[900] Authentication failed` | `4010` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | `4010` | The ticket has expired or does not exist. |
| Document not found | `4041` | The path does not resolve to an existing document. |
| Access denied | `4030` | The caller may not change the document's properties. |
| URL and shortcut files do not have text content. | `4000` | The document has no content to read. |
| This document is marked as 'offline'... | `4230` | The document is offline; try again later. |
| No keywords could be extracted from this document. | `4000` | Connect is not configured, or it read the document and found nothing to tag. |
| (any `status="Failed"` message) | `5030` | Connect could not produce keywords and the job is parked. |

## Related APIs

- [GetDocumentKeywords](GetDocumentKeywords.md) - Read every keyword on a document
- [UpdateDocumentKeywords](UpdateDocumentKeywords.md) - Set the keywords a user curated
- [GetDocumentSummary](GetDocumentSummary.md) - The same queue and status model, for summaries
- [SetFolderAIPreferences](SetFolderAIPreferences.md) - Have keywords produced automatically on upload
