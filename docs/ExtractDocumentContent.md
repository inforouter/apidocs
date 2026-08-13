# ExtractDocumentContent API

Has the local **infoRouter Connect** service produce content for a document version — a summary, a description, keywords, the text of a scan, the document type — and reports where each of the things you asked for has got to.

This API **never calls the Connect service itself**. Producing any of this takes as long as a language model takes to answer, which is far too long to hold a web request open, so the work is queued and a background worker runs it. A call returns whatever is already stored, queues the rest, and tells you which is which. Asking twice does not queue the work twice, and a request from a user is placed ahead of everything queued automatically when documents were uploaded.

> **Ask for everything you want in one call.** It is not merely convenient — it is usually cheaper. A description, a summary, keywords and a document type are **one** AI call between them, where four separate requests would be four. The `plannedCalls` attribute on the response tells you the cost before any of it is spent.

## Endpoint

```
/srv.asmx/ExtractDocumentContent
```

## Methods

- **GET** `/srv.asmx/ExtractDocumentContent?AuthenticationTicket=...&Path=...&VersionNumber=0&ReplaceExisting=false&Summary=true&Description=true&Keywords=true&OcrText=false&DocumentType=false`
- **POST** `/srv.asmx/ExtractDocumentContent` (form data)
- **SOAP** Action: `http://tempuri.org/ExtractDocumentContent`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket obtained from `AuthenticateUser`. |
| `Path` | string | Yes | Full infoRouter path to the document, or a short document ID path (`~D{id}` or `~D{id}.ext`). |
| `VersionNumber` | int | Yes | Version to read. Pass `0` for the latest published version. Must be `0` or a modern-format version number (>= 1,000,000). |
| `ReplaceExisting` | bool | Yes | `true` produces the requested items again even where they are already stored. See *ReplaceExisting* below. |
| `Summary` | bool | Yes | Ask for a summary of the document. |
| `Description` | bool | Yes | Ask for a one line description, and the abstract that comes with it. |
| `Keywords` | bool | Yes | Ask for keywords, stored as the document's *generated* keywords rather than the user's own. |
| `OcrText` | bool | Yes | Ask for the text of a scan, written back so the document becomes searchable. |
| `DocumentType` | bool | Yes | Ask which document type the document looks like, and for the values of the property set that type requires. |

**At least one of the five must be `true`.** All of them off is not a request and is rejected.

### What each switch produces, and where it lands

| Switch | Produces | Read it back with |
|--------|----------|-------------------|
| `Summary` | A summary of this version | [GetDocumentSummary](GetDocumentSummary.md) |
| `Description` | A one line description, and an abstract | [GetDocument](GetDocument.md) |
| `Keywords` | Generated keywords | [GetDocumentKeywords](GetDocumentKeywords.md) |
| `OcrText` | The text of a scan, in the warehouse | [GetDocumentTextOnlyContent](GetDocumentTextOnlyContent.md) |
| `DocumentType` | The document type, and the values of its required property set | [GetDocument](GetDocument.md) |

`DocumentType` covers the type match **and** the property set extraction that rides with it. They arrive from the same call and there is no way to ask for one without the other.

The document type is only ever written onto a document that has **no type yet** — a type somebody chose is never replaced — and only when Connect is sure enough of the match (`IRConnect.DocumentTypeMinConfidence`, 0.75 by default). The same applies per field to the property set values.

### `ReplaceExisting`

`false` — anything already stored is returned as it is, and only what is missing is produced. This is the normal setting: a caller that asks twice pays once.

`true` — the requested items are produced again even where they are already stored.

It does **not** override the rule that a summary or description **a person wrote** is never replaced by generated content. That rule is enforced where the answer is written, so a request with `ReplaceExisting=true` on a document whose summary was written by hand will spend the AI call and then decline to overwrite. If you want the generated content back, remove the hand-written content first.

## Response

Every successful call carries the aggregate `status`, the `plannedCalls` count, and one `<Operation>` row per thing you asked for.

```xml
<response success="true" error="" status="Processing" plannedCalls="1">
  <Operations>
    <Operation name="Summary" status="Ready">
      <Content>The document sets out the Q3 revenue …</Content>
    </Operation>
    <Operation name="Description" status="Ready">
      <Content>Q3 revenue report for the northern region.</Content>
    </Operation>
    <Operation name="Keywords" status="Processing" />
    <Operation name="OcrText" status="Disabled" error="Not available" />
    <Operation name="DocumentType" status="Failed" error="[503] Connect could not match this document." />
  </Operations>
</response>
```

