# GetVersionRendition API

Returns a derived rendition of a document version: the structured markdown or the redacted text infoRouter Connect produced for it.

A rendition is derived from the version rather than uploaded with it — every one can be produced again from the document, and losing one is a rebuild rather than a restore. They live beside the version in the warehouse, not in the database, because each is the size of the document.

## Endpoint

```
/srv.asmx/GetVersionRendition
```

## Methods

- **GET** `/srv.asmx/GetVersionRendition?AuthenticationTicket=...&Path=...&VersionNumber=0&Rendition=Markdown`
- **POST** `/srv.asmx/GetVersionRendition` (form data)
- **SOAP** Action: `http://tempuri.org/GetVersionRendition`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `AuthenticationTicket` | string | Yes | Authentication ticket |
| `Path` | string | Yes | Full infoRouter path to the document, or a short document ID path (`~D{id}` or `~D{id}.ext`) |
| `VersionNumber` | int | Yes | Version to read. Pass `0` for the published version, or for the latest version when the document has never been published. |
| `Rendition` | string | Yes | `Markdown`, `RedactedText`, or `Text` for the plain text. Case-insensitive. |

## Renditions

| Value | What it is | Produced by |
|-------|-----------|-------------|
| `Markdown` | The document as markdown — real headings and real pipe tables, which flat text extraction loses. For a digital PDF this is the only way to get its tables out. | [GetConnectProfile](GetConnectProfile.md) with `IncludeMarkdown=true` |
| `RedactedText` | The text with personal data replaced by `[REDACTED]`. One way: there is no key that puts the real values back. Covers the whole document even where the AI answers saw only its beginning. | [GetConnectProfile](GetConnectProfile.md) with `IncludeRedactedText=true` |
| `Text` | The plain text, from a text layer or from OCR. The same content [GetVersionTextOnlyContent](GetVersionTextOnlyContent.md) returns. | [GetConnectProfile](GetConnectProfile.md) with `IncludeOcrText=true` |

## Response

### Success Response
```xml
<response success="true" error="" rendition="Markdown">## Quarterly Revenue

| Tier | Revenue |
|------|---------|
| Basic | 1,204 |
</response>
```

### A rendition that has not been produced
```xml
<response success="true" error="" rendition="Markdown"></response>
```

Empty and **successful**, not an error: a document nobody has asked Connect to produce a rendition for is a perfectly ordinary document. Ask [GetConnectProfile](GetConnectProfile.md) to find out whether one exists, whether one is on its way, or to have one produced.

### Error Response
```xml
<response success="false" error="[ErrorCode] Error message" />
```

## Required Permissions

Any authenticated user with read access to the document.

## Example

### Request (POST)
```
POST /srv.asmx/GetVersionRendition HTTP/1.1
Content-Type: application/x-www-form-urlencoded

AuthenticationTicket=abc123&Path=/Finance/Q3.pdf&VersionNumber=0&Rendition=RedactedText
```

## JavaScript

Every call answers XML with HTTP 200, success or not, so `success` is the thing to branch on and
`errorCode` is the number to report.

```javascript
async function call(action, params) {
  const response = await fetch(`/srv.asmx/${action}?${new URLSearchParams(params)}`);
  const root = new DOMParser()
    .parseFromString(await response.text(), 'text/xml')
    .documentElement;

  if (root.getAttribute('success') !== 'true') {
    throw new Error(`${root.getAttribute('errorCode')}: ${root.getAttribute('error')}`);
  }
  return root;
}
```

Reads a derived rendition of one document version - the plain text, the structured markdown, or the
text with personal data removed.

```javascript
const root = await call('GetVersionRendition', {
  authenticationTicket: ticket,
  Path: '/Finance/Reports/Q1.pdf',
  VersionNumber: 0,             // 0 means the published version
  Rendition: 'Markdown'
});

const text = root.textContent;                    // on the root itself
const which = root.getAttribute('rendition');     // echoed back exactly as it was asked for
```

**`Rendition` is one of `Text`, `Markdown` or `RedactedText`**, matched without regard to case.
Anything else is refused `4000` with those three names in the message - worth relying on, because
`redacted` looks as though it should work and does not. An empty `Rendition` is refused by model
binding with HTTP 400 before the operation runs.

A rendition that has not been produced yet is a success with empty text, not an error, so there is no
way to tell "not generated" from "generated and empty".

## Notes

- Characters XML cannot carry are removed from the response. Text pulled out of a PDF is full of one of them — the form feed a page break leaves behind — and these are artifacts of the extraction rather than anything a reader wrote. A caller that needs the bytes exactly as stored wants the file, not an XML element holding it.
- Renditions travel with the document: copying a document copies them, so a copy is not asked to produce them all over again.
- Each rendition belongs to one version. A new version has none until one is asked for.

## Error Codes

The `errorCode` values this operation returns, checked against a running server:

| `errorCode` | When |
|---:|---|
| `4010` | the ticket is expired or unknown, or there is no ticket at all |
| `4000` | `Rendition` is not one of `Text`, `Markdown`, `RedactedText` |
| `4041` | no document at that path, or no version carries that number |
| `HTTP 400` | a required string parameter was empty; refused by model binding, so there is no error document |

A call with no ticket signs in as the anonymous user, so a document in a library flagged as anonymous
can be read without authenticating.