| Attribute | Description |
|-----------|-------------|
| `status` | The one status for the whole request. See below. |
| `plannedCalls` | How many AI calls this request spends. `0` when everything asked for was already stored or refused. |

### `<Operation>` rows

| Attribute | Description |
|-----------|-------------|
| `name` | `Summary`, `Description`, `Keywords`, `OcrText` or `DocumentType` — the switch that asked for it. |
| `status` | `Ready`, `Queued`, `Processing`, `Failed` or `Disabled`. |
| `error` | Why, on `Failed` and `Disabled`. Absent otherwise. |

`<Content>` is present only on a `Ready` row that has something to carry. **`OcrText` never carries content** even when ready: it runs to megabytes, and a response you are polling every few seconds is the wrong place for it. Read it with [GetDocumentTextOnlyContent](GetDocumentTextOnlyContent.md).

### Status values

| `status` | Meaning | What a client should do |
|----------|---------|-------------------------|
| `Ready` | The answer is there | use it |
| `Queued` | Work is waiting for a worker | ask again in a few seconds |
| `Processing` | A worker has it and is waiting on Connect | ask again in a few seconds |
| `Failed` | Connect could not produce it and the job used up its attempts | report it; retrying will not help |
| `Disabled` | It will never be produced, and nothing went wrong | stop asking; do not show an error |

`Disabled` means one of three things, and the `error` attribute says which: this instance has switched that operation off (`IRConnect.Operations`), this server cannot carry it out, or the document is a file type Connect cannot read. It is final. A greyed-out row is the right way to show it.

### The aggregate `status`

The single status for the whole request, so a client can drive a dialog from it without reading every row:

- Anything **`Processing`** or **`Queued`** wins — that is the answer meaning *ask again*.
- **`Failed`** only when *every* row failed. One failure beside a success is not a failed request.
- **`Disabled`** only when every row was refused: nothing went wrong and nothing is coming.
- Otherwise **`Ready`**, including a mixture of ready, failed and refused rows.

`success="false"` appears **only** when the aggregate is `Failed`. A response can carry `success="true"` with a failed row inside it — the request was valid and the answers that arrived are worth having.

## What a request costs

The server works out the cheapest set of calls that answers what you asked for. A profile call returns the description, summary, keywords and document type together, and carries the text of a scan back with them, so anything that needs a description or a document type gets the rest of it free:

| Asked for | AI calls | Why |
|-----------|:--------:|-----|
| `Summary` | 1 | A summarize call |
| `Keywords` | 1 | A keywords call |
| `Summary` + `Keywords` | 2 | Two calls on purpose — see below |
| `Summary` + `Description` + `Keywords` | **1** | Only a profile produces a description, and it answers the rest too |
| … + `OcrText` | **1** | The profile carries a scan's text back with it |
| … + `DocumentType` | **1** | The profile carries the type match too |

`Summary` + `Keywords` is deliberately **not** collapsed into a profile, though it would cost the same. The profile would also write a description, an abstract and possibly a document type that nobody asked for, and unasked-for writes are their own harm.

`plannedCalls` on the response is this number, for the request you actually made.

## Behavior

1. **Nothing asked for** - an error; at least one switch must be `true`.
2. **Version resolution** - `VersionNumber=0` resolves to the latest published version. A document with no published version is an error.
3. **Shortcut and URL documents** - an error; they have no content to read.
4. **Offline documents** - an error; the content is temporarily inaccessible.
5. **Permission** - the caller must be able to change the document's properties. The answers are written onto the document, so this is a write however it looks from the caller's side.
6. **Connect not configured** - every requested row comes back `Disabled`.
7. **Already stored** - anything present is returned as `Ready` and is not produced again, unless `ReplaceExisting=true`.
8. **Plan** - what is left is turned into the fewest AI calls that answer it, dropping anything switched off, unimplemented, or asking to read a file type Connect cannot read. Those come back `Disabled`.
9. **Queue** - the planned work is queued at user priority. A job already there has its state reported instead, and a job queued automatically is moved to the front because somebody is now waiting for it.

### Supported file types

`pdf`, `docx`, `xlsx`, `pptx`, `html`, `htm`, `txt`, `md`, `csv` (configurable via `IRConnect.SupportedExtensions`).

`OcrText` is deliberately exempt: a scanned TIFF is exactly what that list leaves out and exactly what OCR is for.

## Polling

Ask once. While the aggregate `status` is `Queued` or `Processing`, ask again every few seconds; the rows that are already `Ready` stay ready. The background worker polls every 5 seconds by default (`IRConnect.QueuePollSeconds`) and runs one job at a time, so a busy server may leave work queued for a while. There is no callback; polling is the only way to learn the work has finished.

Rows that are `Ready`, `Failed` or `Disabled` are final and will not change on a later call.

## Required Permissions

The calling user must be able to change the document's properties.

## Example

### Request (GET)

```
GET /srv.asmx/ExtractDocumentContent
  ?AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
  &Path=/Finance/Reports/Q1-2024-Report.pdf
  &VersionNumber=0
  &ReplaceExisting=false
  &Summary=true
  &Description=true
  &Keywords=true
  &OcrText=false
  &DocumentType=false
HTTP/1.1
```

### Request (POST)

```
POST /srv.asmx/ExtractDocumentContent HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=3f2504e0-4f89-11d3-9a0c-0305e82c3301
&Path=/Finance/Reports/Q1-2024-Report.pdf
&VersionNumber=0
&ReplaceExisting=false
&Summary=true
&Description=true
&Keywords=true
&OcrText=false
&DocumentType=false
```

### Request (SOAP)

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://tempuri.org/">
  <soap:Body>
    <tns:ExtractDocumentContent>
      <tns:AuthenticationTicket>3f2504e0-4f89-11d3-9a0c-0305e82c3301</tns:AuthenticationTicket>
      <tns:Path>/Finance/Reports/Q1-2024-Report.pdf</tns:Path>
      <tns:VersionNumber>0</tns:VersionNumber>
      <tns:ReplaceExisting>false</tns:ReplaceExisting>
      <tns:Summary>true</tns:Summary>
      <tns:Description>true</tns:Description>
      <tns:Keywords>true</tns:Keywords>
      <tns:OcrText>false</tns:OcrText>
      <tns:DocumentType>false</tns:DocumentType>
    </tns:ExtractDocumentContent>
  </soap:Body>
</soap:Envelope>
```

## Notes

- Folders can have any of this produced automatically for documents added to them; see [SetFolderAIPreferences](SetFolderAIPreferences.md). A folder that asks for profiling gets the description, summary, keywords and document type from one call, the same way this API does.
- Generated keywords are a separate kind from the ones a user curated, so this API never destroys a keyword somebody entered. Unlike [ExtractDocumentKeywords](ExtractDocumentKeywords.md), `ReplaceExisting` here does **not** clear the user's own keywords.
- [ExtractDocumentKeywords](ExtractDocumentKeywords.md) is the one-switch form of this API and is served by the same implementation.
- Generation requires infoRouter Connect to be configured through the `IRConnect` application settings.

## Error Codes

Errors carry an `errorcode` attribute alongside the message. The code is the HTTP status multiplied by ten, so `4041` is 404 and `5030` is 503.

| Error | `errorcode` | Description |
|-------|-------------|-------------|
| `[900] Authentication failed` | `4010` | Invalid or missing authentication ticket. |
| `[901] Session expired or Invalid ticket` | `4010` | The ticket has expired or does not exist. |
| Required field | `4000` | No switch was set to `true`. |
| Document not found | `4041` | The path does not resolve to an existing document. |
| Access denied | `4030` | The caller may not change the document's properties. |
| URL and shortcut files do not have text content. | `4000` | The document has no content to read. |
| This document is marked as 'offline'... | `4230` | The document is offline; try again later. |
| Invalid argument exception. Version numbers cannot be less than 1000000... | `4000` | `VersionNumber` is between 1 and 999,999. |
| (any aggregate `status="Failed"` message) | `5030` | Every requested item failed; the message is the first failure. |

## Related APIs

- [ExtractDocumentKeywords](ExtractDocumentKeywords.md) - The one-switch form, for keywords only
- [GetDocumentSummary](GetDocumentSummary.md) - Read a stored summary; it never produces one
- [GetDocumentKeywords](GetDocumentKeywords.md) - Read every keyword on a document
- [GetDocumentTextOnlyContent](GetDocumentTextOnlyContent.md) - Read the stored text, including OCR output
- [SetFolderAIPreferences](SetFolderAIPreferences.md) - Have this produced automatically on upload
- [GetDocument](GetDocument.md) - Read the description, document type and property set values
